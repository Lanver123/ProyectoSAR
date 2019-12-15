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

    def __repr__(self):
        print(self.pila)

    def best(self, elem):
        analizado, nodo, distancia = elem
        for dis in range(distancia):
            if (analizado, nodo, dis) in self.pila:
                return False
        return True

    def length(self):
        return len(self.pila)

    def add(self, elem):
        if elem not in self.pila and self.best(elem):
            self.pila.append(elem)

    def pop(self):
        return self.pila.pop(0)


def syntax():
    print("argumentos <trie_generado> <palabra> <distancia max>")
    exit(1)


@utils_algoritmica.timer
def calculaDistancia(trie, palabra, distancia):
    pila = PilaBranch((0, 0, 0))
    cercanos = set()
    pprint.pprint(trie)
    while PilaBranch.length(pila) != 0:
        nodo_ppal = pila.pop()
        analizado, nodo, coste = nodo_ppal
        # Coincidencia encontrada
        if(trie[nodo][1] != None and coste <= distancia and (len(palabra) == analizado)):
            cercanos.add(trie[nodo][1])

        if analizado < len(palabra) - 1:  # Hay al menos 1 carácter borrable
            son_node = (analizado + 1, nodo, coste + 1)
            pila.add(son_node)  # Borrado

        for letra_hijo in trie[nodo][2]:
            nodo_hijo = trie[nodo][2].get(letra_hijo)

            if coste < distancia:
                son_node = (analizado, nodo_hijo, coste + 1)
                pila.add(son_node)  # Insercion

            if analizado < len(palabra):  # Si hay al menos 1 carácter sustituible
                son_node = (analizado+1, nodo_hijo, coste +
                            (letra_hijo != palabra[analizado]))
                pila.add(son_node)  # Sustitucion

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
    print(len(cercanos), cercanos)

# 
