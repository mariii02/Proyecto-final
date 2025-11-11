# Dashboard de Sensor de Luminosidad
# Autor: [Tu nombre]
# Descripción: Aplicación en Streamlit para analizar datos de luminosidad (lux)

import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Sensor de Luminosidad - EAFIT",
    page_icon="💡",
    layout="wide"
)

# Estilos personalizados (tema claro, moderno)
st.markdown("""
    <style>
    .main {
        background-color: #FAFAFA;
        padding: 2rem;
        font-family: "Segoe UI", sans-serif;
    }
    h1, h2, h3 {
        color: #2C3E50;
    }
    .stMetric {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Título y descripción
st.title("Sensor de Luminosidad - Universidad EAFIT")
st.markdown(
    "Aplicación para visualizar y analizar los datos obtenidos del sensor de luminosidad instalado en el campus universitario."
)

# Mapa de ubicación del sensor
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783]
})
st.map(eafit_location, zoom=15, size=50)

st.markdown("### Cargar archivo CSV con lecturas de luminosidad (lux)")

# Subida de archivo
uploaded_file = st.file_uploader("Seleccione un archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Cargar los datos
        df = pd.read_csv(uploaded_file)

        # Detección y limpieza de columnas
        if 'Time' in df.columns:
            df['Time'] = pd.to_datetime(df['Time'])
            df = df.rename(columns={df.columns[1]: 'Luminosidad (lux)'})
        else:
            df = df.rename(columns={df.columns[0]: 'Luminosidad (lux)'})
            df['Time'] = pd.date_range(start=datetime.now(), periods=len(df), freq='min')

        df = df.set_index('Time')

        # Cálculo de estadísticas básicas
        mean_val = df['Luminosidad (lux)'].mean()
        max_val = df['Luminosidad (lux)'].max()
        min_val = df['Luminosidad (lux)'].min()
        current_val = df['Luminosidad (lux)'].iloc[-1]

        # Sección de métricas
        st.markdown("### Indicadores de Luminosidad")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Valor actual", f"{current_val:.2f} lux")
        col2.metric("Promedio", f"{mean_val:.2f} lux")
        col3.metric("Máximo", f"{max_val:.2f} lux")
        col4.metric("Mínimo", f"{min_val:.2f} lux")

        # Gráficos
        st.markdown("### Visualización de Datos")

        # Gráfico de línea temporal
        fig_line = px.line(
            df,
            y='Luminosidad (lux)',
            title="Evolución temporal de la luminosidad",
            labels={'Time': 'Tiempo', 'Luminosidad (lux)': 'Luminosidad (lux)'},
            template="plotly_white",
            color_discrete_sequence=['#3498DB']
        )
        fig_line.update_layout(title_x=0.5)
        st.plotly_chart(fig_line, use_container_width=True)

        # Histograma de distribución
        st.markdown("### Distribución de valores de luminosidad")
        fig_hist = px.histogram(
            df,
            x='Luminosidad (lux)',
            nbins=30,
            title="Distribución de luminosidad",
            color_discrete_sequence=['#1ABC9C'],
            template="plotly_white"
        )
        fig_hist.update_layout(title_x=0.5)
        st.plotly_chart(fig_hist, use_container_width=True)

        # Mostrar tabla opcional
        with st.expander("Ver datos en tabla"):
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

else:
    st.info("Cargue un archivo CSV para comenzar el análisis.")

# Pie de página
st.markdown("""
---
Desarrollado para el curso de Computación Física e IoT
Universidad EAFIT - Medellín, Colombia  
Autor: [Mariana Echeverri Rincón]
""")
