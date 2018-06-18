from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

class Kmeans():
    """Classe para agrupar descritores das imagens"""
    def __init__(self, n_clusters=3):
        # Quantidade de cluster(grupos) que serão gerados
        self.n_clusters = n_clusters

    def _clusters(self, pred, des):
        '''Zipa descritores com valores preditos'''
        # zip([1, 1, 2, ..., 0], [12.44, 22.5, 54.4, ... , 22.5] ~> [(1, 12.44), (1, 22.5), (2, 54.4), ..., (0, 22.5)]
        pred_des = zip(pred, des)
        
        # Cria lista para receber os grupos
        clusters = [[] for _ in range(self.n_clusters)]
        
        # Percorre lista zipada adicionando descritores nos respectivos grupos
        for (p, d) in pred_des:
            clusters[p].append(d)
        return clusters

    def predict(self, X):
        # Istancia classe (Nesse caso, sklearn.cluster.KMeans)
        kmeans_instance = KMeans(n_clusters=self.n_clusters, random_state=0)
        # Calcula clusters e gera vetor de clusters
        # EX: pred = [1, 1, 3, 2, ..., 3, 2, 0, 0]
        pred = kmeans_instance.fit_predict(X)

        return (kmeans_instance.cluster_centers_, np.array([elem for elem in self._clusters(pred, X)]))