# DAMERAU
import damerau_branch
import damerau_cadenas
import damerau_trie

# LEVENSHTEIN
import levenshtein_branch
import levenshtein_cadenas
import levenshtein_trie

import sys
import pickle
import re
import numpy
import utils_algoritmica
class CalculoDistancia:
    def __init__(self, palabra, distancia):
        self.palabra = palabra
        self.distancia = distancia
    
    @utils_algoritmica.timer
    def palabrasCercanas(self, metodo, fuente):
        return metodo.palabrasCercanas(fuente, self.palabra, self.distancia)

def syntax():
    print("Llamada incorrecta")
    print("comparador.py <trie_path> <text_path> <palabra> <distancia>")
    exit(1)

def generar_diccionario_palabras(text_path):
    readFile = open(text_path, "r")

    texto = readFile.read()
    er = re.compile("\w+")
    lines = []
    diccionarioPalabras = {}
    for word in er.findall(texto):
        word = word.lower()               
        diccionarioPalabras[word] = diccionarioPalabras.get(word, 0) + 1 
    return diccionarioPalabras

def leer_trie(trie_path):
    with open(trie_path, 'rb') as handle:
        return pickle.load(handle)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        syntax()

    _, trie_path, text_path, palabra, distancia = sys.argv
    distancia = int(distancia)

    trie = leer_trie(trie_path)
    diccionario_palabras = generar_diccionario_palabras(text_path)

    calculoPalabra = CalculoDistancia(palabra, distancia)

    print("Metodo levenshtein_branch")
    print(len(calculoPalabra.palabrasCercanas(levenshtein_branch, trie)), "palabras")
    print()    

    print("Metodo levenshtein_trie")
    print(len(calculoPalabra.palabrasCercanas(levenshtein_trie, trie)), "palabras")
    print()

    print("Metodo levenshtein_cadenas")
    print(len(calculoPalabra.palabrasCercanas(levenshtein_cadenas, diccionario_palabras.keys())), "palabras")
    print()

    print("Metodo damerau_branch")
    print(len(calculoPalabra.palabrasCercanas(damerau_branch, trie)), "palabras")
    print()

    print("Metodo damerau_trie")
    print(len(calculoPalabra.palabrasCercanas(damerau_trie, trie)), "palabras")
    print()

    print("Metodo damerau_cadenas")
    print(len(calculoPalabra.palabrasCercanas(damerau_cadenas, diccionario_palabras.keys())), "palabras")        
    print()
