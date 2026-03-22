import streamlit as st
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

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

    from collections import Counter

    st.header("Visualizaciones")

    cargador = CargadorDatos(ruta)
    df = cargador.cargar()
    procesador = ProcesadorEda(df)
    df_limpio = procesador.limpieza_datos()


    # Selector de año
    anios = sorted(df_limpio["anio_estreno"].dropna().unique().astype(int).tolist())
    anios_opciones = ["Todos"] + [str(a) for a in anios]
    anio_seleccionado = st.selectbox("Filtrar por año:", anios_opciones)


    if anio_seleccionado != "Todos":
        df_limpio = df_limpio[df_limpio["anio_estreno"] == int(anio_seleccionado)]

    # Gráfico 1 - Histograma
    st.subheader("¿Cómo califican los usuarios las películas?")
    datos = df_limpio[df_limpio["vote_average"] > 1]
    fig1 = px.histogram(datos, x="vote_average", nbins=30,
                        title="Distribución de calificaciones TMDB 2020-2025",
                        color_discrete_sequence=["steelblue"])
    fig1.update_layout(xaxis_title="Calificación promedio",
                       yaxis_title="Número de películas")
    st.plotly_chart(fig1)

    # Gráfico 2 - Barras por año
    st.subheader("¿Cuántas películas se produjeron por año?")
    por_anio = df_limpio.groupby("anio_estreno")["id"].count().reset_index()
    fig2 = px.bar(por_anio, x="anio_estreno", y="id",
                  title="Películas producidas por año TMDB 2020-2025",
                  color_discrete_sequence=["steelblue"])
    fig2.update_layout(xaxis_title="Año", yaxis_title="Número de películas")
    st.plotly_chart(fig2)

    # Gráfico 3 - Scatter
    st.subheader("¿Las películas más populares son las mejor calificadas?")
    fig3 = px.scatter(df_limpio, x="popularity", y="vote_average",
                      hover_name="title",
                      title="Popularidad vs Calificación TMDB 2020-2025",
                      color_discrete_sequence=["steelblue"])
    fig3.update_layout(xaxis_title="Popularidad", yaxis_title="Calificación promedio")
    st.plotly_chart(fig3)

    # Gráfico 4 - Top géneros
    st.subheader("¿Qué géneros dominan el cine global?")
    todos_generos = []
    for lista in df_limpio["genre_ids"]:
        todos_generos.extend(lista)
    conteo = Counter(todos_generos)
    top10 = pd.DataFrame(conteo.most_common(10), columns=["genero", "cantidad"])
    fig4 = px.bar(top10, x="cantidad", y="genero", orientation="h",
                  title="Top 10 géneros TMDB 2020-2025",
                  color_discrete_sequence=["steelblue"])
    st.plotly_chart(fig4)

