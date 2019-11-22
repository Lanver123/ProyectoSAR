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
    pila = [(0,0,0)]
    cercanos = []
    while len(pila) > 0:
        estadoActual = pila.pop(0)
        cadena = estadoActual[0]
        nodo = estadoActual[1]
        dist = estadoActual[2]
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
    readFile = open(fichero, "r")

    texto = readFile.read()
    trie = generarTrie(texto)
    cercanos = calculaDistancia(trie,palabra,distancia)
    print(cercanos)