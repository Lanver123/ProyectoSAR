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
import utils_algoritmica
import numpy as np

def syntax():
    print("argumentos <archivo.txt> <palabra> <distancia max>")
    exit(1)

def levenshtein_distance(x,y):
    D = np.empty((len(x)+1,len(y)+1),dtype=np.int8)
    D[0,0] = 0
    for i in range(1,len(x)+1):
        D[i,0] = D[i-1, 0] + 1
    for j in range(1, len(y)+1):
        D[0,j] = D[0, j-1] + 1
        for i in range(1, len(x)+1):
            D[i,j] = min(D[i-1,j]+1, D[i,j-1]+1,D[i-1,j-1]+(x[i-1] != y[j-1]))
    return D[len(x),len(y)]

@utils_algoritmica.timer
def cercanos_levenshtein(word, diccionario, distance):
    cercanas = []
    for palabra in diccionario:
        dist = levenshtein_distance(word, palabra)
        if dist <= distance:
            cercanas.append((palabra, dist))
    return cercanas            

if __name__ == "__main__":
    directorioColeccion = ""
    fichero = ""
    if len(sys.argv) != 4:
        syntax()

    fichero = sys.argv[1]
    palabra = sys.argv[2]
    distancia = int(sys.argv[3])
    readFile = open(fichero, "r")

    texto = readFile.read()
    er = re.compile("\w+")
    lines = []
    diccionarioPalabras = {}
    for word in er.findall(texto):                
        diccionarioPalabras[word] = diccionarioPalabras.get(word, 0) + 1
    
    cercanos = cercanos_levenshtein(palabra, diccionarioPalabras.keys(), distancia)

    print(len(cercanos), " palabras encontradas")
    for z in range(len(cercanos)):
        print(cercanos[z][1],":",cercanos[z][0],end=" ",sep="")
    print()