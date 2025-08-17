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

REPETICIONES: int = 5

LISTADEOPCIONES: tuple[str] = ("100", "1000", "10000", "100000")
diccionario_algoritmo_tiempo = {}

diccionario_algoritmo_tiempo['lineal'] = np.zeros(shape=len(LISTADEOPCIONES), dtype="uint32")
diccionario_algoritmo_tiempo['binario'] = np.zeros(shape=len(LISTADEOPCIONES), dtype="uint32")

diccionario_barras = {'lineal': None, 'binario': None}

def generar_datos(envoltura) -> None:
        boton_busqueda_binaria.configure(state="active")
        boton_busqueda_lineal.configure(state="active")
        tamano = int(tamano_Lista.get())
        envoltura[0] = np.random.default_rng().integers(tamano*10,size=tamano, dtype="int32")
        envoltura[0].sort()
        lista_datos.delete(0, lista_datos.size())
        for i, number in enumerate(envoltura[0]):
                lista_datos.insert(i, number)
        return

def busqueda_lineal():
        dato = int(numero_a_buscar.get())
        tiempo_promedio: int = 0
        for r in range(REPETICIONES):
                tiempo_inicial = time.perf_counter()
                for i, _dato in enumerate(interfaz_datos[0]):
                        if dato == _dato:
                                break
                tiempo_final = time.perf_counter()
                tiempo_promedio = tiempo_promedio + tiempo_final - tiempo_inicial
        lista_datos.yview_scroll(i, "units")
        tiempo_promedio = tiempo_promedio / REPETICIONES
        #diccionario_barras["lineal"][LISTADEOPCIONES.index(lista_datos.get())].
                
def busqueda_binaria(lista: list[int], dato:int):
        raise NotImplementedError 

def revisar_si_es_numero(nuevoValor:int)->bool:
        return re.match('^[0-9]*$', nuevoValor) is not None 

def aumentar_tamano_array(envoltura):
        envoltura[0] = np.resize(envoltura[0], int(tamano_Lista.get()))
        return envoltura

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
        frame_lista_datos.grid(row=2, column=0, pady=10)
        
        lista_datos = tk.Listbox(frame_lista_datos, height=10)
        lista_datos.grid(column=0,row=0,sticky=(tk.W,tk.E,tk.S,tk.N))
        
        scroll_lista_datos = tk.Scrollbar(frame_lista_datos, orient="vertical", command=lista_datos.yview)
        scroll_lista_datos.grid(column=1,row=0,sticky=(tk.N,tk.S))
        lista_datos['yscrollcommand'] = scroll_lista_datos.set
        
        interfaz_revisar = (ventana.register(revisar_si_es_numero), '%P')
        numero_a_buscar = tk.IntVar()
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
        
        figura = Figure(figsize=(6, 4), dpi=100)
        grafica = figura.add_subplot()
        for algoritmo, tiempo in diccionario_algoritmo_tiempo.items():
                diccionario_barras[algoritmo] = grafica.bar(LISTADEOPCIONES, tiempo, data=tiempo, label=algoritmo)
        grafica.set_title("Tiempo promedio de los algoritmos")
        grafica.legend()         
        grafica.set_xlabel("Cantidad de elementos")
        grafica.set_ylabel("Tiempo promedio")
        
        diccionario_algoritmo_tiempo["lineal"][0] = 9
        
        for algoritmo, tiempo in diccionario_algoritmo_tiempo.items():
                diccionario_barras[algoritmo] = grafica.bar(LISTADEOPCIONES, tiempo, data=tiempo, label=algoritmo)
        grafica.legend()    
        
        grafica_embebido = FigureCanvasTkAgg(figura, contenido)
        grafica_embebido.draw()
        grafica_embebido.get_tk_widget().grid(column=1,row=1, sticky='se', rowspan=5)
        
        tamano_Lista.set(LISTADEOPCIONES[0])
        ventana.mainloop()