#include <string.h>
#include <string>
#include <iostream>
// #include </usr/include/python3.5m/Python.h>
#include <Python.h>
#include <vector>

// Funcao para calcular a distancia de hamming entre duas bit string
int c_hamming_distance(char string1[], char string2[]){
    // Testa se o tamanho das bit string sao diferentes
    if(strlen(string1) != strlen(string2)) return -1;
    // Declara contador
    int count = 0;
    // Percorre bit strings contando diferencas
    for(unsigned int i = 0; i < strlen(string1); i++){
        if(string1[i] != string2[i]) count++;
    }
    // Retorna quantidade de diferencas
    return count;
}

// Metodo do tipo PyObject
static PyObject * _hamming_distance(PyObject * self, PyObject * args){
  // Declara variaveis para receber os argumentos
  char * string1;
  char * string2;
  // faz o parsing dos argumentos para as variaveis
  if (!PyArg_ParseTuple(args, "s|s", &string1, &string2)) return NULL;
  // Retorna valor do tipo ponteiro Python
  return Py_BuildValue("i", c_hamming_distance(string1, string2));
}

// Metodo para especificar meus metodos
static PyMethodDef myMethods[] = {
  {"hamming_distance", _hamming_distance, METH_VARARGS, "Calculate the Hamming Distance."},
  {NULL, NULL, 0, NULL}
};

// Metodo para definir dados do meu modulo
static struct PyModuleDef MyUtils = {
  PyModuleDef_HEAD_INIT,
  "MyUtils",
  "My Utils Module",
  -1,
  myMethods
};

// Cria meu modulo
PyMODINIT_FUNC PyInit_MyUtils(void){
  return PyModule_Create(&MyUtils);
}