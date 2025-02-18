import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import folium_static
import openrouteservice

# Cargar los datos
barrios_geojson = "Barrios_valencia.geojson"
barrios_gdf = gpd.read_file(barrios_geojson)
pisos = pd.read_json("DATASET_FINAL.json")
colegios_con_barrio = pd.read_csv("colegios_por_barrio.csv")
hospitales_con_barrio = pd.read_csv("hospitales_por_barrio.csv")
parques_con_barrio = pd.read_csv("parques_por_barrio.csv")
buses_con_barrio = pd.read_csv("bus_por_barrio.csv")
tram_con_barrio = pd.read_csv("tram_por_barrio.csv")

# Configurar Streamlit
st.title("Mapa Interactivo de Valencia")

# Crear el mapa centrado en Valencia
m = folium.Map(location=[39.4699, -0.3763], zoom_start=12)

# Añadir polígonos de barrios
for _, row in barrios_gdf.iterrows():
    folium.GeoJson(row["geometry"], name=row["NOMBRE"], tooltip=row["NOMBRE"]).add_to(m)

# Cliente de OpenRouteService
ORS_API_KEY = "TU_API_KEY_AQUI"  # Reemplaza con tu clave de API de OpenRouteService
client = openrouteservice.Client(key=ORS_API_KEY)

# Selección de origen y destino
st.sidebar.header("Calcula una ruta")
origen = st.sidebar.text_input("Origen (lat, lon)", "39.4699, -0.3763")
destino = st.sidebar.text_input("Destino (lat, lon)", "39.4702, -0.3761")

# Selección del tipo de transporte
transporte = st.sidebar.selectbox("Modo de transporte", [
    "foot-walking", "cycling-regular", "driving-car", "driving-hgv", "wheelchair"
])

if st.sidebar.button("Calcular ruta"):
    try:
        coords = [(float(origen.split(",")[1]), float(origen.split(",")[0])),
                  (float(destino.split(",")[1]), float(destino.split(",")[0]))]
        route = client.directions(coords, profile=transporte, format='geojson')
        folium.GeoJson(route, name='Ruta').add_to(m)
    except Exception as e:
        st.sidebar.error(f"Error al calcular la ruta: {e}")

# Mostrar el mapa
folium_static(m)
