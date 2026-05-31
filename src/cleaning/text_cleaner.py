import re
from bs4 import BeautifulSoup
from .extractors import SalaryExtractor, EmailExtractor, WorkModelExtractor


def clean_html(raw_html: str) -> str:
    """Remove tags and normalize whitespace from HTML content.

    Returns an empty string for falsy inputs to keep behaviour stable for
    callers and tests.
    """
    if not raw_html:
        return ""

    soup = BeautifulSoup(raw_html, "lxml")
    text = soup.get_text(separator=" ")

    text_normalized = re.sub(r"\s+", " ", text)
    text_normalized = text_normalized.strip().replace(" !", "!")

    return text_normalized