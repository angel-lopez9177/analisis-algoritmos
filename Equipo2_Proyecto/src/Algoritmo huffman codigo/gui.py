import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import os
import textwrap

try:
    from book_reader import get_book_values
    from binary_tree import BinaryTree, TreeNode
    from huffman_encoding import (
        create_huffman_tree,
        encode_text_to_bit_string,
        write_binary_file,
        read_binary_file,
        decode_bits_to_text
    )
except ImportError as e:
    print(f"Error: No se pudieron importar los módulos necesarios: {e}")
    print("Asegúrate de que gui.py esté en la misma carpeta que tus otros archivos .py")
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error de Importación", f"No se pudieron importar los módulos: {e}\n\nAsegúrate de que gui.py esté en la misma carpeta que los otros archivos .py.")
    except tk.TclError:
        pass
    exit()



class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresor Huffman")
        self.root.geometry("850x650")
        self.root.minsize(600, 400)

        self.selected_file_path = None

        top_frame = tk.Frame(root, pady=10, padx=10)
        top_frame.pack(fill='x')

        self.select_button = tk.Button(top_frame, text="1. Seleccionar Archivo .txt", command=self.select_file)
        self.select_button.pack(side=tk.LEFT, padx=(0, 10))

        self.compress_button = tk.Button(top_frame, text="2. Comprimir y Analizar", command=self.run_compression, state=tk.DISABLED)
        self.compress_button.pack(side=tk.LEFT)

        self.file_label = tk.Label(top_frame, text="Archivo: (Ninguno seleccionado)", anchor='w')
        self.file_label.pack(side=tk.LEFT, fill='x', expand=True, padx=10)

        main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=8)
        main_pane.pack(expand=True, fill='both', pady=5, padx=10)

        left_pane = tk.PanedWindow(main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=8)
        main_pane.add(left_pane, minsize=300)

        codes_frame = ttk.Labelframe(left_pane, text="Diccionario de Códigos Huffman")
        codes_frame.pack(expand=True, fill='both')
        self.codes_text = scrolledtext.ScrolledText(codes_frame, height=15, width=40, wrap=tk.NONE, font=("Courier New", 10))
        self.codes_text.pack(expand=True, fill='both', padx=5, pady=5)
        left_pane.add(codes_frame)

        sizes_frame = ttk.Labelframe(left_pane, text="Análisis de Tamaño")
        sizes_frame.pack(expand=True, fill='both')
        self.sizes_text = scrolledtext.ScrolledText(sizes_frame, height=10, width=40, wrap=tk.WORD, font=("Arial", 10))
        self.sizes_text.pack(expand=True, fill='both', padx=5, pady=5)
        left_pane.add(sizes_frame)

        huff_frame = ttk.Labelframe(main_pane, text="Vista Previa del Archivo .huff (Hexadecimal)")
        huff_frame.pack(expand=True, fill='both')
        self.huff_text = scrolledtext.ScrolledText(huff_frame, height=25, width=50, wrap=tk.WORD, font=("Courier New", 10))
        self.huff_text.pack(expand=True, fill='both', padx=5, pady=5)
        main_pane.add(huff_frame, minsize=300)

        self.clear_results()


    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if filepath:
            self.selected_file_path = filepath
            self.file_label.config(text=f"Archivo: {os.path.basename(filepath)}")
            self.compress_button.config(state=tk.NORMAL)
            self.clear_results()

    def clear_results(self):
        self.codes_text.config(state=tk.NORMAL)
        self.sizes_text.config(state=tk.NORMAL)
        self.huff_text.config(state=tk.NORMAL)
        self.codes_text.delete(1.0, tk.END)
        self.sizes_text.delete(1.0, tk.END)
        self.huff_text.delete(1.0, tk.END)
        self.codes_text.config(state=tk.DISABLED)
        self.sizes_text.config(state=tk.DISABLED)
        self.huff_text.config(state=tk.DISABLED)

    def run_compression(self):
        if not self.selected_file_path:
            messagebox.showerror("Error", "Por favor, selecciona un archivo primero.")
            return
        
        self.compress_button.config(state=tk.DISABLED)
        self.select_button.config(state=tk.DISABLED)
        self.root.update_idletasks()

        try:
            results = self.process_huffman(self.selected_file_path)
            
            self.populate_results(results)
            if results['verified']:
                messagebox.showinfo("Éxito", "¡Compresión y decodificación completadas!\nEl archivo original y el decodificado coinciden.")
            else:
                messagebox.showwarning("Advertencia", "¡Error!\nEl archivo original y el decodificado NO coinciden.")

        except Exception as e:
            messagebox.showerror("Error en el Proceso", f"Ocurrió un error: {e}")
        
        finally:
            self.compress_button.config(state=tk.NORMAL)
            self.select_button.config(state=tk.NORMAL)

    def populate_results(self, results):
        self.codes_text.config(state=tk.NORMAL)
        self.codes_text.delete(1.0, tk.END)
        for char, code in sorted(results['codes'].items()):
            if char == ' ': display_char = "' ' (espacio)"
            elif char == '\n': display_char = "'\\n' (salto)"
            else: display_char = f"'{char}'"
            self.codes_text.insert(tk.END, f"{display_char:<15} : {code}\n")
        self.codes_text.config(state=tk.DISABLED)

        self.sizes_text.config(state=tk.NORMAL)
        self.sizes_text.delete(1.0, tk.END)
        self.sizes_text.insert(tk.END, f"Archivo Original (.txt):\n")
        self.sizes_text.insert(tk.END, f"  Ruta: {results['original_name']}\n")
        self.sizes_text.insert(tk.END, f"  Tamaño: {results['original_size']:,} bytes\n\n")
        
        self.sizes_text.insert(tk.END, f"Archivo Comprimido (.huff):\n")
        self.sizes_text.insert(tk.END, f"  Ruta: {results['huff_name']}\n")
        self.sizes_text.insert(tk.END, f"  Tamaño: {results['huff_size']:,} bytes\n\n")

        self.sizes_text.insert(tk.END, f"Archivo Decodificado (.txt):\n")
        self.sizes_text.insert(tk.END, f"  Ruta: {results['decoded_name']}\n")
        self.sizes_text.insert(tk.END, f"  Tamaño: {results['decoded_size']:,} bytes\n\n")

        if results['original_size'] > 0 and results['huff_size'] > 0:
            reduction = (1 - (results['huff_size'] / results['original_size'])) * 100
            self.sizes_text.insert(tk.END, f"--- RESULTADO ---\n")
            self.sizes_text.insert(tk.END, f"Reducción: {reduction:.2f}%\n")
            self.sizes_text.insert(tk.END, f"Ratio Compresión: {results['original_size'] / results['huff_size']:.2f} a 1\n")
        elif results['original_size'] > 0:
             self.sizes_text.insert(tk.END, f"--- RESULTADO ---\nReducción: 0.00%\n")
        self.sizes_text.config(state=tk.DISABLED)

        self.huff_text.config(state=tk.NORMAL)
        self.huff_text.delete(1.0, tk.END)
        self.huff_text.insert(tk.END, f"Mostrando primeros 512 bytes de '{results['huff_name']}':\n\n")
        self.huff_text.insert(tk.END, results['huff_content_hex'])
        self.huff_text.config(state=tk.DISABLED)

    def process_huffman(self, book_name):
        huff_filename = "encoded_text.huff"
        decoded_filename = "decoded_book.txt"

        values_list = get_book_values(book_name)
        if not values_list:
            raise ValueError(f"El archivo '{os.path.basename(book_name)}' está vacío o no se pudo leer.")
            
        huffman_tree = create_huffman_tree(values_list)
        codes = huffman_tree.get_huffman_codes() 

        try:
            with open(book_name, 'r', encoding='utf-8') as f:
                original_text = f.read()
        except Exception as e:
            raise IOError(f"Error leyendo el archivo original '{book_name}': {e}")

        bit_string = encode_text_to_bit_string(original_text, codes)
        write_binary_file(bit_string, huff_filename)
        
        bit_string_from_file = read_binary_file(huff_filename)
        if bit_string_from_file is None:
            raise IOError(f"No se pudo leer el archivo .huff generado ('{huff_filename}')")
            
        decoded_text = decode_bits_to_text(bit_string_from_file, huffman_tree.root)

        try:
            with open(decoded_filename, "w", encoding='utf-8') as f:
                f.write(decoded_text)
        except IOError as e:
            raise IOError(f"Error escribiendo archivo decodificado '{decoded_filename}': {e}")
        
        original_size = os.path.getsize(book_name)
        huff_size = os.path.getsize(huff_filename)
        decoded_size = os.path.getsize(decoded_filename)
        huff_content_hex = ""
        try:
            with open(huff_filename, "rb") as f:
                data = f.read(512)
                lines = []
                for i in range(0, len(data), 16):
                    data_chunk = data[i:i+16]
                    hex_line = " ".join(f"{b:02x}" for b in data_chunk)
                    lines.append(hex_line)
                
                huff_content_hex = "\n".join(lines)
                
        except Exception as e:
            huff_content_hex = f"Error al leer .huff: {e}"
            
        verified = (decoded_text == original_text)

        return {
            "codes": codes,
            "original_name": os.path.basename(book_name),
            "original_size": original_size,
            "huff_name": huff_filename,
            "huff_size": huff_size,
            "decoded_name": decoded_filename,
            "decoded_size": decoded_size,
            "huff_content_hex": huff_content_hex,
            "verified": verified
        }


def run_gui():
    try:
        root = tk.Tk()
        app = HuffmanGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Error fatal al iniciar la GUI: {e}")
        input("Presiona Enter para salir...")