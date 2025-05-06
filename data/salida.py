import numpy as np

try:
    from core.analisis import calcular_estructura
except ImportError:
    pass

def formatear_resultados(resultados):
    def convertir_float(val):
        if isinstance(val, dict):
            return {k: convertir_float(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [float(v) for v in val]
        elif isinstance(val, np.float64):
            return float(val)
        return val

    resultados_formateados = convertir_float(resultados)

    print("Desplazamientos:")
    for nodo, desplazamiento in resultados_formateados["desplazamientos"].items():
        dx = f"{desplazamiento[0]:.2f}"
        dy = f"{desplazamiento[1]:.2f}"
        print(f"  Nodo {nodo}: dx = {dx}, dy = {dy}")

    print("\nFuerzas Internas:")
    for barra, fuerza in resultados_formateados["fuerzas_internas"].items():
        print(f"  {barra}: {fuerza:.2f} N")

    print("\nReacciones:")
    for nodo, reaccion in resultados_formateados["reacciones"].items():
        fx = f"{reaccion[0]:.2f}"
        fy = f"{reaccion[1]:.2f}"
        print(f"  Nodo {nodo}: Fx = {fx}, Fy = {fy}")