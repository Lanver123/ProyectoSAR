import sys
import os
import pprint
import json
import re
import pickle
import numpy as np
from collections import deque

def generarTrie(texto):
    """
    Generar la representacion de un trie en forma de diccionario:
        key: Numero de nodo
        value: [nodo_padre, palabra_formada, letras_siguientes]
    """
    er = re.compile("\w+")
    # diccionario que guarda todos los nodos
    trie = {}
    numNodes = 0

    tamano_texto = sum([1 for word in er.findall(texto)])
    print("Palabras a procesar: ", tamano_texto)
    progreso = 1

    # cada elemento del vacabulario es una lista de nodo padre, si es palabra final y cual, y un diccionario
    #   con la key la siguiente letra y devuelve el nodo hijo
    trie[0] = [None, None, {}]
    for word in er.findall(texto):
        if(progreso % 10000 == 0):
            print("%d / %d: %.2f %%" %
                  (progreso, tamano_texto, (progreso/tamano_texto) * 100))
        progreso += 1
        # pasar la palabra a minusculas

        word = word.lower()
        nodeCurrent = 0
        for i, letter in enumerate(word):
            # se recupera el nodo siguiente
            nodeChild = trie[nodeCurrent][2].get(letter)
            if nodeChild is None:
                # si no existe el nodo siguiente, se crea, con su tripleta viendo si es palabra final y
                # se añade este nuevo nodo al diccionario del padre, ademas del diccionario de todos los nodos
                numNodes = numNodes + 1
                nodeChild = numNodes
                childList = [nodeCurrent, None, {}]
                trie[nodeCurrent][2][letter] = nodeChild
                trie[nodeChild] = childList
            # para ir recorriendo el trie
            nodeCurrent = nodeChild
            # si es la ultima letra, se ha procesado toda la palabra y se añade como nodo final
            if i + 1 == len(word):
                trie[nodeCurrent][1] = word

    return trie

#######################################
# Funciones de distancias de palabras #
#######################################

# LEVENSHTEIN CADENA CONTRA CADENA #

def levenshtein_distance(x, y):
    D = np.empty((len(x)+1, len(y)+1), dtype=np.int8)
    D[0, 0] = 0
    for i in range(1, len(x)+1):
        D[i, 0] = D[i-1, 0] + 1
    for j in range(1, len(y)+1):
        D[0, j] = D[0, j-1] + 1
        for i in range(1, len(x)+1):
            D[i, j] = min(D[i-1, j]+1, D[i, j-1]+1,
                          D[i-1, j-1]+(x[i-1] != y[j-1]))
    return D[len(x), len(y)]


def lev_cadenaVScadena(diccionario, word, distance):
    cercanas = []
    for palabra in diccionario:
        dist = levenshtein_distance(word, palabra)
        if dist <= distance:
            cercanas.append((palabra, dist))
    return cercanas

# DAMERAU CADENA CONTRA CADENA #

def damerau_levenshtein_distance(x, y):
    D = np.empty((len(x)+1, len(y)+1), dtype=np.int8)
    D[0, 0] = 0
    for i in range(1, len(x)+1):
        D[i, 0] = D[i-1, 0] + 1
    for j in range(1, len(y)+1):
        D[0, j] = D[0, j-1] + 1
        for i in range(1, len(x)+1):
            if i > 1 and j > 1:
                cond_damerau = (x[i-1] == y[j-2] and x[i-2] == y[j-1])
                D[i, j] = min(D[i-1, j]+1, D[i, j-1]+1, D[i-1, j-1]+(x[i-1] != y[j-1]),
                              ((D[i-2, j-2] + 1)*cond_damerau)+(sys.maxsize*(1-cond_damerau)))
            else:
                D[i, j] = min(D[i-1, j]+1, D[i, j-1]+1,
                              D[i-1, j-1]+(x[i-1] != y[j-1]))

    return D[len(x), len(y)]


def dam_cadenaVScadena(diccionario, word, distance):
    cercanas = []
    for palabra in diccionario:
        dist = damerau_levenshtein_distance(word, palabra)
        if dist <= distance:
            cercanas.append((palabra, dist))
    return cercanas


# LEVENSHTEIN CADENA CONTRA TRIE #

def lev_cadenaVStrie(trie, palabra, distancia):
    M = np.empty(dtype=np.int8, shape=(len(palabra)+1, len(trie)))
    for i in range(len(palabra)+1):  # La primera columna
        M[i, 0] = i
    for j in range(len(trie)):  # La primera fila (profundidades de los nodos del trie)
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
            costeIns = M[i, padre] + 1
            letra = palabra[i-1]
            costeSus = M[i-1, padre] + \
                (trie[padre][2].get(palabra[i-1], -1) != j)
            M[i, j] = min(costeBorr, costeIns, costeSus)

    # Matriz llena, sacar las palabras cercanas
    palabras_cercanas = []
    for j in range(1, len(trie)):
        if (trie[j][1] != None and M[len(palabra), j] <= distancia):
            palabras_cercanas.append(trie[j][1])

    return palabras_cercanas


# DAMERAU CADENA CONTRA TRIE #

def dam_cadenaVStrie(trie, palabra, distancia):
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


# LEVENSHTEIN BRANCH #

def lev_branch(trie, palabra, distancia):
    pila = deque([(0, 0, 0)])
    cercanos = set()
    while len(pila) > 0:
        nodo_ppal = pila.popleft()
        analizado, nodo, coste = nodo_ppal
        if coste > distancia:
            continue

        # Coincidencia encontrada
        if(trie[nodo][1] != None and coste <= distancia and (len(palabra) == analizado)):
            cercanos.add(trie[nodo][1])

        if analizado < len(palabra):  # Hay al menos 1 carácter borrable
            pila.appendleft((analizado + 1, nodo, coste + 1))  # Borrado

        for letra_hijo in trie[nodo][2]:
            nodo_hijo = trie[nodo][2].get(letra_hijo)

            if coste < distancia:
                pila.appendleft((analizado, nodo_hijo, coste + 1))  # Insercion

            if analizado < len(palabra):  # Si hay al menos 1 carácter sustituible
                pila.appendleft((analizado+1, nodo_hijo, coste +
                                 (letra_hijo != palabra[analizado])))  # Sustitucion

    return cercanos


# DAMERAU BRANCH #

    def dam_branch(trie, palabra, distancia):
    pila = deque([(0, 0, 0)])
    cercanos = set()
    while len(pila) > 0:
        nodo_ppal = pila.popleft()
        analizado, nodo, coste = nodo_ppal
        if coste > distancia:
            continue

        # Coincidencia encontrada
        if(trie[nodo][1] != None and coste <= distancia and (len(palabra) == analizado)):
            cercanos.add(trie[nodo][1])

        if analizado < len(palabra) - 1:  # Swap posible
            letra_actual, letra_siguiente = palabra[analizado], palabra[analizado+1]
            if letra_siguiente in trie[nodo][2]:
                nodo_hijo = trie[nodo][2][letra_siguiente]
                if letra_actual in trie[nodo_hijo][2]:
                    nieto = trie[nodo_hijo][2][letra_actual]
                    pila.appendleft((analizado + 2, nieto, coste + 1))  # Swap

        if analizado < len(palabra):  # Hay al menos 1 carácter borrable
            pila.appendleft((analizado + 1, nodo, coste + 1))  # Borrado

        for letra_hijo in trie[nodo][2]:
            nodo_hijo = trie[nodo][2].get(letra_hijo)

            if coste < distancia:
                pila.appendleft((analizado, nodo_hijo, coste + 1))  # Insercion

            if analizado < len(palabra):  # Si hay al menos 1 carácter sustituible
                pila.appendleft((analizado+1, nodo_hijo, coste +
                                 (letra_hijo != palabra[analizado])))  # Sustitucion

    return cercanos