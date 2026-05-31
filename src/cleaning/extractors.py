import re
from abc import ABC, abstractmethod


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
        return match.group(0).lower().strip() if match else None
