# ui/app.py
import tkinter as tk
from .components import InputFrame, ResultFrame, DrawFrame
from core.analisis import calcular_estructura


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Análisis Matricial de Armaduras")
        self.geometry("900x600")

        self.input_frame = InputFrame(self, on_submit=self.realizar_analisis)
        self.input_frame.pack(side="left", fill="both", expand=True)

        self.draw_frame = DrawFrame(self)
        self.draw_frame.pack(side="right", fill="both", expand=True)

        self.result_frame = ResultFrame(self)
        self.result_frame.pack(side="bottom", fill="x")

    def realizar_analisis(self, datos):
        resultado = calcular_estructura(datos)
        self.result_frame.mostrar(resultado)
        self.draw_frame.dibujar(datos, resultado)