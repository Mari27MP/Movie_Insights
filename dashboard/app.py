import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from eda.cargador_datos import CargadorDatos
from eda.procesador_eda import ProcesadorEda
from visualizacion.visualizador import Visualizador

st.title("TMDB Movie Insights 2020-2025")
st.write("Análisis exploratorio de películas usando datos de TMDB.")


# Cargar datos