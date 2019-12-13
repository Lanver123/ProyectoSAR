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

class PilaBranch:
    def __init__(self, first):
        self.pila = [first]
    
    def length(self):
        return len(self.pila)

    def add(self, elem):
        if elem not in self.pila:
            self.pila.append(elem)

    def pop(self):
        return self.pila.pop(0)

def syntax():
    print("argumentos <trie_generado> <palabra> <distancia max>")
    exit(1)


@utils_algoritmica.timer
def calculaDistancia(trie, palabra, distancia):
    pila = PilaBranch((0, 0, 0))
    cercanos = []
    while PilaBranch.length(pila) > 0:
        analizado, nodo, coste = pila.pop()
        print(analizado, nodo, coste)
        letras_hijos_nodo = list(trie[nodo][2].keys())

        if(analizado < len(palabra) - 1):  # Borrado disponible
            pila.add((analizado+1, nodo, coste+1))  # Borrado

        for letra_hijo in letras_hijos_nodo:
            nodo_hijo = trie[nodo][2].get(letra_hijo)
            pila.add((analizado, nodo_hijo, coste+1))  # Insercion
            if(analizado < len(palabra)):  # Sustitucion disponible
                pila.add((analizado+1, nodo_hijo, coste +
                             (letra_hijo != palabra[analizado])))  # Sustitucion

        # Coincidencia encontrada
        if(trie[nodo][1] != None and coste <= distancia and (len(palabra)-1 == analizado)):
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
