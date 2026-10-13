"""Model training/loading, prediction, and result charting."""
from pathlib import Path
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "synthetic_data.csv"
SCALER_PATH = BASE_DIR / "1_scaler.pkl"
MODEL_PATH = BASE_DIR / "1_svm_model.pkl"
STATIC_DIR = BASE_DIR / "static"


def train_model(data_path=DATA_PATH):
    """Train an SVC model from synthetic_data.csv and save artifacts.

    The source thesis selects every column except the last as features and the
    final column as the target. The CSV is not included in the supplied pages.
    """
    data = pd.read_csv(data_path)
    if data.shape[1] < 2:
        raise ValueError("Training CSV must contain at least one feature and one target column.")

    x = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, random_state=100, test_size=0.3
    )

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    model = SVC(probability=True)
    model.fit(x_train_scaled, y_train)

    y_pred = model.predict(x_test_scaled)
    print("Classification report:\n", classification_report(y_test, y_pred))
    matrix = confusion_matrix(y_test, y_pred, labels=model.classes_)

    STATIC_DIR.mkdir(exist_ok=True)
    plt.figure(figsize=(12, 9))
    sns.heatmap(
        matrix, annot=True, fmt="d", cmap="Blues",
        xticklabels=model.classes_, yticklabels=model.classes_
    )
    plt.title("SVM Confusion Matrix")
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.tight_layout()
    plt.savefig(STATIC_DIR / "svm_confusion_matrix.png", bbox_inches="tight")
    plt.close()

    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved scaler to {SCALER_PATH}")
    print(f"Saved model to {MODEL_PATH}")


def load_recommender():
    """Load previously trained model and scaler."""
    if not SCALER_PATH.exists() or not MODEL_PATH.exists():
        raise FileNotFoundError("Model artifacts not found. Run `python train_model.py`.")
    return joblib.load(SCALER_PATH), joblib.load(MODEL_PATH)


def predict_career(scaler, model, average_scores):
    """Predict a career class from the feature averages."""
    features = list(average_scores)
    if len(features) != getattr(model, "n_features_in_", len(features)):
        raise ValueError(
            f"Model expects {getattr(model, 'n_features_in_', 'an unknown number of')} "
            f"features, but {len(features)} were provided."
        )
    scaled = scaler.transform([features])
    career = model.predict(scaled)[0]
    return career, features[-1]


def create_ocean_chart(ocean_averages):
    """Write an OCEAN personality chart under static/ and return its path."""
    labels = [
        "Openness", "Conscientiousness", "Extraversion",
        "Agreeableness", "Neuroticism"
    ]
    if len(ocean_averages) != len(labels):
        raise ValueError("Five OCEAN scores are required.")
    STATIC_DIR.mkdir(exist_ok=True)
    output = STATIC_DIR / "ocean_score.png"

    fig, ax = plt.subplots(figsize=(9, 5))
    palette = ["#3498DB", "#2ecc71", "#e74c3c", "#9b59b6", "#f1c40f"]
    sns.barplot(x=labels, y=ocean_averages, hue=labels, palette=palette, legend=False, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha="right")
    for index, score in enumerate(ocean_averages):
        ax.text(index, score, f"{score:.2f}", ha="center", va="bottom", color="black", fontweight="bold")
    ax.set_title("OCEAN Personality Scores")
    ax.set_ylabel("Average response (1–5)")
    ax.set_xlabel("")
    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    return str(output.relative_to(BASE_DIR))
