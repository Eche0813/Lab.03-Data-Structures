"""
=============================================================================
LABORATORIO 03: ESTUDIO ESTADÍSTICO DE ESCALABILIDAD EN ESTRUCTURAS DE BÚSQUEDA
=============================================================================
Módulo principal para la ejecución de experimentos de benchmarking y
recolección de métricas de rendimiento (Tiempos de Inserción y Búsqueda).

Autor: Samuel Echeverri Ortiz
Materia: Estructuras de Datos, Universidad de Antioquia
Fecha: Octubre de 2026
=============================================================================
"""

import time
import math
import random
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from BTrees.OOBTree import OOBTree
from sortedcontainers import SortedDict

# ---------------------------------------------------------------------------
# CONFIGURACIÓN DEL DISEÑO EXPERIMENTAL
# ---------------------------------------------------------------------------
SEMILLA = 42                  # Semilla determinista para garantizar reproducibilidad exacta
N_CORRIDAS = 30               # Repeticiones (n >= 30) para cumplir el Teorema del Límite Central
M_BUSQUEDAS = 1000            # Cantidad de consultas por iteración para reducir el ruido del SO
RANGOS_N = [1000, 5000, 10000, 25000, 50000] # Niveles discretos de escalabilidad (Factor N)

NOMBRES_EJEMPLO = ["Ana", "Carlos", "María", "Juan", "Laura", "Pedro", "Sofia", "Diego", "Elena", "Lucas"]

# ---------------------------------------------------------------------------
# ADAPTADORES DE ESTRUCTURAS DE DATOS (PATRÓN WRAPPER)
# ---------------------------------------------------------------------------

class SistemaLista:
    """Implementación de búsqueda lineal sobre una lista secuencial en memoria (Complejidad: O(N))."""
    
    def __init__(self):
        self.datos = []

    def insertar(self, estudiante: dict) -> None:
        """Inserta un registro al final de la lista en tiempo O(1) amortizado."""
        self.datos.append(estudiante)

    def buscar_por_id(self, id_estudiante: int) -> dict | None:
        """Realiza una búsqueda secuencial O(N) utilizando un generador interno."""
        return next((est for est in self.datos if est["id"] == id_estudiante), None)


class SistemaABB:
    """Implementación de Árbol Binario de Búsqueda Autobalanceado usando SortedDict (Complejidad: O(log N))."""
    
    def __init__(self):
        self.arbol = SortedDict()

    def insertar(self, estudiante: dict) -> None:
        """Inserta un registro manteniendo el balance del árbol en O(log N)."""
        self.arbol[estudiante["id"]] = estudiante

    def buscar_por_id(self, id_estudiante: int) -> dict | None:
        """Busca una clave en el árbol en tiempo O(log N)."""
        return self.arbol.get(id_estudiante)


class SistemaBPlus:
    """Implementación de Árbol B+ en RAM basada en ZODB.OOBTree (Complejidad: O(log N))."""
    
    def __init__(self):
        self.arbol = OOBTree()

    def insertar(self, estudiante: dict) -> None:
        """Inserta un registro en el nodo hoja correspondiente en O(log N)."""
        self.arbol[estudiante["id"]] = estudiante

    def buscar_por_id(self, id_estudiante: int) -> dict | None:
        """Busca un elemento aprovechando la jerarquía de nodos en RAM en O(log N)."""
        return self.arbol.get(id_estudiante)


# ---------------------------------------------------------------------------
# MÓDULO DE GENERACIÓN Y SINTETIZACIÓN DE DATOS
# ---------------------------------------------------------------------------

def generar_estudiantes(cantidad: int, rng: random.Random) -> list[dict]:
    """
    Genera un conjunto de datos sintéticos de estudiantes con IDs únicos.

    Args:
        cantidad (int): Número N de estudiantes a generar.
        rng (random.Random): Instancia del generador pseudoaleatorio con semilla fija.

    Returns:
        list[dict]: Lista de diccionarios con atributos sintéticos del estudiante.
    """
    ids_unicos = rng.sample(range(1000, 1000000), cantidad)
    return [
        {
            "id": uid,
            "nombre": rng.choice(NOMBRES_EJEMPLO),
            "edad": rng.randint(17, 28),
            "promedio": round(rng.uniform(5.0, 10.0), 1)
        }
        for uid in ids_unicos
    ]

# ---------------------------------------------------------------------------
# MOTOR DE EXPERIMENTACIÓN Y MEDICIÓN DE PRECISIÓN
# ---------------------------------------------------------------------------

def medir_operaciones(ClaseEstructura, estudiantes: list[dict], ids_a_buscar: list[int]) -> tuple[float, float]:
    """
    Aísla y mide los tiempos de ejecución de la fase de construcción y la fase de búsqueda.

    Args:
        ClaseEstructura: Clase wrapper de la estructura a instanciar (Lista, ABB o B+).
        estudiantes (list[dict]): Datos de entrada para poblar la estructura.
        ids_a_buscar (list[int]): Lista de IDs objetivo para la prueba de consulta.

    Returns:
        tuple[float, float]: (Tiempo de Inserción en segundos, Tiempo de Búsqueda en segundos)
    """
    # 1. Medición aislada del tiempo de construcción (Inserción masiva)
    t0 = time.perf_counter()
    instancia = ClaseEstructura()
    for est in estudiantes:
        instancia.insertar(est)
    t_construccion = time.perf_counter() - t0

    # 2. Medición aislada de la batería de M búsquedas
    t0 = time.perf_counter()
    for uid in ids_a_buscar:
        _ = instancia.buscar_por_id(uid)
    t_busqueda = time.perf_counter() - t0

    return t_construccion, t_busqueda


def ejecutar_estudio_estadistico() -> list[dict]:
    """
    Ejecuta el diseño factorial completo (N x Escenarios x Estructuras x Corridas)
    y exporta los datos crudos a un archivo CSV.
    """
    rng = random.Random(SEMILLA)
    resultados_raw = []

    print("==========================================================")
    print(" INICIANDO EXPERIMENTACIÓN ESTADÍSTICA (N_CORRIDAS = 30)")
    print("==========================================================\n")

    estructuras = {
        "Lista": SistemaLista,
        "ABB (SortedDict)": SistemaABB,
        "B+ (OOBTree)": SistemaBPlus
    }

    for N in RANGOS_N:
        print(f"[*] Procesando nivel de entrada N = {N} ...")
        
        for corrida in range(1, N_CORRIDAS + 1):
            base_estudiantes = generar_estudiantes(N, rng)
            
            # Selección uniforme de la muestra de consulta M
            muestra_busquedas = rng.sample(base_estudiantes, min(M_BUSQUEDAS, N))
            ids_a_buscar = [est["id"] for est in muestra_busquedas]

            escenarios = {
                "Aleatorio": base_estudiantes.copy(),
                "Ordenado": sorted(base_estudiantes, key=lambda x: x["id"])
            }

            for nombre_escenario, datos in escenarios.items():
                for nombre_est, clase_est in estructuras.items():
                    
                    t_const, t_busq = medir_operaciones(clase_est, datos, ids_a_buscar)

                    resultados_raw.append({
                        "N": N,
                        "Corrida": corrida,
                        "Escenario": nombre_escenario,
                        "Estructura": nombre_est,
                        "Tiempo_Construccion_s": t_const,
                        "Tiempo_Busqueda_s": t_busq
                    })

    # Persistencia de los datos crudos
    guardar_resultados_csv(resultados_raw, "resultados_raw_experimento.csv")
    print("\n[OK] Datos crudos exportados a 'resultados_raw_experimento.csv'")
    
    return resultados_raw

# ---------------------------------------------------------------------------
# RESUMEN Y PROCESAMIENTO ESTADÍSTICO DESCRIPTIVO
# ---------------------------------------------------------------------------

def guardar_resultados_csv(datos: list[dict], nombre_archivo: str) -> None:
    """Escribe una lista de diccionarios en formato tabular CSV."""
    if not datos:
        return
    keys = datos[0].keys()
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(datos)


def calcular_resumen_estadistico(resultados_raw: list[dict]) -> pd.DataFrame:
    """
    Calcula la media muestra, desviación estándar e intervalo de confianza al 95%
    usando la distribución t-Student para cada grupo experimental.
    """
    df = pd.DataFrame(resultados_raw)
    
    def stats_ic95(series):
        mean = series.mean()
        std = series.std()
        n = len(series)
        # Valor crítico de t-Student para alpha/2 = 0.025 y df = n - 1 (29 df -> t ≈ 2.045)
        h = 2.045 * (std / math.sqrt(n)) if n > 1 else 0.0
        return pd.Series({
            "Media": mean,
            "Desv_Est": std,
            "IC95_Inf": mean - h,
            "IC95_Sup": mean + h
        })

    resumen = df.groupby(["N", "Escenario", "Estructura"])["Tiempo_Busqueda_s"].apply(stats_ic95).unstack()
    resumen.to_csv("resumen_estadistico_busqueda.csv")
    print("[OK] Resumen descriptivo guardado en 'resumen_estadistico_busqueda.csv'\n")
    return df

# ---------------------------------------------------------------------------
# GENERACIÓN DE GRÁFICAS Y VISUALIZACIÓN
# ---------------------------------------------------------------------------

def generar_graficas(df: pd.DataFrame) -> None:
    """Genera y guarda los gráficos de escalabilidad (Escala Log) y de dispersión (Boxplots)."""
    sns.set_theme(style="whitegrid")
    
    # 1. Curva de Escalabilidad (Escala Logarítmica en Eje Y)
    plt.figure(figsize=(10, 6))
    g = sns.lineplot(
        data=df,
        x="N", y="Tiempo_Busqueda_s",
        hue="Estructura", style="Escenario",
        markers=True, dashes=False, err_style="band", ci=95
    )
    g.set_yscale("log")
    plt.title("Escalabilidad del Tiempo de Búsqueda (Escala Logarítmica - IC 95%)", fontsize=14)
    plt.xlabel("Tamaño de Entrada (N)", fontsize=12)
    plt.ylabel("Tiempo de Búsqueda (s - Escala Log)", fontsize=12)
    plt.savefig("escalabilidad_busqueda.png", dpi=300, bbox_inches="tight")
    plt.close()

    # 2. Boxplot de Dispersión para N Máximo (50,000)
    n_max = df["N"].max()
    plt.figure(figsize=(10, 6))
    sns.boxplot(
        data=df[df["N"] == n_max],
        x="Estructura", y="Tiempo_Busqueda_s",
        hue="Escenario"
    )
    plt.title(f"Dispersión y Variabilidad del Tiempo de Búsqueda (N = {n_max})", fontsize=14)
    plt.xlabel("Estructura de Datos", fontsize=12)
    plt.ylabel("Tiempo de Búsqueda (s)", fontsize=12)
    plt.savefig("variabilidad_boxplot.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("[OK] Gráficas exportadas ('escalabilidad_busqueda.png', 'variabilidad_boxplot.png')")


if __name__ == "__main__":
    datos_crudos = ejecutar_estudio_estadistico()
    df_resultados = calcular_resumen_estadistico(datos_crudos)
    generar_graficas(df_resultados)