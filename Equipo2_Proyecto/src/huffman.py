import heapq
from collections import Counter, defaultdict

def build_shared_huffman_map(text1, text2):
    # 1. Análisis de frecuencia global (ambos textos juntos)
    combined_text = text1 + text2
    frequency = Counter(combined_text)
    
    # 2. Crear heap inicial [peso, [simbolo, ""]]
    heap = [[weight, [sym, ""]] for sym, weight in frequency.items()]
    heapq.heapify(heap)
    
    # 3. Construir el árbol
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1] # Lado izquierdo
        for pair in hi[1:]:
            pair[1] = '1' + pair[1] # Lado derecho
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    # 4. Extraer el mapa {caracter: codigo_binario}
    huff_map = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    return {sym: code for sym, code in huff_map}

def encode_text(text, huff_map):
    return [huff_map[char] for char in text]

def decode_tokens(token_list, huff_map):
    # Invertir el mapa: {codigo: caracter}
    reverse_map = {v: k for k, v in huff_map.items()}
    return "".join([reverse_map[token] for token in token_list])