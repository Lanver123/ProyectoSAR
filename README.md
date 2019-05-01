# ProyectoSAR


## Indexer

- **[DONE]** Aceptará dos argumentos de entrada: el primero el directorio donde está la colección
de noticias y el segundo el nombre del fichero donde se guardará el índice.
- **[DONE]** Procesará los documentos y extraerá las noticias: eliminar símbolos no alfanuméricos
(comillas, sostenidos, interrogantes,…), extraer los términos (consideraremos
separadores de términos los espacios, los saltos de línea y los tabuladores). No se
deben distinguir mayúsculas y minúsculas en la indexación.
- **[DONE]** A cada documento se le asignará un identificador único (docid) que será un entero
secuencial.
- **[DONE]** A cada noticia se le asignará un identificador único. Se debe saber cada noticia a que
documento pertenece y que posición ocupa dentro de él.
- **[DONE]** Se deberá crear una fichero invertido accesible por término. Cada entrada contendrá
una lista con las noticias en las que aparece ese término.
- **[DONE]** Toda la información necesaria para el recuperador de noticias se guardará en un único
fichero en disco

## Search

- **[No completado]** Aceptará uno o dos argumentos de entrada. El primero será siempre el nombre del
fichero que contiene los índices. Si se le proporciona una consulta como segundo
argumento resolveré la consulta y finalizará. Si sólo se le pasa un argumento, el
programa entrará en un bucle de petición de consulta y devolución de las noticias
relevantes hasta que la consulta esté vacía.
- **[No completado]** La búsqueda se hará en el cuerpo de las noticias. Las noticias relevantes para una
consulta serán aquellas que contengan todos los términos de la misma (búsqueda
binaria).
- **[No completado]** Se debe permitir utilizar AND, OR y NOT en las consultas. El orden de evaluación de las
conectivas (orden de prelación de las operaciones) será de izquierda a derecha.
    Ejemplo: la consulta “term1 AND NOT term2 OR term3”deberá devolver las
    noticias que contienen “term1” pero no “term2” más las que contienen “term3”.
Se deben implementar los algoritmos de merge de postings list vistos en teoría.
- **[No completado]** La presentación de los resultados se realizará en función del número de resultados
obtenidos:
    - Si sólo hay una o dos noticias relevantes. Se mostrará la fecha, el titular, las
keywords y todo el cuerpo la o las noticias.
    - Si hay entre 3 y 5 noticias relevantes. Se mostrará de cada noticia la fecha, el
titular, las keywords y un snippet del cuerpo de la noticia que contenga los
términos buscados. Si no se hace búsqueda por el cuerpo de la noticia se
mostrarán las primeras 100 palabras.
    - Si hay más de 5 noticias relevantes. Se mostrará la fecha, el titular y las
keywords de las 10 primeras en una única línea por noticia.
En todos los casos se mostrará el nombre de los ficheros que contienen las noticias y
se informará al usuar
