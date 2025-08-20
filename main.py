import tkinter as tk
import tkinter.ttk as ttk
import time
import numpy as np
import numpy.typing as npt
import re

from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

REPETICIONES: int = 30

LISTADEOPCIONES: tuple[str] = ("100", "200", "300", "400", "500", "600", "700", "800", "900", "1000")
diccionario_algoritmo_tiempo = {}

diccionario_algoritmo_tiempo['lineal'] = np.zeros(shape=len(LISTADEOPCIONES), dtype="float64")
diccionario_algoritmo_tiempo['binario'] = np.zeros(shape=len(LISTADEOPCIONES), dtype="float64")

def generar_datos(envoltura) -> None:
        boton_busqueda_binaria.configure(state="active")
        boton_busqueda_lineal.configure(state="active")
        tamano = int(tamano_Lista.get())
        envoltura[0] = np.random.default_rng().integers(100000,size=tamano, dtype="int32")
        envoltura[0].sort()
        lista_datos.delete(0, lista_datos.size())
        for i, number in enumerate(envoltura[0]):
                lista_datos.insert(i, number)
        return

def busqueda_lineal():
        if not numero_a_buscar.get() == "":
                dato = int(numero_a_buscar.get())
                tiempo_promedio: float = 0
                for reps in range(REPETICIONES):
                        tiempo_inicial = time.perf_counter()
                        for i, _dato in enumerate(interfaz_datos[0]):
                                if dato == _dato:
                                        break
                        tiempo_final = time.perf_counter()
                        tiempo_promedio = tiempo_promedio + tiempo_final - tiempo_inicial
                lista_datos.yview_moveto(float(i/lista_datos.size()))
                tiempo_promedio = tiempo_promedio / REPETICIONES
                tiempo_promedio = tiempo_promedio * 1000
                if interfaz_datos[0][i] == dato:
                        resultados_texto.set(f"El numero {dato} se encontró en el indice {i} en un tiempo de {tiempo_promedio:.3f} ms")
                else:
                        resultados_texto.set(f"No se encontro el numero en la lista, tiempo de ejecución: {tiempo_promedio:.3f} ms")
                global diccionario_algoritmo_tiempo
                diccionario_algoritmo_tiempo["lineal"][LISTADEOPCIONES.index(str(lista_datos.size()))] = tiempo_promedio
                actualizar_grafica()
        else:
                resultados_texto.set("Ingresa un valor valido a la busqueda")
                return
                
def busqueda_binaria():
        if not numero_a_buscar.get() == "":
                dato = int(numero_a_buscar.get())
                tiempo_promedio: float = 0
                for reps in range(REPETICIONES):
                        tiempo_inicial = time.perf_counter()
                        r = interfaz_datos[0].shape[0]
                        l = 0
                        while r >= l:
                                m = int((r + l) / 2)
                                if interfaz_datos[0][m] == dato:
                                        break
                                elif interfaz_datos[0][m] < dato:
                                        l = m + 1
                                else:
                                        r = m - 1
                        tiempo_final = time.perf_counter()
                        tiempo_promedio = tiempo_promedio + tiempo_final - tiempo_inicial
                lista_datos.yview_moveto(float(m/lista_datos.size()))
                tiempo_promedio = tiempo_promedio / REPETICIONES
                tiempo_promedio = tiempo_promedio * 1000
                if interfaz_datos[0][m] == dato:
                        resultados_texto.set(f"El numero {dato} se encontró en el indice {m} en un tiempo de {tiempo_promedio:.3f} ms")
                else:
                        resultados_texto.set(f"No se encontro el numero en la lista, tiempo de ejecución: {tiempo_promedio:.3f} ms")
                global diccionario_algoritmo_tiempo
                diccionario_algoritmo_tiempo["binario"][LISTADEOPCIONES.index(str(lista_datos.size()))] = tiempo_promedio
                actualizar_grafica()
        else:
                resultados_texto.set("Ingresa un valor valido a la busqueda")
                return

def revisar_si_es_numero(nuevoValor:int)->bool:
        return re.match('^[0-9]*$', nuevoValor) is not None 

def aumentar_tamano_array(envoltura):
        envoltura[0] = np.resize(envoltura[0], int(tamano_Lista.get()))
        return envoltura

def actualizar_grafica():
        global figura
        figura.clear()
        grafica = figura.add_subplot()
        x = np.arange(len(LISTADEOPCIONES))
        offset = 0
        w = 0.4
        for algoritmo, tiempos in diccionario_algoritmo_tiempo.items():
                grafica.plot(x, tiempos)
        grafica.grid()
        grafica.set_title("Tiempo promedio de los algoritmos")
        grafica.legend(diccionario_algoritmo_tiempo.keys())         
        grafica.set_xlabel("Cantidad de elementos")
        grafica.set_ylabel("Tiempo promedio (ms)")
        grafica.set_xticks(x+w/2, LISTADEOPCIONES)
        
        global grafica_embebido
        grafica_embebido.draw()

if __name__ == "__main__":
        datos: npt.ArrayLike = np.empty(shape=100, dtype="int32")
        interfaz_datos = [datos]
        ventana = tk.Tk()
        ventana.title("Analisis de algoritmos de busqueda")
        ventana.geometry("1080x540")
        contenido = tk.Frame(ventana)
        contenido.grid(column=0, row=0, sticky='wnes')
        
        frame_tamano_lista = tk.Frame(contenido)
        frame_tamano_lista.grid(column=0, row=0, padx=10, pady=10)
        
        label_tamano_lista = tk.Label(frame_tamano_lista, text="Selecciona la cantidad de elementos que tendra la lista")
        label_tamano_lista.grid(column=0, row=0)
        
        tamano_Lista = tk.StringVar()
                
        opciones = ttk.Combobox(frame_tamano_lista, values=LISTADEOPCIONES, textvariable=tamano_Lista)
        opciones.state(["readonly"])
        opciones.grid(column=0, row=1, pady=5)
        
        interfaz_generar_datos = lambda: generar_datos(aumentar_tamano_array(interfaz_datos))
        boton_generar_datos = tk.Button(contenido, text="Generar datos", command=interfaz_generar_datos)
        boton_generar_datos.grid(row=1, column=0)
        
        frame_lista_datos = tk.Frame(contenido)
        frame_lista_datos.grid(row=2, column=0, pady=10, sticky="sn")
        
        lista_datos = tk.Listbox(frame_lista_datos, height=10)
        lista_datos.grid(column=0, row=0, sticky=(tk.W,tk.E,tk.S,tk.N))
        
        scroll_lista_datos = tk.Scrollbar(frame_lista_datos, orient="vertical", command=lista_datos.yview)
        scroll_lista_datos.grid(column=1,row=0,sticky=(tk.N,tk.S))
        lista_datos['yscrollcommand'] = scroll_lista_datos.set
        
        interfaz_revisar = (ventana.register(revisar_si_es_numero), '%P')
        numero_a_buscar = tk.StringVar()
        label_numero_buscar = tk.Label(contenido, text="Ingrese el numero que desea buscar")
        label_numero_buscar.grid(row=3, column=0, pady=5)
        input_de_numero = tk.Entry(contenido, textvariable=numero_a_buscar, validate="key", validatecommand=interfaz_revisar)
        input_de_numero.grid(row=4, column=0)
        
        frame_opciones_busqueda = tk.Frame(contenido)
        frame_opciones_busqueda.grid(row=5, column=0, pady=10)
        boton_busqueda_lineal = tk.Button(frame_opciones_busqueda, text="Busqueda lineal", command=busqueda_lineal, state="disabled")
        boton_busqueda_lineal.grid(column=0,row=0, padx=5)
        boton_busqueda_binaria = tk.Button(frame_opciones_busqueda, text="Busqueda binaria", command=busqueda_binaria, state="disabled")
        boton_busqueda_binaria.grid(column=1, row=0, padx=5)
        
        resultados_texto = tk.StringVar()
        label_resultados = tk.Label(contenido, textvariable=resultados_texto)
        resultados_texto.set("Resultados:")
        label_resultados.grid(column=1, row=0)
        
        figura = Figure(figsize=(LISTADEOPCIONES.__len__()+2, 4), dpi=100, layout="constrained")
        grafica_embebido = FigureCanvasTkAgg(figura, contenido)
        
        actualizar_grafica()
        
        grafica_embebido.get_tk_widget().grid(column=1,row=1, sticky='snwe', rowspan=5)
        
        ventana.rowconfigure(0, weight=1)
        ventana.columnconfigure(0, weight=1)
        
        contenido.rowconfigure(0, weight=0)
        contenido.columnconfigure(0, minsize=400, weight=0)
        contenido.rowconfigure(2, weight=1, minsize=250)
        contenido.columnconfigure(1, minsize=400, weight=1)
        frame_lista_datos.rowconfigure(0, weight=1)
        frame_lista_datos.columnconfigure(0, weight=1)
        
        tamano_Lista.set(LISTADEOPCIONES[0])
        ventana.mainloop()