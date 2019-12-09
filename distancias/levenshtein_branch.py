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
import utils_algoritmica
import pickle


def syntax():
    print("argumentos <trie_generado> <palabra> <distancia max>")
    exit(1)


@utils_algoritmica.timer
def calculaDistancia(trie, palabra, distancia):
    pila = [(0, 0, 0)]
    cercanos = []
    while len(pila) > 0:
        cadena, nodo, dist = pila.pop(0)
        letras_hijos_nodo = list(trie[nodo][2].keys())

        if(cadena < len(palabra)):  # Borrado disponible
            pila.append((cadena+1, nodo, dist+1))  # Borrado

        for letra_hijo in letras_hijos_nodo:
            nodo_hijo = trie[nodo][2].get(letra_hijo)
            pila.append((cadena, nodo_hijo, dist+1))  # Insercion
            if(cadena < len(palabra)):  # Sustitucion disponible
                pila.append((cadena+1, nodo_hijo, dist +
                             (letra_hijo != palabra[cadena])))  # Sustitucion

        # Coincidencia encontrada
        if(trie[nodo][1] != None and dist <= distancia and (len(palabra)-1 == cadena)):
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

    cercanos = calculaDistancia(trie, palabra, distancia)
    print(cercanos)
