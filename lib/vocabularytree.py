import numpy as np
# from utils import memory_usage_psutil

# Subclasse da classe str para armazenar descritores do tipo str
'''361 bytes para cada descritor'''
class StrDescriptor(str):
    __slots__ = ['IMAGE_ID']
    def __init__(self, value):
        self = str.__new__(StrDescriptor, value)

# Subclasse da classe ndarray para armazenar descritores do tipo list
# des.append(np.array(image['des'][0]).view(ArrayDescriptor))
# des[-1].image = image['_id']
class ArrayDescriptor(np.ndarray):
    __slots__ = ['IMAGE_ID']
    def __init__(self):
        self.IMAGE_ID = None

# LEAVES = []
INVERTED_FILE = {}
COUNTER = 0

# Cria TF_IDF em relação aos descritores das imagens que passaram pelo nodo
def TF_IDF(bit_string_vector):
    # Dicionário de retorno
    ret = {}
    # Percorre descritores presentes no nodo
    for bsv in bit_string_vector:
        if isinstance(bsv, (StrDescriptor, ArrayDescriptor)):
            # Testa se imagem já foi adicionada ao dicionário
            if bsv.IMAGE_ID in ret.keys():
                # Se sim, incrementa contador
                ret[bsv.IMAGE_ID] += 1
            else:
                # Se não, adiciona imagem ao dicionário
                ret[bsv.IMAGE_ID] = 1
        else:
            continue
    return ret

class Node:
    __slots__ = 'level', 'W', 'centroids', 'children'
    def __init__(self, _clustering=None, _bit_string_vector=[], _n_images=0, _level=0, _levels_to_use=0):
        # self.id = None
        # Nível do nodo na árvore
        self.level = _level
        global COUNTER
        COUNTER += 1

        if self.level <= _levels_to_use:
            # Dicionário { image_id: mi }
            # EX: 'images/infrared/1.jpg': [6, 0.6106961658596544]
            tf_idf = TF_IDF(_bit_string_vector)

            # _n_images: Quantidade total de imagens na base de dados
            # Ni: Quantidade de imagens que tiveram pelo menos um descritor passado pelo nodo
            # self.W: ln( _n_images/Ni)
            Ni = len(tf_idf.keys())
            self.W = np.log(_n_images/Ni) # [Equação 4]

            # Multiplica os valores(Mi) das imagens pelo peso(self.W)
            # Dicionário { image_id: mi*Wi }
            # EX: 'images/infrared/1.jpg': 0.6106961658596544
            for image in tf_idf.keys():
                # Mi * self.W
                tf_idf[image] = tf_idf[image] * self.W

            # Adiciona dados do nodo ao Inverted File
            # Dicionário de dicionários {node_id : { image_id: mi*wi } }
            ''' Inverted file é um dicionario de dicionários onde a chave é o ID do nodo e 
            o valor é outro dicionário, o qual a chave é o ID da imagem e o valor é mi*wi da imagem no nodo i'''
            INVERTED_FILE[self] = tf_idf

            tf_idf = None
            del tf_idf, Ni

        # Testa de chegou às folhas ou se tem poucos descritrores
        if self.level == 0 or len(_bit_string_vector) <= _clustering.n_clusters*3:
            # Adiciona à lista de folhas
            # memory_usage_psutil()
            # Deleta variáveis desnecessárias
            _bit_string_vector = None
            del _clustering, _n_images, _levels_to_use, _bit_string_vector, _level
            # Para de descer
            return
        
        # Calcula clusters dos seus descritores
        self.centroids, clusters = _clustering.predict(_bit_string_vector)
        del _bit_string_vector, _level
        # Divide seus clusters entre seus nodos filho
        self.children = [Node(  _clustering=_clustering,
                                _bit_string_vector=tuple(clusters[i]),
                                _n_images=_n_images,
                                _level=self.level-1,
                                _levels_to_use=_levels_to_use) for i in range(len(clusters))]
        # Deleta variáveis desnecessárias
        clusters = None
        del _clustering, _n_images, _levels_to_use, clusters
        

class VocabularyTree:
    __slots__ = 'tree', 'inverted_file', 'n_nodes'
    def __init__(self):
        self.tree = None
        # self.leaves = LEAVES
        self.inverted_file = INVERTED_FILE

    def create(self, clustering=None, bit_string_vector=[], n_images=0, L=0, K=0, levels_to_use=0):
        self.tree = Node(   _clustering=clustering,
                            _bit_string_vector=bit_string_vector,
                            _n_images=n_images,
                            _level=L,
                            _levels_to_use=levels_to_use)
        self.n_nodes = COUNTER