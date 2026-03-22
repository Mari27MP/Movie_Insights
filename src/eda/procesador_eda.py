
import pandas as pd
import ast # convierte la columna de generos
import os

class ProcesadorEda:
    def __init__(self,df):
        self.df = df.copy()  # copia del DF para no modificar el original

#Limpieza de datos

    def limpieza_datos(self):
        #Eliminar colummnas que no sirven
        self.df.drop(columns=[ "adult", "backdrop_path", "poster_path", "video"], inplace=True)

        #Convertir column release date a formato fecha
        self.df["release_date"] = pd.to_datetime(self.df["release_date"],errors="coerce")

        #Extraer el año de la fecha
        self.df["anio_estreno"]= self.df["release_date"].dt.year

        #Convertir genre_ids de texto a lista
        self.df["genre_ids"]=self.df["genre_ids"].apply(ast.literal_eval)


        # Diccionario de géneros
        generos = {
            28: "Acción",
            12: "Aventura",
            16: "Animación",
            35: "Comedia",
            80: "Crimen",
            99: "Documental",
            18: "Drama",
            10751: "Familia",
            14: "Fantasía",
            36: "Historia",
            27: "Terror",
            10402: "Música",
            9648: "Misterio",
            10749: "Romance",
            878: "Ciencia ficción",
            10770: "Película de TV",
            53: "Thriller",
            10752: "Bélica",
            37: "Western"
        }

        # Reemplazar códigos por nombres
        self.df["genre_ids"] = self.df["genre_ids"].apply(
            lambda x: [generos[g] for g in x if g in generos]
        )

        # Rellenar nulos en overview
        self.df["overview"] = self.df["overview"].fillna("Sin descripcion")

        print("Limpieza de datos completada")
        print("Columnas actuales:", list(self.df.columns))

        # Guardar dataset limpio
        ruta_procesado = "../../data/processed/tmdb_movies_clean.csv"
        os.makedirs(os.path.dirname(ruta_procesado), exist_ok=True)
        self.df.to_csv(ruta_procesado, index=False)
        print(f"Dataset limpio guardado en {ruta_procesado}")

        return self.df



# Resumen descriptivo

    def resumen_descriptivo(self):
        columnas = ["popularity","vote_average","vote_count"]  # variables numericas de interes
        resumen = self.df[columnas].describe()
        print ("Resumen de descriptivo:")
        print(resumen)
        return resumen

# metodo  matriz de correlación.

    def matriz_correlacion(self):
        columnas = ["popularity", "vote_average", "vote_count", "anio_estreno"]
        datos = self.df[self.df["vote_count"] > 0][columnas]
        correlacion = datos.corr()
        print("Matriz de correlacion:")
        print(correlacion)
        return correlacion

# Metodo peliculas por año

    def peliculas_por_anio(self):
        resumen = self.df.groupby("anio_estreno")["id"].count()  # agrupar las peliculas por anios y contarlas
        print("Peliculas por año:")
        print(resumen)
        return resumen

    def top_peliculas_populares(self):
        top = self.df[["title", "popularity"]].sort_values("popularity", ascending=False).head(10)
        print("Top 10 películas más populares:")
        print(top)
        return top



    def top_peliculas_calificadas(self):
        top = self.df[self.df["vote_count"] >= 50][["title", "vote_average", "vote_count"]].sort_values("vote_average",ascending=False).head(10)
        print("Top 10 películas mejor calificadas:")
        print(top)
        return top

    def generos_mas_comunes(self):
        generos = self.df["genre_ids"].explode().value_counts().head(10)
        print("Top 10 géneros más comunes:")
        print(generos)
        return generos

    def idiomas_mas_comunes(self):
        idiomas = self.df["original_language"].value_counts().head(10)
        print("Top 10 idiomas más comunes:")
        print(idiomas)
        return idiomas

    def promedio_calificacion_por_genero(self):
        datos = self.df[self.df["vote_count"] >= 50].explode("genre_ids")
        promedio = datos.groupby("genre_ids")["vote_average"].mean().sort_values(ascending=False).round(2)
        print("Promedio de calificación por género:")
        print(promedio)
        return promedio

    def outliers_popularidad(self):
        q1 = self.df["popularity"].quantile(0.25)
        q3 = self.df["popularity"].quantile(0.75)
        iqr = q3 - q1
        limite = q3 + 1.5 * iqr
        outliers = self.df[self.df["popularity"] > limite][["title", "popularity"]].sort_values("popularity",ascending=False)
        print(f"Películas con popularidad anormalmente alta (>{limite:.2f}):")
        print(outliers)
        return outliers

if __name__=="__main__":
    from cargador_datos import CargadorDatos

    ruta = "../../data/raw/tmdb_2020_to_2025.csv"
    cargador = CargadorDatos(ruta)
    df = cargador.cargar()

    procesador = ProcesadorEda(df)
    procesador.limpieza_datos()
    procesador.resumen_descriptivo()
    procesador.matriz_correlacion()
    procesador.peliculas_por_anio()
    procesador.top_peliculas_populares()
    procesador.top_peliculas_calificadas()
    procesador.generos_mas_comunes()
    procesador.idiomas_mas_comunes()
    procesador.promedio_calificacion_por_genero()
    procesador.outliers_popularidad()