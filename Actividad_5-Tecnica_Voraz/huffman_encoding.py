from book_reader import get_book_values
from binary_tree import BinaryTree, TreeNode
import priority_queue

def encode_text_to_bit_string(text, codes):
    encoded_parts = []
    for char in text:
        encoded_parts.append(codes[char])
    return "".join(encoded_parts)

def write_binary_file(bit_string, filename):
    padding_needed = (8 - (len(bit_string) % 8)) % 8
    padded_bit_string = bit_string + ("0" * padding_needed)
    
    b_array = bytearray([padding_needed])
    
    for i in range(0, len(padded_bit_string), 8):
        byte_chunk = padded_bit_string[i:i+8]
        int_value = int(byte_chunk, 2)
        b_array.append(int_value)
        
    try:
        with open(filename, "wb") as f:
            f.write(b_array)
    except IOError as e:
        print(f"Error escribiendo archivo binario '{filename}': {e}")


def read_binary_file(filename):
    print(f"Leyendo archivo binario de '{filename}'...")
    try:
        with open(filename, "rb") as f:
            binary_data = f.read()
    except IOError as e:
        print(f"Error leyendo archivo binario '{filename}': {e}")
        return None
        
    if not binary_data:
        print("Error: El archivo binario está vacío.")
        return None
        
    padding_to_remove = binary_data[0]
    data_bytes = binary_data[1:]
    
    bit_parts = []
    for byte_val in data_bytes:
        bit_parts.append(f'{byte_val:08b}')
        
    full_bit_string = "".join(bit_parts)
    
    if padding_to_remove > 0:
        final_bit_string = full_bit_string[:-padding_to_remove]
    else:
        final_bit_string = full_bit_string

    return final_bit_string

def decode_bits_to_text(encoded_data, tree_root):
    if tree_root is None:
        return ""

    if tree_root.left is None and tree_root.right is None:
        if tree_root.value is not None:
            return tree_root.value * len(encoded_data)
        else:
            return ""

    decoded_parts = []
    current_node = tree_root

    for bit in encoded_data:
        if bit == '0':
            current_node = current_node.left
        elif bit == '1':
            current_node = current_node.right
        
        if current_node and current_node.value is not None:
            decoded_parts.append(current_node.value)
            current_node = tree_root
    
    return "".join(decoded_parts)

def create_huffman_tree(values):
    queue = []
    for char, frecuency in values:
        queue.append(TreeNode(char, frecuency))

    while len(queue) > 1:
        aux_value_1 = priority_queue.delete(queue)
        aux_value_2 = priority_queue.delete(queue)
        
        parent_node = TreeNode(None, aux_value_1.frecuency + aux_value_2.frecuency)
        parent_node.left = aux_value_1
        parent_node.right = aux_value_2
        
        queue.append(parent_node)

    huffman_tree = BinaryTree()
    if queue: 
        huffman_tree.root = queue[0]

    return huffman_tree

def run_huffman_algorithm(book_name):
    huff_filename = "encoded_text.huff"
    decoded_filename = "decoded_book.txt"
    
    values_list = get_book_values(book_name)
    huffman_tree = create_huffman_tree(values_list)
    
    print("Códigos de Huffman generados:")
    codes = huffman_tree.get_huffman_codes()
    for char, code in sorted(codes.items()):
        if char == ' ': print(f"  - ' ' (espacio): {code}")
        elif char == '\n': print(f"  - '\\n' (salto): {code}")
        else: print(f"  - '{char}': {code}")
    print("-" * 30) 


    try:
        with open(book_name, 'r') as f:
            original_text = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {book_name}")
        return

    bit_string = encode_text_to_bit_string(original_text, codes)
    
    write_binary_file(bit_string, huff_filename)
    print("-" * 30) 

    original_bits = len(original_text) * 8
    compressed_bits = len(bit_string)
    
    print("Resultados de la Compresión (basado en bits):")
    print(f"  - Tamaño original: {original_bits} bits ({original_bits / 8:.0f} bytes)")
    print(f"  - Tamaño comprimido: {compressed_bits} bits ({compressed_bits / 8:.2f} bytes)")
    
    if original_bits > 0:
        reduction = (1 - (compressed_bits / original_bits)) * 100
        print(f"  - Reducción: {reduction:.2f}%")
    print("-" * 30)

    print("Proceso de Decodificación:")
    bit_string_from_file = read_binary_file(huff_filename)
    
    if bit_string_from_file is None:
        print("Fallo en la decodificación.")
        return
        
    decoded_text = decode_bits_to_text(bit_string_from_file, huffman_tree.root)
    try:
        with open(decoded_filename, "w") as f:
            f.write(decoded_text)
        print(f"Texto decodificado guardado en '{decoded_filename}'")
    except IOError as e:
        print(f"Error escribiendo archivo decodificado: {e}")
        
    print("-" * 30)
    print("✅ Verificación:")
    if decoded_text == original_text:
        print("¡Éxito! El texto decodificado es idéntico al original.")
    else:
        print("¡Error! El texto decodificado NO coincide con el original.")
    print("-" * 30)
