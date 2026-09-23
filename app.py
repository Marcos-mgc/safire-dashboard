import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="SAFIRE - Municipal Data Dashboard", page_icon="🏢", layout="wide")

st.title("🏢 SAFIRE: Portal de Viabilidad Urbanística y Burocrática")
st.markdown("Herramienta de análisis para inversores inmobiliarios: Cruzando datos municipales y tiempos de tramitación en Portugal.")

# 2. Base de datos simulada de municipios (Simulando los datos que extraerías en el challenge)
data = {
    "Municipio": ["Lisboa", "Oporto", "Cascais", "Coímbra", "Braga", "Faro"],
    "Region": ["Lisboa", "Norte", "Lisboa", "Centro", "Norte", "Algarve"],
    "Tiempo_Licencia_Dias": [210, 150, 240, 90, 110, 130],
    "Coste_Suelo_m2": [3500, 2200, 4100, 1200, 1400, 2000],
    "Tasa_Aprobacion_%": [72, 85, 65, 90, 88, 80],
    "Calidad_Dato": ["Medio", "Alto", "Bajo", "Alto", "Alto", "Medio"]
}

df = pd.DataFrame(data)

# 3. Barra lateral de filtros (Filtros interactivos)
st.sidebar.header("🔍 Filtros de Inversión")
region_seleccionada = st.sidebar.selectbox("Selecciona Región:", ["Todas"] + list(df["Region"].unique()))

if region_seleccionada != "Todas":
    df_filtrado = df[df["Region"] == region_seleccionada]
else:
    df_filtrado = df

max_dias = st.sidebar.slider("Máximo días de espera aceptables:", min_to=60, max_value=300, value=250, step=10)
df_filtrado = df_filtrado[df_filtrado["Tiempo_Licencia_Dias"] <= max_dias]

# 4. Tarjetas de Métricas Principales (KPIs arriba)
st.markdown("### 📊 Indicadores Clave de Mercado")
col1, col2, col3 = st.columns(3)

if not df_filtrado.empty:
    tiempo_medio = int(df_filtrado["Tiempo_Licencia_Dias"].mean())
    coste_medio = int(df_filtrado["Coste_Suelo_m2"].mean())
    aprobacion_media = int(df_filtrado["Tasa_Aprobacion_%"].mean())
    
    col1.metric("⏱️ Tiempo Medio de Licencia", f"{tiempo_medio} días", delta="-12 días vs media nacional" if tiempo_medio < 170 else "+30 días (Riesgo alto)", delta_color="inverse")
    col2.metric("💶 Coste Medio del Suelo", f"{coste_medio} €/m²")
    col3.metric("📈 Tasa de Éxito de Aprobación", f"{aprobacion_media}%")
else:
    st.warning("No hay municipios que cumplan con los filtros seleccionados.")

st.markdown("---")

# 5. Gráficos Interactivos (El núcleo visual con Plotly)
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("⏱️ Retraso Burocrático por Municipio")
    fig_bar = px.bar(df_filtrado, x="Municipio", y="Tiempo_Licencia_Dias", color="Municipio",
                     text="Tiempo_Licencia_Dias", title="Días de espera para concesión de licencias")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_g2:
    st.subheader("⚠️ Coste de Suelo vs. Plazos Burocráticos")
    fig_scatter = px.scatter(df_filtrado, x="Coste_Suelo_m2", y="Tiempo_Licencia_Dias", 
                             size="Tasa_Aprobacion_%", color="Calidad_Dato", hover_name="Municipio",
                             title="Matriz de Riesgo: Precio vs Burocracia")
    st.plotly_chart(fig_scatter, use_container_width=True)

# 6. Tabla de Datos Auditados (Para cumplir con la auditoría del Track B)
st.markdown("### 📋 Auditoría de Datos Municipales")
st.dataframe(df_filtrado, use_container_width=True)

# 7. Conclusión o Juicio de Viabilidad Automatizado
st.info("💡 **Juicio de Viabilidad SAFIRE:** Los municipios con alta calidad de datos y plazos inferiores a 150 días (como Oporto o Braga) presentan la mejor relación riesgo-beneficio para la promoción inmobiliaria a corto plazo.")