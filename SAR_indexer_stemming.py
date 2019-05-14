# Cardona Lorenzo, Victor
# Gavilán Gil, Marc
# Martínez Bernia, Javier
# Murcia Serrano, Andrea

######      Indexer      ######
# Extrae las noticias de una 
# colección de documentos alojados 
# en un directorio, las indexa y 
# guarda en disco los índices creados

import sys
import os
import pprint
import json
import re
import pickle
from nltk.stem import SnowballStemmer

def syntax():
    print("argumentos <coleccion dir> <fichero indice>")
    exit(1)

def indexarCuerpo(directorioInicio):
    """ Devuelve una tupla con (IndiceInvertido, DiccionarioDocumentos) """

    indiceInvertidoArticle= {}
    indiceInvertidoTitle= {}
    indiceInvertidoSummary= {}
    indiceInvertidoKeywords= {}
    indiceInvertidoDate= {}
    indices = {}

    diccionarioDocumentos={}
    diccionarioStemming={}
    stemmer = SnowballStemmer('spanish')
    #start_path = os.path.join(".",directorioInicio)
    idsNoticias=[]
    nNoticias = 0

    for dirName, _, fileList in os.walk(directorioInicio):
        numeroDocumento = 0
        for fname in fileList:
            numeroNoticia = 0
            #rel_file = os.path.join(start_path, fname)
            rel_file = os.path.join(dirName, fname)
            with open(rel_file, 'r') as json_file:  
                data = json.load(json_file)
            for i in range(len(data)):
                nNoticias += 1
                idNoticia = (numeroDocumento,numeroNoticia)
                idsNoticias.append(idNoticia)
                diccionarioDocumentos[idNoticia]=(rel_file,numeroNoticia)
                numeroNoticia = numeroNoticia+1
                er = re.compile(r'\w+')
                for word in er.findall(str(data[i]['article'])):
                    #Repitiendo
                    #indiceInvertido.setdefault(word, []).append(idNoticia)

                    #Sin repetir apariciones
                    indiceInvertidoArticle.setdefault(word.lower(), [])
                    indiceInvertidoArticle[word.lower()] = list(set().union(indiceInvertidoArticle[word.lower()], [idNoticia]))
                    stemWord = stemmer.stem(word.lower())
                    diccionarioStemming.setdefault(stemWord,[])
                    diccionarioStemming[stemWord] = list(set().union(diccionarioStemming[stemWord],[idNoticia]))

                for word in er.findall(str(data[i]['title'])):
                    #Repitiendo
                    #indiceInvertido.setdefault(word, []).append(idNoticia)

                    #Sin repetir apariciones
                    indiceInvertidoTitle.setdefault(word.lower(), [])
                    indiceInvertidoTitle[word.lower()] = list(set().union(indiceInvertidoTitle[word.lower()], [idNoticia]))  
                for word in er.findall(str(data[i]['summary'])):
                    #Repitiendo
                    #indiceInvertido.setdefault(word, []).append(idNoticia)

                    #Sin repetir apariciones
                    indiceInvertidoSummary.setdefault(word.lower(), [])
                    indiceInvertidoSummary[word.lower()] = list(set().union(indiceInvertidoSummary[word.lower()], [idNoticia]))    
                for word in er.findall(str(data[i]['keywords'])):
                    #Repitiendo
                    #indiceInvertido.setdefault(word, []).append(idNoticia)

                    #Sin repetir apariciones
                    indiceInvertidoKeywords.setdefault(word.lower(), [])
                    indiceInvertidoKeywords[word.lower()] = list(set().union(indiceInvertidoKeywords[word.lower()], [idNoticia]))  
                for word in er.findall(str(data[i]['date'])):
                    #Repitiendo
                    #indiceInvertido.setdefault(word, []).append(idNoticia)

                    #Sin repetir apariciones
                    indiceInvertidoDate.setdefault(word.lower(), [])
                    indiceInvertidoDate[word.lower()] = list(set().union(indiceInvertidoDate[word.lower()], [idNoticia]))                                                                                                   
            numeroDocumento = numeroDocumento+1

    indices["article"] = indiceInvertidoArticle
    indices["title"] = indiceInvertidoTitle
    indices["summary"] = indiceInvertidoSummary
    indices["keywords"] = indiceInvertidoKeywords
    indices["date"] = indiceInvertidoDate
    indices["stemming"] = diccionarioStemming

    return (indices, diccionarioDocumentos,idsNoticias)
             


if __name__ == "__main__":
    directorioColeccion = ""
    ficheroIndice = ""
    if len(sys.argv) != 3:
        syntax()

    directorioColeccion = sys.argv[1]
    ficheroIndice = sys.argv[2]

    (indices, diccionarioDocumentos,noticias) = indexarCuerpo(directorioColeccion)
    for subIndex in indices.values():
        pprint.pprint(subIndex)


    pickle.dump((indices,diccionarioDocumentos,noticias),open(ficheroIndice, "wb"))
    
    #save_object((indiceInvertido,diccionarioDocumentos),ficheroIndice)