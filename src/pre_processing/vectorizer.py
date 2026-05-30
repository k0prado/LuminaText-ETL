from abc import ABC, abstractmethod
from sklearn.feature_extraction.text import TfidfVectorizer

class TextVectorizer(ABC):
    @abstractmethod
    def fit_transform(self, documents: list[str]) -> list[list[float]]:
        pass

class TfidfTextVectorizer(TextVectorizer):
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self, documents: list[str]) -> list[list[float]]:
        if not documents or all(not doc.strip() for doc in documents):
            return []
            
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        return tfidf_matrix.toarray().tolist()

    def get_feature_names(self) -> list[str]:
        if not hasattr(self.vectorizer, "vocabulary_"):
            return []
        return self.vectorizer.get_feature_names_out().tolist()