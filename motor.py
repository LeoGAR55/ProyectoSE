from hechos import DatosDelEquipo,TipoPartido,AusenciasClave
from experta import KnowledgeEngine, Rule, MATCH, P

# ver https://experta.readthedocs.io/en/latest/thebasics.html#knowledgeengine

class MotorDeInferencia(KnowledgeEngine):
    def __init__(self,output_fn=print):
        super().__init__()
        self.puntajes = {}  # diccionario para almacenar los puntajes
        self.output_fn = output_fn # funcion de salida para imprimir los mensajes en el qboxedit de la interfaz

    def log(self, mensaje):
        self.output_fn(mensaje)

    # funcion para reiniciar los puntajes
    def reset_puntajes(self):
        self.puntajes = {}  # setea el diccionario a uno vacio

  # suma puntos al equipo correspondiente, creando la entrada si no existe
    def sumar_punto(self, equipo, valor=1):
        if equipo not in self.puntajes:
            self.puntajes[equipo] = 0
        self.puntajes[equipo] += valor
        print(f"Sumando {valor} puntos a {equipo}. Puntos actuales: {self.puntajes[equipo]}")  # debug

    # función que imprime los puntajes finales y evalúa al ganador o si hay empate
    def evaluar_ganador(self):
        self.log("\nResultado del análisis:")
        for equipo, puntos in self.puntajes.items():
            self.log(f"Puntos {equipo.upper()}: {puntos}")

        puntaje_local = self.puntajes.get("local", 0) # obtenemos del diccionario el valor del puntaje del elemento con la llave local
        puntaje_visitante = self.puntajes.get("visitante", 0)
        diferencia = abs(puntaje_local - puntaje_visitante) # no necesitamos negativos
        total_puntos = puntaje_local + puntaje_visitante # suma de los puntos obtenidos de los 2 equipos

        if total_puntos == 0: # el programa explotaba cuando intentaba realizar una division entre cero en algunos casos especificos
            confianza = 0  # si no se acumuló nada, la predicción es vacía (te estoy viendo a ti santos)
        else:
            confianza = round((diferencia / total_puntos) * 100)  # porcentaje de diferencia

        # margen de 1 punto se considera empate
        # evaluación final basada en puntajes
        if diferencia <= 1:
            self.log(" Predicción: Empate probable (diferencia de 1 punto o menos)")
            self.log(f" Confianza en la predicción: Baja ({confianza}%)")
        elif puntaje_local > puntaje_visitante:
            self.log(" Predicción: Gana el LOCAL")
            self.log(f" Confianza en la predicción: {confianza}%")
        else:
            self.log(" Predicción: Gana el VISITANTE")
            self.log(f" Confianza en la predicción: {confianza}%")

    # REGLAS -----------------------------------------------------------------------------
    # RULE indica que la funcion es una regla en experta 
    # esta se activa si los hechos declarados se activan con las condiciones
    # con match capturamos los valores de un hecho para trabajar con ellos
    # en la mayoria de las funciones usamos match para capturar si el equipo es local o visitante
    # y posteriormente imprimirlo en la interfaz
    # P es la expresion reservada en experta para un predicado
    # con los predicados aplicamos condicion logica a los valores de los hechos
    # cumplir la regla SI Y SOLO SI se cumple esta condicion (valor del hecho) 
    # p recibe una funcion anonima que actua como la condicion logica
    @Rule(DatosDelEquipo(equipo=MATCH.equipo, ganados=P(lambda g: g >= 15), perdidos=P(lambda p: p <= 5)))
    def historial_consistente(self, equipo):
        self.log(f"[{equipo.upper()}] Historial consistente (15+ ganados, ≤5 perdidos).")
        self.sumar_punto(equipo, 2)

    @Rule(DatosDelEquipo(equipo=MATCH.equipo, goles_favor=P(lambda gf: gf >= 50), goles_contra=P(lambda gc: gc <= 30)))
    def equipo_equilibrado(self, equipo):
        self.log(f"[{equipo.upper()}] Ataque fuerte y defensa sólida (≥50 GF, ≤30 GC).")
        self.sumar_punto(equipo, 1)

    @Rule(DatosDelEquipo(equipo=MATCH.equipo, clas_general=P(lambda c: c <= 4)))
    def buen_posicionamiento(self, equipo):
        self.log(f"[{equipo.upper()}] En TOP 4 de la tabla.")
        self.sumar_punto(equipo, 3)

    @Rule(DatosDelEquipo(equipo=MATCH.equipo, clas_general=P(lambda c: c >= 15)))
    def mal_posicionamiento(self, equipo):
        self.log(f"[{equipo.upper()}] Al fondo de la tabla (posición 15+).")
        self.sumar_punto(equipo, -2)

    @Rule(DatosDelEquipo(equipo=MATCH.equipo, forma=P(lambda f: f >= 9)))
    def buena_forma(self, equipo):
        self.log(f"[{equipo.upper()}] Buena forma reciente (9+ pts).")
        self.sumar_punto(equipo, 2)

    @Rule(DatosDelEquipo(equipo=MATCH.equipo, forma=P(lambda f: f <= 4)))
    def mala_forma(self, equipo):
        self.log(f"[{equipo.upper()}] Mala forma reciente (≤4 pts).")
        self.sumar_punto(equipo, -1)

    @Rule(DatosDelEquipo(equipo=MATCH.equipo, clas_general=P(lambda c: c >= 15), forma=P(lambda f: f <= 5)))
    def bajo_rendimiento(self, equipo):
        self.log(f"[{equipo.upper()}] Mal clasificado y en mala forma.")
        self.sumar_punto(equipo, -3)

    @Rule(DatosDelEquipo(equipo="local", goles_favor_local=P(lambda g: g >= 30)))
    def ataque_fuerte_local(self):
        self.log("LOCAL con gran cantidad de goles a favor cuando juega de local")
        self.sumar_punto("local", 3)

    @Rule(TipoPartido(eliminatoria=True))
    def es_eliminatoria(self):
        self.log("[Contexto] Partido de eliminación directa.")
        self.sumar_punto("local", 1)
        self.sumar_punto("visitante", 1)

    @Rule(TipoPartido(ida=False))
    def es_vuelta(self):
        self.log("[Contexto] Partido de vuelta. Más presión.")
        self.sumar_punto("local", 1)
        self.sumar_punto("visitante", 1)

    @Rule(AusenciasClave(equipo="local", portero_ausente=True))
    def portero_ausente_local(self):
        self.log("[Ausencia] LOCAL sin portero titular.")
        self.sumar_punto("local", -1)

    @Rule(AusenciasClave(equipo="visitante", portero_ausente=True))
    def portero_ausente_visitante(self):
        self.log("[Ausencia] VISITANTE sin portero titular.")
        self.sumar_punto("visitante", -1)

    @Rule(AusenciasClave(equipo="local", delantero_ausente=True))
    def delantero_ausente_local(self):
        self.log("[Ausencia] LOCAL sin delantero clave.")
        self.sumar_punto("local", -2)

    @Rule(AusenciasClave(equipo="visitante", delantero_ausente=True))
    def delantero_ausente_visitante(self):
        self.log("[Ausencia] VISITANTE sin delantero clave.")
        self.sumar_punto("visitante", -2)

    