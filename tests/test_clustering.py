import pytest
from src.models.clustering import VacancyClusteringModel

def test_kmeans_clustering_returns_correct_labels_length():
    model = VacancyClusteringModel(n_clusters=2)
    mock_tfidf_matrix = [
        [1.0, 0.0, 0.0],
        [0.9, 0.1, 0.0],
        [0.0, 0.2, 0.8],
        [0.0, 0.0, 1.0]
    ]
    
    labels = model.fit_predict(mock_tfidf_matrix)
    
    assert len(labels) == 4
    assert isinstance(labels[0], int)

def test_clustering_handles_insufficient_data():
    model = VacancyClusteringModel(n_clusters=3)
    mock_matrix = [[1.0, 0.0]]
    
    labels = model.fit_predict(mock_matrix)
    assert labels == [0]