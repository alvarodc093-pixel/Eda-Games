# Video Game Market Analysis (VGChartz 2024)

## Descripción del Proyecto

Este proyecto analiza más de 64.000 videojuegos utilizando datos extraídos de VGChartz con el objetivo de identificar patrones de mercado, tendencias históricas y factores relacionados con el éxito comercial de los videojuegos.

A través de un Análisis Exploratorio de Datos (EDA), se estudian aspectos clave de la industria como:

* Evolución del mercado a lo largo del tiempo.
* Géneros más populares y rentables.
* Consolas con mayor impacto comercial.
* Publishers líderes de la industria.
* Diferencias entre regiones geográficas.
* Relación entre la valoración crítica y las ventas.

El proyecto está orientado a la construcción de un dashboard interactivo en Streamlit y a la presentación de insights de negocio mediante técnicas de storytelling.

App desplegada: https://eda-games-apdqgafan5itappced9lpes.streamlit.app/

---

# Objetivos del Proyecto

Responder a las siguientes preguntas de negocio:

### Mercado

* ¿Qué géneros dominan la industria del videojuego?
* ¿Qué plataformas generan mayores ventas?
* ¿Qué publishers lideran el mercado?

### Evolución Temporal

* ¿Cómo ha evolucionado la industria a lo largo de los años?
* ¿Cuándo se produjo el pico de ventas del mercado?

### Rendimiento Comercial

* ¿Existe relación entre la puntuación de la crítica y las ventas?

### Análisis Regional

* ¿Cómo varían las preferencias de consumo entre Norteamérica, Europa y Japón?

---

# Dataset

### Fuente

VGChartz 2024

### Tamaño

| Métrica   | Valor  |
| --------- | ------ |
| Registros | 64.016 |
| Variables | 14     |

### Variables principales

| Variable     | Descripción              |
| ------------ | ------------------------ |
| title        | Nombre del videojuego    |
| console      | Plataforma               |
| genre        | Género                   |
| publisher    | Empresa publicadora      |
| developer    | Estudio desarrollador    |
| critic_score | Puntuación de la crítica |
| total_sales  | Ventas globales          |
| na_sales     | Ventas en Norteamérica   |
| jp_sales     | Ventas en Japón          |
| pal_sales    | Ventas en Europa/PAL     |
| other_sales  | Ventas en otras regiones |
| release_date | Fecha de lanzamiento     |
| last_update  | Última actualización     |
| img          | URL de imagen            |

---

# Metodología

El análisis se desarrolló siguiendo las fases habituales de un proyecto profesional de análisis de datos:

## 1. Comprensión del problema

Definición de preguntas de negocio y objetivos del análisis.

## 2. Exploración inicial

* Dimensiones del dataset.
* Tipos de datos.
* Identificación de posibles problemas de calidad.

## 3. Limpieza de datos

* Eliminación de duplicados.
* Conversión de variables temporales.
* Gestión de valores nulos.
* Creación de subconjuntos específicos para cada análisis.

## 4. Análisis exploratorio

### Análisis univariante

* Géneros.
* Consolas.
* Publishers.

### Análisis temporal

* Evolución de lanzamientos.
* Evolución de ventas.

### Análisis regional

* Comparación de mercados.
* Distribución de ventas por región.

### Análisis de correlación

* Critic Score vs Total Sales.

---

# Calidad de los Datos

Durante la auditoría inicial se detectó una elevada presencia de valores faltantes.

## Variables más afectadas

| Variable     | % Valores Nulos |
| ------------ | --------------- |
| critic_score | 89.57%          |
| jp_sales     | 89.49%          |
| na_sales     | 80.26%          |
| pal_sales    | 79.97%          |
| other_sales  | 76.37%          |
| total_sales  | 70.44%          |
| last_update  | 72.07%          |

### Decisiones tomadas

No se realizaron imputaciones artificiales sobre variables de ventas o puntuaciones debido a la elevada proporción de datos faltantes.

En su lugar:

* Se mantuvieron los datos originales.
* Se crearon subconjuntos específicos para cada análisis.
* Se evitaron transformaciones que pudieran introducir sesgos.

Esta decisión garantiza la integridad y fiabilidad de las conclusiones obtenidas.

---

# Principales Análisis Realizados

## Distribución de Géneros

Identificación de los géneros con mayor presencia dentro del catálogo.

### Pregunta de negocio

¿Qué tipo de videojuegos predominan en la industria?

---

## Distribución de Consolas

Análisis de las plataformas con mayor número de títulos publicados.

### Pregunta de negocio

¿Qué ecosistemas concentran la mayor actividad de desarrollo?

---

## Top Publishers por Ventas

Ranking de compañías según ventas globales acumuladas.

### Pregunta de negocio

¿Quién controla el mercado del videojuego?

---

## Consolas con Mayores Ventas

Comparación de ingresos generados por plataforma.

### Pregunta de negocio

¿Qué plataformas han sido más exitosas comercialmente?

---

## Evolución Temporal

Análisis histórico de:

* Número de lanzamientos.
* Ventas globales.

### Pregunta de negocio

¿Cómo ha evolucionado la industria del videojuego?

---

## Ventas Regionales

Comparación entre:

* Norteamérica
* Europa (PAL)
* Japón
* Otras regiones

### Pregunta de negocio

¿Existen diferencias culturales entre mercados?

---

## Relación entre Crítica y Ventas

Estudio de correlación entre:

* Critic Score
* Total Sales

### Pregunta de negocio

¿La calidad percibida influye en el éxito comercial?

---

# Tecnologías Utilizadas

## Lenguaje

* Python

## Librerías

* Pandas
* NumPy
* Matplotlib
* Seaborn

## Visualización

* Streamlit
* Plotly

## Entorno

* Jupyter Notebook
* Visual Studio Code

---

# Estructura del Proyecto

```text
VideoGameMarketAnalysis/

│
├── data/
│   └── vgchartz-2024.csv
│
├── notebooks/
│   └── EDA_VideoGames.ipynb
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

---

# Dashboard Interactivo

El proyecto incluye un dashboard desarrollado con Streamlit que permite explorar los resultados de forma interactiva.

### Secciones principales

* Overview
* Market Analysis
* Publishers
* Consoles
* Sales Analysis
* Regional Analysis
* Critic Analysis

---

# Principales Insights Esperados

* Identificación de los géneros más rentables.
* Descubrimiento de las plataformas más exitosas.
* Concentración de ventas en grandes publishers.
* Diferencias de comportamiento entre regiones.
* Evaluación del impacto de la crítica especializada sobre las ventas.


---

# Autor

Álvaro Domingo

Proyecto desarrollado como parte de mi portfolio de Data Analytics con el objetivo de aplicar técnicas de análisis exploratorio, visualización y comunicación de datos en un caso real relacionado con la industria del videojuego.
