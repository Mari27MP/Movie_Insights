# Movie Insights — Análisis de Películas TMDB 2020-2025

## Descripción

Movie Insights es un sistema desarrollado en Python con Programación Orientada a Objetos (POO) que permite ingestar, procesar, analizar y visualizar datos de películas provenientes de TMDB (The Movie Database) del período 2020 al 2025.

El sistema realiza análisis exploratorio de datos (EDA), genera estadísticas descriptivas y produce visualizaciones que cuentan historias a partir de los datos cinematográficos.

## Integrantes

| Nombre | 
|--------|
| Mariana Méndez Pérez |
| Claret Rodríguez Jiménez |

## Información del curso

- **Institución:** Colegio Universitario de Cartago (CUC)
- **Curso:** BD-143 Programación II
- **Profesor:** Osvaldo González Chaves
- **Cuatrimestre:** I Cuatrimestre 2026

## Estructura del proyecto

```
Movie_Insights/
├── src/                        # Código fuente principal
│   ├── eda/                    # Análisis exploratorio de datos
│   │   ├── cargador_datos.py   # Clase CargadorDatos
│   │   └── procesador_eda.py   # Clase ProcesadorEDA
│   ├── visualizacion/          # Visualización de datos
│   │   └── visualizador.py     # Clase Visualizador
│   ├── helpers/                # Funciones auxiliares
│   │   └── utilidades.py       # Clase Utilidades
│   └── main.py                 # Punto de entrada del proyecto
│
├── notebooks/                  # Jupyter Notebooks
│   ├── 01_EDA.ipynb            # Análisis exploratorio
│   └── 02_Visualizacion.ipynb  # Visualizaciones
│
├── data/
│   ├── raw/                    # Dataset original
│   │   └── tmdb_2020_to_2025.csv
│   └── processed/              # Dataset limpio generado
│       └── tmdb_movies_clean.csv
│
├── dashboard/                  # Dashboard interactivo (Streamlit)
│   └── app.py
│
└── README.md
```

## Tecnologías utilizadas

| Tecnología | Uso |
|------------|-----|
| Python 3.14 | Lenguaje principal |
| Pandas | Carga y manipulación de datos |
| Matplotlib | Visualizaciones estáticas |
| Plotly | Visualizaciones interactivas |
| Jupyter | Notebooks de análisis |
| Streamlit | Dashboard interactivo (puntos extra) |
| GitHub + Sourcetree | Control de versiones |

## Cómo correr el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/Mari27MP/Movie_Insights.git
cd Movie_Insights
```

### 2. Instalar las librerías necesarias
```bash
pip install pandas matplotlib plotly jupyter streamlit
```

### 3. Correr el programa principal
```bash
python src/main.py
```

### 4. Abrir los notebooks
```bash
jupyter notebook
```


### 5. Correr el dashboard (opcional)
```bash
streamlit run dashboard/app.py
```

## Dataset

- **Fuente:** TMDB (The Movie Database)
- **Archivo:** `tmdb_2020_to_2025.csv`
- **Período:** 2020 – 2025
- **Ubicación:** `data/raw/`

## Módulos principales

- **CargadorDatos:** Carga el CSV, registra número de filas y porcentaje de nulos.
- **ProcesadorEDA:** Limpia los datos, genera resumen descriptivo y matriz de correlación.
- **Visualizador:** Crea gráficas con historias (histogramas, scatter, heatmaps, etc.).
- **Utilidades:** Funciones auxiliares reutilizables para validaciones y formateo.
