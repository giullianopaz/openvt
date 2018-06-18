# Python Modules
import sys
import MySQLdb as mysql
import numpy as np
from time import time
from tqdm import tqdm
from json import loads
from threading import Thread
# from memory_profiler import profile
# My Modules
sys.path.insert(0, 'c_modules')
sys.path.insert(0, 'cython_modules')
sys.path.insert(0, 'lib')
from settings import GLOBAL_SETTINGS, DATABASE_SETTINGS, BINARY_FEATURE_DETECTOR_ALG_LIST, NUMERICAL_FEATURE_DETECTOR_ALG_LIST
from textcolors import color, cprint
from utils import  memory_usage_psutil, get_sizeof, fn_timer
from kmajority import Kmajority
from kmeans import Kmeans
from vocabularytree import VocabularyTree, Node, StrDescriptor, ArrayDescriptor

# @profile(precision=10, stream=open('logs/build_memory_profiler.log','a'))
def build():

    K = GLOBAL_SETTINGS["branch-factor"]
    L = GLOBAL_SETTINGS["levels"]
    LEVELS_TO_USE = GLOBAL_SETTINGS["levels-to-use"]
    FEATURE_DETECTOR_ALG = GLOBAL_SETTINGS["feature-detector-alg"].upper()
    FONT_COLOR = GLOBAL_SETTINGS['font-color']

    print("{} Descriptor Extractor:             [{}]".format(memory_usage_psutil(), color(FEATURE_DETECTOR_ALG.upper(), fontcolor=FONT_COLOR, bold=True)))

    print("{} Clusters:                         [{}]".format(memory_usage_psutil(), color(K, fontcolor=FONT_COLOR, bold=True)))

    print("{} Levels:                           [{}]".format(memory_usage_psutil(), color(L, fontcolor=FONT_COLOR, bold=True)))

    # Connect to DATABASE
    print("{} Connecting to the MySQL database...".format(memory_usage_psutil()), end=' ')
    try:
        DB_CONN = mysql.Connect(DATABASE_SETTINGS["host"], DATABASE_SETTINGS["user"], DATABASE_SETTINGS["password"], DATABASE_SETTINGS["database"])
        DB_CURSOR = mysql.cursors.SSCursor(DB_CONN)
    except Exception as e:
        raise e
    cprint("OK\n", fontcolor=FONT_COLOR, bold=True)

    print("{} Loading image info from the database...".format(memory_usage_psutil()), end=' ')
    start_time = time()
    try:
        DB_CURSOR.execute('''
            SELECT _id, _descriptors
            FROM {}
            ;
            '''.format(DATABASE_SETTINGS["table"]))
    except Exception as e:
        raise e
    cprint("OK ({} seg)\n".format(time() - start_time), fontcolor=FONT_COLOR, bold=True)

    # Variável global para armazenar os bit-string-descriptors(BSV) das imagens
    BIT_STRING_VECTOR = []
    N_IMAGES = 0

    start_time = time()
    print("{} Building Descriptor Vector...".format(memory_usage_psutil()), end=' ')
    # Percorre imagens da base de dados
    for image_id, descriptors in DB_CURSOR:
        N_IMAGES += 1

        if FEATURE_DETECTOR_ALG in BINARY_FEATURE_DETECTOR_ALG_LIST:
            for bit_string in loads(descriptors):
                BIT_STRING_VECTOR.append(StrDescriptor(bit_string))
                BIT_STRING_VECTOR[-1].IMAGE_ID = image_id
        elif FEATURE_DETECTOR_ALG in NUMERICAL_FEATURE_DETECTOR_ALG_LIST:
            for des in loads(descriptors):
                BIT_STRING_VECTOR.append(np.array(des).view(ArrayDescriptor))
                BIT_STRING_VECTOR[-1].IMAGE_ID = image_id
        else:
            raise Exception("Algoritmo não foi adicionado à lista de algoritmos válidos!")
    elapsed_time = time() - start_time
    cprint("OK ({} min)\n".format(elapsed_time/60), fontcolor=FONT_COLOR, bold=True)

    print("{} Images:                           [{}]".format(
        memory_usage_psutil(),
        color(N_IMAGES, fontcolor=FONT_COLOR, bold=True)))

    print("{} Descriptors:                      [{} | {}]".format(
        memory_usage_psutil(),
        color(len(BIT_STRING_VECTOR), fontcolor=FONT_COLOR, bold=True),
        color(get_sizeof(BIT_STRING_VECTOR), fontcolor=FONT_COLOR, bold=True)))

    # Fecha conexão
    print("{} Closing the connection to the database...".format(memory_usage_psutil()), end=' ')
    try:
        DB_CURSOR.close()
        DB_CONN.close()
    except Exception as e:
        raise e
    cprint("OK\n", fontcolor=FONT_COLOR, bold=True)

    # for elem in BIT_STRING_VECTOR[:10]:
    #     print(len(elem) , elem)
    # exit()

    if FEATURE_DETECTOR_ALG in BINARY_FEATURE_DETECTOR_ALG_LIST:
        print("{} Setting K-Majority to clustering...".format(memory_usage_psutil()), end=' ')
        clustering = Kmajority(n_clusters=K)
        cprint("OK\n", fontcolor=FONT_COLOR, bold=True)
    elif FEATURE_DETECTOR_ALG in NUMERICAL_FEATURE_DETECTOR_ALG_LIST:
        print("{} Setting K-Means to clustering...".format(memory_usage_psutil()), end=' ')
        clustering = Kmeans(n_clusters=K)
        cprint("OK\n", fontcolor=FONT_COLOR, bold=True)
    else:
        raise Exception("Algoritmo não foi adicionado à lista de algoritmos válidos!")

    start_time = time()
    print("{} Building Vocabulary Tree...".format(memory_usage_psutil()))
    vocab_tree = VocabularyTree()
    vocab_tree.create(  clustering=clustering,
                        bit_string_vector=tuple(BIT_STRING_VECTOR),
                        n_images=N_IMAGES,
                        L=L,
                        levels_to_use=LEVELS_TO_USE)
    elapsed_time = time() - start_time
    cprint("OK ({} min)\n".format(elapsed_time/60), fontcolor=FONT_COLOR, bold=True)
    BIT_STRING_VECTOR.clear()

    print("{} Inverted Files:                     [{} | {}]".format(
        memory_usage_psutil(),
        color(len(vocab_tree.inverted_file.keys()), fontcolor=FONT_COLOR, bold=True),
        color(get_sizeof(vocab_tree.inverted_file), fontcolor=FONT_COLOR, bold=True)))
    
    print("{} Nodes:                              [{} | {}]".format(
        memory_usage_psutil(),
        color(vocab_tree.n_nodes, fontcolor=FONT_COLOR, bold=True),
        color(get_sizeof(vocab_tree.tree), fontcolor=FONT_COLOR, bold=True)))
    
    del BIT_STRING_VECTOR, clustering, L, K, LEVELS_TO_USE, FEATURE_DETECTOR_ALG, FONT_COLOR
    return vocab_tree, N_IMAGES

if __name__ == '__main__':
    build()