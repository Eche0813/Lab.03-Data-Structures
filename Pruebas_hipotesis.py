"""
=============================================================================
LABORATORIO 03: PRUEBAS DE HIPÓTESIS Y ANÁLISIS INFERENCIAL NO PARAMÉTRICO
=============================================================================
Módulo encargado de evaluar la normalidad de los residuos (Shapiro-Wilk)
y realizar comparaciones estadísticas multigrupo (Kruskal-Wallis y Test de Dunn).

Autor: Samuel Echeverri Ortiz
Materia: Estructuras de Datos, Universidad de Antioquia
Fecha: Octubre de 2026
=============================================================================
"""

import pandas as pd
import numpy as np
from scipy import stats
import scikit_posthocs as sp


def realizar_pruebas_hipotesis(csv_path: str = "resultados_raw_experimento.csv") -> None:
    """
    Carga los resultados crudos del experimento, ejecuta la verificación de normalidad
    y aplica la batería de pruebas de hipótesis inferenciales para N_max.
    """
    df = pd.read_csv(csv_path)
    
    # Evaluación sobre el nivel de entrada de mayor carga (N = 50,000)
    n_max = df["N"].max()
    df_nmax = df[df["N"] == n_max].copy()

    print("=================================================================")
    print(f" PRUEBAS DE HIPÓTESIS Y ANÁLISIS INFERENCIAL (N = {n_max})")
    print("=================================================================\n")

    # -------------------------------------------------------------------
    # 1. PRUEBA DE NORMALIDAD (Shapiro-Wilk Test)
    # H0: La muestra proviene de una distribución normal (alpha = 0.05)
    # -------------------------------------------------------------------
    print("1. EVALUACIÓN DE NORMALIDAD (Shapiro-Wilk Test)")
    print("-----------------------------------------------------------------")
    
    normalidad_cumplida = True
    for (escenario, estructura), group in df_nmax.groupby(["Escenario", "Estructura"]):
        stat, p_val = stats.shapiro(group["Tiempo_Busqueda_s"])
        es_normal = p_val > 0.05
        if not es_normal:
            normalidad_cumplida = False
        print(f" > [{escenario}] {estructura:<18}: W = {stat:.4f}, p-valor = {p_val:.4e} -> {'Normal' if es_normal else 'NO Normal'}")

    print("\n-----------------------------------------------------------------")
    
    # -------------------------------------------------------------------
    # 2. COMPARACIÓN MULTIGRUPO (Kruskal-Wallis / ANOVA)
    # H0: No existen diferencias en las medianas de tiempo de búsqueda entre estructuras
    # -------------------------------------------------------------------
    for escenario in df_nmax["Escenario"].unique():
        df_esc = df_nmax[df_nmax["Escenario"] == escenario]
        
        grupos = [group["Tiempo_Busqueda_s"].values for _, group in df_esc.groupby("Estructura")]

        print(f"\n2. PRUEBA COMPARATIVA EN ESCENARIO: '{escenario}'")
        print("-----------------------------------------------------------------")

        if normalidad_cumplida:
            # Paramétrico: ANOVA de una vía
            f_stat, p_val = stats.f_oneway(*grupos)
            print(f" Test Aplicado: ANOVA de una vía")
            print(f" Estadístico F: {f_stat:.4f} | p-valor: {p_val:.4e}")
        else:
            # No Paramétrico: Kruskal-Wallis
            h_stat, p_val = stats.kruskal(*grupos)
            print(f" Test Aplicado: Kruskal-Wallis (No Paramétrico)")
            print(f" Estadístico H: {h_stat:.4f} | p-valor: {p_val:.4e}")
            
            if p_val < 0.05:
                print(" Conclusión: Se RECHAZA H0. Existen diferencias estadísticamente significativas.")
                
                # Test Post-Hoc de Dunn con corrección de Bonferroni
                dunn = sp.posthoc_dunn(df_esc, val_col="Tiempo_Busqueda_s", group_col="Estructura", p_adjust="bonferroni")
                print("\n  [Matriz de p-valores ajustados - Test Post-Hoc de Dunn]")
                print(dunn)
            else:
                print(" Conclusión: No se rechaza H0. Sin diferencias significativas.")

if __name__ == "__main__":
    realizar_pruebas_hipotesis()