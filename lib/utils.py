# Python Modules
import numpy as np
from sys import path, getsizeof
from os import walk, getpid
from time import time
from psutil import Process
from collections import Mapping, Container
from functools import wraps
# from memory_profiler import profile
# My Modules
path.insert(0, '../cython_modules')
path.insert(0, '../c_modules')
from cp_utils import cp_majority, cp_hamming_distance, cp_to_bit_string, cp_to_n_bits
from MyUtils import hamming_distance as _hamming_distance
from textcolors import color
from vocabularytree import Node

# Cria lista de imagens
# @profile(precision=10, stream=open('logs/utils_memory_profiler.log','a'))
def make_image_list(dataset_path):
      images_list = []
      for dataset_path, _, images in walk(dataset_path):
            images_list += [str(dataset_path) + '/' + elem.strip() for elem in images]
      return tuple(images_list)

def chi2_distance(histA, histB, eps = 1e-10):
    # compute the chi-squared distance
    dist = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])

    # return the chi-squared distance
    # print("Distance: {}".format(dist))
    return dist

# Calcula distância de Hamming entre duas string de bits
def hamming_distance(bit_string_1, bit_string_2, bit_string_len):
    if len(bit_string_1) != len(bit_string_2):
        raise Exception('[ERROR] String de bits de tamanhos diferentes!')
    return cp_hamming_distance(bit_string_1, bit_string_2, bit_string_len)

def c_hamming_distance(bit_string_1, bit_string_2):
    if len(bit_string_1) != len(bit_string_2):
        raise Exception('[ERROR] String de bits de tamanhos diferentes!')
    return _hamming_distance(bit_string_1, bit_string_2)

def majority(data=[], data_len=0, n_bits=256):
    if len(data) <= 0:
        return None
    return cp_majority(data, data_len, n_bits)

# Transforma valores inteiros em bytes
def to_bit_string(des=[], n_bits=8):
    return cp_to_bit_string(des, len(des), n_bits)
    # ret = ''
    # if isinstance(des, (int, str)):
    #     des = [des]

    # for elem in des:
    #     ret += to_n_bits(format(elem, 'b'), n_bits=n_bits) 
    # return ret

# Formatiza string de bits para 8 bits
def to_n_bits(bit_string, n_bits=8):
    return cp_to_n_bits(bit_string, n_bits)
    # return '0'*(n_bits - len(bit_string)) + str(bit_string)

def memory_usage_psutil():
    # return the memory usage in percentage like top
    process = Process(getpid())
    mem = process.memory_info()[0]
    if mem > float(2**30):
        mem = color("{}GB".format(str(mem / float(2 ** 30))[:6]), fontcolor='red', bold=True)
    elif mem > float(2**20):
        mem = color("{}MB".format(str(mem / float(2 ** 20))[:6]), fontcolor='yellow', bold=True)
    elif mem > float(2**10):
        mem = color("{}KB".format(str(mem / float(2 ** 10))[:6]), fontcolor='green', bold=True)
    else:
        mem = color("{}B".format(mem), fontcolor='green', bold=True)
    return "  | {}% | {} |".format(str(process.memory_percent())[:6], mem)

def deep_get_sizeof(_object, _id_list=set()):
    _deep_get_sizeof = deep_get_sizeof
    if id(_object) in _id_list:
        return 0
    r = getsizeof(_object)
    _id_list.add(id(_object))
    if isinstance(_object, str):
        return r
    if isinstance(_object, (Node)):
        try:
            # Está nos níveis a serem utilizados
            r += _deep_get_sizeof(_object.W, _id_list)
        except Exception as e:
            pass
        try:
            # Demais nodos
            r += _deep_get_sizeof(_object.level, _id_list) + _deep_get_sizeof(_object.centroids, _id_list)
            r += sum(_deep_get_sizeof(c, _id_list) for c in _object.children)
        except Exception as e:
            # É folha
            r += _deep_get_sizeof(_object, _id_list) + _deep_get_sizeof(_object.level, _id_list)
        return r
    if isinstance(_object, Mapping):
        return r + sum(_deep_get_sizeof(k, _id_list) + _deep_get_sizeof(v, _id_list) for k, v in _object.items())
    if isinstance(_object, Container):
        return r + sum(_deep_get_sizeof(x, _id_list) for x in _object)
    return r

def get_sizeof(_object=None):
    id_list = set()
    mem = deep_get_sizeof(_object, id_list)
    id_list.clear(); del id_list
    if mem > float(2**30):
        mem = color("{}GB".format(str(mem / float(2 ** 30))[:6]), fontcolor='red', bold=True)
    elif mem > float(2**20):
        mem = color("{}MB".format(str(mem / float(2 ** 20))[:6]), fontcolor='yellow', bold=True)
    elif mem > float(2**10):
        mem = color("{}KB".format(str(mem / float(2 ** 10))[:6]), fontcolor='green', bold=True)
    else:
        mem = color("{}B".format(mem), fontcolor='green', bold=True)
    return mem

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time()
        result = function(*args, **kwargs)
        t1 = time()
        print(" Total time running {}: {} seconds".format(function.__name__, str(t1-t0)))
        return result
    return function_timer


if __name__ == '__main__':
    print("\n{}".format(c_hamming_distance('10000000000000000000', '10000000000000100001')))