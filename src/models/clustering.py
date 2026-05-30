from sklearn.cluster import KMeans

class VacancyClusteringModel:
    def __init__(self, n_clusters: int = 2, random_state: int = 42):
        self.model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")

    def fit_predict(self, tfidf_matrix: list[list[float]]) -> list[int]:
        if not tfidf_matrix or len(tfidf_matrix) < self.model.n_clusters:
            return [0] * len(tfidf_matrix)
            
        cluster_labels = self.model.fit_predict(tfidf_matrix)
        return cluster_labels.tolist()