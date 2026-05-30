import pytest
from src.pre_processing.vectorizer import TfidfTextVectorizer

def test_tfidf_vectorizer_shape_and_vocabulary():
    vectorizer = TfidfTextVectorizer()
    documents = [
        "python docker mloops",
        "python sql database",
        "docker kubernetes cloud"
    ]
    
    matrix = vectorizer.fit_transform(documents)
    features = vectorizer.get_feature_names()
    
    assert len(matrix) == 3
    assert len(matrix[0]) == len(features)
    assert "python" in features
    assert "docker" in features

def test_tfidf_vectorizer_handles_empty_and_whitespace():
    vectorizer = TfidfTextVectorizer()
    
    assert vectorizer.fit_transform([]) == []
    assert vectorizer.fit_transform(["", "   "]) == []

def test_tfidf_vectorizer_feature_names_before_fit():
    vectorizer = TfidfTextVectorizer()
    assert vectorizer.get_feature_names() == []