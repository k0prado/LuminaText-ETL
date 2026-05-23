import re
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


def clean_html(raw_html: str) -> str:

    if not raw_html:
        return ""
    
    soup = BeautifulSoup(raw_html, "lxml")
    text = soup.get_text(separator=" ")
    
    text_normalized = re.sub(r"\s+", " ", text)
    
    text_normalized = text_normalized.strip().replace(" !", "!")
    
    return text_normalized



class TextExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> str | None:
        pass


class SalaryExtractor(TextExtractor):
    def __init__(self):
        self.pattern = re.compile(r"(?:R\$\s?)(?:\d{1,3}(?:\.\d{3})*)(?:,\d{2})?")

    def extract(self, text: str) -> str | None:
        if not text:
            return None
        match = self.pattern.search(text)
        return match.group(0).strip() if match else None

class EmailExtractor(TextExtractor):
    def __init__(self):
        self.pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    def extract(self, text: str) -> str | None:
        if not text:
            return None
        match = self.pattern.search(text)
        return match.group(0).lower().strip() if match else None

class WorkModelExtractor(TextExtractor):
    def __init__(self):
        self.pattern = re.compile(
            r"\b(remoto|híbrido|hibrido|presencial)\b", 
            re.IGNORECASE
        )

    def extract(self, text: str) -> str | None:
        if not text:
            return None
        match = self.pattern.search(text)
        # Retorna o termo padronizado em minúsculas se houver match
        return match.group(0).lower().strip() if match else None