import sys
import time
import matplotlib

# Configurar el backend de Matplotlib para que funcione con PySide6
matplotlib.use('QtAgg')

from PySide6 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Tus importaciones originales (Asegúrate de que estos archivos existan en tu carpeta)
from huffman import build_shared_huffman_map, encode_text, decode_tokens
from fuerza_bruta.lcs_fuerza_bruta import lcs_brute_force
from programacion_dinamica.lcs_programacion_dinamica import lcs_dinamyc_programing
from divide_y_venceras.lcs_divide_y_venceras import lcs_dc_dp
from Bio import SeqIO

# --- Clase para el Canvas de Matplotlib ---
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        
        # Ajustes de estilo para coincidir con el tema oscuro
        self.fig.patch.set_facecolor('#2e2e2e')  # Color de fondo de la figura (borde)
        self.axes.set_facecolor('#1c1c1c')      # Color de fondo de la gráfica
        
        # Colores de ejes y texto
        self.axes.spines['bottom'].set_color('#ecf0f1')
        self.axes.spines['top'].set_color('#ecf0f1') 
        self.axes.spines['right'].set_color('#ecf0f1')
        self.axes.spines['left'].set_color('#ecf0f1')
        self.axes.tick_params(axis='x', colors='#ecf0f1')
        self.axes.tick_params(axis='y', colors='#ecf0f1')
        self.axes.yaxis.label.set_color('#ffffff')
        self.axes.xaxis.label.set_color('#ffffff')
        self.axes.title.set_color('#ffffff')

        super(MplCanvas, self).__init__(self.fig)

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Longest Common Subsequence (LCS) & Complexity Analysis")
        self.resize(1000, 750) # Hice la ventana un poco más ancha para la gráfica
        
        self.apply_styles()

        self.seq1 = None
        self.seq2 = None
        self.file1_path = ""
        self.file2_path = ""
        self.huffman_dict = {}
        self.tokens_a = []
        self.tokens_b = []

        # Estructura para guardar datos de la gráfica: {'algo': str, 'n': int, 'time': float}
        self.history_data = [] 

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal: Izquierda (Controles), Derecha (Gráfica y Resultados)
        self.main_layout = QtWidgets.QHBoxLayout(central_widget)

        # --- Panel Izquierdo (Controles) ---
        left_panel = QtWidgets.QWidget()
        self.left_layout = QtWidgets.QVBoxLayout(left_panel)

        self.create_file_selection_group(self.left_layout)
        self.create_range_selection_group(self.left_layout)
        self.create_action_buttons(self.left_layout)
        self.create_text_results_area(self.left_layout)
        
        self.left_layout.addStretch()

        # --- Panel Derecho (Gráfica) ---
        right_panel = QtWidgets.QWidget()
        self.right_layout = QtWidgets.QVBoxLayout(right_panel)
        
        self.create_plot_area(self.right_layout)

        # Añadir paneles al layout principal
        self.main_layout.addWidget(left_panel, 40) # 40% ancho
        self.main_layout.addWidget(right_panel, 60) # 60% ancho

    def apply_styles(self):
        style_sheet = """
        /* Fondo general y texto */
        QMainWindow, QWidget {
            background-color: #2e2e2e;
            color: #ecf0f1;
            font-family: 'Segoe UI', sans-serif;
            font-size: 12px;
        }

        /* Grupos (Cajas) */
        QGroupBox {
            border: 2px solid #8e44ad;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 15px;
            font-weight: bold;
            color: #d2b4de;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 5px;
            background-color: #2e2e2e;
        }

        /* Botones */
        QPushButton {
            background-color: #6c3483;
            color: white;
            border: 2px solid #5b2c6f;
            border-radius: 6px;
            padding: 8px 15px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #8e44ad;
            border-color: #9b59b6;
        }
        QPushButton:pressed {
            background-color: #4a235a;
        }

        /* Inputs numéricos */
        QSpinBox {
            background-color: #404040;
            border: 1px solid #8e44ad;
            border-radius: 4px;
            padding: 5px;
            color: white;
            selection-background-color: #9b59b6;
        }
        
        /* Área de texto */
        QPlainTextEdit {
            background-color: #1c1c1c;
            border: 1px solid #8e44ad;
            border-radius: 5px;
            color: #00ffcc;
            font-family: 'Consolas', monospace;
            padding: 5px;
        }
        
        QLabel { color: #ecf0f1; }
        """
        self.setStyleSheet(style_sheet)

    # --- UI CREATION HELPERS (Modificados para recibir layout) ---

    def create_file_selection_group(self, parent_layout):
        group_box = QtWidgets.QGroupBox("Selección de Archivos FASTA")
        layout = QtWidgets.QGridLayout()

        self.lbl_file1 = QtWidgets.QLabel("Archivo 1 no seleccionado")
        self.lbl_file1.setStyleSheet("color: #95a5a6; font-style: italic;")
        btn_select1 = QtWidgets.QPushButton("Seleccionar .fna 1")
        btn_select1.clicked.connect(self.open_selector_1)

        self.lbl_file2 = QtWidgets.QLabel("Archivo 2 no seleccionado")
        self.lbl_file2.setStyleSheet("color: #95a5a6; font-style: italic;")
        btn_select2 = QtWidgets.QPushButton("Seleccionar .fna 2")
        btn_select2.clicked.connect(self.open_selector_2)

        layout.addWidget(QtWidgets.QLabel("Secuencia 1:"), 0, 0)
        layout.addWidget(btn_select1, 1, 0)
        layout.addWidget(self.lbl_file1, 1, 1)

        layout.addWidget(QtWidgets.QLabel("Secuencia 2:"), 2, 0)
        layout.addWidget(btn_select2, 3, 0)
        layout.addWidget(self.lbl_file2, 3, 1)

        group_box.setLayout(layout)
        parent_layout.addWidget(group_box)

    def create_range_selection_group(self, parent_layout):
        group_box = QtWidgets.QGroupBox("Configuración de Rangos")
        layout = QtWidgets.QVBoxLayout() 

        # Rango 1
        range1_layout = QtWidgets.QHBoxLayout()
        range1_layout.addWidget(QtWidgets.QLabel("Rango 1:"))
        self.spin_r1_start = QtWidgets.QSpinBox()
        self.spin_r1_start.setRange(0, 999999999) 
        self.spin_r1_start.setValue(0)
        self.spin_r1_end = QtWidgets.QSpinBox()
        self.spin_r1_end.setRange(0, 999999999)
        self.spin_r1_end.setValue(10000)
        range1_layout.addWidget(self.spin_r1_start)
        range1_layout.addWidget(QtWidgets.QLabel("-"))
        range1_layout.addWidget(self.spin_r1_end)

        # Rango 2
        range2_layout = QtWidgets.QHBoxLayout()
        range2_layout.addWidget(QtWidgets.QLabel("Rango 2:"))
        self.spin_r2_start = QtWidgets.QSpinBox()
        self.spin_r2_start.setRange(0, 999999999)
        self.spin_r2_start.setValue(3600000)
        self.spin_r2_end = QtWidgets.QSpinBox()
        self.spin_r2_end.setRange(0, 999999999)
        self.spin_r2_end.setValue(3610000)
        range2_layout.addWidget(self.spin_r2_start)
        range2_layout.addWidget(QtWidgets.QLabel("-"))
        range2_layout.addWidget(self.spin_r2_end)

        layout.addLayout(range1_layout)
        layout.addLayout(range2_layout)
        
        group_box.setLayout(layout)
        parent_layout.addWidget(group_box)

    def create_action_buttons(self, parent_layout):
        layout = QtWidgets.QHBoxLayout()
        
        btn_brute = QtWidgets.QPushButton("Fuerza Bruta")
        btn_brute.setCursor(QtCore.Qt.PointingHandCursor)
        btn_brute.clicked.connect(self.execute_brute_force)
        
        btn_dc = QtWidgets.QPushButton("Divide y Vencerás")
        btn_dc.setCursor(QtCore.Qt.PointingHandCursor)
        btn_dc.clicked.connect(self.execute_divide_conquer)
        
        btn_dp = QtWidgets.QPushButton("Prog. Dinámica")
        btn_dp.setCursor(QtCore.Qt.PointingHandCursor)
        btn_dp.clicked.connect(self.execute_dinamyc_programing)

        layout.addWidget(btn_brute)
        layout.addWidget(btn_dc)
        layout.addWidget(btn_dp)

        parent_layout.addLayout(layout)

    def create_text_results_area(self, parent_layout):
        group_box = QtWidgets.QGroupBox("Detalles de Ejecución")
        layout = QtWidgets.QVBoxLayout()

        estilo_resaltado = "color: #bb8fce; font-weight: bold;"

        self.lbl_huffman = QtWidgets.QLabel("Dict Huffman: ...")
        self.lbl_huffman.setStyleSheet(estilo_resaltado)

        self.lbl_type = QtWidgets.QLabel("Algoritmo: ...")
        self.lbl_type.setStyleSheet(estilo_resaltado)
        
        self.lbl_size = QtWidgets.QLabel("LCS Len: ...")
        self.lbl_size.setStyleSheet(estilo_resaltado)
        
        self.lbl_time = QtWidgets.QLabel("Tiempo: ...")
        self.lbl_time.setStyleSheet(estilo_resaltado)
        
        layout.addWidget(self.lbl_type)
        layout.addWidget(self.lbl_size)
        layout.addWidget(self.lbl_time)
        layout.addWidget(self.lbl_huffman)
        
        self.txt_lcs = QtWidgets.QPlainTextEdit() 
        self.txt_lcs.setReadOnly(True) 
        self.txt_lcs.setPlaceholderText("Resultado de la secuencia...")
        self.txt_lcs.setMaximumHeight(100)
        self.txt_lcs.setStyleSheet(estilo_resaltado)
        
        layout.addWidget(QtWidgets.QLabel("LCS Resultante:"))
        layout.addWidget(self.txt_lcs)

        group_box.setLayout(layout)
        parent_layout.addWidget(group_box)

    def create_plot_area(self, parent_layout):
        group_box = QtWidgets.QGroupBox("Gráfica de Complejidad Temporal")
        layout = QtWidgets.QVBoxLayout()

        # Instanciar el canvas de Matplotlib
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.sc)
        
        # Botón para limpiar gráfica
        btn_clear = QtWidgets.QPushButton("Limpiar Gráfica")
        btn_clear.clicked.connect(self.clear_plot)
        layout.addWidget(btn_clear)

        group_box.setLayout(layout)
        parent_layout.addWidget(group_box)

    # --- PLOTTING LOGIC ---

    def update_plot(self):
        self.sc.axes.cla() # Limpiar ejes anteriores
        
        # Configurar etiquetas
        self.sc.axes.set_xlabel('Tamaño de Entrada (N)', color='#ecf0f1')
        self.sc.axes.set_ylabel('Tiempo (Segundos)', color='#ecf0f1')
        self.sc.axes.set_title('Comparativa de Rendimiento', color='#ecf0f1')
        self.sc.axes.grid(True, linestyle='--', alpha=0.3)

        # Separar datos por algoritmo
        algos = {}
        for entry in self.history_data:
            name = entry['algo']
            if name not in algos:
                algos[name] = {'x': [], 'y': []}
            algos[name]['x'].append(entry['n'])
            algos[name]['y'].append(entry['time'])

        # Graficar cada algoritmo
        colors = {'Fuerza Bruta': '#e74c3c', 'Divide y Vencerás': '#f39c12', 'Prog. Dinámica': '#3498db'}
        markers = {'Fuerza Bruta': 'o', 'Divide y Vencerás': '^', 'Prog. Dinámica': 's'}

        for name, data in algos.items():
            # Ordenar puntos por eje X para que la línea se dibuje bien
            points = sorted(zip(data['x'], data['y']))
            x_sorted = [p[0] for p in points]
            y_sorted = [p[1] for p in points]
            
            c = colors.get(name, 'white')
            m = markers.get(name, 'o')
            
            self.sc.axes.plot(x_sorted, y_sorted, label=name, color=c, marker=m, linewidth=2)

        if algos:
            legend = self.sc.axes.legend()
            # Ajustar color de leyenda para fondo oscuro
            frame = legend.get_frame()
            frame.set_facecolor('#404040')
            frame.set_edgecolor('#8e44ad')
            for text in legend.get_texts():
                text.set_color("white")

        self.sc.draw()

    def clear_plot(self):
        self.history_data = []
        self.update_plot()

    # --- FUNCIONES LOGICAS ---

    def open_selector_1(self):
        filtro = "Archivos de Fasta (*.fna)"
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Abrir Secuencia 1", "", filtro)
        if file_path:
            self.file1_path = file_path
            filename = QtCore.QFileInfo(file_path).fileName()
            self.lbl_file1.setText(filename)
            self.lbl_file1.setStyleSheet("color: #2ecc71; font-weight: bold;") 

    def open_selector_2(self):
        filtro = "Archivos de Fasta (*.fna)"
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Abrir Secuencia 2", "", filtro)
        if file_path:
            self.file2_path = file_path
            filename = QtCore.QFileInfo(file_path).fileName()
            self.lbl_file2.setText(filename)
            self.lbl_file2.setStyleSheet("color: #2ecc71; font-weight: bold;")

    def parse_files(self):
        if not self.file1_path or not self.file2_path:
            QtWidgets.QMessageBox.warning(self, "Error", "Selecciona ambos archivos primero.")
            return False
        try:
            record1 = next(SeqIO.parse(self.file1_path, "fasta"))
            record2 = next(SeqIO.parse(self.file2_path, "fasta"))
            self.seq1 = record1.seq
            self.seq2 = record2.seq
            return True
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error parsing files: {e}")
            return False

    def create_tokens(self):
        if not self.parse_files():
            return False

        try:
            start1, end1 = int(self.spin_r1_start.value()), int(self.spin_r1_end.value())
            start2, end2 = int(self.spin_r2_start.value()), int(self.spin_r2_end.value())

            sub1 = self.seq1[start1:end1]
            sub2 = self.seq2[start2:end2]

            self.huffman_dict = build_shared_huffman_map(sub1, sub2)
            self.tokens_a = encode_text(sub1, self.huffman_dict)
            self.tokens_b = encode_text(sub2, self.huffman_dict)
            dict_str = "Diccionario: \n{\n"
            for k, v in self.huffman_dict.items():
                dict_str = dict_str + f"  '{k}': {v}\n"
            dict_str = dict_str + "}"
            self.lbl_huffman.setText(dict_str)
            return True
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error creando tokens: {e}")
            return False

    def execute_brute_force(self):
        if not self.create_tokens(): return
        print("Ejecutando Fuerza Bruta...")
        self.lbl_type.setText("Algoritmo: Fuerza bruta")
        
        # Medición
        start = time.time()
        res = lcs_brute_force(self.tokens_a, self.tokens_b, len(self.tokens_a), len(self.tokens_b))
        end = time.time()
        duration = end - start
        
        # Actualizar UI
        self.lbl_size.setText(f"Tamaño LCS: {res}")
        self.lbl_time.setText(f"Tiempo: {duration:.5f} s")
        self.txt_lcs.setPlainText("(Resultado texto no disponible en FB)")
        
        # Guardar en gráfica (Usamos len(tokens_a) como referencia de tamaño de entrada N)
        self.history_data.append({'algo': 'Fuerza Bruta', 'n': len(self.tokens_a), 'time': duration})
        self.update_plot()

    def execute_divide_conquer(self):
        if not self.create_tokens(): return
        print("Ejecutando DyV...")
        self.lbl_type.setText("Algoritmo: DyV combinado")
        
        start = time.time()
        size, lcs_sequence = lcs_dc_dp(self.tokens_a, self.tokens_b)
        end = time.time()
        duration = end - start
        
        self.lbl_size.setText(f"Tamaño LCS: {size}")
        self.lbl_time.setText(f"Tiempo: {duration:.5f} s")
        final_result = decode_tokens(lcs_sequence, self.huffman_dict)
        self.txt_lcs.setPlainText(final_result)
        
        self.history_data.append({'algo': 'Divide y Vencerás', 'n': len(self.tokens_a), 'time': duration})
        self.update_plot()

    def execute_dinamyc_programing(self):
        if not self.create_tokens(): return
        print("Ejecutando Prog. Dinamica...")
        self.lbl_type.setText("Algoritmo: Prog. Dinamica")
        
        start = time.time()
        dp_lcs_sequence = lcs_dinamyc_programing(self.tokens_a, self.tokens_b)
        end = time.time()
        duration = end - start
        
        self.lbl_size.setText(f"Tamaño LCS: {len(dp_lcs_sequence)}")
        self.lbl_time.setText(f"Tiempo: {duration:.5f} s")
        
        final_result = decode_tokens(dp_lcs_sequence, self.huffman_dict)
        self.txt_lcs.setPlainText(final_result)
        
        self.history_data.append({'algo': 'Prog. Dinámica', 'n': len(self.tokens_a), 'time': duration})
        self.update_plot()

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()