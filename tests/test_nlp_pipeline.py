import pytest
from src.pre_processing.nlp_pipeline import (
    TokenizerProcessor,
    StopwordsProcessor,
    LemmatizerProcessor
)

def test_tokenizer_processor_splits_text():
    processor = TokenizerProcessor()
    text = "Desenvolvedor Python júnior"
    expected = ["Desenvolvedor", "Python", "júnior"]
    assert processor.process(text) == expected

def test_tokenizer_handles_empty():
    processor = TokenizerProcessor()
    assert processor.process("") == []

def test_stopwords_processor_removes_noise():
    processor = StopwordsProcessor()
    text = "Vaga para o candidato que programa em Python."
    result = processor.process(text)
    
    assert "para" not in result.split()
    assert "o" not in result.split()
    assert "em" not in result.split()
    assert "Python" in result.split()

def test_lemmatizer_processor_reduces_words():
    processor = LemmatizerProcessor()
    text = "programando programou programas"
    result = processor.process(text)
    
    assert "programar" in result

def test_processors_handle_none_and_empty():
    processors = [StopwordsProcessor(), LemmatizerProcessor()]
    for processor in processors:
        assert processor.process("") == ""
        assert processor.process(None) == ""