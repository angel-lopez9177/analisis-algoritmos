- [1. Introducción al curso](#1-introducción-al-curso)
- [2. Actividad 1 - Busqueda](#2-actividad-1---busqueda)
  - [2.1. Ejecución](#21-ejecución)
    - [2.1.1. Librerias](#211-librerias)
- [3. Practica - MergeSort y QuickSort](#3-practica---mergesort-y-quicksort)
  - [3.1. Ejecución](#31-ejecución)
- [4. Participación - Fibonacci](#4-participación---fibonacci)
  - [4.1. Ejecución](#41-ejecución)
    - [4.1.1. Librerias](#411-librerias)

# 1. Introducción al curso

Este repositorio contiene todas las actividades realizadas por mi en la materia de analisis de algoritmos.

**Para la ejecución de algunos de los programas es necesario la creación de un entorno virtual con las librerias que se encuentran en el archivo "requirements.txt", en la descripción de cada actividad se especifica cada libreria necesaria para su propia ejecución.**

# 2. Actividad 1 - Busqueda

La actividad 1 consiste en la creacion de una GUI para analizar las diferencias entre los algoritmos de busqueda lineal y binarios.

## 2.1. Ejecución
No existe ninguna nota para le ejecución de este programa.

### 2.1.1. Librerias
    numpy
    matplotlib
    tkinter

# 3. Practica - MergeSort y QuickSort

La practica consistió en el desarrollo de 2 ambos algoritmos mencionados en el titulo. La implementación fue sencilla ya que no fue necesaria la construcción de alguna GUI, si no que unicamente se mostraban los resultados en la terminal.

## 3.1. Ejecución
No existe ninguna nota para le ejecución de este programa.

# 4. Participación - Fibonacci

En esta participación se propone hacer una comparativa entre un algoritmo recursivo que utiliza una estrategia de solución **divide y venceras** para encontrar el n-esimo numero en la secuencia de fibonacci, frente a otro algoritmo que utiliza la misma estrategia en adición de programación dinamica.

Durante el programa podemos observar como la inclusión de la programación dinamica mejora drasticamente los tiempos de ejecución del algoritmo, reduciendo su complejidad temporal de O(2^N) a O(N).

## 4.1. Ejecución
Para correr el codigo es necesesario utilizar memory profiler, por lo que la siguiente sentencia es clave para obtener los resultados:

    -mprof run -E --multiprocess --include-children --output mprof_fibonacci.dat --python python main.py

Cuando se cuente con el archivo *mprof_fibonacci.dat*, es necesario utilizar el siguiente comando en la terminal para observar la grafica con ayuda de matplotlib.
    
    -mprof plot mprof_fibonacci.dat -s -t "Fibonacci Complejidad Espacial"

*Utilice las sentencias en su terminal, en la ruta Participacion-Fibonacci/Codigo"*

### 4.1.1. Librerias
    matplotlib
    memory-profiler

