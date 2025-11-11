# Dashboard de Sensor de Luminosidad
# Autor: [Mariana Echeverri]
# Descripción: Visualización de datos del sensor de luminosidad (lux) con estilo moderno.

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

#ESTILO PERSONALIZADO
st.markdown("""
    <style>
    /* Fondo general */
    .main {
        background-color: #F8F9FA;
        font-family: "Inter", sans-serif;
        color: #2C3E50;
        padding: 2rem;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #1E3D58;
        font-weight: 700;
    }

    /* Tarjetas (métricas) */
    .stMetric {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }

    /* Gráficos */
    .plot-container {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 1px 1px 8px rgba(0,0,0,0.05);
    }

    /* Expander y tablas */
    .streamlit-expanderHeader {
        background-color: #E9ECEF;
        border-radius: 6px;
        color: #1E3D58;
        font-weight: 500;
    }

    /* Pie de página */
    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ENCABEZADO
st.markdown("""
    <div style="background-color:#FFFFFF; padding:20px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);">
        <h1 style="text-align:center; margin-bottom:0;">Sensor de Luminosidad - Universidad EAFIT</h1>
        <p style="text-align:center; color:#555;">Monitoreo y análisis de la intensidad lumínica en el campus universitario</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("")

# UBICACIÓN
st.subheader("Ubicación del sensor")
eafit_location = pd.DataFrame({'lat': [6.2006], 'lon': [-75.5783]})
st.map(eafit_location, zoom=15, size=50)

# CARGA DE DATOS
st.markdown("### Cargar archivo CSV con lecturas de luminosidad (lux)")
uploaded_file = st.file_uploader("Seleccione el archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Cargar datos
        df = pd.read_csv(uploaded_file)

        # Normalizar columnas
        if 'Time' in df.columns:
            df['Time'] = pd.to_datetime(df['Time'])
            df = df.rename(columns={df.columns[1]: 'Luminosidad (lux)'})
        else:
            df = df.rename(columns={df.columns[0]: 'Luminosidad (lux)'})
            df['Time'] = pd.date_range(start=datetime.now(), periods=len(df), freq='min')

        df = df.set_index('Time')

        # Estadísticas básicas
        mean_val = df['Luminosidad (lux)'].mean()
        max_val = df['Luminosidad (lux)'].max()
        min_val = df['Luminosidad (lux)'].min()
        current_val = df['Luminosidad (lux)'].iloc[-1]

        # MÉTRICAS
        st.markdown("### Indicadores principales")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Valor actual", f"{current_val:.2f} lux")
        col2.metric("Promedio", f"{mean_val:.2f} lux")
        col3.metric("Máximo", f"{max_val:.2f} lux")
        col4.metric("Mínimo", f"{min_val:.2f} lux")

        st.markdown("---")

        # GRÁFICOS
        st.markdown("### Visualización de datos")

        # Línea temporal
        fig_line = px.line(
            df,
            y='Luminosidad (lux)',
            title="Evolución temporal de la luminosidad",
            labels={'Time': 'Tiempo', 'Luminosidad (lux)': 'Luminosidad (lux)'},
            template="plotly_white",
            color_discrete_sequence=['#3B82F6']
        )
        fig_line.update_traces(line=dict(width=2.5))
        fig_line.update_layout(
            title_x=0.5,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14)
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Histograma de distribución
        st.markdown("### Distribución de valores de luminosidad")
        fig_hist = px.histogram(
            df,
            x='Luminosidad (lux)',
            nbins=25,
            title="Distribución de luminosidad",
            color_discrete_sequence=['#10B981'],
            template="plotly_white"
        )
        fig_hist.update_layout(title_x=0.5)
        st.plotly_chart(fig_hist, use_container_width=True)

        # ======== DATOS ========
        with st.expander("Ver tabla de datos"):
            st.dataframe(df.style.highlight_max(axis=0, color='#D4EFDF'))

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

else:
    st.info("Cargue un archivo CSV para comenzar el análisis.")

# PIE DE PÁGINA
st.markdown("""
---
<div style="text-align:center; color:#555;">
    <p>Proyecto desarrollado para el curso de Computación Física e IoT- Universidad EAFIT</p>
    <p>Autor: [Mariana Echeverri]</p>
</div>
""", unsafe_allow_html=True)
