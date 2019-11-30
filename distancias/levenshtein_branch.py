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
import time
import pickle

def syntax():
    print("argumentos <trie_generado> <palabra> <distancia max>")
    exit(1)

def calculaDistancia(trie,palabra,distancia):
    pila = [(0,0,0)]
    cercanos = []
    while len(pila) > 0:
        cadena, nodo, dist = pila.pop(0)
        hijos_trie = list(trie[nodo][2].keys())
        
        if(cadena < len(palabra)-1): # Borrado disponible
            pila.append((cadena+1,nodo,dist+1)) # Borrado

        for letra_hijo in hijos_trie:
            nodo_hijo = trie[nodo][2].get(letra_hijo)
            pila.append((cadena,nodo_hijo,dist+1)) #Insercion
            if(cadena < len(palabra)): # Sustitucion disponible      
                pila.append((cadena+1,nodo_hijo, dist + (letra_hijo != palabra[cadena]))) #Sustitucion        
        
        if(trie[nodo][1] != None and dist <= distancia and (len(palabra)-1 == cadena)): # Coincidencia encontrada
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
        
    start_time = time.time()
    cercanos = calculaDistancia(trie,palabra,distancia)
    end_time = time.time()
    print(cercanos)
    print("Tiempo transcurrido en la búsqueda %.2f:" % (end_time - start_time))