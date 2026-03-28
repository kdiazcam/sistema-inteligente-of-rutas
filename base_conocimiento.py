"""
base_conocimiento.py
====================
Base de conocimiento del sistema inteligente de transporte masivo.

Estructura inspirada en lógica de predicados (Prolog):
  - HECHOS: datos estáticos (estaciones y conexiones)
  - REGLAS: funciones que derivan conocimiento nuevo a partir de los hechos

"""

import math

# =============================================================================
# HECHOS — Estaciones
# =============================================================================
# Equivalente Prolog: estacion(id, nombre, linea, lat, lon).
#
# Red genérica de 3 líneas con 2 nodos de transferencia:
#   L1 (Azul)  - Norte/Sur      : terminal_norte … terminal_sur
#   L2 (Roja)  - Este/Oeste     : terminal_oeste … terminal_este
#   L3 (Verde) - Diagonal NE-SO : terminal_noreste … terminal_suroeste
#
# 'central'  es el nodo de transferencia entre L1 y L2.
# 'nodo_sur' es el nodo de transferencia entre L1 y L3.
# =============================================================================

ESTACIONES: dict[str, dict] = {
    # ── Línea 1 – Azul (Norte-Sur) ──────────────────────────────────────────
    "terminal_norte":    {"nombre": "Terminal Norte",    "linea": "L1",    "lat": 4.78, "lon": -74.10},
    "norte_2":           {"nombre": "Norte 2",           "linea": "L1",    "lat": 4.72, "lon": -74.10},
    "central":           {"nombre": "Central",           "linea": "L1/L2", "lat": 4.66, "lon": -74.10},
    "sur_2":             {"nombre": "Sur 2",             "linea": "L1",    "lat": 4.62, "lon": -74.10},
    "nodo_sur":          {"nombre": "Nodo Sur",          "linea": "L1/L3", "lat": 4.56, "lon": -74.10},
    "terminal_sur":      {"nombre": "Terminal Sur",      "linea": "L1",    "lat": 4.50, "lon": -74.10},

    # ── Línea 2 – Roja (Este-Oeste) ─────────────────────────────────────────
    "terminal_oeste":    {"nombre": "Terminal Oeste",    "linea": "L2",    "lat": 4.66, "lon": -74.26},
    "oeste_2":           {"nombre": "Oeste 2",           "linea": "L2",    "lat": 4.66, "lon": -74.20},
    "oeste_3":           {"nombre": "Oeste 3",           "linea": "L2",    "lat": 4.66, "lon": -74.16},
    # "central" compartida con L1 (definida arriba)
    "este_2":            {"nombre": "Este 2",            "linea": "L2",    "lat": 4.66, "lon": -74.04},
    "este_3":            {"nombre": "Este 3",            "linea": "L2",    "lat": 4.66, "lon": -74.00},
    "terminal_este":     {"nombre": "Terminal Este",     "linea": "L2",    "lat": 4.66, "lon": -73.94},

    # ── Línea 3 – Verde (Diagonal Noreste-Suroeste) ──────────────────────────
    "terminal_noreste":  {"nombre": "Terminal Noreste",  "linea": "L3",    "lat": 4.68, "lon": -73.98},
    "noreste_2":         {"nombre": "Noreste 2",         "linea": "L3",    "lat": 4.62, "lon": -74.04},
    # "nodo_sur" compartida con L1 (definida arriba)
    "suroeste_2":        {"nombre": "Suroeste 2",        "linea": "L3",    "lat": 4.50, "lon": -74.14},
    "terminal_suroeste": {"nombre": "Terminal Suroeste", "linea": "L3",    "lat": 4.44, "lon": -74.18},
}


# =============================================================================
# HECHOS — Conexiones
# =============================================================================
# Equivalente Prolog: conecta(origen, destino, tiempo_min, distancia_km).
# Las conexiones son BIDIRECCIONALES; la regla consultar_vecinos las expone
# en ambas direcciones.
# =============================================================================

CONEXIONES: list[tuple[str, str, float, float]] = [
    # ── Línea 1 – Azul (Norte-Sur) ──────────────────────────────────────────
    ("terminal_norte",   "norte_2",            5.0, 1.3),
    ("norte_2",          "central",            5.0, 1.3),
    ("central",          "sur_2",              3.0, 0.9),
    ("sur_2",            "nodo_sur",           4.0, 1.1),
    ("nodo_sur",         "terminal_sur",       6.0, 1.3),

    # ── Línea 2 – Roja (Este-Oeste) ─────────────────────────────────────────
    ("terminal_oeste",   "oeste_2",            7.0, 1.3),
    ("oeste_2",          "oeste_3",            5.0, 1.1),
    ("oeste_3",          "central",            4.0, 0.9),
    ("central",          "este_2",             5.0, 1.3),
    ("este_2",           "este_3",             4.0, 0.9),
    ("este_3",           "terminal_este",      6.0, 1.3),

    # ── Línea 3 – Verde (Diagonal Noreste-Suroeste) ──────────────────────────
    ("terminal_noreste", "noreste_2",          6.0, 1.3),
    ("noreste_2",        "nodo_sur",           7.0, 1.3),
    ("nodo_sur",         "suroeste_2",         6.0, 1.3),
    ("suroeste_2",       "terminal_suroeste",  7.0, 1.3),
]


# =============================================================================
# REGLAS
# =============================================================================
# Las reglas son funciones que derivan conocimiento nuevo a partir de los
# hechos, de forma análoga a las reglas en Prolog.
# =============================================================================

def hecho_estacion(id_estacion: str) -> bool:
    """
    Regla: una estación es válida si está registrada en la base de conocimiento.
    Prolog equivalente: estacion_valida(X) :- estacion(X, _, _, _, _).
    """
    return id_estacion in ESTACIONES


def hecho_conectados(origen: str, destino: str) -> bool:
    """
    Regla: dos estaciones están conectadas si existe una conexión directa
    en cualquier dirección.
    Prolog equivalente: conectados(X,Y) :- conecta(X,Y,_,_) ; conecta(Y,X,_,_).
    """
    for o, d, _, _ in CONEXIONES:
        if (o == origen and d == destino) or (o == destino and d == origen):
            return True
    return False


def consultar_costo(origen: str, destino: str) -> float | None:
    """
    Regla: obtiene el tiempo (minutos) entre dos estaciones adyacentes.
    Prolog equivalente: costo(X, Y, T) :- conecta(X, Y, T, _) ; conecta(Y, X, T, _).
    Retorna None si no son adyacentes.
    """
    for o, d, tiempo, _ in CONEXIONES:
        if (o == origen and d == destino) or (o == destino and d == origen):
            return tiempo
    return None


def consultar_vecinos(estacion: str) -> list[tuple[str, float]]:
    """
    Regla derivada: obtiene todos los vecinos de una estación con su costo.
    Prolog equivalente: vecino(X, Y, T) :- conecta(X, Y, T, _) ; conecta(Y, X, T, _).
    """
    vecinos: list[tuple[str, float]] = []
    for o, d, tiempo, _ in CONEXIONES:
        if o == estacion:
            vecinos.append((d, tiempo))
        elif d == estacion:
            vecinos.append((o, tiempo))
    return vecinos


def distancia_euclidiana_minutos(id_a: str, id_b: str) -> float:
    """
    Regla heurística h(n): estima el tiempo mínimo entre dos estaciones
    usando la distancia en línea recta (admisible para A*).

    Cálculo:
        distancia_km = sqrt((Δlat)² + (Δlon)²) × 111  [111 km por grado]
        tiempo_min   = (distancia_km / 30 km/h) × 60   [velocidad promedio]

    Propiedad de admisibilidad: la distancia en línea recta nunca supera
    la distancia real de viaje, por lo tanto h(n) ≤ h*(n) y A* es óptimo.

    Prolog equivalente:
        heuristica(X, Y, H) :-
            lat(X, Lx), lon(X, Ox), lat(Y, Ly), lon(Y, Oy),
            D is sqrt((Lx-Ly)^2 + (Ox-Oy)^2) * 111,
            H is (D / 30) * 60.
    """
    a = ESTACIONES[id_a]
    b = ESTACIONES[id_b]
    delta_lat = a["lat"] - b["lat"]
    delta_lon = a["lon"] - b["lon"]
    distancia_km = math.sqrt(delta_lat ** 2 + delta_lon ** 2) * 111.0
    tiempo_min = (distancia_km / 30.0) * 60.0
    return tiempo_min


def construir_grafo() -> dict[str, list[tuple[str, float]]]:
    """
    Regla de construcción: materializa las listas de adyacencia del grafo
    a partir de los hechos de conexión. Es consumida por el motor de búsqueda.

    Prolog equivalente (regla derivada de múltiples hechos):
        arco(X, Y, T) :- conecta(X, Y, T, _) ; conecta(Y, X, T, _).
    """
    grafo: dict[str, list[tuple[str, float]]] = {e: [] for e in ESTACIONES}
    for origen, destino, tiempo, _ in CONEXIONES:
        grafo[origen].append((destino, tiempo))
        grafo[destino].append((origen, tiempo))
    return grafo
