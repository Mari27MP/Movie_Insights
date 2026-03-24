import matplotlib.pyplot as plt
import pandas as pd


class Visualizador:

    def __init__(self, df):
        self.df = df.copy()

    def histograma_calificaciones(self):
        # Filtrar peliculas que si tienen calificacion (mayor a 1)
        datos = self.df[self.df["vote_average"] > 1]["vote_average"]

        plt.figure(figsize=(10, 5))
        plt.hist(datos, bins=30, color="steelblue", edgecolor="black")
        plt.title("¿Cómo califican los usuarios las películas? \n TMDB 2020-2025")
        plt.xlabel("Calificación promedio")
        plt.ylabel("Número de películas")
        plt.gca().set_facecolor("white")
        plt.gcf().set_facecolor("white")
        plt.figtext(0.5, 0.01,
                    "La mayoría de películas se concentran entre 6 y 7 de calificación. Las notas perfectas (10) y muy bajas son poco frecuentes.",
                    ha="center", fontsize=9, style="italic")
        plt.show()

    def barras_por_anio(self):
        resumen = self.df.groupby("anio_estreno")["id"].count()

        plt.figure(figsize=(10, 5))
        plt.bar(resumen.index.astype(str), resumen.values, color="steelblue", edgecolor="black")
        plt.title("¿Cuántas películas se produjeron por año?\n TMDB 2020-2025")
        plt.xlabel("Año")
        plt.ylabel("Número de películas")
        plt.gca().set_facecolor("white")
        plt.gcf().set_facecolor("white")
        plt.figtext(0.5, 0.01,
                    "2022 fue el año más productivo con ~1,875 películas. 2020 tuvo la menor producción, posiblemente por el impacto del COVID-19.",
                    ha="center", fontsize=9, style="italic")
        plt.show()

    def scatter_popularidad_rating(self):
        plt.figure(figsize=(10, 6))
        plt.scatter(self.df["popularity"], self.df["vote_average"],
                    color="steelblue", alpha=0.5, edgecolors="none")
        plt.title("¿Las películas más populares son las mejor calificadas?\n TMDB 2020-2025")
        plt.xlabel("Popularidad")
        plt.ylabel("Calificación promedio")
        plt.gca().set_facecolor("white")
        plt.gcf().set_facecolor("white")
        plt.figtext(0.5, 0.01,
                    "No hay correlación entre popularidad y calificación. El outlier con 951 puntos de popularidad tiene calificación media de 7.9.",
                    ha="center", fontsize=9, style="italic")
        plt.show()

    def heatmap_correlacion(self):
        import seaborn as sns

        columnas = ["popularity", "vote_average", "vote_count"]
        correlacion = self.df[columnas].corr()

        plt.figure(figsize=(7, 5))
        sns.heatmap(correlacion, annot=True, cmap="Blues", fmt=".2f", linewidths=0.5)
        plt.title("¿Qué variables están más relacionadas?\n Matriz de correlación TMDB 2020-2025")
        plt.gca().set_facecolor("white")
        plt.gcf().set_facecolor("white")
        plt.figtext(0.5, 0.01,
                    "Las tres variables son casi independientes. La correlación más alta es entre vote_average y vote_count (0.20).",
                    ha="center", fontsize=9, style="italic")
        plt.show()

    def barras_top_generos(self):
        from collections import Counter

        todos_generos = []
        for lista in self.df["genre_ids"]:
            todos_generos.extend(lista)

        conteo = Counter(todos_generos)
        top10 = dict(conteo.most_common(10))

        plt.figure(figsize=(10, 6))
        plt.barh(list(top10.keys()), list(top10.values()), color="steelblue", edgecolor="black")
        plt.title("¿Qué tipo de películas domina el cine global?\n Top 10 géneros TMDB 2020-2025")
        plt.xlabel("Número de películas")
        plt.gca().set_facecolor("white")
        plt.gcf().set_facecolor("white")
        plt.figtext(0.5, 0.01,
                    "Drama domina con ~4,100 películas, casi el doble que Comedia. Fantasía y Ciencia ficción son los menos frecuentes del top 10.",
                    ha="center", fontsize=9, style="italic")
        plt.show()

    def barras_top_peliculas_populares(self):
        top = self.df[["title", "popularity"]].sort_values("popularity", ascending=False).head(10)

        plt.figure(figsize=(10, 6))
        plt.barh(top["title"], top["popularity"], color="steelblue", edgecolor="black")
        plt.title("¿Cuáles son las películas más populares?\n Top 10 TMDB 2020-2025")
        plt.xlabel("Popularidad")
        plt.gca().invert_yaxis()
        plt.gca().set_facecolor("white")
        plt.gcf().set_facecolor("white")
        plt.tight_layout()
        plt.figtext(0.5, 0.01,
                    "Frankenstein domina con 951 puntos, muy por encima del resto. Playdate y Predator: Badlands ocupan el segundo y tercer lugar.",
                    ha="center", fontsize=9, style="italic")
        plt.show()

    def barras_promedio_por_genero(self):
        datos = self.df[self.df["vote_count"] >= 50].explode("genre_ids")
        promedio = datos.groupby("genre_ids")["vote_average"].mean().sort_values(ascending=False).round(2)

        plt.figure(figsize=(10, 6))
        plt.barh(promedio.index, promedio.values, color="steelblue", edgecolor="black")
        plt.title("¿Qué géneros tienen mejor calificación?\n Promedio por género TMDB 2020-2025")
        plt.xlabel("Calificación promedio")
        plt.gca().invert_yaxis()
        plt.gca().set_facecolor("white")
        plt.gcf().set_facecolor("white")
        plt.tight_layout()
        plt.figtext(0.5, 0.01,
                    "Animación y Documental lideran con ~7.3 de calificación. Terror es el peor calificado con 6.1, a pesar de ser muy producido.",
                    ha="center", fontsize=9, style="italic")
        plt.show()

    def barras_top_idiomas(self):
        top = self.df["original_language"].value_counts().head(10)

        plt.figure(figsize=(10, 6))
        plt.barh(top.index, top.values, color="steelblue", edgecolor="black")
        plt.title("¿En qué idiomas se producen más películas?\n Top 10 idiomas TMDB 2020-2025")
        plt.xlabel("Número de películas")
        plt.gca().invert_yaxis()
        plt.gca().set_facecolor("white")
        plt.gcf().set_facecolor("white")
        plt.tight_layout()
        plt.figtext(0.5, 0.01,
                    "El inglés domina masivamente con ~5,500 películas. Francés y japonés ocupan el segundo y tercer lugar con menos de 600 cada uno.",
                    ha="center", fontsize=9, style="italic")
        plt.show()


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from eda.cargador_datos import CargadorDatos
    from eda.procesador_eda import ProcesadorEda

    ruta = "../../data/raw/tmdb_2020_to_2025.csv"
    cargador = CargadorDatos(ruta)
    df = cargador.cargar()

    procesador = ProcesadorEda(df)
    df_limpio = procesador.limpieza_datos()

    viz = Visualizador(df_limpio)
    viz.histograma_calificaciones()
    viz.barras_por_anio()
    viz.scatter_popularidad_rating()
    viz.heatmap_correlacion()
    viz.barras_top_generos()

