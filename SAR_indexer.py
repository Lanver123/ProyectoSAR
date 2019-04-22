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
    start_path = os.path.join(".",directorioInicio)

    
    for dirName, subdirList, fileList in os.walk(directorioInicio):
        numeroDocumento = 0
        for fname in fileList:
            numeroNoticia = 0
            numeroDocumento = numeroDocumento+1
            rel_file = os.path.join(start_path, fname)
            with open(rel_file, 'r') as json_file:  
                data = json.load(json_file)
            for i in range(len(data)):
                numeroNoticia = numeroNoticia+1
                idNoticia = "%i , %i" % (numeroDocumento,numeroNoticia)
                diccionarioDocumentos[idNoticia]=(rel_file,numeroNoticia)
                er = re.compile(r"(\w+)")
                for word in er.findall(str(data[i])):
                    #Repitiendo
                    #indiceInvertido.setdefault(word, []).append(idNoticia)

                    #Sin repetir apariciones
                    indiceInvertido.setdefault(word, [])
                    indiceInvertido[word] = list(set().union(indiceInvertido[word], [idNoticia]))

    return (indiceInvertido, diccionarioDocumentos)
             
if __name__ == "__main__":
    directorioColeccion = ""
    ficheroIndice = ""
    if len(sys.argv) != 3:
        syntax()

    directorioColeccion = sys.argv[1]
    ficheroIndice = sys.argv[2]

    (indiceInvertido, diccionarioDocumentos) = indexarNoticias(directorioColeccion)
    pprint.pprint(indiceInvertido)

    pickle.dump((indiceInvertido,diccionarioDocumentos),open(ficheroIndice, "wb"))
