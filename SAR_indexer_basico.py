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

def indexarCuerpo(directorioInicio):
    """ Devuelve una tupla con (IndiceInvertido, DiccionarioDocumentos) """

    indiceInvertido= {}

    diccionarioDocumentos={}
    #start_path = os.path.join(".",directorioInicio)
    idsNoticias=[]

    for dirName, _, fileList in os.walk(directorioInicio):
        numeroDocumento = 0
        for fname in fileList:
            numeroNoticia = 0
            #rel_file = os.path.join(start_path, fname)
            rel_file = os.path.join(dirName, fname)
            with open(rel_file, 'r') as json_file:  
                data = json.load(json_file)
            for i in range(len(data)):
                idNoticia = (numeroDocumento,numeroNoticia)
                idsNoticias.append(idNoticia)
                diccionarioDocumentos[idNoticia]=(rel_file,numeroNoticia)
                numeroNoticia = numeroNoticia+1
                er = re.compile('\w+')
                cuerpoNoticia = str(data[i]['article'])
                if cuerpoNoticia.startswith("Actualizado:"):
                    cuerpoNoticia = cuerpoNoticia[29:]
                for word in er.findall(cuerpoNoticia):
                    #Repitiendo
                    #indiceInvertido.setdefault(word, []).append(idNoticia)

                    #Sin repetir apariciones
                    indiceInvertido.setdefault(word.lower(), [])
                    indiceInvertido[word.lower()] = list(set().union(indiceInvertido[word.lower()], [idNoticia]))
            numeroDocumento = numeroDocumento+1

    return (indiceInvertido, diccionarioDocumentos,idsNoticias)
             


if __name__ == "__main__":
    fichero = ""
    if len(sys.argv) != 2:
        syntax()

    fichero = sys.argv[1]

    indices = indexarCuerpo(fichero)

    pprint.pprint(indices)

    pickle.dump(indices,open(fichero, "wb"))
    
    #save_object((indiceInvertido,diccionarioDocumentos),ficheroIndice)