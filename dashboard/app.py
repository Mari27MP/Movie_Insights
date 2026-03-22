import streamlit as st
import sys
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from eda.cargador_datos import CargadorDatos
from eda.procesador_eda import ProcesadorEda
from visualizacion.visualizador import Visualizador

st.title("TMDB Movie Insights 2020-2025")
st.write("Análisis exploratorio de películas usando datos de TMDB.")


# Cargar datos

# Cargar datos
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw", "tmdb_2020_to_2025.csv")

st.sidebar.title("Navegación")
seccion = st.sidebar.radio("Ir a:", ["Inicio", "EDA", "Visualizaciones"])

if seccion == "Inicio":
    st.header("Sobre el proyecto")
    st.write("""
    Este dashboard presenta el análisis exploratorio del dataset TMDB 2020-2025,
    que contiene información de 9,999 películas a nivel mundial.
    """)
    st.info("Usá el menú de la izquierda para navegar entre las secciones.")

elif seccion == "EDA":
    st.header("Análisis Exploratorio de Datos")
    cargador = CargadorDatos(ruta)
    df = cargador.cargar()
    procesador = ProcesadorEda(df)
    df_limpio = procesador.limpieza_datos()
    st.subheader("Resumen descriptivo")
    st.dataframe(procesador.resumen_descriptivo())
    st.subheader("Películas por año")
    st.dataframe(procesador.peliculas_por_anio())

elif seccion == "Visualizaciones":
    st.header("Visualizaciones")
    cargador = CargadorDatos(ruta)
    df = cargador.cargar()
    procesador = ProcesadorEda(df)
    df_limpio = procesador.limpieza_datos()
    viz = Visualizador(df_limpio)
    st.subheader("Distribución de calificaciones")
    viz.histograma_calificaciones()
    st.pyplot(plt)
    st.subheader("Películas producidas por año")
    viz.barras_por_anio()
    st.pyplot(plt)

    st.subheader("Popularidad vs Calificación")
    viz.scatter_popularidad_rating()
    st.pyplot(plt)

    st.subheader("Matriz de correlación")
    viz.heatmap_correlacion()
    st.pyplot(plt)

    st.subheader("Top 10 géneros")
    viz.barras_top_generos()
    st.pyplot(plt)


