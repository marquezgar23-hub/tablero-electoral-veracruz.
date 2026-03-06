import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

"""
=============================================================================
SISTEMA DE INTELIGENCIA ELECTORAL - STREAMLIT APP
Dashboard web interactivo, estetico y de alta fiabilidad estadistica.
=============================================================================
"""

st.set_page_config(page_title="Inteligencia Electoral", layout="wide", initial_sidebar_state="expanded")

class MotorStreamlit:
    def __init__(self):
        self.lista_distritos = [
            'Panuco', 'Tantoyuca', 'Tuxpan', 'Alamo', 'Poza Rica', 'Papantla',
            'Martinez de la Torre', 'Misantla', 'Perote', 'Xalapa I', 'Xalapa II',
            'Coatepec', 'Emiliano Zapata', 'Veracruz I', 'Veracruz II', 'Boca del Rio',
            'Alvarado', 'Huatusco', 'Cordoba', 'Orizaba', 'Rio Blanco', 'Zongolica',
            'Cosamaloapan', 'Santiago Tuxtla', 'San Andres Tuxtla', 'Cosoleacaque',
            'Acayucan', 'Minatitlan', 'Coatzacoalcos I', 'Coatzacoalcos II'
        ]
        self.latitudes = [22.017, 21.350, 20.950, 20.917, 20.533, 20.450, 20.067, 19.933, 19.560, 19.543, 19.513, 19.450, 19.350, 19.193, 19.173, 19.100, 18.767, 19.150, 18.883, 18.850, 18.830, 18.660, 18.367, 18.460, 18.450, 18.000, 17.950, 17.983, 18.150, 18.130]
        self.longitudes = [-98.183, -98.233, -97.400, -97.717, -97.450, -97.317, -97.050, -96.850, -97.240, -96.927, -96.907, -96.967, -96.750, -96.143, -96.133, -96.117, -95.767, -96.960, -96.933, -97.100, -97.150, -97.000, -95.800, -95.300, -95.217, -94.630, -94.917, -94.550, -94.450, -94.430]
        self.colores = {'Sigamos Haciendo Historia': '#8B0000', 'Fuerza y Corazon por Veracruz': '#00008B', 'Movimiento Ciudadano': '#FF8C00'}

    @st.cache_data
    def cargar_datos_territoriales(_self):
        filas_datos = []
        generador = np.random.default_rng(2024)
        for indice in range(30):
            nombre = _self.lista_distritos[indice]
            votos_oficialismo = generador.normal(55000, 10000)
            votos_oposicion = generador.normal(45000, 12000)
            votos_movimiento = generador.normal(15000, 5000)
            tasa_participacion = generador.uniform(45.0, 65.0)
            gasto_campana = generador.uniform(1.0, 5.0)
            indice_socioeconomico = generador.uniform(30.0, 80.0)
            impacto_juventud = generador.integers(10, 100)
            ganador = 'Sigamos Haciendo Historia' if votos_oficialismo > votos_oposicion else 'Fuerza y Corazon por Veracruz'
            filas_datos.append([nombre, _self.latitudes[indice], _self.longitudes[indice], votos_oficialismo, votos_oposicion, votos_movimiento, tasa_participacion, gasto_campana, indice_socioeconomico, impacto_juventud, ganador])
        columnas = ['Distrito', 'Latitud', 'Longitud', 'Votos_SHH', 'Votos_FYCV', 'Votos_MC', 'Participacion', 'Gasto', 'Socioeconomico', 'Movilizacion_Joven', 'Ganador']
        return pd.DataFrame(filas_datos, columns=columnas)

    @st.cache_data
    def cargar_datos_historicos(_self):
        return pd.DataFrame({
            'Año': ['2016', '2018', '2021', '2024'],
            'Participacion_Jovenes': [42.5, 58.3, 49.1, 61.5],
            'Participacion_Nacional': [54.2, 65.1, 57.4, 60.3]
        })

    @st.cache_data
    def cargar_datos_metodos(_self):
        return pd.DataFrame({'Metodo': ['Casilla', 'Anticipado', 'Correo', 'Extranjero'], 'Votos': [82.5, 12.0, 4.5, 1.0]})

    @st.cache_data
    def cargar_datos_congreso(_self):
        return pd.DataFrame({
            'Coalicion': ['SHH', 'SHH', 'SHH', 'FYCV', 'FYCV', 'MC'],
            'Partido': ['MORENA', 'PVEM', 'PT', 'PAN', 'PRI', 'MC'],
            'Escanos': [21, 5, 4, 11, 6, 3]
        })

motor = MotorStreamlit()
df = motor.cargar_datos_territoriales()
df_hist = motor.cargar_datos_historicos()
df_met = motor.cargar_datos_metodos()
df_congreso = motor.cargar_datos_congreso()

st.title("Cuarto de Guerra Electoral - Analisis Multidimensional")
st.markdown("Plataforma de inteligencia de datos basada en granularidad geografica, demografia, e interacciones socioeconomicas.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Mapa Coroplético Regional")
    fig1 = px.scatter_geo(df, lat='Latitud', lon='Longitud', color='Ganador', size='Participacion', hover_name='Distrito', color_discrete_map=motor.colores, projection='mercator')
    fig1.update_geos(fitbounds="locations", visible=False, showcoastlines=True, coastlinecolor="LightGray")
    fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("2. Gráfico de Barras: Apoyo Total")
    datos_barras = pd.DataFrame({'Fuerza Politica': ['SHH', 'FYCV', 'MC'], 'Votos Totales': [df['Votos_SHH'].sum(), df['Votos_FYCV'].sum(), df['Votos_MC'].sum()]})
    fig2 = px.bar(datos_barras, x='Fuerza Politica', y='Votos Totales', color='Fuerza Politica', color_discrete_sequence=['#8B0000', '#00008B', '#FF8C00'])
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("3. Gráfico Circular: Métodos de Votación")
    fig3 = px.pie(df_met, values='Votos', names='Metodo', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("4. Gráfico de Líneas: Evolución Participativa")
    fig4 = px.line(df_hist, x='Año', y=['Participacion_Nacional', 'Participacion_Jovenes'], markers=True)
    fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig4, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    st.subheader("5. Mapa de Calor: Intensidad de Movilización")
    matriz_calor = df[['Distrito', 'Participacion', 'Movilizacion_Joven']].sort_values(by='Participacion', ascending=False).head(15)
    fig5 = px.density_heatmap(matriz_calor, x='Distrito', y='Participacion', z='Movilizacion_Joven', color_continuous_scale='YlOrRd')
    fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("6. Gráfico de Burbujas: Gasto vs Resultados")
    fig6 = px.scatter(df, x='Gasto', y='Votos_SHH', size='Movilizacion_Joven', color='Ganador', hover_name='Distrito', size_max=40, color_discrete_map=motor.colores)
    fig6.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig6, use_container_width=True)

col7, col8 = st.columns(2)

with col7:
    st.subheader("7. Dispersión: Socioeconomía y Participación")
    fig7 = px.scatter(df, x='Socioeconomico', y='Participacion', color='Ganador', trendline='ols', color_discrete_map=motor.colores)
    fig7.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    st.subheader("8. Treemap: Distribución Legislativa Jerárquica")
    fig8 = px.treemap(df_congreso, path=['Coalicion', 'Partido'], values='Escanos', color='Coalicion')
    fig8.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig8, use_container_width=True)