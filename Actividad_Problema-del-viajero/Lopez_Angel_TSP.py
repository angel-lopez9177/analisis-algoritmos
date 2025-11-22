import tkinter as tk
from tkinter import ttk, messagebox
import math
import itertools
import random
import time

# CLASES

class Ciudad:
    """ 
    Representación de los nodos para el problema del viajero
    """
    def __init__(self, id, x, y, nombre):
        self.id = id
        self.x = x
        self.y = y
        self.nombre = nombre

    def distancia_a(self, otra_ciudad):
        """ 
        Calcula la distancia entre 2 ciudades
        """
        return math.sqrt((self.x - otra_ciudad.x)**2 + (self.y - otra_ciudad.y)**2)

class Grafo:
    """ 
    Contiene los diccionarios con las conexiones de los grafos
    """
    def __init__(self):
        self.ciudades = []
        self.matriz_distancias = []

    def agregar_ciudad(self, ciudad):
        self.ciudades.append(ciudad)
        self.actualizar_matriz()

    def generar_aleatorias(self, n, ancho, alto):
        """ Genera N ciudades en posiciones aleatorias """
        self.ciudades = []
        margen = 50
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(n):
            nombre = letras[i % len(letras)]
            x = random.randint(margen, ancho - margen)
            y = random.randint(margen, alto - margen)
            self.ciudades.append(Ciudad(i, x, y, nombre))
        self.actualizar_matriz()

    def actualizar_matriz(self):
        """ 
        Calcula la distancia entre ciudades para llenar la matriz
        """
        n = len(self.ciudades)
        self.matriz_distancias = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    dist = self.ciudades[i].distancia_a(self.ciudades[j])
                    self.matriz_distancias[i][j] = round(dist, 2)
                else:
                    self.matriz_distancias[i][j] = 0.0

class AlgoritmosViajero:
    """ 
    Implementa el algoritmo para el problema del viajero
    """
    
    def __init__(self, grafo):
        self.grafo = grafo

    def tsp_fuerza_bruta_paso_a_paso(self):
        """
        Implementación de Fuerza Bruta:
        """
        ciudades = self.grafo.ciudades
        n = len(ciudades)
        if n < 2:
            return

        # Generamos índices
        indices = list(range(n))
        
        # Comenzamos con la ciudad A
        inicio = indices[0] 
        resto = indices[1:]

        mejor_ruta = None
        mejor_distancia = float('inf')

        # Itertools.permutations genera todas las combinaciones
        for perm in itertools.permutations(resto):
            # Construimos la ruta
            ruta_actual = [inicio] + list(perm) + [inicio]
            
            # Calculamos el costo de esta ruta específica
            distancia_actual = 0
            for i in range(len(ruta_actual) - 1):
                u = ruta_actual[i]
                v = ruta_actual[i+1]
                distancia_actual += self.grafo.matriz_distancias[u][v]

            # Verificamos si es la mejor hasta el momento
            if distancia_actual < mejor_distancia:
                mejor_distancia = distancia_actual
                mejor_ruta = list(ruta_actual)
            
            # Enviamos datos a la GUI para pintar el intento
            yield ('intento', ruta_actual, distancia_actual, mejor_ruta, mejor_distancia)

        # Al terminar todas las permutaciones, enviamos el resultado final
        yield ('final', mejor_ruta, mejor_distancia, mejor_ruta, mejor_distancia)

# INTERFAZ GRÁFICA


class AplicacionTSP:
    def __init__(self, root):
        self.root = root
        self.root.title("TSP - Problema del Viajero (Fuerza Bruta)")
        self.root.geometry("900x650")

        self.grafo = Grafo()
        self.algoritmos = AlgoritmosViajero(self.grafo)
        self.animando = False
        self.generador_animacion = None
        
        self._crear_interfaz()

        self.root.after(100, self._inicializar_grafo_defecto)

    def _crear_interfaz(self):
        # Panel de Control
        panel_izq = tk.Frame(self.root, width=220, bg="#f0f0f0", padx=10, pady=10)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(panel_izq, text="TSP Solver", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        # Configuración del Mapa
        frame_gen = tk.LabelFrame(panel_izq, text="Mapa de Ciudades", bg="#f0f0f0")
        frame_gen.pack(fill="x", pady=5)
        
        tk.Label(frame_gen, text="Número de Ciudades:", bg="#f0f0f0").pack()
        self.spin_n = tk.Spinbox(frame_gen, from_=4, to=9, width=5) # Limitamos a 9 para que fuerza bruta no tarde años
        self.spin_n.delete(0,"end")
        self.spin_n.insert(0,5)
        self.spin_n.pack(pady=2)
        
        tk.Button(frame_gen, text="Generar Nuevo Mapa", command=self.generar_ciudades, bg="white").pack(pady=5)
        tk.Button(panel_izq, text="Ver Matriz de Distancias", command=self.mostrar_matriz).pack(fill="x", pady=5)

        # Algoritmo
        frame_algo = tk.LabelFrame(panel_izq, text="Control", bg="#f0f0f0")
        frame_algo.pack(fill="x", pady=15)

        tk.Button(frame_algo, text="▶ Iniciar Búsqueda TSP", bg="#d1e7dd", font=("Arial", 10, "bold"), command=self.iniciar_tsp).pack(fill="x", pady=5, padx=5)
        
        # Slider de Velocidad
        tk.Label(panel_izq, text="Velocidad Animación:", bg="#f0f0f0").pack(pady=(20, 5))
        self.slider_velocidad = tk.Scale(panel_izq, from_=1, to=100, orient=tk.HORIZONTAL, bg="#f0f0f0")
        self.slider_velocidad.set(50)
        self.slider_velocidad.pack(fill="x")

        # Área de Logs/Estado
        tk.Label(panel_izq, text="Estado de la Búsqueda:", bg="#f0f0f0", anchor="w").pack(fill="x", pady=(20,0))
        self.lbl_estado = tk.Label(panel_izq, text="Listo para iniciar.", bg="white", relief="sunken", height=12, wraplength=180, justify="left", anchor="nw", padx=5, pady=5)
        self.lbl_estado.pack(fill="both", expand=True, pady=5)

        # Grafo
        self.canvas = tk.Canvas(self.root, bg="#fafafa", highlightthickness=0) 
        self.canvas.pack(side=tk.RIGHT, fill="both", expand=True)

    def _inicializar_grafo_defecto(self):
        self.generar_ciudades()

    def generar_ciudades(self):
        #Generar 
        self.detener_animacion()
        try:
            n = int(self.spin_n.get())
        except:
            n = 5
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100: w, h = 600, 500

        self.grafo.generar_aleatorias(n, w, h)
        self.dibujar_grafo_base()
        self.log(f"Mapa generado con {n} ciudades.\nMatriz de distancias actualizada.")

    def dibujar_grafo_base(self):
        self.canvas.delete("all")
        
        # Dibujar conexiones tenues de fondo
        for i, c1 in enumerate(self.grafo.ciudades):
            for j, c2 in enumerate(self.grafo.ciudades):
                if i < j:
                    self.canvas.create_line(c1.x, c1.y, c2.x, c2.y, fill="#cccccc", width=1)

        # Dibujar ciudades
        r = 15
        for c in self.grafo.ciudades:
            # Círculo
            self.canvas.create_oval(c.x-r, c.y-r, c.x+r, c.y+r, fill="#3498db", outline="black", tags="nodo")
            # Etiqueta
            self.canvas.create_text(c.x, c.y, text=c.nombre, fill="white", font=("Arial", 10, "bold"))

    def dibujar_ruta(self, indices_ciudades, color, ancho=2, tags="ruta"):
        """ Dibuja líneas conectando una lista de índices de ciudades """
        ciudades = self.grafo.ciudades
        if not indices_ciudades: return
        
        for i in range(len(indices_ciudades) - 1):
            c1 = ciudades[indices_ciudades[i]]
            c2 = ciudades[indices_ciudades[i+1]]
            self.canvas.create_line(c1.x, c1.y, c2.x, c2.y, fill=color, width=ancho, tags=tags, capstyle=tk.ROUND)

    def detener_animacion(self):
        self.animando = False
        self.generador_animacion = None

    def mostrar_matriz(self):
        """ Muestra la matriz de distancias en una ventana nueva """
        top = tk.Toplevel(self.root)
        top.title("Matriz de Distancias")
        top.geometry("500x300")
        
        text_area = tk.Text(top, font=("Courier", 10))
        text_area.pack(fill="both", expand=True)
        
        ciudades = self.grafo.ciudades
        linea_header = "      " + " ".join([f"{c.nombre:>6}" for c in ciudades]) + "\n"
        text_area.insert(tk.END, linea_header)
        text_area.insert(tk.END, "-" * len(linea_header) + "\n")

        # Filas
        matriz = self.grafo.matriz_distancias
        for i, row in enumerate(matriz):
            linea = f"{ciudades[i].nombre:>4} |"
            for val in row:
                linea += f"{val:6.1f} "
            text_area.insert(tk.END, linea + "\n")

    def log(self, mensaje):
        self.lbl_estado.config(text=mensaje)

    # Ejecución del Algoritmo
 
    def iniciar_tsp(self):
        self.detener_animacion()
        self.dibujar_grafo_base()
        # Obtenemos el generador del algoritmo
        self.generador_animacion = self.algoritmos.tsp_fuerza_bruta_paso_a_paso()
        self.animando = True
        self.log("Iniciando búsqueda por Fuerza Bruta...")
        self.paso_animacion()

    def paso_animacion(self):
        """ Animación """
        if not self.animando: return

        try:
            datos = next(self.generador_animacion)
            tipo = datos[0]
            
            #Limpiar la ruta 
            self.canvas.delete("temp")

            if tipo == 'intento':
                ruta, dist, mejor_ruta, mejor_dist = datos[1:]
                
                # Dibujar ruta actual
                self.dibujar_ruta(ruta, "#999999", 2, "temp")
                
                # Dibujar la mejor ruta encontrada hasta el momento
                self.canvas.delete("mejor")
                if mejor_ruta:
                    self.dibujar_ruta(mejor_ruta, "#2ecc71", 4, "mejor")

                # Actualizar rutas
                txt = f"Evaluando: {'-'.join([self.grafo.ciudades[i].nombre for i in ruta])}\n"
                txt += f"Distancia: {dist:.2f}\n\n"
                txt += f"MEJOR ACTUAL: {mejor_dist:.2f}"
                self.log(txt)

            elif tipo == 'final':
                mejor_ruta, mejor_dist = datos[1], datos[2]
                self.canvas.delete("temp")
                self.canvas.delete("mejor")
                # Dibujar resultado final
                self.dibujar_ruta(mejor_ruta, "#e74c3c", 5, "final")
                
                txt = f"--- BÚSQUEDA TERMINADA ---\n\n"
                txt += f"Ruta Óptima: {'-'.join([self.grafo.ciudades[i].nombre for i in mejor_ruta])}\n"
                txt += f"Costo Mínimo: {mejor_dist:.2f}"
                self.log(txt)
                self.animando = False
                return

            # Control de velocidad
            val = self.slider_velocidad.get()
            delay = int(800 - (val * 7.9)) 
            if delay < 1: delay = 1
            
            self.root.after(delay, self.paso_animacion)

        except StopIteration:
            self.animando = False

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionTSP(root)
    root.mainloop()