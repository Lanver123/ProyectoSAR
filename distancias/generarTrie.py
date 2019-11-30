#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Cardona Lorenzo, Victor
# Gavilán Gil, Marc
# Martínez Bernia, Javier
# Murcia Serrano, Andrea

import sys
import os
import pprint
import json
import re
import pickle

def syntax():
    print("argumentos <archivo.txt> <nombre_output>")
    exit(1)

def generarTrie(texto, nombre_output):
    er = re.compile("\w+")
    #diccionario que guarda todos los nodos
    trie = {}
    numNodes = 0
    #cada elemento del vacabulario es una lista de nodo padre, si es palabra final y cual, y un diccionario
    #   con la key la siguiente letra y devuelve el nodo hijo
    trie[0] = [None, None, {}]
    for word in er.findall(texto):
        # pasar la palabra a minusculas
        word = word.lower()
        nodeCurrent = 0
        for i, letter in enumerate(word):
            #se recupera el nodo siguiente
            nodeChild = trie[nodeCurrent][2].get(letter)
            if nodeChild is None:
                #si no existe el nodo siguiente, se crea, con su tripleta viendo si es palabra final y 
                #se añade este nuevo nodo al diccionario del padre, ademas del diccionario de todos los nodos
                numNodes = numNodes + 1
                nodeChild = numNodes
                childList = [nodeCurrent, None, {}]
                trie[nodeCurrent][2][letter] = nodeChild
                trie[nodeChild] = childList
            #para ir recorriendo el trie
            nodeCurrent = nodeChild
            #si es la ultima letra, se ha procesado toda la palabra y se añade como nodo final
            if i + 1 == len(word):
                trie[nodeCurrent][1] = word  
    
        #Guardar el trie generado en memoria secundaria
        with open(nombre_output, 'wb') as handle:
            pickle.dump(trie, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        syntax()
    
    readFile = open(sys.argv[1], "r")
    texto = readFile.read()
    
    generarTrie(texto, sys.argv[2])
