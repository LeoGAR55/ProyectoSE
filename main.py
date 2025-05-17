import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QComboBox, QCheckBox, QTextEdit, QGroupBox
)
from motor import MotorDeInferencia
from extras import cargar_equipo, obtener_lista_equipos
from hechos import TipoPartido, AusenciasClave

#.\venv\Scripts\activate
#python c:/vscWorkspace/python/main.py

# clase principal de la interfaz gráfica
class PrediccionFutbolApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Experto - Predicción de Partidos")
        self.setGeometry(100, 100, 500, 400)
        self.init_ui()  # inicializa la interfaz

    # construir la interfaz gráfica
    def init_ui(self):
        layout = QVBoxLayout()  # layout vertical principal

        # combos para seleccionar los equipos
        self.combo_local = QComboBox()
        self.combo_visitante = QComboBox()

        equipos = obtener_lista_equipos()  # carga los nombres de equipos desde un CSV
        self.combo_local.addItems(equipos)
        self.combo_visitante.addItems(equipos)

        # etiquetas y combos agregados al layout
        layout.addWidget(QLabel("Selecciona equipo LOCAL:"))
        layout.addWidget(self.combo_local)
        layout.addWidget(QLabel("Selecciona equipo VISITANTE:"))
        layout.addWidget(self.combo_visitante)

        # grupo de checkboxes para el tipo de partido
        tipo_box = QGroupBox("Tipo de Partido")
        tipo_layout = QVBoxLayout()
        self.chk_jornada = QCheckBox("Jornada regular")
        self.chk_eliminatoria = QCheckBox("Liguilla / Eliminatoria")
        self.chk_ida = QCheckBox("Partido de ida")

        # añadir opciones al layout del tipo de partido
        tipo_layout.addWidget(self.chk_jornada)
        tipo_layout.addWidget(self.chk_eliminatoria)
        tipo_layout.addWidget(self.chk_ida)
        tipo_box.setLayout(tipo_layout)
        layout.addWidget(tipo_box)

        # grupo de checkboxes para registrar ausencias clave
        ausencias_box = QGroupBox("Ausencias Clave")
        ausencias_layout = QVBoxLayout()

        self.chk_portero_local = QCheckBox("Portero local ausente")
        self.chk_delantero_local = QCheckBox("Delantero local ausente")
        self.chk_portero_visitante = QCheckBox("Portero visitante ausente")
        self.chk_delantero_visitante = QCheckBox("Delantero visitante ausente")

        # añadir los checkboxes al layout de ausencias
        ausencias_layout.addWidget(self.chk_portero_local)
        ausencias_layout.addWidget(self.chk_delantero_local)
        ausencias_layout.addWidget(self.chk_portero_visitante)
        ausencias_layout.addWidget(self.chk_delantero_visitante)
        ausencias_box.setLayout(ausencias_layout)
        layout.addWidget(ausencias_box)

        # botón que lanza el análisis del sistema experto
        self.btn_predecir = QPushButton("Predecir Resultado")
        self.btn_predecir.clicked.connect(self.ejecutar_prediccion)
        layout.addWidget(self.btn_predecir)

        # cuadro de texto para mostrar los resultados
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    # logica que se ejecuta cuando se presiona el botón "Predecir Resultado"    
    def ejecutar_prediccion(self):
        equipo_local = self.combo_local.currentText()
        equipo_visitante = self.combo_visitante.currentText()

        # cargar los hechos de cada equipo desde el archivo CSV
        local = cargar_equipo(equipo_local, "local")
        visitante = cargar_equipo(equipo_visitante, "visitante")

        if not local or not visitante:
            self.resultado.setText("Error al cargar datos de los equipos.")
            return
        
        self.resultado.clear() # limpiar salida
        """
        EXTRAIDO DE LA DOCUMENTACION
        This is the usual process to execute a KnowledgeEngine.
        The class must be instantiated, of course.
        The reset method must be called:
        This declares the special fact InitialFact. Necessary for some rules to work properly.
        Declare all facts yielded by the methods decorated with @DefFacts.
        The run method must be called. This starts the cycle of execution.
        """
        # inicializa el motor de inferencia
        motor = MotorDeInferencia(output_fn=self.resultado.append)
        motor.reset()  
        motor.reset_puntajes()  # Limpia los puntajes previos

        # declarar los hechos (datos) de los equipos
        motor.declare(local)
        motor.declare(visitante)

        # declarar hechos adicionales sobre el tipo de partido
        motor.declare(TipoPartido(
            jornada_regular=self.chk_jornada.isChecked(),
            eliminatoria=self.chk_eliminatoria.isChecked(),
            ida=self.chk_ida.isChecked()
        ))

        # declarar hechos sobre las ausencias
        motor.declare(AusenciasClave(
            equipo="local",
            portero_ausente=self.chk_portero_local.isChecked(),
            delantero_ausente=self.chk_delantero_local.isChecked()
        ))
        motor.declare(AusenciasClave(
            equipo="visitante",
            portero_ausente=self.chk_portero_visitante.isChecked(),
            delantero_ausente=self.chk_delantero_visitante.isChecked()
        ))

        # ejecuta el motor de inferencia (aplica reglas)
        motor.run()
        motor.evaluar_ganador()

# main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PrediccionFutbolApp()
    ventana.show()
    sys.exit(app.exec_())  # bucle 