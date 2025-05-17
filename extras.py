import csv
from hechos import DatosDelEquipo # para pasar a la funcion cargar_equipo csv

"""
funcion para manejar el campo ult_5 del csv, este es una cadena de texto y podemos
convertirlo a un dato númerico haciendo una suma de los valores
"""
def calcForma(ult_5):
    puntos = {'v': 3, 'e': 1, 'd': 0} # diccionario
    return sum(puntos.get(i, 0) for i in ult_5.lower()) 
"""
para cada literal del string ult_5 (lista) obtenemos el valor de la llave en el diccionario 
(0 es el default por si viene algo que no este en el dict) y lo sumamos
"""

def cargar_equipo(equipoABuscar, local_visitante): # 2do argumento para decidir si cargar los datos locales o de visitante
    with open('csv/datos.csv', mode='r') as file: # modo lectura # 
        reader = csv.DictReader(file) # dict tipo col dato 
        for col in reader: # cada fila es un diccionario donde la llave es la col
            if col['equipo'] == equipoABuscar:
               # print(f"Cargando equipo {local_visitante}: {equipoABuscar}") #depuracion
                if local_visitante == "local":
                    return DatosDelEquipo( # si el equipo es local regresamos en una instancia del objeto datos equipo la informacion
                        equipo=local_visitante,
                        goles_favor_local=int(col['goles_favor_local']), # convertir strings a int para que el motor los pueda usar
                        goles_contra_local=int(col['goles_contra_local']), # accedemos a los datos con la llave del diccionario
                        ganados=int(col['ganados']),
                        perdidos=int(col['perdidos']),
                        goles_favor=int(col['goles_favor']),
                        goles_contra=int(col['goles_contra']),
                        clas_general=int(col['clas_general']),
                        forma=calcForma(col['ult_5'])
                    )
                elif local_visitante == "visitante": # ...
                    return DatosDelEquipo(
                        equipo=local_visitante,
                        goles_favor_visitante=int(col['goles_favor_visitante']),
                        goles_contra_visitante=int(col['goles_contra_visitante']),
                        ganados=int(col['ganados']),
                        perdidos=int(col['perdidos']),
                        goles_favor=int(col['goles_favor']),
                        goles_contra=int(col['goles_contra']),
                        clas_general=int(col['clas_general']),
                        forma=calcForma(col['ult_5'])
                    )
    return None

# funcion para obtener los equipos del csv, guardarlos en una lista para luego mandarlos a la combobox
def obtener_lista_equipos():
    equipos = []
    with open('csv/datos.csv', mode='r', encoding='utf-8') as file: # abrir csv (lo estamos cerrando con el with)
        lector = csv.DictReader(file)
        for col in lector: # iterar sobre cada col del dictreader
            equipos.append(col['equipo']) # agregar al arreglo vacio
    return equipos