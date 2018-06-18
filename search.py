# Python Modules
import numpy as np
from scipy.spatial import distance as dist
from cv2 import compareHist, HISTCMP_BHATTACHARYYA, HISTCMP_CHISQR_ALT, HISTCMP_KL_DIV, HISTCMP_CHISQR
from sys import path
from time import ctime
from MySQLdb import Connect
# from memory_profiler import profile
# My Modules
print("\n  Benchmark Init: [{}]\n".format(ctime()))
path.insert(0, 'c_modules')
path.insert(0, 'cython_modules')
path.insert(0, 'lib')
from build import build
from descriptorextractor import DescriptorExtractor
from settings import GLOBAL_SETTINGS, SEARCH_SETTINGS, DATABASE_SETTINGS, BINARY_FEATURE_DETECTOR_ALG_LIST, NUMERICAL_FEATURE_DETECTOR_ALG_LIST
from utils import c_hamming_distance, memory_usage_psutil, to_bit_string, chi2_distance

np.set_printoptions(suppress=False)
VOCAB_TREE, N_IMAGES = build()
TOP_N_RESULTS = SEARCH_SETTINGS['top-n-results']
FEATURE_DETECTOR_ALG = GLOBAL_SETTINGS['feature-detector-alg']
LEVELS_TO_USE = GLOBAL_SETTINGS['levels-to-use']
HIST_COMP_METHOD = SEARCH_SETTINGS['hist-comp-method']

# Histrograma da Query
QUERY_HISTOGRAM = {}
# Dicionário de Histogramas de imagens para calcular o Score
MATCHED_IMAGES = {}

# Método para explorar a VocabTree
# @profile(precision=10, stream=open('logs/benchmark_memory_profiler.log','a'))
def explore(node, bit_string_des, ni):
    # Testa se o nodo está abaixo da linha de níveis a serem usados
    if node.level <= LEVELS_TO_USE:
        # Calcula histograma da query
        if node in QUERY_HISTOGRAM.keys():
            QUERY_HISTOGRAM[node] += node.W
        else:
            QUERY_HISTOGRAM[node] = node.W

    # Testa se nodo não é folha
    if node.level != 0:
        try:
            if FEATURE_DETECTOR_ALG in BINARY_FEATURE_DETECTOR_ALG_LIST:
                index = min([(c_hamming_distance(to_bit_string(bit_string_des), node.centroids[i]), i) for i in range(len(node.centroids))])[1]
            elif FEATURE_DETECTOR_ALG in NUMERICAL_FEATURE_DETECTOR_ALG_LIST:
                index = min([(dist.euclidean(bit_string_des, node.centroids[i]), i) for i in range(len(node.centroids))])[1]
            else:
                raise Exception("Algoritmo não foi adicionado à lista de algoritmos válidos!")
            
            explore(node.children[index], bit_string_des, ni)
        except Exception as e:
            pass
    else:
        global MATCHED_IMAGES
        for image_id in VOCAB_TREE.inverted_file[node].keys():   
            if image_id not in MATCHED_IMAGES.keys():
                MATCHED_IMAGES[image_id] = []

# Método para calcular histogramas
def compare_hist(hist1, hist2, hist_comp_method=1):
    ret = 0
    if hist_comp_method == 1:
        'Bhattacharyya distance (In fact, OpenCV computes Hellinger distance) - 91.75% to 100 images'
        ret = compareHist(hist1, hist2, method=HISTCMP_BHATTACHARYYA)
    elif hist_comp_method == 2:
        'Alternative Chi-Square - 92.0% to 100 images'
        ret = compareHist(hist1, hist2, method=HISTCMP_CHISQR_ALT)
    elif hist_comp_method == 3:
        'Kullback-Leibler divergence - 90.75% to 100 images'
        ret = compareHist(hist1, hist2, method=HISTCMP_KL_DIV)
    elif hist_comp_method == 4:
        'Chi-Square - 89.5% to 100 images'
        ret = compareHist(hist1, hist2, method=HISTCMP_CHISQR)
    elif hist_comp_method == 5:    
        'Euclidean Distance - 90.5% to 100 images'
        ret = dist.euclidean(hist1, hist2)
    return ret

# @profile(precision=10, stream=open('logs/benchmark_memory_profiler.log','a'))
def image_search(query_path, hist_comp_method=4, top_n_results=4):
    global QUERY_HISTOGRAM
    global MATCHED_IMAGES
    QUERY_HISTOGRAM = {}
    MATCHED_IMAGES = {}
    
    # Instancia classe de extração de descritores
    des_extract = DescriptorExtractor()
    bit_string_vector = des_extract.extract(img_name=query_path, feature_detector_alg=FEATURE_DETECTOR_ALG)
    # Percorre lista de descritores da imagem
    for bit_string_des in bit_string_vector:
        # Explora recursivamente a VocabTree
        explore(VOCAB_TREE.tree, bit_string_des, len(bit_string_vector))

    bit_string_vector = None
    del bit_string_vector, des_extract

    # global MATCHED_IMAGES
    # print("[{}] MATCHED_IMAGES: {}".format(len(MATCHED_IMAGES), MATCHED_IMAGES))

    # Percorre lista de imagens que podem ser semelhantes
    for d_image in MATCHED_IMAGES.keys():
        # Percorre lista de nodos pelos quais os descritores da Query passaram
        for node in QUERY_HISTOGRAM.keys():
            # Testa se imagem passou pelo nodo em quastão
            if d_image in VOCAB_TREE.inverted_file[node].keys():
                # Se sim, adiciona qi ao histograma
                MATCHED_IMAGES[d_image].append(VOCAB_TREE.inverted_file[node][d_image])
            else:
                # Semão, adiciona 0 ao histograma
                MATCHED_IMAGES[d_image].append(0)


    # Mostra lista de imagens
    # print("\n\nd_images: ")
    # Percorre chaves do dicionário de imagens possivelmente semelhantes
    for key in MATCHED_IMAGES.keys():
        # Normaliza histograma da imagem da base de dados
        MATCHED_IMAGES[key] = np.array(tuple(MATCHED_IMAGES[key])) / np.linalg.norm(np.array(tuple(MATCHED_IMAGES[key])), ord=1)
        MATCHED_IMAGES[key] = MATCHED_IMAGES[key].astype('float32')
        # Mostra histrograma
        # print("\n\n[{}] {} ~> {}".format(MATCHED_IMAGES[key].size, key, MATCHED_IMAGES[key]))

    # Normaliza histograma da query
    q_values = np.array(tuple(QUERY_HISTOGRAM.values())) / np.linalg.norm(np.array(tuple(QUERY_HISTOGRAM.values())), ord=1)
    q_values = q_values.astype('float32')
    # Mostra histograma da query
    # print("\n\n[{}] {} ~> {}".format(q_values.size, "query", q_values))

    # CALCULA SCORE
    score = []
    for _image_id in MATCHED_IMAGES.keys():
        if q_values.size != MATCHED_IMAGES[_image_id].size:
            raise Exception("Query histogram and database image histogram are different!")
        # Compara histogramas
        s = compare_hist(q_values, MATCHED_IMAGES[_image_id], hist_comp_method)
        score.append((s, _image_id))

    q_values = None
    del q_values
    # Ordena score
    score.sort()
    del score[top_n_results:]

    image_list = []

    # Connect to DATABASE
    try:
        DB_CONN = Connect(DATABASE_SETTINGS["host"], DATABASE_SETTINGS["user"], DATABASE_SETTINGS["password"], DATABASE_SETTINGS["database"])
        DB_CURSOR = DB_CONN.cursor()
    except Exception as e:
        raise e

    for _s, _image_id in score:
        try:
            DB_CURSOR.execute('''
                SELECT _path
                FROM {}
                WHERE _id = {}
                ;
                '''.format(DATABASE_SETTINGS["table"], _image_id))
            query_image_path = DB_CURSOR.fetchall()[0][0].split('/')[-1]

            image_list.append((_s, query_image_path))
        except Exception as e:
            raise Exception("Error to read image path from database!!")
    
    # Fecha conexão
    try:
        DB_CONN.close()
    except Exception as e:
        raise e

    return image_list

if __name__ == '__main__':
    while True:
        query_path = input(" > ")
        
        if query_path.upper() == 'XX':
            break

        image_search(query_path, hist_comp_method=HIST_COMP_METHOD, top_n_results=TOP_N_RESULTS)