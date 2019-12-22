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


def syntax():
    print("argumentos <trieGenerado.txt> <palabra> <distancia max>")
    exit(1)


def palabrasCercanas(trie, palabra, distancia):
    M = np.empty(dtype=np.int8, shape=(len(palabra)+1, len(trie)))
    for i in range(len(palabra)+1):
        M[i, 0] = i
    for j in range(len(trie)):
        profun = 0
        padre = trie[j][0]
        while padre != None:
            padre = trie[padre][0]
            profun += 1
        M[0, j] = profun

    for i in range(1, len(palabra)+1):
        for j in range(1, len(trie)):
            costeBorr = M[i-1, j]+1
            padre = trie[j][0]
            costeIns = M[i,padre] + 1
            costeSus = M[i-1,padre] + (trie[padre][2].get(palabra[i-1], -1) != j)
            costeDam = sys.maxsize
            if i > 1 :
                abuelo = trie[padre][0]
                if abuelo != None:
                    costeDam = M[i-1,padre] + (not(trie[padre][2].get(palabra[i-2], -1) == j and 
                    trie[abuelo][2].get(palabra[i-1], -1) == padre))

            M[i,j] = min(costeBorr,costeIns,costeSus,costeDam)
            
    #Matriz llena, sacar las palabras cercanas
    palabras_cercanas = []
    for j in range (1,len(trie)):
        if (trie[j][1] != None and M[len(palabra),j] <= distancia):
            palabras_cercanas.append(trie[j][1])
    return palabras_cercanas


if __name__ == "__main__":

    if len(sys.argv) != 4:
        syntax()
    fichero = sys.argv[1]
    palabra = sys.argv[2]
    distancia = int(sys.argv[3])

    trie = {}
    with open(fichero, 'rb') as handle:
        trie = pickle.load(handle)

    cercanos = calculaDistancia(trie,palabra,distancia)
    print(len(cercanos), " palabras encontradas")
    #pprint.pprint(cercanos)
