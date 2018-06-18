#!python
#cython: language_level=3, wraparound=False, boundscheck=False
import numpy as np
# cimport numpy as np
cpdef cp_majority(data, unsigned int data_len, unsigned int n_bits):
    cdef Py_ssize_t i = 0
    cdef Py_ssize_t j = 0
    cdef long[:] counter = np.zeros(n_bits, dtype=np.int)
    # Percorre lista de descritores
    for i in range(data_len):
        # Vai de zero até n_bits
        for j in range(n_bits):
            # Se, nessa posição, o bit for 1, incrementa
            if data[i][j] == '1':
                counter[j] += 1
    # Percorre lista de retorno
    i = 0
    ret = ''
    cpdef int data_len_half = data_len//2
    for i in range(n_bits):
        # Se for >= que zero, o bit majority é 1
        if counter[i] >= data_len_half:
            ret += '1'
        else:
            ret += '0'
    # print("\nret: ",ret)
    return ''.join(ret)

cpdef cp_hamming_distance(bit_string_1, bit_string_2, unsigned int bit_string_len):
    # Declara contador
    cpdef unsigned int count = 0
    # Declara iterador
    cdef Py_ssize_t i = 0
    # Percorre string_bits comparando elas bit a bit
    for i in range(bit_string_len):
        # Se bits são diferentes, incrementa contador
        if(bit_string_1[i] != bit_string_2[i]):
            count += 1
    return count

cpdef cp_to_bit_string(array_des, unsigned int array_des_len, unsigned int n_bits):
    cdef Py_ssize_t i = 0
    if isinstance(array_des, (int)):
        array_des = [array_des]
    ret = ''
    for i in range(array_des_len):
        ret += cp_to_n_bits(bit_string=format(array_des[i], 'b'), n_bits=n_bits) 
    return ret

# Formatiza string de bits para 8 bits
cpdef cp_to_n_bits(bit_string, unsigned int n_bits):
    return '0'*(n_bits - len(bit_string)) + bit_string
