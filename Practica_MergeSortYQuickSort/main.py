from typing import List
import random

LIMITE_INFERIOR = 0
LIMITE_SUPERIOR = 99
CANTIDAD_ELEMENTOS = 100

def generarLista(lim_inf, lim_sup, len):
    return [random.randint(lim_inf, lim_sup) for _ in range(len)]

def quickSort(lista: List[int]):
    if len(lista) <= 1:
        return lista
    pivote = lista[0]
    menor = [x for x in lista if x < pivote]
    mayor = [x for x in lista if x > pivote]
    return quickSort(menor) + [pivote] + quickSort(mayor)

def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        mergeSort(left_half)
        mergeSort(right_half)
        
        merge(arr, left_half, right_half)
        
    return arr

def merge(arr, left_half, right_half):
    i = j = k = 0
    
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1
        
    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1
        
    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1

if __name__ == "__main__":
    lista_desordenada: List[int] = generarLista(LIMITE_INFERIOR, LIMITE_SUPERIOR, CANTIDAD_ELEMENTOS)
    print(f"Lista inicial: {lista_desordenada} \n")
    lista_quickSort = quickSort(lista_desordenada)
    print(f"Lista Quick Sort: {lista_quickSort} \n")
    lista_mergeSort = mergeSort(lista_desordenada)
    print(f"Lista Merge Sort: {lista_quickSort}")