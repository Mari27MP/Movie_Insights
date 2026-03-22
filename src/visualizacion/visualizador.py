import matplotlib.pyplot as plt
import pandas as pd


class Visualizador:

    def __init__(self, df):
        self.df = df.copy()

    def histograma_calificaciones(self):
        # Filtrar peliculas que si tienen calificacion
        datos = self.df[self.df["vote_average"] > 0]["vote_average"]

        plt.figure(figsize=(10, 5))
        plt.hist(datos, bins=30, color="red", edgecolor="black")
        plt.title("¿Cómo califican los usuarios las películas? \n TMDB 2020-2025")
        plt.xlabel("Calificación promedio")
        plt.ylabel("Número de películas")
        plt.grid(True)
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