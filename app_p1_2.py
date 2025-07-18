import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from PIL import Image
from io import BytesIO
import requests

# --- Paleta de Colores ---
# Definición de colores en formato RGB (0-1) para Matplotlib
color_primario_1_rgb = (14/255, 69/255, 74/255) # 0E454A (Oscuro)
color_primario_2_rgb = (31/255, 255/255, 95/255) # 1FFF5F (Verde vibrante)
color_primario_3_rgb = (255/255, 255/255, 255/255) # FFFFFF (Blanco)

# Colores del logo de Sustrend para complementar
color_sustrend_1_rgb = (0/255, 155/255, 211/255) # 009BD3 (Azul claro)
color_sustrend_2_rgb = (0/255, 140/255, 207/255) # 008CCF (Azul medio)
color_sustrend_3_rgb = (0/255, 54/255, 110/255) # 00366E (Azul oscuro)

# Selección de colores para los gráficos
colors_for_charts = [color_primario_1_rgb, color_primario_2_rgb, color_sustrend_1_rgb, color_sustrend_3_rgb]

# --- Configuración de la página de Streamlit ---
st.set_page_config(
    page_title="Visualizador de Impactos - Proyecto P2.1",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Main Simulation Function ---
def simular_impactos(volumen_total, tasa_recuperacion, factor_emision, factor_sustitucion, precio_mercado):
    """
    Simula los impactos circulares para el Proyecto P2.1 basados en los parámetros de entrada.
    """
    material_valorizado = volumen_total * tasa_recuperacion
    gei_evitado = volumen_total * factor_emision
    antioxidantes_sustituidos = material_valorizado * factor_sustitucion
    ingresos_estimados = antioxidantes_sustituidos * precio_mercado
    
    # Static values from the original script
    personas_capacitadas = 30
    simbiosis_industrial = 5

    return {
        "material_valorizado": material_valorizado,
        "gei_evitado": gei_evitado,
        "antioxidantes_sustituidos": antioxidantes_sustituidos,
        "ingresos_estimados": ingresos_estimados,
        "personas_capacitadas": personas_capacitadas,
        "simbiosis_industrial": simbiosis_industrial
    }

# --- Header Section ---
st.title('✨ Visualizador de Impactos - Proyecto P2.1')
st.subheader('Recuperación de Descartes Hortofrutícola con propiedades herbicidas')
st.markdown("""
    Ajusta los parámetros para explorar cómo las proyecciones de impacto ambiental y económico del proyecto
    varían con diferentes escenarios de volumen total, tasa de recuperación, factores de emisión y sustitución, y precio de mercado.
""")

# --- Sidebar for Inputs ---
st.sidebar.header("Parámetros de Simulación")

volumen_total = st.sidebar.slider(
    "Volumen Total Disponible (ton/año)",
    min_value=50,
    max_value=200,
    step=10,
    value=90,
    help="Cantidad total de descartes hortofrutícolas disponibles para valorización anualmente."
)

tasa_recuperacion = st.sidebar.slider(
    "Tasa de Recuperación (%)",
    min_value=0.10,
    max_value=0.50,
    step=0.01,
    value=0.276,
    format="%.1f%%",
    help="Porcentaje de material recuperado del volumen total disponible."
)

factor_emision = st.sidebar.slider(
    "Factor de Emisión (tCO₂e/ton)",
    min_value=0.5,
    max_value=2.0,
    step=0.1,
    value=0.8,
    help="Factor de emisión de GEI evitado por tonelada de descarte valorizado."
)

factor_sustitucion = st.sidebar.slider(
    "Factor de Sustitución (%)",
    min_value=0.10,
    max_value=0.50,
    step=0.01,
    value=0.20,
    format="%.1f%%",
    help="Porcentaje de antioxidantes sintéticos que pueden ser sustituidos por el material valorizado."
)

precio_mercado = st.sidebar.slider(
    "Precio de Mercado (USD/ton)",
    min_value=1000,
    max_value=10000,
    step=500,
    value=4000,
    help="Precio estimado en el mercado para los antioxidantes naturales sustituidos."
)

# --- Perform Simulation ---
resultados = simular_impactos(
    volumen_total,
    tasa_recuperacion,
    factor_emision,
    factor_sustitucion,
    precio_mercado
)

# --- Display Metrics ---
st.header("Resultados Clave del Proyecto (Proyección Anual)")
col1, col2, col3, col4 = st.columns(4)

# Data línea base (según ficha de ejemplo para P2.1, ajustada)
base_material = 24.8
base_gei = 72
base_antiox = 4.96
base_ingresos = 19840

with col1:
    st.metric(
        label="🌳 **Material Valorizado**",
        value=f"{resultados['material_valorizado']:.2f} ton/año",
        delta=f"{(resultados['material_valorizado'] - base_material):.2f} ton"
    )
    st.caption("Cantidad de material residual transformado en un nuevo producto.")
with col2:
    st.metric(
        label="💨 **Emisiones GEI Evitadas**",
        value=f"{resultados['gei_evitado']:.2f} tCO₂e/año",
        delta=f"{(resultados['gei_evitado'] - base_gei):.2f} tCO₂e"
    )
    st.caption("Reducción de gases de efecto invernadero por evitar la disposición de residuos.")
with col3:
    st.metric(
        label="🧪 **Antioxidantes Sustituidos**",
        value=f"{resultados['antioxidantes_sustituidos']:.2f} ton/año",
        delta=f"{(resultados['antioxidantes_sustituidos'] - base_antiox):.2f} ton"
    )
    st.caption("Cantidad de antioxidantes sintéticos reemplazados por los de origen natural.")
with col4:
    st.metric(
        label="💰 **Ingresos Estimados**",
        value=f"USD {resultados['ingresos_estimados']:,.2f}",
        delta=f"USD {(resultados['ingresos_estimados'] - base_ingresos):,.2f}"
    )
    st.caption("Estimación de ingresos generados por la venta del material valorizado.")

st.header("Otros Indicadores de Impacto")
col_otros1, col_otros2 = st.columns(2)
with col_otros1:
    st.metric(
        label="👥 **Personas Capacitadas**",
        value=f"{resultados['personas_capacitadas']}",
        help="Número de personas capacitadas por el proyecto."
    )
with col_otros2:
    st.metric(
        label="🤝 **Simbiosis Industrial**",
        value=f"{resultados['simbiosis_industrial']} interacciones",
        help="Número de alianzas o interacciones de simbiosis industrial generadas."
    )

st.markdown("---")

st.header('📊 Análisis Gráfico de Impactos')

# --- Visualización (Gráficos 2D con Matplotlib) ---
# Data for charts (using the base values defined above)
labels = ['Línea Base', 'Proyección Actual']
bar_width = 0.6
x = np.arange(len(labels))

# Create a figure with 3 subplots (2D)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7), facecolor=color_primario_3_rgb)
fig.patch.set_facecolor(color_primario_3_rgb)

# --- Gráfico 1: Emisiones de GEI Evitadas (tCO₂e/año) ---
gei_values = [base_gei, resultados['gei_evitado']]
bars1 = ax1.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax1.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax1.set_title('Emisiones de GEI Evitadas', fontsize=14, color=colors_for_charts[3], pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax1.yaxis.set_tick_params(colors=colors_for_charts[0])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(axis='x', length=0)
max_gei_val = max(gei_values)
ax1.set_ylim(bottom=0, top=max(max_gei_val * 1.15, 10)) # Asegura un margen superior o mínimo 10
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 2: Material Valorizado (ton/año) ---
material_values = [base_material, resultados['material_valorizado']]
bars2 = ax2.bar(x, material_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax2.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[0])
ax2.set_title('Material Valorizado', fontsize=14, color=colors_for_charts[3], pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax2.yaxis.set_tick_params(colors=colors_for_charts[0])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(axis='x', length=0)
max_material_val = max(material_values)
ax2.set_ylim(bottom=0, top=max(max_material_val * 1.15, 5)) # Asegura un margen superior o mínimo 5
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 3: Ingresos Estimados (USD/año) ---
ingresos_values = [base_ingresos, resultados['ingresos_estimados']]
bars3 = ax3.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax3.set_ylabel('USD/año', fontsize=12, color=colors_for_charts[3])
ax3.set_title('Ingresos Estimados', fontsize=14, color=colors_for_charts[3], pad=20)
ax3.set_xticks(x)
ax3.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax3.yaxis.set_tick_params(colors=colors_for_charts[0])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.tick_params(axis='x', length=0)
max_ingresos_val = max(ingresos_values)
ax3.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 5000)) # Asegura un margen superior o mínimo 5000
for bar in bars3:
    yval = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"${yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
st.pyplot(fig)

# --- Funcionalidad de descarga de cada gráfico ---
st.markdown("---")
st.subheader("Descargar Gráficos Individualmente")

# Función auxiliar para generar el botón de descarga
def download_button(fig, filename_prefix, key):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button(
        label=f"Descargar {filename_prefix}.png",
        data=buf.getvalue(),
        file_name=f"{filename_prefix}.png",
        mime="image/png",
        key=key
    )

# Crear figuras individuales para cada gráfico para poder descargarlas
# Figura 1: GEI Evitadas
fig_gei, ax_gei = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_gei.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax_gei.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax_gei.set_title('Emisiones de GEI Evitadas', fontsize=14, color=colors_for_charts[3], pad=20)
ax_gei.set_xticks(x)
ax_gei.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_gei.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_gei.spines['top'].set_visible(False)
ax_gei.spines['right'].set_visible(False)
ax_gei.tick_params(axis='x', length=0)
ax_gei.set_ylim(bottom=0, top=max(max_gei_val * 1.15, 10))
for bar in ax_gei.patches:
    yval = bar.get_height()
    ax_gei.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_gei, "GEI_Evitadas", "download_gei")
plt.close(fig_gei)

# Figura 2: Material Valorizado
fig_material, ax_material = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_material.bar(x, material_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax_material.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[0])
ax_material.set_title('Material Valorizado', fontsize=14, color=colors_for_charts[3], pad=20)
ax_material.set_xticks(x)
ax_material.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_material.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_material.spines['top'].set_visible(False)
ax_material.spines['right'].set_visible(False)
ax_material.tick_params(axis='x', length=0)
ax_material.set_ylim(bottom=0, top=max(max_material_val * 1.15, 5))
for bar in ax_material.patches:
    yval = bar.get_height()
    ax_material.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_material, "Material_Valorizado", "download_material")
plt.close(fig_material)

# Figura 3: Ingresos Estimados
fig_ingresos, ax_ingresos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_ingresos.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax_ingresos.set_ylabel('USD/año', fontsize=12, color=colors_for_charts[3])
ax_ingresos.set_title('Ingresos Estimados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_ingresos.set_xticks(x)
ax_ingresos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_ingresos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_ingresos.spines['top'].set_visible(False)
ax_ingresos.spines['right'].set_visible(False)
ax_ingresos.tick_params(axis='x', length=0)
ax_ingresos.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 5000))
for bar in ax_ingresos.patches:
    yval = bar.get_height()
    ax_ingresos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"${yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_ingresos, "Ingresos_Estimados", "download_ingresos")
plt.close(fig_ingresos)

st.markdown("---")
st.markdown("### Información Adicional:")
st.markdown(f"- **Estado de Avance y Recomendaciones:** El Proyecto P2 se encuentra en una etapa avanzada de validación de laboratorio, con estudios que han confirmado el potencial herbicida de extractos obtenidos a partir de residuos hortofrutícolas, como el pelón de nuez. La evidencia científica preliminar respalda su capacidad fitotóxica selectiva, lo que constituye un insumo clave para el desarrollo de bioherbicidas comerciales en reemplazo de productos sintéticos de importación.")


st.markdown("---")
# Texto de atribución centrado
st.markdown("<div style='text-align: center;'>Visualizador Creado por el equipo Sustrend SpA en el marco del Proyecto TT GREEN Foods</div>", unsafe_allow_html=True)

# Aumentar el espaciado antes de los logos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Mostrar Logos ---
col_logos_left, col_logos_center, col_logos_right = st.columns([1, 2, 1])

with col_logos_center:
    sustrend_logo_url = "https://drive.google.com/uc?id=1vx_znPU2VfdkzeDtl91dlpw_p9mmu4dd"
    ttgreenfoods_logo_url = "https://drive.google.com/uc?id=1uIQZQywjuQJz6Eokkj6dNSpBroJ8tQf8"

    try:
        # Load Sustrend and TT Green Foods logos
        sustrend_response = requests.get(sustrend_logo_url)
        sustrend_response.raise_for_status()
        sustrend_image = Image.open(BytesIO(sustrend_response.content))

        ttgreenfoods_response = requests.get(ttgreenfoods_logo_url)
        ttgreenfoods_response.raise_for_status()
        ttgreenfoods_image = Image.open(BytesIO(ttgreenfoods_response.content))

        # Load additional logos
        creas_response = requests.get(creas_logo_url)
        creas_response.raise_for_status()
        creas_image = Image.open(BytesIO(creas_response.content))

        corfo_response = requests.get(corfo_logo_url)
        corfo_response.raise_for_status()
        corfo_image = Image.open(BytesIO(corfo_response.content))
        
        ciisa_response = requests.get(ciisa_logo_url)
        ciisa_response.raise_for_status()
        ciisa_image = Image.open(BytesIO(ciisa_response.content))

        # Display logos in a row
        logo_cols = st.columns(5) # Adjust number of columns based on how many logos you have
        with logo_cols[0]:
            st.image(sustrend_image, width=80)
        with logo_cols[1]:
            st.image(ttgreenfoods_image, width=80)
        with logo_cols[2]:
            st.image(creas_image, width=80)
        with logo_cols[3]:
            st.image(corfo_image, width=80)
        with logo_cols[4]:
            st.image(ciisa_image, width=80)

    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar los logos desde las URLs. Por favor, verifica los enlaces: {e}")
    except Exception as e:
        st.error(f"Error inesperado al procesar las imágenes de los logos: {e}")

st.markdown("<div style='text-align: center; font-size: small; color: gray;'>Viña del Mar, Valparaíso, Chile</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align: center; font-size: smaller; color: gray;'>Versión del Visualizador: 1.0 (Proyecto P2.1)</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='text-align: center; font-size: x-small; color: lightgray;'>Desarrollado con Streamlit</div>", unsafe_allow_html=True)
