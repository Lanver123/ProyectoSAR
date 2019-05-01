# Cardona Lorenzo, Victor
# Gavilán Gil, Marc
# Martínez Bernia, Javier
# Murcia Serrano, Andrea

######   Search    ###########
# Lee los índices y recupera
# aquellas noticias relevantes 
# para las consultas que se realicen

import sys
import pickle

def syntax():
    print("\nSAR_searcher.py <index_file> <Query>")
    exit(1)

def op_AND(l1,l2):
    res = []

    return res

def op_ANDNOT(l1,l2):
    res = []
    
    return res

def op_OR(l1,l2):
    res = []
    
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
def procesarConsulta(query,postingList,noticias):
    res = noticias  #Inicializamos al conjunto completo para hacer una AND en caso
                    # de que la primera palabra de la query no sea un operador (AND, OR)
    query = query.split()
    isNot = 0       #Variable para identificar NOT en la consulta (1=NOT)
    operador = 'AND' #Esta variable indica el operador a utilizar

    posibleFinal = False    #Para controlar que la consulta acaba con un termino

    for word in query:
        if word == 'AND' or word == 'OR':
            operador = word
        elif word == 'NOT':
            if isNot = 0:
                isNot = 1
            else:
                isNot = 0
        else:
            res = operar(operador,isNot,res,postingList[word],noticias)
            operador = 'AND'
            isNot = 0
            posibleFinal = True
    
    if posibleFinal:
        return res
    else:
        return []
            


#En esta funcion se va a mostrar el resultado dada una lista de
# noticias relevantes a la consulta
def mostrarRes(newsList, dicDocumentos):


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv > 3):
        syntax()

    modoBucle = True
    if len(sys.argv) == 3:
        query = sys.argv[2]
        modoBucle = False
    
    #Cargamos el archivo donde estan los indices
    objetos = load_object(sys.argv[1])
    indiceInvertido = objetos[0]
    dicDocumentos = objetos[1]
    noticias = objetos[2]

    if not modoBucle:
        newsList = procesarConsulta(query,indiceInvertido,noticias)
        mostrarRes(newsList,dicDocumentos)
    while(modoBucle):
       query = input('Consulta: ')
       if len(query)==0:
           break
       newsList = procesarConsulta(query,indiceInvertido,noticias)
       mostrarRes(newsList,dicDocumentos)