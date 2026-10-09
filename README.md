# Laboratorio 03: Estudio Estadístico de Escalabilidad y Rendimiento en Estructuras de Datos de Búsqueda

**Autor:** Samuel Echeverri Ortiz  
**Programa:** Ingeniería de Sistemas, Universidad de Antioquia  
**Fecha:** Octubre de 2026  

---

## Descripción del Proyecto

Este proyecto realiza un análisis experimental e inferencial riguroso para comparar el rendimiento de tres estructuras de datos fundamentales en memoria RAM durante operaciones de búsqueda de información:

1. **Lista Secuencial** (Búsqueda lineal $O(N)$)[cite: 1, 3]
2. **Árbol Binario de Búsqueda Autobalanceado** (`sortedcontainers.SortedDict`, $O(\log N)$)
3. **Árbol B+** (`BTrees.OOBTree`, $O(\log N)$)

El estudio evalúa cómo escala la latencia de consulta ante variaciones en el tamaño de la base de datos sintética ($N \in \{1.000, 5.000, 10.000, 25.000, 50.000\}$) y el orden de inserción inicial (Aleatorio vs. Ascendente Ordenado)[cite: 2, 3]. Para mitigar el ruido del sistema operativo, el experimento aplica muestreo repetido ($n = 30$ corridas independientes), medición con alta precisión y pruebas de hipótesis no paramétricas (Shapiro-Wilk, Kruskal-Wallis y Test Post-Hoc de Dunn)[cite: 2, 3].

---

## Requisitos e Instalación

### Pre-requisitos
- **Python 3.12** o superior instalado.
- Entorno de ejecución local (se recomienda evitar entornos compartidos como Google Colab para no introducir sesgos de variabilidad en la CPU/RAM)[cite: 2, 3].

### Instalación de Dependencias

Ejecuta el siguiente comando en tu terminal para instalar todas las librerías necesarias[cite: 2, 3]:

```bash
pip install numpy pandas matplotlib seaborn scipy scikit-posthocs BTrees sortedcontainers
