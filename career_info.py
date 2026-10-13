"""Static career-area information used by the chatbot."""


def get_topic_info(topic: str) -> str:
    topic = topic.lower()
    if "science" in topic:
        return "Chatbot: Science-related career paths include biology, chemistry, physics, astronomy, environmental science, and geology."
    if any(term in topic for term in ["technology", "tech"]):
        return "Chatbot: Technology careers span software development, data science, cybersecurity, network engineering, artificial intelligence, and robotics."
    if "engineering" in topic:
        return "Chatbot: Engineering offers diverse fields like civil, mechanical, electrical, chemical, aerospace, and biomedical engineering."
    if any(term in topic for term in ["medicine", "healthcare"]):
        return "Chatbot: Medical professions encompass doctors, nurses, pharmacists, dentists, physical therapists, and healthcare administrators."
    if any(term in topic for term in ["business", "management"]):
        return "Chatbot: Business paths cover marketing, finance, human resources, entrepreneurship, supply chain management, and international business."
    if any(term in topic for term in ["arts", "humanities"]):
        return "Chatbot: Arts and humanities fields involve literature, history, languages, visual arts, performing arts, philosophy, and cultural studies."
    if any(term in topic for term in ["law", "legal"]):
        return "Chatbot: Legal careers include lawyers, paralegals, judges, legal consultants, and specialists in corporate or criminal law."
    if any(term in topic for term in ["education", "teaching"]):
        return "Chatbot: Education paths cover teaching, school administration, educational psychology, curriculum development, and special education."
    if any(term in topic for term in ["agriculture", "farming"]):
        return "Chatbot: Agriculture offers careers in farming, agribusiness, agricultural engineering, agronomy, agricultural economics, and sustainable agriculture."
    if any(term in topic for term in ["design", "creative"]):
        return "Chatbot: Design and creative fields include graphic design, interior design, fashion design, animation, user experience design, and game design."
    if any(term in topic for term in ["psychology", "counseling"]):
        return "Chatbot: Psychology careers involve clinical psychology, counseling psychology, industrial-organizational psychology, neuropsychology, and forensic psychology."
    return "Chatbot: I'm sorry, I don't have information about that topic."
