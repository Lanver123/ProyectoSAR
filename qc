[33mcommit 545d7eba1e0177316b676ea3f43f4b097f3a0fa0[m
Author: MARTÍNEZ BERNIA <jamarbe2@EVIRL-006-OK.dsic.cloud>
Date:   Fri Nov 15 13:59:24 2019 +0100

    Ramificacion started

[1mdiff --git a/distancias/levenshtein_branch.py b/distancias/levenshtein_branch.py[m
[1mnew file mode 100644[m
[1mindex 0000000..91d6078[m
[1m--- /dev/null[m
[1m+++ b/distancias/levenshtein_branch.py[m
[36m@@ -0,0 +1,82 @@[m
[32m+[m[32m#!/usr/bin/env python[m
[32m+[m[32m# -*- coding: utf-8 -*-[m
[32m+[m
[32m+[m[32m# Cardona Lorenzo, Victor[m
[32m+[m[32m# Gavilán Gil, Marc[m
[32m+[m[32m# Martínez Bernia, Javier[m
[32m+[m[32m# Murcia Serrano, Andrea[m
[32m+[m
[32m+[m[32mimport sys[m
[32m+[m[32mimport os[m
[32m+[m[32mimport pprint[m
[32m+[m[32mimport json[m
[32m+[m[32mimport re[m
[32m+[m[32mimport pickle[m
[32m+[m
[32m+[m
[32m+[m[32mdef syntax():[m
[32m+[m[32m    print("argumentos <archivo.txt> <palabra> <distancia max>")[m
[32m+[m[32m    exit(1)[m
[32m+[m
[32m+[m[32mdef generarTrie(texto):[m
[32m+[m[32m    er = re.compile("\w+")[m
[32m+[m[32m    #diccionario que guarda todos los nodos[m
[32m+[m[32m    trie = {}[m
[32m+[m[32m    numNodes = 0[m
[32m+[m[32m    #cada elemento del vacabulario es una lista de nodo padre, si es palabra final y cual, y un diccionario[m
[32m+[m[32m    #   con la key la siguiente letra y devuelve el nodo hijo[m
[32m+[m[32m    trie[0] = [None, None, {}][m
[32m+[m[32m    for word in er.findall(texto):[m
[32m+[m[32m        nodeCurrent = 0[m
[32m+[m[32m        for i, letter in enumerate(word):[m
[32m+[m[32m            #se recupera el nodo siguiente[m
[32m+[m[32m            nodeChild = trie[nodeCurrent][2].get(letter)[m
[32m+[m[32m            if nodeChild is None:[m
[32m+[m[32m                #si no existe el nodo siguiente, se crea, con su tripleta viendo si es palabra final y[m[41m [m
[32m+[m[32m                #se añade este nuevo nodo al diccionario del padre, ademas del diccionario de todos los nodos[m
[32m+[m[32m                numNodes = numNodes + 1[m
[32m+[m[32m                nodeChild = numNodes[m
[32m+[m[32m                childList = [nodeCurrent, None, {}][m
[32m+[m[32m                if i + 1 == len(word):[m
[32m+[m[32m                    childList[1] = word[m
[32m+[m[32m                trie[nodeCurrent][2][letter] = nodeChild[m
[32m+[m[32m                trie[nodeChild] = childList[m
[32m+[m[32m            #para ir recorriendo el trie[m
[32m+[m[32m            nodeCurrent = nodeChild[m
[32m+[m[32m    return trie[m
[32m+[m
[32m+[m[32mdef calculaDistancia(trie,palabra,distancia):[m
[32m+[m[32m    pila = [(0,0,0)][m
[32m+[m[32m    cercanos = [][m
[32m+[m[32m    while len(pila) > 0:[m
[32m+[m[32m        estadoActual = pila.pop(0)[m
[32m+[m[32m        cadena = estadoActual[0][m
[32m+[m[32m        nodo = estadoActual[1][m
[32m+[m[32m        dist = estadoActual[2][m
[32m+[m[32m        if cadena < (len(palabra) - 1):[m
[32m+[m[32m            pila.append((cadena+1,nodo,dist+1)) #Borrado[m
[32m+[m[32m            simbolos = trie[nodo][2].keys()[m
[32m+[m[32m            for i in range (len(simbolos)[m
[32m+[m[32m                hijo = trie.get(nodo)[2].get(simbolos[i])[m
[32m+[m[32m                pila.append(cadena,hijo,dist+1) #Insercion[m
[32m+[m[32m                pila.append(cadena+1,hijo,dist + palabra[cadena]!=simbolos[i]) #Sustitucion[m
[32m+[m[32m        else:[m
[32m+[m[32m            if (trie[nodo][1] != None and dist <= distancia):[m
[32m+[m[32m                cercanos.append(trie[nodo][1])[m
[32m+[m[32m    return cercanos[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mif __name__ == "__main__":[m
[32m+[m
[32m+[m[32m    if len(sys.argv) != 4:[m
[32m+[m[32m        syntax()[m
[32m+[m[32m    fichero = sys.argv[1][m
[32m+[m[32m    palabra = sys.argv[2][m
[32m+[m[32m    distancia = int(sys.argv[3])[m
[32m+[m[32m    readFile = open(fichero, "r")[m
[32m+[m
[32m+[m[32m    texto = readFile.read()[m
[32m+[m[32m    trie = generarTrie(texto)[m
[32m+[m[32m    cercanos = calculaDistancia(trie,palabra,distancia)[m
[32m+[m[32m    print(cercanos)[m
\ No newline at end of file[m
