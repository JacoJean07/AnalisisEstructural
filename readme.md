# 🧱 Análisis Estructural con Métodos Matriciales 🧮

*Proyecto de análisis matricial de estructuras usando Python*

---

## 📌 Descripción del Proyecto

Este es un programa en **Python** que realiza el **análisis matricial de armaduras planas** utilizando el **método de la rigidez**. Permite al usuario:

- Ingresar datos de nodos, elementos, cargas y restricciones.
- Visualizar la estructura ingresada.
- Calcular desplazamientos, fuerzas internas y reacciones.

🎯 Ideal para estudiantes y profesionales de ingeniería civil y mecánica.

---

## 🛠️ Tecnologías Usadas

- 🐍 **Python 3.10+**
- 🖥️ **Tkinter** – Para la interfaz gráfica
- 📊 **NumPy** – Para cálculos matriciales
- 🎨 **Matplotlib / Canvas** – Para dibujar la estructura

---

## 📦 Requerimientos

Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes paquetes:

```bash
numpy
matplotlib
```

Puedes instalarlos usando el gestor de paquetes de tu sistema operativo o utilizando el siguiente comando en la terminal:

```bash
pip install numpy matplotlib
```

---

## 💻 Ejecución

Para ejecutar el proyecto, sigue estos pasos:

1. Clona este repositorio en tu computadora.

```bash
git clone https://github.com/jaco-mancuso/AnalisisEstructural.git
```

2. Entra en la carpeta del proyecto.

```bash
cd AnalisisEstructural
```

3. Ejecuta el archivo `main.py` con Python.

```bash
python main.py
```

4. El programa se ejecutará automáticamente y se abrirá una ventana gráfica con el menú principal.

5. Ejemplos de entrada:

    - Nodos, elementos, cargas y restricciones:

```json
{
    "nodos": {
        "1": [0, 0],
        "2": [2, 0],
        "3": [4, 0],
        "4": [6, 0],
        "5": [8, 0]
    },
    "elementos": [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5]
    ],
    "cargas": {
        "1": [0, 0]
    },
    "restricciones": {
        "1": [0, 0]
    }
}
```

    - Armadura de techo simple (5 nodos, 7 barras)

```json

{
    "nodos": {
        "1": [0, 0],
        "2": [2, 0],
        "3": [4, 0],
        "4": [1, 1],
        "5": [3, 1]
    },
    "elementos": [
        [1, 4], [4, 2], [2, 5], [5, 3],
        [4, 5], [1, 2], [2, 3]
    ],
    "cargas": {
        "4": [0, -5000],
        "5": [0, -5000]
    },
    "restricciones": {
        "1": [1, 1],
        "3": [0, 1]
    }
}
```

---

## 📝 Licencia

Este proyecto está licenciado bajo la licencia MIT. Puedes encontrar más información sobre la licencia en el archivo `LICENSE`.

---

## 📝 Créditos

Este proyecto ha sido desarrollado por **JacoJean07**.