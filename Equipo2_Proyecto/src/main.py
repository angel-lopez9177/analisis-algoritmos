import graphic 
import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("default")
    app = graphic.App(root)
    root.mainloop()