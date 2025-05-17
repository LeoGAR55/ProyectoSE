from experta import Fact # https://experta.readthedocs.io/en/latest/thebasics.html

# datos obtenidos de: https://fbref.com/es/comps/31/Estadisticas-de-Liga-MX#all_results2024-2025310
# https://footystats.org/es/mexico/liga-mx

class DatosDelEquipo(Fact):
    #Los hechos en experta son la unidad basica de información en experta
    equipo = ""
    ganados = 0
    empatados = 0
    perdidos = 0
    goles_favor = 0
    goles_contra = 0
    goles_favor_local = 0
    goles_contra_local = 0
    goles_favor_visitante = 0
    goles_contra_visitante = 0
    clas_general = 0
    ult_5 = ""  # CADENA DE TEXTO vvevd
    forma = 0 # ver la funcion calcular forma en extras

    # clases para definir el cotexto en el que se va a jugar el partido
class TipoPartido(Fact):
    jornada_regular = True   # true si es jornada regular, false si es liguilla
    eliminatoria = False     # true si es partido de eliminación directa
    ida = True               # true si es partido de ida, false si es vuelta

class AusenciasClave(Fact):
    equipo = ""              # local o visitante
    portero_ausente = False
    delantero_ausente = False