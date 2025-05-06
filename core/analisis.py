# core/analisis.py
import numpy as np


def calcular_estructura(datos):
    """
    Realiza el análisis matricial de una armadura plana.
    Entrada: diccionario con nodos, elementos, cargas, restricciones.
    Salida: desplazamientos, fuerzas internas y reacciones.
    """
    nodos = datos["nodos"]           # {id: [x, y]}
    elementos = datos["elementos"]   # [[nodo_i, nodo_j]]
    cargas = datos.get("cargas", {})     # {nodo: [Fx, Fy]}
    restricciones = datos.get("restricciones", {})  # {nodo: [ux_fijo, uy_fijo]}

    num_nodos = len(nodos)
    num_gdl = 2 * num_nodos

    K_global = np.zeros((num_gdl, num_gdl))
    F_global = np.zeros(num_gdl)

    # === Cargar fuerzas ===
    for nodo, (fx, fy) in cargas.items():
        idx = int(nodo)
        F_global[2*(idx-1)] += fx
        F_global[2*(idx-1)+1] += fy

    # === Ensamblaje de la matriz global ===
    for elem_id, (i, j) in enumerate(elementos, start=1):
        i = int(i)
        j = int(j)

        # Coordenadas de los nodos
        xi, yi = nodos[str(i)]
        xj, yj = nodos[str(j)]
        dx = xj - xi
        dy = yj - yi
        L = np.hypot(dx, dy)
        c = dx / L
        s = dy / L

        # Propiedades del material (ajustables)
        A = 0.01      # Área
        E = 200e9     # Módulo de Young

        # Matriz local
        k_local = (A * E / L) * np.array([
            [ c*c,  c*s, -c*c, -c*s ],
            [ c*s,  s*s, -s*s, -s*s ],
            [-c*c, -c*s,  c*c,  c*s ],
            [-c*s, -s*s,  c*s,  s*s ]
        ])

        # Mapeo de GDL
        gdl = [
            2*(i-1),     # ux
            2*(i-1)+1,   # uy
            2*(j-1),     # vx
            2*(j-1)+1    # vy
        ]

        # Ensamblar
        for r in range(4):
            for s in range(4):
                K_global[gdl[r], gdl[s]] += k_local[r, s]

    # === Aplicar condiciones de frontera ===
    fixed_dofs = []
    for nodo, (ux_fijo, uy_fijo) in restricciones.items():
        idx = int(nodo)
        if ux_fijo:
            fixed_dofs.append(2*(idx-1))
        if uy_fijo:
            fixed_dofs.append(2*(idx-1)+1)

    all_dofs = list(range(num_gdl))
    free_dofs = [dof for dof in all_dofs if dof not in fixed_dofs]

    # Reducir matrices
    K_red = K_global[np.ix_(free_dofs, free_dofs)]
    F_red = F_global[free_dofs]

    # Resolver sistema
    try:
        U_red = np.linalg.solve(K_red, F_red)
    except np.linalg.LinAlgError:
        return {"error": "Sistema singular (estructura inestable o mal definida)"}

    # Reconstruir desplazamientos globales
    U_global = np.zeros(num_gdl)
    for i, dof in enumerate(free_dofs):
        U_global[dof] = U_red[i]

    # Calcular reacciones
    Reacciones = K_global[:, fixed_dofs].dot(U_global[fixed_dofs])

    # Calcular fuerzas internas
    fuerzas = {}
    for elem_id, (i, j) in enumerate(elementos, start=1):
        i = int(i)
        j = int(j)

        xi, yi = nodos[str(i)]
        xj, yj = nodos[str(j)]
        dx = xj - xi
        dy = yj - yi
        L = np.hypot(dx, dy)
        c = dx / L
        s = dy / L

        # Desplazamientos globales
        u_i = U_global[2*(i-1)]
        v_i = U_global[2*(i-1)+1]
        u_j = U_global[2*(j-1)]
        v_j = U_global[2*(j-1)+1]

        # Fuerza axial
        q = (c * (u_j - u_i) + s * (v_j - v_i)) * (200e9 * 0.01) / L
        fuerzas[f"Barra {elem_id}"] = q

    # Formatear desplazamientos
    desplazamientos = {
        str(i+1): [U_global[2*i], U_global[2*i+1]]
        for i in range(num_nodos)
    }

    # Formatear reacciones
    reacciones = {
        str(i+1): [Reacciones[2*i], Reacciones[2*i+1]]
        for i in range(num_nodos) if 2*i in fixed_dofs or 2*i+1 in fixed_dofs
    }

    # Formatear fuerzas internas
    fuerzas = {
        f"Barra {elem_id}": fuerza
        for elem_id, fuerza in fuerzas.items()
    }

    # Verificar que las variables son diccionarios
    if not isinstance(desplazamientos, dict):
        raise TypeError("La variable 'desplazamientos' no es un diccionario.")
    if not isinstance(reacciones, dict):
        raise TypeError("La variable 'reacciones' no es un diccionario.")
    if not isinstance(fuerzas, dict):
        raise TypeError("La variable 'fuerzas' no es un diccionario.")

    # Construir el formato de salida
    resultado_formateado = []

    # Desplazamientos
    resultado_formateado.append("Desplazamientos:")
    for nodo, desplazamiento in desplazamientos.items():
        dx = f"{desplazamiento[0]:.2f}"
        dy = f"{desplazamiento[1]:.2f}"
        resultado_formateado.append(f"  Nodo {nodo}: dx = {dx}, dy = {dy}")

    # Fuerzas internas
    resultado_formateado.append("\nFuerzas Internas:")
    for barra, fuerza in fuerzas.items():
        resultado_formateado.append(f"  {barra}: {fuerza:.2f} N")

    # Reacciones
    resultado_formateado.append("\nReacciones:")
    for nodo, reaccion in reacciones.items():
        fx = f"{reaccion[0]:.2f}"
        fy = f"{reaccion[1]:.2f}"
        resultado_formateado.append(f"  Nodo {nodo}: Fx = {fx}, Fy = {fy}")

    # Unir el resultado en una sola cadena
    return "\n".join(resultado_formateado)