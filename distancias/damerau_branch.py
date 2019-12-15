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
    print("argumentos <trieGenerado.txt> <palabra> <distancia max>")
    exit(1)

def calculaDistancia(trie,palabra,distancia):
    pila = [(0,0,0)]
    cercanos = []
    while len(pila) > 0:
        cadena, nodo, dist = pila.pop(0)
        if cadena < (len(palabra) - 1):
            pila.append((cadena+1,nodo,dist+1)) #Borrado
            simbolos = trie[nodo][2].keys()
            for i in range (len(simbolos)
                hijo = trie.get(nodo)[2].get(simbolos[i])
                pila.append(cadena,hijo,dist+1) #Insercion
                pila.append(cadena+1,hijo,dist + palabra[cadena]!=simbolos[i]) #Sustitucion
        else:
            if (trie[nodo][1] != None and dist <= distancia):
                cercanos.append(trie[nodo][1])
    return cercanos



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
    print(cercanos)