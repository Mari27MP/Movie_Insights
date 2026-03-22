import os
from datetime import datetime

class Utilidades:

    @staticmethod
    def validar_archivo(ruta):
        if not os.path.exists(ruta):
            print("El archivo no existe:", ruta)
            return False
        print("Archivo encontrado:", ruta)
        return True


    @staticmethod
    def crear_carpeta(ruta):
        os.makedirs(ruta, exist_ok=True)
        print("Carpeta creada",ruta)

    @staticmethod
    def timestamp():
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

if __name__ == "__main__":
    ruta = r"C:\Users\mari2\Desktop\Progra 2\Proyecto2\Movie_Insights\data\raw\tmdb_2020_to_2025.csv"
    Utilidades.validar_archivo(ruta)
    Utilidades.crear_carpeta("../../data/processed")
    print("Fecha y hora actual:", Utilidades.timestamp())
    print(os.path.exists(ruta))
