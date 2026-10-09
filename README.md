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
```
## Estructura del repositorio
```
Lab.03-Data-Structures/
│
├── Reto_busqueda_estadistico.py  # Script principal de experimentación y benchmarking
├── Pruebas_hipotesis.py          # Script de análisis inferencial no paramétrico
├── resultados_raw_experimento.csv# Dataset crudo con las 30 corridas independientes
├── resumen_estadistico_busqueda.csv # Matriz de datos procesados (Media, Std, IC 95%)
├── escalabilidad_busqueda.png    # Gráfico de escalabilidad asintótica (Escala Logarítmica)
├── variabilidad_boxplot.png      # Diagrama de cajas (Boxplot) de dispersión para N = 50,000
└── README.md                     # Documentación general del laboratorio
```
## Guía de ejecución
### 1.Generación de Experimentos y Benchmark; Corre el script principal para poblar las estructuras, medir los tiempos de forma aislada, generar los archivos .csv y exportar las gráficas:
```bash
python Reto_busqueda_estadistico.py
```
**Salidas generadas:**

resultados_raw_experimento.csv (contiene los 900 registros del diseño factorial completo).

resumen_estadistico_busqueda.csv (resumen estadístico descriptivo).   

escalabilidad_busqueda.png y variabilidad_boxplot.png. 

### 2. Evaluación de pruebas de hipótesis
Una vez generado el dataset crudo, ejecuta el análisis inferencial:
```bash
python Pruebas_hipotesis.py
```
**Salidas en consola:**

Prueba de normalidad de Shapiro-Wilk ($p < 0.05$ en Lista y ABB justifica el enfoque no paramétrico).   

Test global de Kruskal-Wallis ($H = 79.1209, p = 6.59 \times 10^{-18}$).   

Matriz de p-valores ajustados mediante el Test Post-Hoc de Dunn con corrección de Bonferroni. 

## Metodología Experimental

Factor Tamaño de Entrada ($N$): $1.000, 5.000, 10.000, 25.000, 50.000$ registros. 

Repeticiones ($n$): 30 corridas independientes por configuración (Teorema del Límite Central).

Muestra de Consulta ($M$)$1.000$ búsquedas por iteración. 

Control Aleatorio: Semilla fija (SEMILLA = 42) para reproducibilidad exacta.

Reloj de Precisión: time.perf_counter() con resolución a nivel de nanosegundos.

## Resultados principales

1. **Escalabilidad Asintótica:** La Lista confirmó su comportamiento lineal $O(N)$, mientras que el ABB y el Árbol B+ ratificaron la cota logarítmica $O(\log N)$ manteniendo respuestas en microsegundos.
2. **Superioridad del Árbol B+:** La prueba Post-Hoc de Dunn evidenció que el Árbol B+ (OOBTree) superó significativamente al ABB autobalanceado (SortedDict) con un $p\text{-valor} = 0.000026$.
3. **Jerarquía de Memoria:** La densidad de claves por nodo y la estructura de hojas enlazadas del Árbol B+ reducen los fallos de caché en CPU, optimizando la latencia de consulta en RAM.

## Uso de herramientas de IA
Afirmo haber hecho uso de la herramienta de inteligencia artificial proveída por Gemini y me hago responsable unica y exclusivamente de su uso para:
1. Diseño e implementación de Pruebas de hipótesis. (Acompañamiento en el desarrollo.)
2. Diseño e implementación de Bloque de ejecución del estudio estadístico. (Acompañamiento en el desarrollo.)
3. Diseño e implementación de Bloque de calcular el resumen estadístico. (Acompañamiento en el desarrollo.)
4. Diseño e implementación de Bloque de generación de gráficas automatizadas. (Completamente diseñado por la IA)

PD: con "Acompañamiento en el desarrollo" me refiero a que hice uso de la IA para entender conceptos, buscar librerías y encontrar vías eficientes para la implementación del código, más no a que la IA llevó a cabo por si sola el diseño del código.
