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

def syntax():
    print("argumentos <coleccion dir> <fichero indice>")
    exit(1)

def indexarNoticias(directorioInicio):
    """ Devuelve una tupla con (IndiceInvertido, DiccionarioDocumentos) """

    indiceInvertido= {}
    diccionarioDocumentos={}
    #start_path = os.path.join(".",directorioInicio)
    idsNoticias=[]
    nNoticias = 0
    for dirName, subdirList, fileList in os.walk(directorioInicio):
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
                er = re.compile('\w+')
                for word in er.findall(str(data[i]['article'])):
                    #Repitiendo
                    #indiceInvertido.setdefault(word, []).append(idNoticia)

                    #Sin repetir apariciones
                    indiceInvertido.setdefault(word.lower(), [])
                    indiceInvertido[word.lower()] = list(set().union(indiceInvertido[word.lower()], [idNoticia]))
            numeroDocumento = numeroDocumento+1

    return (indiceInvertido, diccionarioDocumentos,idsNoticias)
             
if __name__ == "__main__":
    directorioColeccion = ""
    ficheroIndice = ""
    if len(sys.argv) != 3:
        syntax()

    directorioColeccion = sys.argv[1]
    ficheroIndice = sys.argv[2]

    (indiceInvertido, diccionarioDocumentos,noticias) = indexarNoticias(directorioColeccion)
    pprint.pprint(indiceInvertido)


    pickle.dump((indiceInvertido,diccionarioDocumentos,noticias),open(ficheroIndice, "wb"))
    #save_object((indiceInvertido,diccionarioDocumentos),ficheroIndice)