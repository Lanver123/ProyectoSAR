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
    print("argumentos <archivo.txt> <palabra> <distancia max>")
    exit(1)

def calculaDistancia(trie,palabra,distancia):
    pila = [(0,0,0)]
    cercanos = []
    while len(pila) > 0:
        estadoActual = pila.pop(0)
        cadena = estadoActual[0]
        nodo = estadoActual[1]
        dist = estadoActual[2]
        
        #cadena, nodo, dist = estadoActual


        hijos_trie = list(trie[nodo][2].keys())
        
        if(cadena < len(palabra)): # Borrado disponible
            pila.append((cadena+1,nodo,dist+1)) # Borrado

        for hijo in hijos_trie:
            pila.append((cadena,hijo,dist+1)) #Insercion
            if(cadena <= len(palabra)): # Sustitucion disponible      
                pila.append((cadena+1,hijo,dist + (hijo != palabra[cadena])) #Sustitucion        

        if (trie[nodo][1] != None and dist <= distancia and len(palabra) == cadena): # Coincidencia encontrada
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