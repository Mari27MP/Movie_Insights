import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from eda.cargador_datos import CargadorDatos
from eda.procesador_eda import ProcesadorEda
from visualizacion.visualizador import Visualizador
from helpers.utilidades import Utilidades

def main():
    print("=" * 50)
    print("   TMDB Movie Insights - Programación II")
    print("   Colegio Universitario de Cartago 2026")
    print("=" * 50)

    #Cargar datos

    ruta = os.path.join(os.path.dirname(__file__),  "..", "data", "raw", "tmdb_2020_to_2025.csv")
    ruta = os.path.normpath(ruta)

    if not Utilidades.validar_archivo(ruta):
        return

    cargador = CargadorDatos(ruta)
    df = cargador.cargar()

    #EDA

    procesador = ProcesadorEda(df)
    df_limpio = procesador.limpieza_datos()
    procesador.resumen_descriptivo()
    procesador.matriz_correlacion()
    procesador.peliculas_por_anio()

    # Visualizaciones

    viz = Visualizador(df_limpio)
    viz.histograma_calificaciones()
    viz.barras_por_anio()
    viz.scatter_popularidad_rating()
    viz.heatmap_correlacion()
    viz.barras_top_generos()

    print("=" * 50)
    print("Proceso Finalizado", Utilidades.timestamp())
    print("=" * 50)


if __name__ == "__main__":
    main()

