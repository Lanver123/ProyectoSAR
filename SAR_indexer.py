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
    """ Devuelve una tupla con (IndiceInvertido, DiccionarioDocumentos, idsNoticias, IndicesStemming) """

    indiceInvertidoArticle= {}
    indiceInvertidoTitle= {}
    indiceInvertidoSummary= {}
    indiceInvertidoKeywords= {}
    indiceInvertidoDate= {}
    indices = {}
    indicesStemming = {}
    indiceStemmArticle={}
    indiceStemmTitle={}
    indiceStemmSummary={}
    indiceStemmKeywords={}
    indiceStemmDate={}
    diccionarioDocumentos={}
    
    stemmer = SnowballStemmer('spanish')
    idsNoticias=[]
    nNoticias = 0
    numeroDocumento = 0
    for dirName, _, fileList in os.walk(directorioInicio):
        for fname in fileList:
            numeroNoticia = 0
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

                    indiceInvertidoArticle.setdefault(word.lower(), [])
                    indiceInvertidoArticle[word.lower()] = list(set().union(indiceInvertidoArticle[word.lower()], [idNoticia]))

                    stemWord = stemmer.stem(word.lower())
                    indiceStemmArticle.setdefault(stemWord,[])
                    indiceStemmArticle[stemWord] = list(set().union(indiceStemmArticle[stemWord],[idNoticia]))

                for word in er.findall(str(data[i]['title'])):

                    indiceInvertidoTitle.setdefault(word.lower(), [])
                    indiceInvertidoTitle[word.lower()] = list(set().union(indiceInvertidoTitle[word.lower()], [idNoticia]))  

                    stemWord = stemmer.stem(word.lower())
                    indiceStemmTitle.setdefault(stemWord,[])
                    indiceStemmTitle[stemWord] = list(set().union(indiceStemmTitle[stemWord],[idNoticia]))
                for word in er.findall(str(data[i]['summary'])):

                    indiceInvertidoSummary.setdefault(word.lower(), [])
                    indiceInvertidoSummary[word.lower()] = list(set().union(indiceInvertidoSummary[word.lower()], [idNoticia]))  

                    stemWord = stemmer.stem(word.lower())
                    indiceStemmSummary.setdefault(stemWord,[])
                    indiceStemmSummary[stemWord] = list(set().union(indiceStemmSummary[stemWord],[idNoticia]))                      
                for word in er.findall(str(data[i]['keywords'])):

                    indiceInvertidoKeywords.setdefault(word.lower(), [])
                    indiceInvertidoKeywords[word.lower()] = list(set().union(indiceInvertidoKeywords[word.lower()], [idNoticia]))  

                    stemWord = stemmer.stem(word.lower())
                    indiceStemmKeywords.setdefault(stemWord,[])
                    indiceStemmKeywords[stemWord] = list(set().union(indiceStemmKeywords[stemWord],[idNoticia]))                
                for word in er.findall(str(data[i]['date'])):

                    indiceInvertidoDate.setdefault(word.lower(), [])
                    indiceInvertidoDate[word.lower()] = list(set().union(indiceInvertidoDate[word.lower()], [idNoticia]))

                    indiceStemmTitle.setdefault(word,[])
                    indiceStemmTitle[word] = list(set().union(indiceStemmTitle[word],[idNoticia]))                                                                                                  
            numeroDocumento = numeroDocumento+1

    indices["article"] = indiceInvertidoArticle
    indices["title"] = indiceInvertidoTitle
    indices["summary"] = indiceInvertidoSummary
    indices["keywords"] = indiceInvertidoKeywords
    indices["date"] = indiceInvertidoDate

    indicesStemming["article"] = indiceStemmArticle
    indicesStemming["title"] = indiceStemmTitle
    indicesStemming["summary"] = indiceStemmSummary
    indicesStemming["keywords"] = indiceStemmKeywords
    indicesStemming["date"] = indiceStemmDate

    return (indices, diccionarioDocumentos,idsNoticias, indicesStemming)
             


if __name__ == "__main__":
    directorioColeccion = ""
    ficheroIndice = ""
    if len(sys.argv) != 3:
        syntax()

    directorioColeccion = sys.argv[1]
    ficheroIndice = sys.argv[2]

    (indices, diccionarioDocumentos,noticias, indicesStemming) = indexarCuerpo(directorioColeccion)
    #for subIndex in indices.values():
    #    pprint.pprint(subIndex)


    pickle.dump((indices,diccionarioDocumentos,noticias,indicesStemming),open(ficheroIndice, "wb"))