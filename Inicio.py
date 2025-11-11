
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="💡 Sensor de Luminosidad - EAFIT",
    page_icon="🌞",
    layout="wide"
)

# ESTILO
st.markdown("""
    <style>
    body {
        background-color: #FDFEFE;
    }
    .main {
        background: linear-gradient(180deg, #FDFEFE 0%, #E8F6F3 100%);
        font-family: "Poppins", sans-serif;
        color: #2C3E50;
        padding: 2rem;
    }
    h1, h2, h3 {
        color: #1A5276;
        font-weight: 700;
    }
    .stMetric {
        background-color: #FFFFFF;
        border: 2px solid #D6EAF8;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
    }
    .block-container {
        padding-top: 1rem;
    }
    .metric-label {
        font-weight: bold;
        color: #154360;
    }
    .stTabs [role="tablist"] {
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# ENCABEZADO
st.markdown("""
<div style="background-color:#FDFEFE; padding:20px; border-radius:10px; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.05);">
    <h1>🌞 Sensor de Luminosidad - Universidad EAFIT</h1>
    <p style="color:#117864; font-size:16px;">Analiza cómo varía la luz ambiental en la universidad.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# MAPA DEL SENSOR
st.subheader("📍 Ubicación del sensor")
eafit_location = pd.DataFrame({'lat': [6.2006], 'lon': [-75.5783]})
st.map(eafit_location, zoom=15, size=60)

st.markdown("### 📁 Cargar archivo CSV con lecturas de luminosidad (lux)")
uploaded_file = st.file_uploader("Selecciona tu archivo CSV", type=["csv"])

# PROCESAMIENTO DE DATOS
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Procesar columnas
        if 'Time' in df.columns:
            df['Time'] = pd.to_datetime(df['Time'])
            df = df.rename(columns={df.columns[1]: 'Luminosidad (lux)'})
        else:
            df = df.rename(columns={df.columns[0]: 'Luminosidad (lux)'})
            df['Time'] = pd.date_range(start=datetime.now(), periods=len(df), freq='min')

        df = df.set_index('Time')

        # Calcular estadísticas
        mean_val = df['Luminosidad (lux)'].mean()
        max_val = df['Luminosidad (lux)'].max()
        min_val = df['Luminosidad (lux)'].min()
        current_val = df['Luminosidad (lux)'].iloc[-1]

        # MÉTRICAS COLOR
        st.markdown("## ✨ Indicadores Principales")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🔆 Valor actual", f"{current_val:.2f} lux")
        col2.metric("🌤️ Promedio", f"{mean_val:.2f} lux")
        col3.metric("☀️ Máximo", f"{max_val:.2f} lux")
        col4.metric("🌙 Mínimo", f"{min_val:.2f} lux")

        st.markdown("---")

       
        # GRÁFICOS 
        st.markdown("## 📊 Visualización de Datos")

        # Gráfico de línea
        fig_line = px.line(
            df,
            y='Luminosidad (lux)',
            title="📈 Evolución temporal de la luminosidad",
            labels={'Time': 'Tiempo', 'Luminosidad (lux)': 'Luminosidad (lux)'},
            color_discrete_sequence=['#2E86DE'],
            template="plotly_white"
        )
        fig_line.update_traces(line=dict(width=3))
        fig_line.update_layout(
            title_x=0.5,
            font=dict(size=14),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Histograma de distribución
        st.markdown("## 🌈 Distribución de Luminosidad")
        fig_hist = px.histogram(
            df,
            x='Luminosidad (lux)',
            nbins=25,
            title="🌤️ Distribución de los valores medidos",
            color_discrete_sequence=['#1ABC9C'],
            template="plotly_white"
        )
        fig_hist.update_layout(title_x=0.5)
        st.plotly_chart(fig_hist, use_container_width=True)

        # Mostrar tabla con estilo
        with st.expander("📋 Ver datos en tabla"):
            st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Ocurrió un error al procesar el archivo: {e}")

else:
    st.info("👆 Carga un archivo CSV para comenzar el análisis.")

# PIE DE PÁGINA
st.markdown("""
---
<div style="text-align:center; color:#117A65;">
    <p>💻 Proyecto de Computación Física e IoT- Universidad EAFIT</p>
    <p>Mariana Echeverri</p>
</div>
""", unsafe_allow_html=True)
