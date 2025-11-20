class TreeNode:
    def __init__(self, value, frecuency):
        self.value = value
        self.frecuency = frecuency
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None
        
    def print_in_order(self):
        if self.root is not None:
            self._print_recursively(self.root)
        else:
            print("El árbol está vacío.")
        print()

    def _print_recursively(self, node):
        if node is not None:
            self._print_recursively(node.left)
            print(end=f"({node.value}, {node.frecuency}) ")
            self._print_recursively(node.right)
            
    def get_huffman_codes(self):
        """
        Función pública para iniciar la generación de códigos.
        Devuelve un diccionario. Ej: {'a': '01', 'b': '101'}
        """
        codes = {}
        if self.root is None:
            return codes
        
        self._generate_codes_recursively(self.root, "", codes)
        return codes

    def _generate_codes_recursively(self, node, current_code, codes_dict):
        """
        Función privada recursiva para recorrer el árbol.
        """
        if node is None:
            return

        # Si es un nodo hoja (tiene un caracter, no es un nodo interno)
        if node.value is not None:
            # Caso especial: si el árbol solo tiene un nodo (ej. texto "aaaa")
            if current_code == "":
                codes_dict[node.value] = "0"
            else:
                codes_dict[node.value] = current_code
        
        # Si es un nodo interno, seguimos bajando
        else:
            # 0 para la izquierda
            self._generate_codes_recursively(node.left, current_code + "0", codes_dict)
            # 1 para la derecha
            self._generate_codes_recursively(node.right, current_code + "1", codes_dict)