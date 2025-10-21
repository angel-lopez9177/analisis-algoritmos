import lcs
import colors
import tkinter as tk
from tkinter import ttk, messagebox
import time
import tracemalloc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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

        # Contenedor de entradas
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

        # Frame para la animación de la tabla (ahora en la ventana principal)
        self.animation_frame = ttk.Frame(left_panel, style="App.TFrame")
        self.animation_frame.pack(fill="both", expand=True, pady=(10,0))


        # --- Panel Derecho (Gráficas) ---
        self.right_panel = ttk.Frame(main_frame, style="App.TFrame")
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.anim_after_id = None

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        # Estilo general
        style.configure(".", background=self.colors["bg"], foreground=self.colors["text"], font=("Segoe UI", 10))
        # Frame
        style.configure("App.TFrame", background=self.colors["bg"])
        # Labels
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["text"])
        # Botones
        style.configure("TButton", background=self.colors["accent2"], foreground="#FFFFFF", borderwidth=0)
        style.map("TButton", background=[("active", self.colors["highlight"])])
        # Checkbutton
        style.configure("TCheckbutton", background=self.colors["bg"], indicatorcolor=self.colors["text"])
        style.map("TCheckbutton",
                    indicatorcolor=[('selected', self.colors["highlight"])])
        # Entry
        style.configure("TEntry", fieldbackground=self.colors["panel"], foreground=self.colors["text"], borderwidth=1, insertcolor=self.colors["text"])
        
    def on_limpiar(self):
        self.entry_X.delete(0, tk.END)
        self.entry_Y.delete(0, tk.END)
        self.result_label.config(text="Resultados aparecerán aquí.")
        # Limpiar frames de animación y gráficas
        for w in self.animation_frame.winfo_children():
            w.destroy()
        for w in self.right_panel.winfo_children():
            w.destroy()

    def on_calcular(self):
        X = self.entry_X.get()
        Y = self.entry_Y.get()
        if not X or not Y:
            messagebox.showerror("Error", "Ingresa ambas cadenas.")
            return

        # Limpiar animación y gráficas previas
        for w in self.animation_frame.winfo_children():
            w.destroy()
        for w in self.right_panel.winfo_children():
            w.destroy()

        if len(X) > 12 or len(Y) > 12:
            do_rec = messagebox.askyesno("Advertencia", "El cálculo recursivo puede ser muy lento para cadenas largas. ¿Deseas ejecutarlo de todas formas?")
        else:
            do_rec = True

        # Ejecutar recursivo
        t_rec, peak_rec, lcs_rec = None, None, None
        result_text_parts = []
        if do_rec:
            tracemalloc.start()
            t0 = time.perf_counter()
            lcs_rec = lcs.lcs_recursivo(X, Y, len(X), len(Y))
            t_rec = time.perf_counter() - t0
            peak_rec = tracemalloc.get_traced_memory()[1] / 1024.0
            tracemalloc.stop()
            result_text_parts.append(f"• Recursivo: {lcs_rec} (len) | {t_rec:.5f}s | {peak_rec:.1f} KB")
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
            self.animate_table(X, Y)

    def plot_comparison(self, did_rec, t_rec, t_dyn, mem_rec, mem_dyn):
        fig = Figure(figsize=(6, 5), dpi=100)
        fig.patch.set_facecolor(self.colors["bg"])

        # Gráfica de Tiempo
        ax1 = fig.add_subplot(211)
        names = ['Dinámico']
        times = [t_dyn]
        if did_rec:
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
        if did_rec:
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

        m, n = len(X), len(Y)
        rows, cols = m + 1, n + 1
        
        # Crear widgets en el frame de animación
        labels = [[None] * cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                lbl = tk.Label(self.animation_frame, text=" " if i > 0 and j > 0 else "", 
                               width=4, height=2, relief="solid", borderwidth=1,
                               bg=self.colors["panel"], fg=self.colors["text"],
                               font=("Consolas", 9))
                lbl.grid(row=i, column=j, padx=1, pady=1)
                labels[i][j] = lbl
        
        L = [[0] * (n + 1) for _ in range(m + 1)]
        delay = 80 # ms

        steps = [(i, j) for i in range(1, m + 1) for j in range(1, n + 1)]
        state = {"index": 0, "steps": steps, "L": L, "labels": labels, "X": X, "Y": Y}

        def step_animation():
            idx = state["index"]
            if idx >= len(state["steps"]):
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

        self.anim_after_id = self.root.after(100, step_animation)