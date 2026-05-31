from abc import ABC, abstractmethod
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List

class TextVectorizer(ABC):
    @abstractmethod
    def fit_transform(self, documents: List[str]) -> List[List[float]]:
        pass

class TfidfTextVectorizer(TextVectorizer):
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self, documents: list[str]) -> list[list[float]]:
        """Fit the TF-IDF vectorizer and return a dense matrix as list of lists.

        Returns an empty list for empty/whitespace-only inputs.
        """
        if not documents or all(not doc.strip() for doc in documents):
            return []

        tfidf_matrix = self.vectorizer.fit_transform(documents)
        return tfidf_matrix.toarray().tolist()

    def fit(self, documents: List[str]):
        """Fit the underlying vectorizer (no return value)."""
        if not documents or all(not doc.strip() for doc in documents):
            return
        self.vectorizer.fit(documents)

    def transform(self, documents: List[str]) -> List[List[float]]:
        """Transform documents using a previously-fitted vectorizer."""
        if not hasattr(self.vectorizer, "vocabulary_"):
            raise RuntimeError("Vectorizer must be fitted before calling transform")
        if not documents or all(not doc.strip() for doc in documents):
            return []
        matrix = self.vectorizer.transform(documents)
        return matrix.toarray().tolist()

    def get_feature_names(self) -> list[str]:
        if not hasattr(self.vectorizer, "vocabulary_"):
            return []
        return self.vectorizer.get_feature_names_out().tolist()