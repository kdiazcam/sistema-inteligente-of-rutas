# 🚇 Sistema Inteligente de Rutas — Transporte Masivo

> **Búsqueda informada con algoritmo A\*** aplicada a una red de transporte masivo de tres líneas.

---

## 📋 Descripción

Sistema de planificación de rutas óptimas para una red de metro/transporte masivo ficticia. Dado un par de estaciones (origen y destino), el sistema encuentra el **camino de menor tiempo** utilizando el **algoritmo A\*** con una heurística euclidiana admisible.

El proyecto está estructurado siguiendo los principios de la **lógica de predicados** (inspirado en Prolog): separa los _hechos_ (datos estáticos) de las _reglas_ (funciones que derivan conocimiento nuevo).

---

## 🗺️ Red de Estaciones

La red cuenta con **3 líneas** y **2 nodos de transferencia**:

| Línea  | Color    | Dirección          | Nodos de transferencia                  |
| ------ | -------- | ------------------ | --------------------------------------- |
| **L1** | 🔵 Azul  | Norte ↔ Sur        | `central` (con L2), `nodo_sur` (con L3) |
| **L2** | 🔴 Roja  | Oeste ↔ Este       | `central` (con L1)                      |
| **L3** | 🟢 Verde | Noreste ↔ Suroeste | `nodo_sur` (con L1)                     |

### Estaciones disponibles

| ID (para ingresar)  | Nombre            | Línea   |
| ------------------- | ----------------- | ------- |
| `terminal_norte`    | Terminal Norte    | L1      |
| `norte_2`           | Norte 2           | L1      |
| `central`           | Central           | L1 / L2 |
| `sur_2`             | Sur 2             | L1      |
| `nodo_sur`          | Nodo Sur          | L1 / L3 |
| `terminal_sur`      | Terminal Sur      | L1      |
| `terminal_oeste`    | Terminal Oeste    | L2      |
| `oeste_2`           | Oeste 2           | L2      |
| `oeste_3`           | Oeste 3           | L2      |
| `este_2`            | Este 2            | L2      |
| `este_3`            | Este 3            | L2      |
| `terminal_este`     | Terminal Este     | L2      |
| `terminal_noreste`  | Terminal Noreste  | L3      |
| `noreste_2`         | Noreste 2         | L3      |
| `suroeste_2`        | Suroeste 2        | L3      |
| `terminal_suroeste` | Terminal Suroeste | L3      |

---

## 🧠 Algoritmo A\*

El motor de búsqueda implementa **A\*** con:

- **Función de costo `g(n)`**: tiempo acumulado en minutos desde el origen.
- **Heurística `h(n)`**: distancia euclidiana entre coordenadas geográficas (lat/lon), convertida a minutos asumiendo 30 km/h de velocidad promedio.
- **Admisibilidad**: `h(n) ≤ h*(n)` garantizada, por lo que A\* siempre retorna la ruta óptima.

---

## 📁 Estructura del Proyecto

```
sistema-inteligente-of-rutas/
│
├── main.py               # Interfaz CLI: entrada/salida y orquestación
├── base_conocimiento.py  # Hechos (estaciones, conexiones) y reglas derivadas
├── busqueda.py           # Implementación del algoritmo A*
└── README.md             # Este archivo
```

### Responsabilidades de cada módulo

| Archivo                | Responsabilidad                                                                                                                          |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `base_conocimiento.py` | Define `ESTACIONES`, `CONEXIONES` y las reglas: `hecho_estacion`, `consultar_vecinos`, `distancia_euclidiana_minutos`, `construir_grafo` |
| `busqueda.py`          | Contiene la función `a_estrella(origen, destino)` que devuelve `(camino, costo_total)`                                                   |
| `main.py`              | Muestra el menú, lee las estaciones del usuario, invoca `a_estrella` y presenta el resultado                                             |

---

## ⚙️ Requisitos

- **Python 3.10 o superior** (se usa `list[str] | None` y f-strings con `:`).
- **Sin dependencias externas** — solo módulos de la biblioteca estándar (`math`, `heapq`).

Verifica tu versión de Python con:

```bash
python --version
```

---

## 🚀 Ejecución

### 1. Clona o descarga el repositorio

```bash
git clone https://github.com/kdiazcam/sistema-inteligente-of-rutas.git
cd sistema-inteligente-of-rutas
```

O si ya tienes los archivos, navega a la carpeta del proyecto:

```bash
cd "ruta/a/sistema-inteligente-of-rutas"
```

### 2. Ejecuta el programa principal

```bash
python main.py
```

> En algunos sistemas puede ser necesario usar `python3` en lugar de `python`.

---

## 🖥️ Uso del programa

Al iniciar, el programa mostrará el encabezado y la tabla de estaciones disponibles organizadas por línea:

```
==========================================================
  SISTEMA INTELIGENTE DE RUTAS — TRANSPORTE MASIVO
       Algoritmo A* | Búsqueda Informada Heurística
==========================================================

ESTACIONES DISPONIBLES:
──────────────────────────────────────────────────────────
  [L1]
    terminal_norte         Terminal Norte
    norte_2                Norte 2
    central                Central
    ...
──────────────────────────────────────────────────────────
```

Luego pedirá la estación de **origen** y **destino**. Ingresa los IDs tal como aparecen en la tabla (en minúsculas, con guiones bajos):

```
  Estación de ORIGEN  : terminal_norte
  Estación de DESTINO : terminal_este
```

### Resultado esperado

```
RUTA ÓPTIMA ENCONTRADA
  De: Terminal Norte  →  Hasta: Terminal Este
──────────────────────────────────────────────────────────
   1. Terminal Norte  (L1)
       └─► Norte 2                [+5 min]
   2. Norte 2  (L1)
       └─► Central                [+5 min]
   3. Central  (L1/L2)
       └─► Este 2                 [+5 min]
   4. Este 2  (L2)
       └─► Este 3                 [+4 min]
   5. Este 3  (L2)
       └─► Terminal Este          [+6 min]
   6. Terminal Este  (L2)
──────────────────────────────────────────────────────────
  ESTACIONES RECORRIDAS : 6
  TIEMPO TOTAL ESTIMADO : 25 minutos
──────────────────────────────────────────────────────────
```

---

## ❗ Errores comunes

| Problema                                               | Causa                                                            | Solución                                                     |
| ------------------------------------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------ |
| `ModuleNotFoundError: No module named 'busqueda'`      | El archivo `busqueda.py` está vacío o no implementa `a_estrella` | Completar la implementación en `busqueda.py`                 |
| `SyntaxError` al iniciar                               | Versión de Python < 3.10                                         | Actualizar a Python 3.10+                                    |
| `[!] 'xxx' no se encuentra en la base de conocimiento` | El ID ingresado no existe                                        | Usa los IDs exactos de la tabla (minúsculas y guiones bajos) |

---

## 📐 Diseño basado en lógica de predicados

El módulo `base_conocimiento.py` sigue una analogía con **Prolog**:

```prolog
% Hechos
estacion(central, "Central", "L1/L2", 4.66, -74.10).
conecta(terminal_norte, norte_2, 5.0, 1.3).

% Reglas
estacion_valida(X) :- estacion(X, _, _, _, _).
vecino(X, Y, T)    :- conecta(X, Y, T, _) ; conecta(Y, X, T, _).
heuristica(X, Y, H) :-
    lat(X, Lx), lon(X, Ox), lat(Y, Ly), lon(Y, Oy),
    D is sqrt((Lx-Ly)^2 + (Ox-Oy)^2) * 111,
    H is (D / 30) * 60.
```

---
