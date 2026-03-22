import pandas as pd
import os


class CargadorDatos:

    def __init__(self, ruta_csv):  # recibe la ruta del archivo
        self.ruta_csv = ruta_csv  # la guarda como atributo
        self.df = None  # aca se guarda el DF cuando se cargue
        self.num_filas = 0  # se guardan las filas del archivo

    def cargar(self):
        if not os.path.exists(self.ruta_csv):  # verifique si el archivo existe
            print("El archivo no existe")
            return None

        self.df = pd.read_csv(self.ruta_csv) # lea el archivo
        if "Unnamed: 0" in self.df.columns:
            self.df.drop(columns=["Unnamed: 0"], inplace=True)

        self.num_filas = len(self.df)  # cuente cuanta filas tiene
        print("Filas cargadas", self.num_filas)

        nulos = self.df.isnull().sum()
        porcentaje_nulos = (self.df.isnull().mean() * 100).round(2)
        print("Valores nulos por columna:")
        print(pd.DataFrame({"cantidad": nulos, "porcentaje %": porcentaje_nulos}))

        return self.df


if __name__ == "__main__":
    ruta = "../../data/raw/tmdb_2020_to_2025.csv"
    cargador = CargadorDatos(ruta)
    df = cargador.cargar()
    print(df.head())
