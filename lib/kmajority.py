import numpy as np
from utils import hamming_distance, majority, memory_usage_psutil, c_hamming_distance
import time
import sys
# import gc
# gc.set_debug(gc.DEBUG_STATS)

class Kmajority():
    def __init__(self, n_clusters):
        self.n_clusters = n_clusters

    def predict(self, bit_string_vector=[]):
        n_bits = len(bit_string_vector[0])
        # print(n_bits)
        # Inicializa Lista de centroids aleatoriamente
        # centroids = self.random_bit_string_vector(size=self.n_clusters, n_bits=n_bits)
        centroids = self.init_centroids(bit_string_vector)
        # Inicializa clusters
        clusters = {}
        
        # memory_usage_psutil()
        while True:
            # memory_usage_psutil()
            # Guarda cópia dos centroids para comparação
            old_clusters = clusters.copy()

            # Reseta clusters
            clusters.clear()

            # Percorre lista de descritores
            for b_string in bit_string_vector:
                # Escolhe os centroids
                # choice = min([(hamming_distance(b_string, c, n_bits), c) for c in centroids])[1]
                choice = min([(c_hamming_distance(b_string, c), c) for c in centroids])[1]

                # Adiciona descritor ao seu cluster
                if choice in clusters.keys():
                    clusters[choice].append(b_string)
                else:
                    clusters[choice] = [b_string]

            # Ajusta centroids
            centroids = [majority(data=value, data_len=len(value), n_bits=n_bits) for key, value in clusters.items()]
                
            # Testa se os centroids sofreram modificações
            if old_clusters == clusters:
                break
        centroids = None; old_clusters = None
        del n_bits, centroids, old_clusters
        return tuple(clusters.keys()), tuple(clusters.values())

    def init_centroids(self, bit_string_vector):
        ret = []
        while True:
            choice = np.random.choice(bit_string_vector)
            if choice not in ret:
                ret.append(choice)
            if len(ret) == self.n_clusters:
                break
        return ret

    # Método para gerar um vetor de bit strings aleatoriamente
    def random_bit_string_vector(self, size=0, n_bits=256):       
        bit_string_vector = ['']*size
        for i in range(size):
            for _ in range(n_bits):
                bit_string_vector[i] += np.random.choice(['0', '1'])
        return bit_string_vector


if __name__ == '__main__':
    pass