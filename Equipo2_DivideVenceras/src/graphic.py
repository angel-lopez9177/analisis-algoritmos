import lcs
import colors
import tkinter as tk
from tkinter import ttk, messagebox
import time
import tracemalloc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# --- NUEVAS IMPORTACIONES ---
import requests  # Para llamadas a la API de NCBI
import re        # Para procesar el formato FASTA

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("LCS — Comparador de Algoritmos")
        self.colors = colors.Colores.tk_light() # Usamos la nueva paleta de colores
        self.root.configure(bg=self.colors["bg"])

        # Estilo para los widgets de ttk
        self.setup_styles()

        # --- Nuevo Layout de Dos Columnas ---
        main_frame = ttk.Frame(root, style="App.TFrame")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=2) # Columna izquierda (controles) más ancha
        main_frame.grid_columnconfigure(1, weight=3) # Columna derecha (gráficas)
        main_frame.grid_rowconfigure(0, weight=1)

        # --- Panel Izquierdo (Controles y Animación) ---
        left_panel = ttk.Frame(main_frame, style="App.TFrame")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # --- NUEVO PANEL DE NCBI ---
        ncbi_frame = ttk.Frame(left_panel, style="App.TFrame")
        ncbi_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(ncbi_frame, text="Obtener de NCBI (Nucleotide DB):", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=4)
        
        ttk.Label(ncbi_frame, text="Acceso 1:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_acc1 = ttk.Entry(ncbi_frame, width=20, font=("Segoe UI", 10))
        self.entry_acc1.grid(row=1, column=1, padx=6, pady=4)
        # Ejemplo para el usuario
        self.entry_acc1.insert(0, "NM_000520.6") 
        
        ttk.Label(ncbi_frame, text="Acceso 2:").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_acc2 = ttk.Entry(ncbi_frame, width=20, font=("Segoe UI", 10))
        self.entry_acc2.grid(row=2, column=1, padx=6, pady=4)
        # Ejemplo para el usuario
        self.entry_acc2.insert(0, "NM_001126111.3")

        ttk.Button(ncbi_frame, text="Obtener Secuencias", command=self.on_fetch_ncbi).grid(row=1, column=2, rowspan=2, padx=10)
        
        # Separador
        ttk.Separator(left_panel, orient='horizontal').pack(fill='x', pady=10)
        
        # --- Contenedor de entradas (Original) ---
        inputs = ttk.Frame(left_panel, style="App.TFrame")
        inputs.pack(fill="x", pady=(0, 10))
        ttk.Label(inputs, text="Cadena 1:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_X = ttk.Entry(inputs, width=40, font=("Segoe UI", 10))
        self.entry_X.grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(inputs, text="Cadena 2:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_Y = ttk.Entry(inputs, width=40, font=("Segoe UI", 10))
        self.entry_Y.grid(row=1, column=1, padx=6, pady=4)

        # Opciones y botones
        controls = ttk.Frame(left_panel, style="App.TFrame")
        controls.pack(fill="x", pady=8)
        self.anim_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(controls, text="Animar tabla", variable=self.anim_var).pack(side="left")
        ttk.Button(controls, text="Calcular y Comparar", command=self.on_calcular).pack(side="left", padx=12)
        ttk.Button(controls, text="Limpiar", command=self.on_limpiar).pack(side="left")
        
        # Resultados de texto
        self.result_label = ttk.Label(left_panel, text="Resultados aparecerán aquí.", justify="left", anchor="w")
        self.result_label.pack(fill="x", pady=(10, 5))

        # Frame para la animación de la tabla
        self.animation_frame = ttk.Frame(left_panel, style="App.TFrame")
        self.animation_frame.pack(fill="both", expand=True, pady=(10,0))


        # --- Panel Derecho (Gráficas) ---
        self.right_panel = ttk.Frame(main_frame, style="App.TFrame")
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.anim_after_id = None

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(".", background=self.colors["bg"], foreground=self.colors["text"], font=("Segoe UI", 10))
        style.configure("App.TFrame", background=self.colors["bg"])
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["text"])
        style.configure("TButton", background=self.colors["accent2"], foreground="#FFFFFF", borderwidth=0)
        style.map("TButton", background=[("active", self.colors["highlight"])])
        style.configure("TCheckbutton", background=self.colors["bg"], indicatorcolor=self.colors["text"])
        style.map("TCheckbutton",
                    indicatorcolor=[('selected', self.colors["highlight"])])
        style.configure("TEntry", fieldbackground=self.colors["panel"], foreground=self.colors["text"], borderwidth=1, insertcolor=self.colors["text"])
        
    def on_limpiar(self):
        self.entry_X.delete(0, tk.END)
        self.entry_Y.delete(0, tk.END)
        # --- Limpiar también los campos de acceso ---
        self.entry_acc1.delete(0, tk.END)
        self.entry_acc2.delete(0, tk.END)
        
        self.result_label.config(text="Resultados aparecerán aquí.")
        for w in self.animation_frame.winfo_children():
            w.destroy()
        for w in self.right_panel.winfo_children():
            w.destroy()

    # --- NUEVA FUNCIÓN PARA OBTENER DATOS DE NCBI ---
    def fetch_ncbi_sequences(self, acc1_id, acc2_id):
        """
        Obtiene dos secuencias de la base de datos 'nucleotide' de NCBI usando EFetch.
        """
        try:
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            # db=nucleotide es para secuencias genéticas.
            # rettype=fasta y retmode=text nos da el formato más simple.
            params = {
                "db": "nucleotide",
                "id": f"{acc1_id},{acc2_id}",
                "rettype": "fasta",
                "retmode": "text"
            }
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status() # Lanza un error si la petición falla
            
            fasta_data = response.text
            
            # Procesamos la respuesta FASTA.
            # Dividimos el texto por el caracter '>', que inicia cada secuencia.
            sequences_data = [seq for seq in fasta_data.split('>') if seq.strip()]
            
            if len(sequences_data) < 2:
                messagebox.showerror("Error de API", f"Se esperaban 2 secuencias, pero NCBI retornó {len(sequences_data)}. Verifique los Números de Acceso.")
                return None, None
                
            # Extraemos la secuencia de cada entrada
            seqs_out = []
            for i in range(2): # Solo nos interesan las primeras 2
                # Separamos el encabezado (ej: >NM_000520.6 Homo sapiens...) del resto
                try:
                    parts = sequences_data[i].split('\n', 1)
                    # Unimos todas las líneas de la secuencia y eliminamos espacios/saltos
                    seq = re.sub(r'\s+', '', parts[1])
                    if not seq:
                        raise ValueError(f"El ID {acc1_id if i==0 else acc2_id} no retornó una secuencia.")
                    seqs_out.append(seq)
                except Exception as e:
                    messagebox.showerror("Error de Parseo", f"No se pudo procesar la secuencia {i+1}: {e}")
                    return None, None
                    
            return seqs_out[0], seqs_out[1]
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Red", f"No se pudo conectar a NCBI: {e}")
            return None, None
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")
            return None, None

    # --- NUEVA FUNCIÓN DE "CALLBACK" PARA EL BOTÓN NCBI ---
    def on_fetch_ncbi(self):
        acc1 = self.entry_acc1.get().strip()
        acc2 = self.entry_acc2.get().strip()
        
        if not acc1 or not acc2:
            messagebox.showerror("Entrada Vacía", "Por favor, ingrese ambos Números de Acceso de NCBI.")
            return
            
        seq1, seq2 = self.fetch_ncbi_sequences(acc1, acc2)
        
        if seq1 and seq2:
            # Si tuvimos éxito, poblamos los campos originales
            self.entry_X.delete(0, tk.END)
            self.entry_X.insert(0, seq1)
            self.entry_Y.delete(0, tk.END)
            self.entry_Y.insert(0, seq2)
            
            messagebox.showinfo("Éxito", "Secuencias obtenidas y cargadas en 'Cadena 1' y 'Cadena 2'.\nPresione 'Calcular y Comparar'.")

    # --- FUNCIÓN ORIGINAL (SIN CAMBIOS) ---
    def on_calcular(self):
        X = self.entry_X.get()
        Y = self.entry_Y.get()
        if not X or not Y:
            messagebox.showerror("Error", "Ingresa ambas cadenas.")
            return

        for w in self.animation_frame.winfo_children():
            w.destroy()
        for w in self.right_panel.winfo_children():
            w.destroy()
        
        # Advertencia de longitud: secuencias genéticas pueden ser MUY largas
        # El límite original de 12 es muy bajo, lo subiré a 20.
        # La versión recursiva fallará con casi cualquier secuencia real.
        if len(X) > 20 or len(Y) > 20:
            do_rec = messagebox.askyesno("Advertencia", "El cálculo recursivo es EXTREMADAMENTE lento para cadenas de más de ~15-20 caracteres y fallará.\n¿Deseas intentar ejecutarlo de todas formas?")
        else:
            do_rec = True

        # Ejecutar recursivo
        t_rec, peak_rec, lcs_rec = None, None, None
        result_text_parts = []
        if do_rec:
            tracemalloc.start()
            t0 = time.perf_counter()
            try:
                lcs_rec = lcs.lcs_recursivo(X, Y, len(X), len(Y))
                t_rec = time.perf_counter() - t0
                peak_rec = tracemalloc.get_traced_memory()[1] / 1024.0
                tracemalloc.stop()
                result_text_parts.append(f"• Recursivo: {lcs_rec} (len) | {t_rec:.5f}s | {peak_rec:.1f} KB")
            except Exception as e:
                tracemalloc.stop()
                result_text_parts.append(f"• Recursivo: Falló (Probablemente límite de recursión). {e}")
        else:
            result_text_parts.append("• Recursivo: Saltado por ser muy costoso.")

        # Ejecutar dinámico
        tracemalloc.start()
        t0 = time.perf_counter()
        L_full, lcs_len = lcs.lcs_dinamico_tabla(X, Y)
        t_dyn = time.perf_counter() - t0
        peak_dyn = tracemalloc.get_traced_memory()[1] / 1024.0
        tracemalloc.stop()
        result_text_parts.append(f"• Dinámico: {lcs_len} (len) | {t_dyn:.5f}s | {peak_dyn:.1f} KB")

        # Reconstruir subsecuencia
        lcs_string = lcs.reconstruir_lcs(L_full, X, Y)
        result_text_parts.append(f"↳ Subsecuencia: '{lcs_string}'")
        self.result_label.config(text="\n".join(result_text_parts))

        # Graficar
        self.plot_comparison(do_rec, t_rec, t_dyn, peak_rec, peak_dyn)

        # Animar
        if self.anim_var.get():
            # Advertencia para tablas muy grandes
            if len(X) > 50 or len(Y) > 50:
                 messagebox.showwarning("Animación Saltada", "La animación de la tabla se salta para cadenas de más de 50 caracteres para evitar problemas de rendimiento.")
            else:
                self.animate_table(X, Y)

    def plot_comparison(self, did_rec, t_rec, t_dyn, mem_rec, mem_dyn):
        fig = Figure(figsize=(6, 5), dpi=100)
        fig.patch.set_facecolor(self.colors["bg"])

        # Gráfica de Tiempo
        ax1 = fig.add_subplot(211)
        names = ['Dinámico']
        times = [t_dyn]
        if did_rec and t_rec is not None:
            names.insert(0, 'Recursivo')
            times.insert(0, t_rec)
        ax1.bar(names, times, color=[self.colors["accent2"], self.colors["highlight"]])
        ax1.set_title("Tiempo de Ejecución (s)", color=self.colors["text"])
        ax1.set_ylabel("Segundos", color=self.colors["text"])
        ax1.tick_params(axis='x', colors=self.colors["text"])
        ax1.tick_params(axis='y', colors=self.colors["text"])
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        # Gráfica de Memoria
        ax2 = fig.add_subplot(212)
        mems = [mem_dyn]
        if did_rec and mem_rec is not None:
            mems.insert(0, mem_rec)
        ax2.bar(names, mems, color=[self.colors["accent2"], self.colors["highlight"]])
        ax2.set_title("Uso Máximo de Memoria (KB)", color=self.colors["text"])
        ax2.set_ylabel("KB", color=self.colors["text"])
        ax2.tick_params(axis='x', colors=self.colors["text"])
        ax2.tick_params(axis='y', colors=self.colors["text"])
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.right_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def animate_table(self, X, Y):
        if self.anim_after_id:
            self.root.after_cancel(self.anim_after_id)
            self.anim_after_id = None
            
        # Limpiar frame anterior
        for w in self.animation_frame.winfo_children():
            w.destroy()

        m, n = len(X), len(Y)
        rows, cols = m + 1, n + 1
        
        labels = [[None] * cols for _ in range(rows)]
        
        # --- Añadir encabezados de cadenas ---
        # Encabezado X (vertical)
        for i, char in enumerate(X):
            lbl_h = tk.Label(self.animation_frame, text=char, width=4, height=2,
                             bg=self.colors["bg"], fg=self.colors["accent2"], font=("Consolas", 9, "bold"))
            lbl_h.grid(row=i+1, column=0, padx=1, pady=1)
        
        # Encabezado Y (horizontal)
        for j, char in enumerate(Y):
            lbl_v = tk.Label(self.animation_frame, text=char, width=4, height=2,
                             bg=self.colors["bg"], fg=self.colors["accent2"], font=("Consolas", 9, "bold"))
            lbl_v.grid(row=0, column=j+1, padx=1, pady=1)
        
        # --- Crear celdas de la tabla ---
        for i in range(rows):
            for j in range(cols):
                if i == 0 or j == 0: # Celdas de la fila/columna 0
                    text = "0"
                    if i == 0 and j == 0: text = " "
                    lbl = tk.Label(self.animation_frame, text=text, 
                                   width=4, height=2, relief="solid", borderwidth=1,
                                   bg=self.colors["panel_right"], fg=self.colors["text"],
                                   font=("Consolas", 9))
                else: # Celdas de cálculo
                    lbl = tk.Label(self.animation_frame, text=" ", 
                                   width=4, height=2, relief="solid", borderwidth=1,
                                   bg=self.colors["panel"], fg=self.colors["text"],
                                   font=("Consolas", 9))
                
                # Ubicar la celda (desplazada 1x1 si tenemos encabezados)
                lbl.grid(row=i, column=j, padx=1, pady=1)
                if i > 0 or j > 0: # No guardar las celdas de los encabezados de letras
                    labels[i][j] = lbl

        L = [[0] * (n + 1) for _ in range(m + 1)]
        delay = 80 # ms

        steps = [(i, j) for i in range(1, m + 1) for j in range(1, n + 1)]
        state = {"index": 0, "steps": steps, "L": L, "labels": labels, "X": X, "Y": Y}

        def step_animation():
            try:
                idx = state["index"]
                if idx >= len(state["steps"]):
                    self.anim_after_id = None
                    return

                i, j = state["steps"][idx]
                if X[i-1] == Y[j-1]:
                    L[i][j] = L[i-1][j-1] + 1
                    state["labels"][i][j].config(bg=self.colors["cell_match"])
                else:
                    L[i][j] = max(L[i-1][j], L[i][j-1])
                
                state["labels"][i][j].config(text=str(L[i][j]))
                state["index"] += 1
                self.anim_after_id = self.root.after(delay, step_animation)
            except tk.TclError:
                # La ventana fue cerrada o el widget destruido, detenemos la animación
                self.anim_after_id = None
                
        self.anim_after_id = self.root.after(100, step_animation)