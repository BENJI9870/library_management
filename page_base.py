import tkinter as tk
from Admin import *
from tkinter import ttk
import sv_ttk

class PageBase:
    def __init__(self, root, config):
        self.root = root
        self.config = config
    def show_new_page(self, txt):
        for widget in self.root.winfo_children():
            widget.destroy()
        if txt != "":
            ttk.Label(self.root, text=txt, font=('Courier',24)).pack()
        self.root.geometry("1000x700")
        self.root.title("Benji's Library")
        sv_ttk.set_theme("dark")