"""
Simple keyword-based document retriever for mock RAG.

This module implements a basic in-memory knowledge base with keyword matching.
In a real system, this would query a vector database or full-text search engine.
"""


# Hard-coded document snippets for the knowledge base
DOCUMENTS = [
    "Python is a high-level programming language known for its simplicity and readability.",
    "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
    "GPT models are large language models trained using transformer architectures.",
    "The CAP theorem states that distributed systems can guarantee consistency, availability, or partition tolerance.",
    "Kubernetes is an open-source container orchestration platform for automating deployment and scaling.",
    "REST APIs use HTTP methods like GET, POST, PUT, and DELETE to perform operations on resources.",
    "Docker containers package applications and their dependencies for consistent deployment.",
    "Microservices architecture breaks down applications into small, independent services.",
    "Quantum computing leverages quantum bits (qubits) for computation instead of classical bits.",
    "DevOps combines software development and IT operations to shorten development cycles.",
]


def retrieve(query: str) -> list[str]:
    """
    Retrieve relevant documents from the knowledge base using keyword matching.

    This is a simple implementation that performs case-insensitive keyword matching.
    Documents are ranked by the number of matching keywords and returned in order.

    Args:
        query: A natural language query string.

    Returns:
        A list of relevant document snippets, ranked by relevance (most relevant first).
    """
    query_lower = query.lower()
    keywords = [word for word in query_lower.split() if len(word) > 3]

    if not keywords:
        return []

    # Score each document by matching keywords
    scored_docs = []
    for doc in DOCUMENTS:
        doc_lower = doc.lower()
        score = sum(1 for keyword in keywords if keyword in doc_lower)
        if score > 0:
            scored_docs.append((score, doc))

    # Sort by score (descending) and return just the documents
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored_docs]
