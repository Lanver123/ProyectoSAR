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
    print("argumentos <archivo.txt> <palabra> <distancia max>")
    exit(1)

def generarTrie(texto):
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
    return trie

def calculaDistancia(trie,palabra,distancia):
    M = np.empty(dtype=np.int8, shape=(len(palabra)+1, len(trie)))
    for i in range(len(palabra)+1):
        M[i,0] = i
    for j in range(len(trie)):
        profun = 0
        padre = trie[j][0]
        while padre != 0:
            padre = trie[padre][0]
            profun += 1
        M[0,j] = profun



    for i in range(1,len(palabra)+1):
        for j in range(1,len(trie)):
            costeBorr = M[i-1,j]+1
            padre = trie[j][0]
            costeIns = M[i,padre] + 1
            costeSus = M[i-1,padre] + (trie[padre][2][palabra[i-1]] != j)
            M[i,j] = min(costeBorr,costeIns,costeSus)
    
    #Matriz llena, sacar las palabras cercanas
    palabras_cercanas = []
    for j in range (1,len(trie)):
        if (trie[j][1]!=None and M[len(palabra),j] <= distancia):
            palabras_cercanas.append(trie[j][1])
    return palabras_cercanas

if __name__ == "__main__":

    if len(sys.argv) != 4:
        syntax()
    fichero = sys.argv[1]
    palabra = sys.argv[2]
    distancia = int(sys.argv[3])
    readFile = open(fichero, "r")

    texto = readFile.read()
    trie = generarTrie(texto)
    cercanos = calculaDistancia(trie,palabra,distancia)

    print(cercanos)