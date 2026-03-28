"""
main.py
=======
Interfaz de línea de comandos del sistema inteligente de rutas.

Uso:
    python main.py

Requisitos:
    Python 3.10 o superior.
    No requiere librerías externas (solo módulos de la stdlib).
"""

from base_conocimiento import ESTACIONES, hecho_estacion, consultar_costo
from busqueda import a_estrella

# ── Constantes de presentación ─────────────────────────────────────────────
LINEA = "─" * 58
TITULO = "  SISTEMA INTELIGENTE DE RUTAS — TRANSPORTE MASIVO"
SUBTITULO = "       Algoritmo A* | Búsqueda Informada Heurística"


def mostrar_encabezado() -> None:
    print()
    print("=" * 58)
    print(TITULO)
    print(SUBTITULO)
    print("=" * 58)


def mostrar_estaciones() -> None:
    """Muestra la tabla de estaciones disponibles agrupadas por línea."""
    lineas: dict[str, list[tuple[str, str]]] = {}
    for id_e, datos in ESTACIONES.items():
        linea = datos["linea"]
        lineas.setdefault(linea, []).append((id_e, datos["nombre"]))

    print()
    print("ESTACIONES DISPONIBLES:")
    print(LINEA)
    for linea in sorted(lineas):
        print(f"  [{linea}]")
        for id_e, nombre in lineas[linea]:
            print(f"    {id_e:<22} {nombre}")
    print(LINEA)


def mostrar_resultado(camino: list[str] | None, costo_total: float) -> None:
    """Muestra la ruta óptima con el tiempo parcial entre cada par de estaciones."""
    if camino is None:
        print()
        print("  [!] No existe ruta entre las estaciones seleccionadas.")
        print(LINEA)
        return

    origen_nombre  = ESTACIONES[camino[0]]["nombre"]
    destino_nombre = ESTACIONES[camino[-1]]["nombre"]

    print()
    print("RUTA ÓPTIMA ENCONTRADA")
    print(f"  De: {origen_nombre}  →  Hasta: {destino_nombre}")
    print(LINEA)

    for i, estacion in enumerate(camino):
        nombre = ESTACIONES[estacion]["nombre"]
        linea  = ESTACIONES[estacion]["linea"]
        print(f"  {i + 1:>2}. {nombre}  ({linea})")

        if i < len(camino) - 1:
            siguiente = camino[i + 1]
            tiempo_tramo = consultar_costo(estacion, siguiente)
            nombre_sig   = ESTACIONES[siguiente]["nombre"]
            print(f"       └─► {nombre_sig:<22} [+{int(tiempo_tramo)} min]")

    print(LINEA)
    print(f"  ESTACIONES RECORRIDAS : {len(camino)}")
    print(f"  TIEMPO TOTAL ESTIMADO : {costo_total:.0f} minutos")
    print(LINEA)


def leer_estacion(prompt: str) -> str:
    """Lee y valida un id de estación desde la entrada del usuario."""
    while True:
        valor = input(prompt).strip().lower().replace(" ", "_")
        if hecho_estacion(valor):
            return valor
        print(f"  [!] '{valor}' no se encuentra en la base de conocimiento. Inténtelo de nuevo.")


def main() -> None:
    mostrar_encabezado()
    mostrar_estaciones()

    print()
    print("Ingrese los identificadores tal como aparecen en la tabla.")
    print("Ejemplo: terminal_norte   |   central   |   este_2")
    print()

    origen  = leer_estacion("  Estación de ORIGEN  : ")
    destino = leer_estacion("  Estación de DESTINO : ")

    print()
    print("  Ejecutando búsqueda A* ...")

    camino, costo = a_estrella(origen, destino)
    mostrar_resultado(camino, costo)


if __name__ == "__main__":
    main()
