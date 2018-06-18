# Python Modules
from sys import path
from MySQLdb import Connect
from tqdm import tqdm
from json import dumps
# from memory_profiler import profile
# My Modules
path.insert(0, 'c_modules')
path.insert(0, 'cython_modules')
path.insert(0, 'lib')
from textcolors import color, cprint
from descriptorextractor import DescriptorExtractor
from utils import to_bit_string, memory_usage_psutil, make_image_list
from settings import GLOBAL_SETTINGS, DATABASE_SETTINGS, BINARY_FEATURE_DETECTOR_ALG_LIST, NUMERICAL_FEATURE_DETECTOR_ALG_LIST

DATASET_PATH = GLOBAL_SETTINGS["dataset"]
FEATURE_DETECTOR_ALG = GLOBAL_SETTINGS["feature-detector-alg"].upper()
FONT_COLOR = GLOBAL_SETTINGS['font-color']

# @profile(precision=10, stream=open('logs/extract_memory_profiler.log','a'))
def extract():
    print("{} Descriptor Extractor:             [{}]".format(memory_usage_psutil(), color(FEATURE_DETECTOR_ALG.upper(), fontcolor=FONT_COLOR, bold=True)))

    # Pega lista de imagens
    images_list = make_image_list(DATASET_PATH)
    print("{} Images:                           [{}]".format(memory_usage_psutil(), color(len(images_list), fontcolor=FONT_COLOR, bold=True)))

    # Connect to DATABASE
    print("{} Connecting to the MySQL database...".format(memory_usage_psutil()), end=' ')
    try:
        DB_CONN = Connect(DATABASE_SETTINGS["host"], DATABASE_SETTINGS["user"], DATABASE_SETTINGS["password"], DATABASE_SETTINGS["database"])
        DB_CURSOR = DB_CONN.cursor()
    except Exception as e:
        raise e
    cprint("OK\n", fontcolor=FONT_COLOR, bold=True)

    # Tenta apagar tabela antiga de imagens
    print("{} Dropping the existing image table...".format(memory_usage_psutil()), end=' ')
    try:
        DB_CURSOR.execute("DROP TABLE {};".format(DATABASE_SETTINGS["table"]))
    except Exception as e:
        pass
    cprint("OK\n", fontcolor=FONT_COLOR, bold=True)

    print("{} Creating image table...".format(memory_usage_psutil()), end=' ')
    try:
        DB_CURSOR.execute('''
        CREATE TABLE {}
        (
        _id INT PRIMARY KEY,
        _path VARCHAR(255) NOT NULL UNIQUE,
        _descriptors JSON
        );'''.format(DATABASE_SETTINGS["table"]))
    except Exception as e:
        raise e
    cprint("OK\n", fontcolor=FONT_COLOR, bold=True)

    # Instancia classe de extração de descritores
    des_extract = DescriptorExtractor()
    print("{} Extracting Descriptors".format(memory_usage_psutil()))

    for i in tqdm(iterable=range(0, len(images_list)), ncols=90, unit='images'):
        # Extract image descriptors
        des = des_extract.extract(img_name=images_list[i], feature_detector_alg=FEATURE_DETECTOR_ALG)
        # Insert a img to images collection
        if des:
            if FEATURE_DETECTOR_ALG in BINARY_FEATURE_DETECTOR_ALG_LIST:
                try:
                    DB_CURSOR.execute('''
                        INSERT INTO {}
                        VALUES ({}, '{}', '{}')
                        ;
                        '''.format(
                            DATABASE_SETTINGS["table"], # Nome da tabela
                            int(images_list[i].split('/')[-1]), #ID da imagem em INT
                            images_list[i], # Caminho até a imagem
                            dumps([to_bit_string(elem) for elem in des]) # bit-string-descriptors em JSON
                            )
                    )
                except Exception as e:
                    raise e
            elif FEATURE_DETECTOR_ALG in NUMERICAL_FEATURE_DETECTOR_ALG_LIST:
                try:
                    DB_CURSOR.execute('''
                        INSERT INTO {}
                        VALUES ({}, '{}', '{}')
                        ;
                        '''.format(
                            DATABASE_SETTINGS["table"], # Nome da tabela
                            i, #int(images_list[i].split('/')[-1]), #ID da imagem em INT
                            images_list[i], # Caminho até a imagem
                            dumps([elem for elem in des]) # array-descriptors em JSON
                            )
                    )
                except Exception as e:
                    raise e


            else:
                raise Exception("Algoritmo não foi adicionado à lista de algoritmos válidos!")
        des = None
        del des

    print("{} Descriptors:                      [{}]".format(memory_usage_psutil(), color(des_extract.size, fontcolor=FONT_COLOR, bold=True)))

    print("{} Descriptors per image:            [{}]".format(memory_usage_psutil(), color(des_extract.size/len(images_list), fontcolor=FONT_COLOR, bold=True)))

    images_list = None
    del images_list, des_extract

    # Confirma alterações no BD
    print("{} Writing data in the database...".format(memory_usage_psutil()), end=' ')
    try:
        DB_CONN.commit()
    except Exception as e:
        raise e
    cprint("OK\n", fontcolor=FONT_COLOR, bold=True)

    # Fecha conexão
    print("{} Closing the connection to the database...".format(memory_usage_psutil()), end=' ')
    try:
        DB_CONN.close()
    except Exception as e:
        raise e
    cprint("OK\n", fontcolor=FONT_COLOR, bold=True)

if __name__ == '__main__':
    extract()
