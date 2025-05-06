# ui/components.py
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


class InputFrame(tk.Frame):
    def __init__(self, parent, on_submit):
        super().__init__(parent)
        self.on_submit = on_submit

        tk.Label(self, text="Datos de entrada (JSON):").pack()
        self.text_area = tk.Text(self, height=20, width=40)
        self.text_area.pack()

        self.btn = tk.Button(self, text="Calcular", command=self.enviar_datos)
        self.btn.pack()

    def enviar_datos(self):
        try:
            import json
            texto = self.text_area.get("1.0", "end-1c")
            datos = json.loads(texto)  # Cambiar literal_eval por json.loads
            self.on_submit(datos)
        except json.JSONDecodeError as e:
            print("Error en formato JSON:", e)
            tk.messagebox.showerror("Error", f"Formato de entrada inválido:\n{e}")
        except Exception as e:
            print("Error inesperado:", e)
            tk.messagebox.showerror("Error", f"Error inesperado:\n{e}")

class ResultFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = tk.Label(self, text="Resultados:")
        self.label.pack()
        self.text_area = tk.Text(self, height=10, width=50)
        self.text_area.pack()

    def mostrar(self, resultados):
        self.text_area.delete(1.0, tk.END)
        if isinstance(resultados, dict):  # Verifica si es un diccionario
            for k, v in resultados.items():
                self.text_area.insert(tk.END, f"{k}: {v}\n")
        elif isinstance(resultados, str):  # Si es una cadena, simplemente la muestra
            self.text_area.insert(tk.END, resultados)
        else:
            self.text_area.insert(tk.END, "Error: Formato de resultados no reconocido.")


class DrawFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()

    def dibujar(self, datos, resultados):
        self.canvas.delete("all")
        nodos = datos["nodos"]
        elementos = datos["elementos"]

        escala = 50  # Escala para visualización

        for i, j in elementos:
            x1, y1 = nodos[str(i)]
            x2, y2 = nodos[str(j)]

            # Dibujar barra
            self.canvas.create_line(
                x1 * escala, -y1 * escala + 400,
                x2 * escala, -y2 * escala + 400,
                width=2, fill="black"
            )

        # Mostrar desplazamientos si existen
        if "desplazamientos" in resultados:
            desplazamientos = resultados["desplazamientos"]
            for nodo, (dx, dy) in desplazamientos.items():
                x, y = nodos[str(nodo)]
                self.canvas.create_oval(
                    (x + dx) * escala - 3, (-y - dy) * escala + 400 - 3,
                    (x + dx) * escala + 3, (-y - dy) * escala + 400 + 3,
                    fill="red"
                )