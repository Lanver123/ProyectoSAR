# Cardona Lorenzo, Victor
# Gavilán Gil, Marc
# Martínez Bernia, Javier
# Murcia Serrano, Andrea

######   Search    ###########
# Lee los índices y recupera
# aquellas noticias relevantes 
# para las consultas que se realicen

import sys

def syntax():
    print("\nSAR_searcher.py <index_file> <Query>")
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2 :
        syntax()
    nombreIndice = sys.argv[1]
    modoBucle = True
    if len(sys.argv) == 3:
        query = sys.argv[2]
        modoBucle = False
    if not modoBucle:
        
    while(modoBucle):
       query = input('Consulta: ')