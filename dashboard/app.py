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
st.markdown("### Análisis Exploratorio de Datos del cine mundial 2020-2025")
st.markdown("**Proyecto II** — BD-143 Programación II | I Cuatrimestre 2026 | CUC")
st.markdown("**Estudiantes:** Mariana Pérez & Claret Rodríguez")
st.divider()

# Cargar datos

# Cargar datos
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw", "tmdb_2020_to_2025.csv")

st.sidebar.title("Navegación")
seccion = st.sidebar.radio("Ir a:", ["Inicio", "EDA", "Visualizaciones"])

if seccion == "Inicio":
    st.header("Sobre el proyecto")
    st.write("""
    Este dashboard presenta el análisis exploratorio del dataset **TMDB 2020-2025**,
    una base de datos pública con información de **9,999 películas** producidas a nivel mundial
    entre 2020 y 2025.

    El análisis incluye datos sobre géneros, idiomas, popularidad, calificaciones y fechas de estreno,
    permitiendo identificar tendencias y patrones en la industria cinematográfica global.
    """)

    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎬 Total películas", "9,999")
    col2.metric("🌍 Idiomas", "81")
    col3.metric("📅 Años cubiertos", "2020-2025")
    col4.metric("⭐ Calificación promedio", "5.8")

    st.divider()

    st.info("Usá el menú de la izquierda para navegar entre las secciones.")

elif seccion == "EDA":
    st.header("Análisis Exploratorio de Datos")
    st.write(
        "Exploración estadística del dataset TMDB 2020-2025. Aquí se presentan las métricas descriptivas, distribuciones y patrones principales encontrados en los datos.")
    st.divider()
    cargador = CargadorDatos(ruta)
    df = cargador.cargar()
    procesador = ProcesadorEda(df)
    df_limpio = procesador.limpieza_datos()
    st.subheader("Resumen descriptivo")
    st.dataframe(procesador.resumen_descriptivo())
    st.subheader("Películas por año")
    por_anio = procesador.peliculas_por_anio().reset_index()
    fig_anio = px.bar(por_anio, x="anio_estreno", y="id",
                      title="Películas producidas por año",
                      color_discrete_sequence=["steelblue"])
    fig_anio.update_layout(xaxis_title="Año", yaxis_title="Número de películas")
    st.plotly_chart(fig_anio)
    st.info(
        "La producción se mantiene estable entre 1,400 y 1,900 películas por año. 2022 fue el pico máximo y 2020 el más bajo, probablemente por el impacto del COVID-19.")

    st.subheader("Top 10 géneros más comunes")
    generos = procesador.generos_mas_comunes().reset_index()
    generos.columns = ["genero", "cantidad"]
    fig_generos = px.bar(generos, x="cantidad", y="genero", orientation="h",
                         title="Top 10 géneros más comunes",
                         color_discrete_sequence=["steelblue"])
    fig_generos.update_layout(xaxis_title="Número de películas", yaxis_title="Género")
    st.plotly_chart(fig_generos)
    st.info(
        "Drama es el género más producido con 4,100 películas, casi el doble que Comedia. Una película puede tener varios géneros, por eso los números superan el total de películas.")

    st.subheader("Top 10 idiomas más comunes")
    idiomas = procesador.idiomas_mas_comunes().reset_index()
    idiomas.columns = ["idioma", "cantidad"]
    fig_idiomas = px.bar(idiomas, x="cantidad", y="idioma", orientation="h",
                         title="Top 10 idiomas más comunes",
                         color_discrete_sequence=["steelblue"])
    fig_idiomas.update_layout(xaxis_title="Número de películas", yaxis_title="Idioma")
    st.plotly_chart(fig_idiomas)
    st.info(
        "El inglés domina con el 55% de la producción mundial. Francia y Japón ocupan el segundo y tercer lugar, reflejando su fuerte industria cinematográfica.")

    st.subheader("Top 10 películas más populares")
    st.dataframe(procesador.top_peliculas_populares(), use_container_width=True, hide_index=True)

    st.subheader("Top 10 películas mejor calificadas")
    st.dataframe(procesador.top_peliculas_calificadas(), use_container_width=True, hide_index=True)

    st.subheader("Promedio de calificación por género")
    promedio = procesador.promedio_calificacion_por_genero().reset_index()
    promedio.columns = ["genero", "calificacion"]
    fig_promedio = px.bar(promedio, x="calificacion", y="genero", orientation="h",
                          title="Promedio de calificación por género",
                          color_discrete_sequence=["steelblue"])
    fig_promedio.update_layout(xaxis_title="Calificación promedio", yaxis_title="Género")
    st.plotly_chart(fig_promedio)
    st.info(
        "Animación y Documental son los géneros mejor calificados con 7.25 y 7.23 respectivamente. Terror, a pesar de ser el cuarto género más producido, es el peor calificado con 6.10.")

elif seccion == "Visualizaciones":

    from collections import Counter

    st.header("Visualizaciones")
    st.write(
        "Gráficas interactivas que cuentan la historia del cine mundial entre 2020 y 2025. Podés filtrar por año usando el selector.")
    st.divider()

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
    st.info(
        "La mayoría de las películas se concentran entre 6 y 7.5 de calificación, lo que indica un estándar de calidad medio-alto en la plataforma. Las calificaciones extremas (muy bajas o perfectas) son poco frecuentes.")

    # Gráfico 2 - Barras por año
    st.subheader("¿Cuántas películas se produjeron por año?")
    por_anio = df_limpio.groupby("anio_estreno")["id"].count().reset_index()
    fig2 = px.bar(por_anio, x="anio_estreno", y="id",
                  title="Películas producidas por año TMDB 2020-2025",
                  color_discrete_sequence=["steelblue"])
    fig2.update_layout(xaxis_title="Año", yaxis_title="Número de películas")
    st.plotly_chart(fig2)
    st.info(
        "2022 fue el año con mayor producción cinematográfica con 1,895 películas. 2020 tuvo menos producciones posiblemente por el impacto del COVID-19 en la industria del cine.")

    # Gráfico 3 - Scatter
    st.subheader("¿Las películas más populares son las mejor calificadas?")
    fig3 = px.scatter(df_limpio, x="popularity", y="vote_average",
                      hover_name="title",
                      title="Popularidad vs Calificación TMDB 2020-2025",
                      color_discrete_sequence=["steelblue"])
    fig3.update_layout(xaxis_title="Popularidad", yaxis_title="Calificación promedio")
    st.plotly_chart(fig3)
    st.info(
        "No existe una correlación clara entre popularidad y calificación. Una película puede ser muy popular pero tener calificación media, como se ve con los outliers en el eje de popularidad. Esto indica que popularidad y calidad son métricas independientes.")

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
    st.info(
        "Drama domina ampliamente la producción cinematográfica mundial. Los géneros de entretenimiento masivo como Comedia, Thriller y Terror ocupan los siguientes puestos, reflejando las preferencias del público global.")

    # Gráfico 5 - Heatmap correlación
    st.subheader("¿Qué variables están más relacionadas?")
    import seaborn as sns

    columnas = ["popularity", "vote_average", "vote_count"]
    correlacion = df_limpio[columnas].corr()
    fig5, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(correlacion, annot=True, cmap="Blues", fmt=".2f", linewidths=0.5, ax=ax)
    st.pyplot(fig5)
    st.info(
        "Las variables tienen baja correlación entre sí, siendo la más alta entre vote_average y vote_count (0.16). Esto confirma que popularidad, calificación y número de votos son métricas independientes que miden aspectos distintos de una película.")

    # Gráfico 6 - Top películas más populares
    st.subheader("¿Cuáles son las películas más populares?")
    top_pop = df_limpio[["title", "popularity"]].sort_values("popularity", ascending=False).head(10)
    fig6 = px.bar(top_pop, x="popularity", y="title", orientation="h",
              title="Top 10 películas más populares TMDB 2020-2025",
              color_discrete_sequence=["steelblue"])
    fig6.update_layout(xaxis_title="Popularidad", yaxis_title="Película", yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig6)
    st.info(
        "Las películas de franquicias conocidas lideran en popularidad. Frankenstein es el outlier más extremo con 951 puntos, muy por encima del resto.")

    # Gráfico 7 - Promedio de calificación por género
    st.subheader("¿Qué géneros tienen mejor calificación?")
    datos_genero = df_limpio[df_limpio["vote_count"] >= 50].explode("genre_ids")
    promedio_genero = datos_genero.groupby("genre_ids")["vote_average"].mean().sort_values(ascending=False).round(
    2).reset_index()
    promedio_genero.columns = ["genero", "calificacion"]
    fig7 = px.bar(promedio_genero, x="calificacion", y="genero", orientation="h",
              title="Promedio de calificación por género TMDB 2020-2025",
              color_discrete_sequence=["steelblue"])
    fig7.update_layout(xaxis_title="Calificación promedio", yaxis_title="Género", yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig7)
    st.info(
        "Animación y Documental son los géneros mejor calificados. Terror, a pesar de ser muy producido, tiene las calificaciones más bajas.")

# Gráfico 8 - Top idiomas
st.subheader("¿En qué idiomas se producen más películas?")
top_idiomas = df_limpio["original_language"].value_counts().head(10).reset_index()
top_idiomas.columns = ["idioma", "cantidad"]
fig8 = px.bar(top_idiomas, x="cantidad", y="idioma", orientation="h",
              title="Top 10 idiomas más comunes TMDB 2020-2025",
              color_discrete_sequence=["steelblue"])
fig8.update_layout(xaxis_title="Número de películas", yaxis_title="Idioma", yaxis=dict(autorange="reversed"))
st.plotly_chart(fig8)
st.info(
    "El inglés domina ampliamente con el 55% de la producción mundial. Francia y Japón ocupan el segundo y tercer lugar.")
