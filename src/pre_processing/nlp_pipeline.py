from abc import ABC, abstractmethod
import spacy

class TextProcessor(ABC):
    @abstractmethod
    def process(self, text: str) -> list[str] | str:
        pass

class TokenizerProcessor(TextProcessor):
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")

    def process(self, text: str) -> list[str]:
        if not text:
            return []
        doc = self.nlp(text)
        return [token.text for token in doc if not token.is_space]

class StopwordsProcessor(TextProcessor):
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")

    def process(self, text: str) -> str:
        if not text:
            return ""
        doc = self.nlp(text)
        tokens_filtered = [
            token.text for token in doc 
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        return " ".join(tokens_filtered)

class LemmatizerProcessor(TextProcessor):
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")

    def process(self, text: str) -> str:
        if not text:
            return ""
        doc = self.nlp(text)
        lemmas = [
            token.lemma_ for token in doc 
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        return " ".join(lemmas)