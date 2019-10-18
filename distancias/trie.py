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
import numpy as np

if __name__ == "__main__":

    texto = "caro cara codo caros"
    er = re.compile("\w+")
    #diccionario que guarda todos los nodos
    trie = {}
    numNodes = 0
    #cada elemento del vacabulario es una lista de nodo padre, si es palabra final y cual, y un diccionario
    #   con la key la siguiente letra y devuelve el nodo hijo
    trie[0] = [None, None, {}]
    for word in er.findall(texto):
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
                if i + 1 == len(word):
                    childList[1] = word
                trie[nodeCurrent][2][letter] = nodeChild
                trie[nodeChild] = childList
            #para ir recorriendo el trie
            nodeCurrent = nodeChild
    print trie
            
            
         