# Cardona Lorenzo, Victor
# Gavilán Gil, Marc
# Martínez Bernia, Javier
# Murcia Serrano, Andrea

######   Search    ###########
# Lee los índices y recupera
# aquellas noticias relevantes 
# para las consultas que se realicen

import os
import sys
import pickle
import json
import pprint

def syntax():
    print("\nSAR_searcher.py <index_file> <Query>")
    exit(1)

def op_AND(l1,l2):
    res = []
    p1 = 0
    p2 = 0

    l1 = sorted(l1)
    l2 = sorted(l2)
    while p1 < len(l1) and p2 < len(l2):
        if l1[p1] == l2[p2]:
            res.append(l1[p1])
            p1 += 1
            p2 += 1
        else:
            if l1[p1][0] < l2[p2][0]:
                p1 += 1
            elif l1[p1][0] == l2[p2][0]:
                if l1[p1][1] < l2[p2][1]:
                    p1 += 1
                else:
                    p2 += 1
            else:
                p2 += 1
    return res

def op_ANDNOT(l1,l2):
    res = []
    p1 = 0
    p2 = 0

    l1 = sorted(l1)
    l2 = sorted(l2)

    while p1 < len(l1) and p2 < len(l2):
        if l1[p1] == l2[p2]:
            p1 += 1
            p2 += 1
        else:
            if l1[p1][0] < l2[p2][0]:
                res.append(l1[p1])
                p1 += 1
            elif l1[p1][0] == l2[p2][0]:
                if l1[p1][1] < l2[p2][1]:
                    res.append(l1[p1])
                    p1 += 1
                else:
                    p2 += 1
            else:
                p2 += 1
    while p1 < len(l1):
        res.append(l1[p1])
        p1 += 1
        
    return res

def op_OR(l1,l2):
    res = []
    p1 = 0
    p2 = 0

    l1 = sorted(l1)
    l2 = sorted(l2)

    while p1 < len(l1) and p2 < len(l2):
        if l1[p1] == l2[p2]:
            res.append(l1[p1])
            p1 += 1
            p2 += 1
        else:
            if l1[p1][0] < l2[p2][0]:
                res.append(l1[p1])
                p1 += 1
            elif l1[p1][0] == l2[p2][0]:
                if l1[p1][1] < l2[p2][1]:
                    res.append(l1[p1])
                    p1 += 1
                else:
                    res.append(l2[p2])
                    p2 += 1
            else:
                res.append(l2[p2])
                p2 += 1
    while p1 < len(l1):
        res.append(l1[p1])
        p1 += 1
    while p2 < len(l2):
        res.append(l2[p2])
        p2 += 1
        
    return res

#En esta funcion se llamará a la funcion correspondiente para
# hacer la operación en cuestión sobre dos posting lists
def operar(operador, isNot, lista1, lista2, noticias):
    resultado = []
    if operador == 'AND':
        if isNot == 0:
            resultado = op_AND(lista1, lista2)
        elif isNot == 1:
            resultado = op_ANDNOT(lista1, lista2)
    elif operador == 'OR':
        if isNot == 0:
            resultado = op_OR(lista1, lista2)
        elif isNot == 1:
            #En este caso hacemos primero una ANDNOT para hacer el NOT lista2
            # y despues hacemos una OR con la primera lista
            resultado = op_OR(lista1, op_ANDNOT(noticias,lista2))
    return resultado


#En esta funcion se va a procesar la consulta, devolviendo una lista
# con los identificadores de las noticias relevantes
def procesarConsulta(query,indices,noticias):
    indiceInvertidoArticle = indices["article"]
    indiceInvertidoTitle = indices["title"]
    indiceInvertidoSummary = indices["summary"]
    indiceInvertidoKeywords = indices["keywords"] 
    indiceInvertidoDate = indices["date"]
    res = noticias  #Inicializamos al conjunto completo para hacer una AND en caso
                    # de que la primera palabra de la query no sea un operador (AND, OR)
    query = query.split()
    isNot = 0       #Variable para identificar NOT en la consulta (1=NOT)
    operador = 'AND' #Esta variable indica el operador a utilizar

    posibleFinal = False    #Para controlar que la consulta acaba con un termino
    wordList = []           #Lista de palabras que deben aparecer segun la consulta

    for word in query:
        postingList = indiceInvertidoArticle
        if word.startswith("article:"):
            print("Buscando en el cuerpo de la noticia...")
            word = word[8:]
            postingList = indiceInvertidoArticle
        if word.startswith("title:"):
            print("Buscando por titulo...")
            word = word[6:]
            postingList = indiceInvertidoTitle
        if word.startswith("summary:"):
            print("Buscando por sumario...")
            word = word[8:]
            postingList = indiceInvertidoSummary
        if word.startswith("keywords:"):
            print("Buscando por keywords...")
            word = word[9:]
            postingList = indiceInvertidoKeywords
        if word.startswith("date:"):
            print("Buscando por fecha...")
            word = word[5:]
            postingList = indiceInvertidoDate                              

        print("Palabra: ", word)
        if word == 'AND' or word == 'OR':
            operador = word
            posibleFinal = False
        elif word == 'NOT':
            if isNot == 0:
                isNot = 1
            else:
                isNot = 0
            posibleFinal = False
        else:
            if isNot == 0: wordList.append(word)
            posting = postingList.get(word,[])
            res = operar(operador,isNot,res,posting,noticias)
            #ponemos los operadores a su forma estandar
            operador = 'AND'
            isNot = 0
            posibleFinal = True
    
    if posibleFinal:
        return (res,wordList)
    else:
        return ([],[])
            
#En esta funcion se va a mostrar el resultado dada una lista de
# noticias relevantes a la consulta
def mostrarRes(newsList, dicDocumentos,wordList):
    nRes = len(newsList)
    j = 0
    if nRes == 0:
        print("No se han encontrado resultados para la consulta")

    if nRes == 1 or nRes == 2:
        #Mostrar fecha, titular, keywords y cuerpo
        for idNoticia in newsList:
            (filePath,numeroNoticia)=dicDocumentos[idNoticia]
            with open(filePath,"r") as json_file:
                data = json.load(json_file)
            fecha = data[numeroNoticia]['date']
            titular = data[numeroNoticia]['title']
            keywords = data[numeroNoticia]['keywords']
            cuerpo = data[numeroNoticia]['article']
            print("\n")
            print(filePath)
            print("\nFecha: ",fecha)
            print("\nTitular: ",titular)
            print("\nKeywords: ",keywords)
            print("\n",cuerpo)
            print("---------------------")


    elif nRes >= 3 and nRes <= 5:
        #Mostrar fecha, titular, keywords y snippet
        for idNoticia in newsList:
            (filePath,numeroNoticia)=dicDocumentos[idNoticia]
            with open(filePath,"r") as json_file:
                data = json.load(json_file)
            fecha = data[numeroNoticia]['date']
            titular = data[numeroNoticia]['title']
            keywords = data[numeroNoticia]['keywords']
            cuerpo = data[numeroNoticia]['article']
            print("\n")
            print(filePath)
            print("\nFecha: ",fecha)
            print("\nTitular: ",titular)
            print("\nKeywords: ",keywords)
            cuerpo = cuerpo.lower()
            cuerpo = cuerpo.split()
            apariciones = []
            for word in wordList:
                try:
                    i = cuerpo.index(word)
                    apariciones.append(i)
                except Exception:
                    pass
            maxim = max(apariciones)
            minim = min(apariciones)

            maxim = min(maxim+2, len(cuerpo)-1)
            minim = max(0, minim-2)
            cuerpo = ' '.join(cuerpo[minim:maxim+1])
            print("\nSnippet: ",cuerpo)
            print("---------------------")

    elif nRes > 5:
        while j < 10 and nRes > 0:
            #Mostrar fecha, titular y keywords
            for idNoticia in newsList:
                if j == 10 : break
                (filePath,numeroNoticia)=dicDocumentos[idNoticia]
                with open(filePath,"r") as json_file:
                    data = json.load(json_file)
                fecha = data[numeroNoticia]['date']
                titular = data[numeroNoticia]['title']
                keywords = data[numeroNoticia]['keywords']
                print("\n")
                print(filePath)
                print("\nDocumento: ",filePath," Fecha: ",fecha," Titular: ",titular," Keywords: ",keywords)
                j += 1
                print("---------------------")
    if nRes > 0:
        print("\n Numero de noticias recuperadas: ",nRes)

            


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        syntax()

    modoBucle = True
    if len(sys.argv) == 3:
        query = sys.argv[2]
        modoBucle = False
    
    #Cargamos el archivo donde estan los indices
    with open(sys.argv[1], "rb") as fh:
        objetos = pickle.load(fh)
    indices = objetos[0]

    dicDocumentos = objetos[1]
    noticias = objetos[2]

    if not modoBucle:
        (newsList,wordList) = procesarConsulta(query,indices,noticias)
        mostrarRes(newsList,dicDocumentos,wordList)
    while(modoBucle):
       query = input('Consulta: ')
       if len(query)==0:
           break
       (newsList,wordList) = procesarConsulta(query,indices,noticias)
       mostrarRes(newsList,dicDocumentos,wordList)