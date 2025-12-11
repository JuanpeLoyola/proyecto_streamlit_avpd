import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de estilo para matplotlib y seaborn
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Colores personalizados para un aspecto profesional
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff9800',
    'info': '#17a2b8',
    'gradient_start': '#FF6B6B',
    'gradient_end': '#4ECDC4'
}

@st.cache_data
def load_data():
    """Carga todos los datasets procesados"""
    years = [2015, 2016, 2017, 2018, 2019]
    dataframes = {}
    
    for year in years:
        df = pd.read_csv(f'data/{year}_processed.csv')
        df['Year'] = year
        dataframes[year] = df
    
    # Combinar todos los datasets
    combined_df = pd.concat(dataframes.values(), ignore_index=True)
    
    return dataframes, combined_df

def normalize_country_names(df):
    """
    Normaliza los nombres de países para que coincidan con los códigos ISO de Plotly
    """
    country_mapping = {
        'United States': 'United States of America',
        'United Kingdom': 'United Kingdom',
        'Czech Republic': 'Czechia',
        'Taiwan Province of China': 'Taiwan',
        'Hong Kong S.A.R., China': 'Hong Kong',
        'Trinidad and Tobago': 'Trinidad and Tobago',
        'Northern Cyprus': 'Cyprus',
        'North Cyprus': 'Cyprus',
        'Somaliland region': 'Somalia',
        'Palestinian Territories': 'Palestine',
        'Ivory Coast': "Côte d'Ivoire",
    }
    
    df['Country_Display'] = df['Country']  # Guardar nombre original para display
    df['Country_Map'] = df['Country'].replace(country_mapping)
    return df

def plot_happiness_world_map(df_dict, selected_year):
    """
    Visualización 1: Mapamundi interactivo de felicidad por país
    Los países más felices aparecen en rojo oscuro
    Hover muestra nombre del país y valor de felicidad
    """
    df = df_dict[selected_year].copy()
    
    # Normalizar nombres de países
    df = normalize_country_names(df)
    
    # Crear el mapamundi con Plotly
    # Invertir la escala de colores para que rojo oscuro = más feliz
    fig = go.Figure(data=go.Choropleth(
        locations=df['Country_Map'],
        z=df['Happiness Score'],
        locationmode='country names',
        colorscale=[
            [0, '#2c7bb6'],      # Azul oscuro (menos feliz)
            [0.2, '#abd9e9'],    # Azul claro
            [0.4, '#ffffbf'],    # Amarillo
            [0.6, '#fdae61'],    # Naranja
            [0.8, '#d7191c'],    # Rojo
            [1, '#8B0000']       # Rojo oscuro (más feliz)
        ],
        reversescale=False,
        marker_line_color='white',
        marker_line_width=0.5,
        colorbar=dict(
            title=dict(
                text="Nivel de<br>Felicidad",
                font=dict(size=14, family='Arial Black')
            ),
            thickness=20,
            len=0.7,
            x=1.02,
            tickfont=dict(size=12),
        ),
        hovertemplate='<b>%{location}</b><br>' +
                      'Puntuación de Felicidad: %{z:.3f}<br>' +
                      'Ranking: #%{customdata}<br>' +
                      '<extra></extra>',
        customdata=df['Happiness Rank'],
        text=df['Country_Display'],
    ))
    
    # Actualizar el layout para un diseño profesional
    fig.update_layout(
        title=dict(
            text=f'🌍 Mapa Mundial de Felicidad - {selected_year}<br>' +
                 '<sub>Los países en rojo oscuro son los más felices | Pasa el ratón sobre cada país para más información</sub>',
            x=0.5,
            xanchor='center',
            font=dict(size=24, family='Arial Black', color='#1f77b4')
        ),
        geo=dict(
            showframe=True,
            showcoastlines=True,
            coastlinecolor='#333333',
            projection_type='natural earth',
            bgcolor='rgba(243, 243, 243, 1)',
            landcolor='rgb(243, 243, 243)',
            showcountries=True,
            countrycolor='white',
            showlakes=True,
            lakecolor='rgb(204, 229, 255)',
            showocean=True,
            oceancolor='rgb(230, 245, 255)',
        ),
        height=700,
        margin=dict(l=0, r=0, t=100, b=0),
        paper_bgcolor='white',
        font=dict(family='Arial', size=12),
    )
    
    return fig

def plot_happiness_evolution(combined_df, selected_countries, show_global_avg=True):
    """
    Visualización 2: Evolución de la felicidad a lo largo de los años
    Gráfico de líneas simplificado con países seleccionados por el usuario
    """
    # Crear figura con alta resolución (DPI alto para mejor calidad)
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    
    # Si no hay países seleccionados, mostrar mensaje
    if not selected_countries:
        ax.text(0.5, 0.5, 'Selecciona al menos un país para visualizar', 
                ha='center', va='center', fontsize=18, color='gray',
                transform=ax.transAxes, fontweight='bold')
        ax.set_xlim(2015, 2019)
        ax.set_ylim(0, 1)
        ax.axis('off')
        return fig
    
    # Generar paleta de colores vibrantes
    colors_palette = sns.color_palette("bright", len(selected_countries))
    
    # Plotear cada país seleccionado con mejor estilo
    for idx, country in enumerate(selected_countries):
        country_data = combined_df[combined_df['Country'] == country].sort_values('Year')
        if not country_data.empty:
            # Línea principal
            ax.plot(country_data['Year'], country_data['Happiness Score'], 
                   marker='o', linewidth=3.5, markersize=10, label=country,
                   color=colors_palette[idx], alpha=0.9,
                   markeredgecolor='white', markeredgewidth=2,
                   zorder=3)
    
    # Línea de media global si está activada
    if show_global_avg:
        global_avg = combined_df.groupby('Year')['Happiness Score'].mean().reset_index()
        ax.plot(global_avg['Year'], global_avg['Happiness Score'], 
               linestyle='--', linewidth=4, color='#2c3e50', 
               label='Media Global', alpha=0.7, marker='s', markersize=12,
               markeredgecolor='white', markeredgewidth=2,
               zorder=2)
    
    # Configuración del gráfico con mejor tipografía
    ax.set_xlabel('Año', fontsize=16, fontweight='bold', labelpad=10)
    ax.set_ylabel('Puntuación de Felicidad', fontsize=16, fontweight='bold', labelpad=10)
    ax.set_title('Evolución de la Felicidad Mundial (2015-2019)', 
                fontsize=22, fontweight='bold', pad=25, color='#2c3e50')
    
    # Leyenda mejorada
    legend = ax.legend(loc='best', fontsize=12, framealpha=0.98, 
                      shadow=True, fancybox=True, 
                      edgecolor='#cccccc', frameon=True,
                      ncol=2 if len(selected_countries) > 6 else 1)
    legend.get_frame().set_linewidth(1.5)
    
    # Grid más sutil pero visible
    ax.grid(True, alpha=0.25, linestyle='-', linewidth=0.8, color='#bdc3c7', zorder=1)
    ax.set_axisbelow(True)
    
    # Configurar ejes
    ax.set_xticks([2015, 2016, 2017, 2018, 2019])
    ax.set_xticklabels([2015, 2016, 2017, 2018, 2019], fontsize=13, fontweight='600')
    ax.tick_params(axis='y', labelsize=12)
    
    # Mejorar el aspecto de los bordes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_color('#34495e')
    ax.spines['bottom'].set_color('#34495e')
    
    # Fondo sutil
    ax.set_facecolor('#fafafa')
    fig.patch.set_facecolor('white')
    
    plt.tight_layout()
    return fig

def plot_income_happiness_boxplot(combined_df, year):
    """
    ALTERNATIVA AL SCATTER PLOT: Diagrama de Caja por Niveles Económicos.
    Agrupa los países en 4 cuartiles según su PIB y muestra la distribución de felicidad.
    Es más limpio y analítico que un scatter plot.
    """
    df_year = combined_df[combined_df['Year'] == year].copy()
    
    # Creamos 4 categorías de ingresos basadas en los cuartiles del PIB
    df_year['Income_Group'] = pd.qcut(df_year['Economy (GDP per Capita)'], 
                                      q=4, 
                                      labels=['Bajos Ingresos', 'Ingreso Medio-Bajo', 'Ingreso Medio-Alto', 'Altos Ingresos'])
    
    # Boxplot
    fig = px.box(df_year, 
                 x='Income_Group', 
                 y='Happiness Score', 
                 color='Income_Group',
                 points="all", # Muestra también los puntos individuales
                 hover_name='Country',
                 title=f'📦 Distribución de Felicidad por Nivel Económico ({year})',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    fig.update_layout(
        xaxis_title="Nivel de PIB per Cápita",
        yaxis_title="Puntuación de Felicidad",
        showlegend=False,
        height=500
    )
    return fig

def plot_comparison_bars(df, country1, country2, year):
    """
    SUSTITUTO DEL RADAR PLOT: Gráfico de Barras Agrupadas.
    Compara factor por factor entre dos países de forma clara.
    """
    # Filtrar datos
    data = df[df['Year'] == year]
    df_comp = data[data['Country'].isin([country1, country2])].copy()
    
    if df_comp.empty or len(df_comp) < 2:
        return None

    # Columnas a comparar
    metrics = ['Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)', 
               'Freedom', 'Trust (Government Corruption)', 'Generosity']
    
    # Transformar a formato largo para Plotly Express
    df_melted = df_comp.melt(id_vars=['Country'], value_vars=metrics, var_name='Factor', value_name='Valor')
    
    # Gráfico de barras agrupadas
    fig = px.bar(df_melted, 
                 x='Valor', 
                 y='Factor', 
                 color='Country',
                 barmode='group',
                 orientation='h', # Horizontal para leer mejor las etiquetas
                 title=f'⚔️ Comparativa Directa: {country1} vs {country2} ({year})',
                 color_discrete_map={country1: COLORS['primary'], country2: COLORS['secondary']})
    
    fig.update_layout(
        yaxis=dict(autorange="reversed"), # Invertir eje Y para que el primer factor salga arriba
        xaxis_title="Puntuación (Escala Normalizada)",
        height=500,
        legend_title_text="País"
    )
    return fig

def plot_feature_importance(combined_df):
    """
    Visualización 3: Variables que más afectan a la felicidad
    Gráfico de barras con análisis de correlación
    """
    # Calcular correlaciones con Happiness Score
    features = ['Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)', 
                'Freedom', 'Trust (Government Corruption)', 'Generosity']
    
    correlations = combined_df[features + ['Happiness Score']].corr()['Happiness Score'][features]
    correlations = correlations.sort_values(ascending=True)
    
    # Crear figura con dos subgráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Gráfico 1: Barras horizontales de correlación
    colors_bars = [COLORS['success'] if x > 0 else COLORS['danger'] for x in correlations.values]
    bars = ax1.barh(range(len(correlations)), correlations.values, color=colors_bars, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Añadir valores en las barras
    for idx, (value, bar) in enumerate(zip(correlations.values, bars)):
        ax1.text(value + 0.01 if value > 0 else value - 0.01, idx, 
                f'{value:.3f}', va='center', 
                ha='left' if value > 0 else 'right',
                fontsize=11, fontweight='bold')
    
    # Configuración del primer gráfico
    ax1.set_yticks(range(len(correlations)))
    ax1.set_yticklabels([label.replace(' (', '\n(') for label in correlations.index], fontsize=10)
    ax1.set_xlabel('Correlación con Felicidad', fontsize=12, fontweight='bold')
    ax1.set_title('Impacto de Variables en la Felicidad\n(Correlación de Pearson)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax1.axvline(x=0, color='black', linestyle='-', linewidth=2, alpha=0.5)
    ax1.grid(True, alpha=0.3, axis='x', linestyle=':', linewidth=1)
    ax1.set_xlim(-0.5, 1.0)
    
    # Gráfico 2: Promedio de valores por característica (barras verticales agrupadas)
    avg_values = combined_df[features].mean().sort_values(ascending=False)
    std_values = combined_df[features].std()
    
    x_pos = np.arange(len(avg_values))
    colors_gradient = plt.cm.plasma(np.linspace(0, 1, len(avg_values)))
    
    bars2 = ax2.bar(x_pos, avg_values.values, yerr=std_values[avg_values.index].values,
                   color=colors_gradient, alpha=0.8, edgecolor='black', 
                   linewidth=1.5, capsize=5, error_kw={'linewidth': 2, 'alpha': 0.7})
    
    # Añadir valores encima de las barras
    for idx, (value, std) in enumerate(zip(avg_values.values, std_values[avg_values.index].values)):
        ax2.text(idx, value + std + 0.05, f'{value:.2f}', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Configuración del segundo gráfico
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([label.replace(' (', '\n(') for label in avg_values.index], 
                        rotation=45, ha='right', fontsize=9)
    ax2.set_ylabel('Valor Promedio (Estandarizado)', fontsize=12, fontweight='bold')
    ax2.set_title('Valores Promedio de Factores de Felicidad\n(2015-2019)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3, axis='y', linestyle=':', linewidth=1)
    
    plt.tight_layout()
    return fig

def show_home():
    """Página de inicio con navegación a las diferentes secciones"""
    # Header principal
    st.markdown("""
        <h1 style='text-align: center; color: #1f77b4; padding: 20px; font-size: 48px;'>
            🌍 World Happiness Dashboard 😊
        </h1>
        <p style='text-align: center; font-size: 20px; color: #666; margin-bottom: 30px;'>
            Análisis Profesional de Felicidad Mundial (2015-2019)
        </p>
        <hr style='border: 2px solid #1f77b4;'>
    """, unsafe_allow_html=True)
    
    # Introducción
    st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #f0f8ff; border-radius: 10px; margin: 20px 0;'>
        <h3 style='color: #1f77b4;'>Bienvenido al Dashboard de Felicidad Mundial</h3>
        <p style='font-size: 16px; color: #555;'>
            Explora datos de felicidad de más de 150 países a través de visualizaciones interactivas.
            Descubre qué hace felices a las naciones y cómo ha evolucionado la felicidad en los últimos años.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sección de botones
    st.markdown("### 📊 Selecciona una Visualización")
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 15px; text-align: center; height: 200px;
                    display: flex; flex-direction: column; justify-content: center;'>
            <h2 style='color: white; margin: 0;'>🗺️</h2>
            <h3 style='color: white; margin: 10px 0;'>Mapamundi</h3>
            <p style='color: #f0f0f0; font-size: 14px;'>Visualización geográfica interactiva</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🌍 Ver Mapamundi Interactivo", use_container_width=True, key="btn_map"):
            st.session_state.page = "mapamundi"
            st.rerun()
        
        st.markdown("""
        <p style='text-align: center; padding: 10px; font-size: 14px; color: #666;'>
            Explora la felicidad por países en un mapa mundial. Los países más felices aparecen en rojo oscuro.
        </p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; border-radius: 15px; text-align: center; height: 200px;
                    display: flex; flex-direction: column; justify-content: center;'>
            <h2 style='color: white; margin: 0;'>📈</h2>
            <h3 style='color: white; margin: 10px 0;'>Evolución Temporal</h3>
            <p style='color: #f0f0f0; font-size: 14px;'>Tendencias a lo largo del tiempo</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Ver Evolución Temporal", use_container_width=True, key="btn_evolution"):
            st.session_state.page = "evolucion"
            st.rerun()
        
        st.markdown("""
        <p style='text-align: center; padding: 10px; font-size: 14px; color: #666;'>
            Analiza cómo ha cambiado la felicidad en diferentes países desde 2015 hasta 2019.
        </p>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 20px; border-radius: 15px; text-align: center; height: 200px;
                    display: flex; flex-direction: column; justify-content: center;'>
            <h2 style='color: white; margin: 0;'>🎯</h2>
            <h3 style='color: white; margin: 10px 0;'>Factores Clave</h3>
            <p style='color: #f0f0f0; font-size: 14px;'>Variables que impactan la felicidad</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📉 Ver Análisis de Variables", use_container_width=True, key="btn_factors"):
            st.session_state.page = "factores"
            st.rerun()
        
        st.markdown("""
        <p style='text-align: center; padding: 10px; font-size: 14px; color: #666;'>
            Descubre qué factores tienen mayor impacto en la felicidad: economía, familia, salud y más.
        </p>
        """, unsafe_allow_html=True)
    
    # Insights generales
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🔍 Insights Rápidos")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌍 Países Analizados", "158", delta="5 años de datos")
    
    with col2:
        st.metric("📊 Variables", "6", delta="Factores de felicidad")
    
    with col3:
        st.metric("🥇 País Más Feliz 2019", "Finlandia")
    
    with col4:
        st.metric("📈 Factor Principal", "Economía", delta="Mayor correlación")
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
        <p style='text-align: center; color: #888; font-size: 14px;'>
            Dashboard creado con ❤️ usando Streamlit, Matplotlib, Seaborn y Plotly<br>
            Datos: World Happiness Report (2015-2019)
        </p>
    """, unsafe_allow_html=True)

def show_mapamundi(df_dict):
    """Página del mapamundi interactivo"""
    # Botón de regreso
    if st.button("⬅️ Volver al Inicio", key="back_map"):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Header y descripción integrados
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
            <h1 style='color: #667eea; margin-bottom: 15px;'>
                🗺️ Mapamundi Interactivo de Felicidad
            </h1>
            <p style='font-size: 16px; color: #555; margin-bottom: 10px;'>
                Este mapamundi muestra la distribución de la felicidad a nivel mundial. 
                Los países en <strong style='color: #8B0000;'>rojo oscuro</strong> son los más felices, 
                mientras que los países en <strong style='color: #2c7bb6;'>azul</strong> son los menos felices.
            </p>
            <p style='font-size: 14px; color: #666;'>
                💡 <strong>Tip</strong>: Pasa el ratón sobre cualquier país para ver su información completa.
            </p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        selected_year = st.select_slider(
            "📅 Año:",
            options=[2015, 2016, 2017, 2018, 2019],
            value=2019,
            label_visibility="visible"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualización
    with st.spinner('🌍 Generando mapamundi interactivo...'):
        fig = plot_happiness_world_map(df_dict, selected_year)
        st.plotly_chart(fig, use_container_width=True)
    
    # Información adicional
    st.markdown("---")
    st.markdown("### 📊 Estadísticas del Año Seleccionado")
    
    df_year = df_dict[selected_year]
    top_country = df_year.loc[df_year['Happiness Rank'] == 1, 'Country'].values[0]
    bottom_country = df_year.loc[df_year['Happiness Rank'] == df_year['Happiness Rank'].max(), 'Country'].values[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"🥇 País Más Feliz ({selected_year})", top_country)
    with col2:
        st.metric("📍 Total de Países", len(df_year))
    with col3:
        st.metric(f"🌐 País Menos Feliz ({selected_year})", bottom_country)

def show_evolucion(combined_df):
    """Página de evolución temporal"""
    # Botón de regreso
    if st.button("⬅️ Volver al Inicio", key="back_evolution"):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Header y controles
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <h1 style='color: #f5576c; margin-bottom: 15px;'>
                📈 Evolución de la Felicidad
            </h1>
            <p style='font-size: 16px; color: #555; margin-bottom: 10px;'>
                Analiza cómo ha cambiado la felicidad de los países entre 2015 y 2019.
                Selecciona los países que deseas comparar en el panel de la derecha.
            </p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Controles de selección
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Obtener lista de países únicos ordenados alfabéticamente
        all_countries = sorted(combined_df['Country'].unique().tolist())
        
        # Multiselect con búsqueda
        selected_countries = st.multiselect(
            "🔍 Selecciona los países a visualizar:",
            options=all_countries,
            default=['Finland', 'Spain', 'United States', 'Brazil', 'Japan'],
            help="Puedes buscar escribiendo el nombre del país. Selecciona tantos como quieras.",
            placeholder="Escribe para buscar países..."
        )
    
    with col2:
        # Opción para mostrar/ocultar media global
        show_global = st.checkbox(
            "📊 Mostrar Media Global",
            value=True,
            help="Muestra la línea de media global para comparar"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mensaje si no hay países seleccionados
    if not selected_countries:
        st.info("👆 Selecciona al menos un país para comenzar a visualizar la evolución de su felicidad.")
    
    # Visualización
    with st.spinner('📊 Generando gráfico de evolución...'):
        fig = plot_happiness_evolution(combined_df, selected_countries, show_global)
        st.pyplot(fig)
        plt.close()
    
    # Estadísticas de países seleccionados
    if selected_countries:
        st.markdown("---")
        st.markdown("### � Estadísticas de Países Seleccionados")
        
        # Crear columnas dinámicamente según el número de países
        num_countries = len(selected_countries)
        cols = st.columns(min(num_countries, 4))  # Máximo 4 columnas
        
        for idx, country in enumerate(selected_countries[:4]):  # Mostrar máximo 4
            with cols[idx]:
                country_data = combined_df[combined_df['Country'] == country]
                avg_score = country_data['Happiness Score'].mean()
                first_year = country_data[country_data['Year'] == 2015]['Happiness Score'].values
                last_year = country_data[country_data['Year'] == 2019]['Happiness Score'].values
                
                if len(first_year) > 0 and len(last_year) > 0:
                    delta = last_year[0] - first_year[0]
                    st.metric(
                        label=country,
                        value=f"{avg_score:.3f}",
                        delta=f"{delta:.3f}" if delta != 0 else "Sin cambio",
                        help=f"Promedio 2015-2019. Delta muestra cambio de 2015 a 2019"
                    )
        
        # Si hay más de 4 países, mostrar el resto en otra fila
        if num_countries > 4:
            st.markdown("<br>", unsafe_allow_html=True)
            remaining = selected_countries[4:]
            cols2 = st.columns(min(len(remaining), 4))
            
            for idx, country in enumerate(remaining[:4]):
                with cols2[idx]:
                    country_data = combined_df[combined_df['Country'] == country]
                    avg_score = country_data['Happiness Score'].mean()
                    first_year = country_data[country_data['Year'] == 2015]['Happiness Score'].values
                    last_year = country_data[country_data['Year'] == 2019]['Happiness Score'].values
                    
                    if len(first_year) > 0 and len(last_year) > 0:
                        delta = last_year[0] - first_year[0]
                        st.metric(
                            label=country,
                            value=f"{avg_score:.3f}",
                            delta=f"{delta:.3f}" if delta != 0 else "Sin cambio"
                        )

def show_factores(combined_df):
    """Página de análisis de factores"""
    # Botón de regreso
    if st.button("⬅️ Volver al Inicio", key="back_factors"):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Header (Se mantiene fuera de las pestañas para que sea el título común)
    st.markdown("""
        <h1 style='text-align: center; color: #00f2fe;'>
            🎯 Variables que Más Afectan a la Felicidad
        </h1>
    """, unsafe_allow_html=True)

    # --- INICIO DE LA INTEGRACIÓN DE PESTAÑAS ---
    tab1, tab2 = st.tabs(["📊 Impacto General", "💵 Dinero vs Felicidad"])

    # PESTAÑA 1: TU CÓDIGO ORIGINAL EXACTO (Solo indentado)
    with tab1:
        # Descripción Original
        st.markdown("""
        <div style='background-color: #e1f5fe; padding: 20px; border-radius: 10px; border-left: 4px solid #00f2fe;'>
            <p style='font-size: 16px; margin: 0;'>
            Análisis de <strong>correlación</strong> y <strong>valores promedio</strong> de los factores que influyen 
            en la felicidad mundial. Las correlaciones positivas más altas indican mayor impacto en la felicidad.
            </p>
            <p style='font-size: 14px; margin-top: 10px; color: #666;'>
            El gráfico izquierdo muestra cómo cada factor se relaciona con la felicidad, 
            mientras que el derecho presenta los valores promedio de cada variable.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Visualización Original
        with st.spinner('🎯 Generando análisis de variables...'):
            fig = plot_feature_importance(combined_df)
            st.pyplot(fig)
            plt.close()
        
        # Insights detallados Originales
        st.markdown("---")
        st.markdown("### 🔍 Análisis Detallado por Factor")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background-color: #fff9c4; padding: 15px; border-radius: 8px; height: 100%;'>
                <h4 style='color: #f57f17; margin-top: 0;'>💰 Economía (PIB)</h4>
                <p style='color: #555; font-size: 14px;'>
                    <strong>Factor #1</strong><br>
                    Mayor correlación con felicidad.<br>
                    El desarrollo económico es fundamental.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #f3e5f5; padding: 15px; border-radius: 8px; height: 100%;'>
                <h4 style='color: #6a1b9a; margin-top: 0;'>👨‍👩‍👧‍👦 Familia y Apoyo Social</h4>
                <p style='color: #555; font-size: 14px;'>
                    <strong>Factor #2</strong><br>
                    Las relaciones sociales son cruciales.<br>
                    El apoyo comunitario importa.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; height: 100%;'>
                <h4 style='color: #2e7d32; margin-top: 0;'>🏥 Salud</h4>
                <p style='color: #555; font-size: 14px;'>
                    <strong>Factor #3</strong><br>
                    Esperanza de vida saludable.<br>
                    Acceso a salud de calidad.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background-color: #e3f2fd; padding: 15px; border-radius: 8px; height: 100%;'>
                <h4 style='color: #1565c0; margin-top: 0;'>🕊️ Libertad</h4>
                <p style='color: #555; font-size: 14px;'>
                    Libertad para tomar decisiones de vida.<br>
                    Importante pero variable.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #fce4ec; padding: 15px; border-radius: 8px; height: 100%;'>
                <h4 style='color: #c2185b; margin-top: 0;'>🤝 Generosidad</h4>
                <p style='color: #555; font-size: 14px;'>
                    Donaciones y ayuda a otros.<br>
                    Menor correlación pero presente.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background-color: #efebe9; padding: 15px; border-radius: 8px; height: 100%;'>
                <h4 style='color: #4e342e; margin-top: 0;'>🏛️ Confianza (Gobierno)</h4>
                <p style='color: #555; font-size: 14px;'>
                    Percepción de corrupción.<br>
                    Afecta la felicidad general.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # PESTAÑA 2: NUEVO CONTENIDO (Análisis Dinero vs Felicidad)
    with tab2:
        # Descripción con tu mismo estilo de diseño (Color naranja para diferenciar)
        st.markdown("""
        <div style='background-color: #fff3e0; padding: 20px; border-radius: 10px; border-left: 4px solid #ff9800;'>
            <p style='font-size: 16px; margin: 0;'>
            Análisis de la <strong>Paradoja de Easterlin</strong> mediante Diagrama de Cajas.
            </p>
            <p style='font-size: 14px; margin-top: 10px; color: #666;'>
            Este gráfico agrupa los países en 4 niveles de riqueza (PIB). Observa cómo aumenta la felicidad mediana 
            al subir de nivel económico, pero también observa los <strong>puntos dispersos</strong>: existen países con menos ingresos 
            que son más felices que otros con altos ingresos.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Selector de año exclusivo para esta gráfica
        col_sel, _ = st.columns([1, 3])
        with col_sel:
            year_box = st.selectbox("📅 Selecciona Año:", [2015, 2016, 2017, 2018, 2019], index=4, key="box_year_selector")

        # Visualización del Boxplot
        with st.spinner('💵 Analizando relación economía-felicidad...'):
            # Nota: Asegúrate de tener la función plot_income_happiness_boxplot definida en tu código
            fig_box = plot_income_happiness_boxplot(combined_df, year_box)
            st.plotly_chart(fig_box, use_container_width=True)
        
def show_comparador(combined_df):
    """Nueva página para comparar países"""
    if st.button("⬅️ Volver al Inicio", key="back_comp"):
        st.session_state.page = "home"
        st.rerun()
        
    st.markdown("<br><h1 style='text-align: center; color: #ff7f0e;'>⚔️ Comparador Cara a Cara</h1>", unsafe_allow_html=True)
    
    # Selectores
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        c1 = st.selectbox("País A", sorted(combined_df['Country'].unique()), index=0)
    with col2:
        c2 = st.selectbox("País B", sorted(combined_df['Country'].unique()), index=1)
    with col3:
        year = st.selectbox("Año", [2015, 2016, 2017, 2018, 2019], index=4, key="comp_year")
    
    st.markdown("---")
    
    # Gráfico
    fig = plot_comparison_bars(combined_df, c1, c2, year)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        
        # Conclusión automática en texto
        try:
            score1 = combined_df[(combined_df['Country']==c1) & (combined_df['Year']==year)]['Happiness Score'].values[0]
            score2 = combined_df[(combined_df['Country']==c2) & (combined_df['Year']==year)]['Happiness Score'].values[0]
            diff = score1 - score2
            winner = c1 if diff > 0 else c2
            st.success(f"🏆 En {year}, **{winner}** es más feliz por una diferencia de **{abs(diff):.3f}** puntos.")
        except:
            pass

def main():
    # Inicializar estado de sesión
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    
    # Cargar datos
    df_dict, combined_df = load_data()
    
    # Sidebar con información
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f30d.png", width=100)
        st.title("📊 Panel de Control")
        st.markdown("---")
        
        # Navegación en sidebar
        st.subheader("🧭 Navegación")
        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        if st.button("🗺️ Mapamundi", use_container_width=True):
            st.session_state.page = "mapamundi"
            st.rerun()
        if st.button("📈 Evolución", use_container_width=True):
            st.session_state.page = "evolucion"
            st.rerun()
        if st.button("🎯 Factores", use_container_width=True):
            st.session_state.page = "factores"
            st.rerun()
        if st.button("⚔️ Comparador", use_container_width=True): 
            st.session_state.page = "comparador"
            st.rerun()
        
        st.markdown("---")
        
        # Métricas generales
        st.subheader("📈 Estadísticas Globales")
        total_countries = combined_df['Country'].nunique()
        
        col1, col2 = st.columns(2)
        col1.metric("Países", total_countries)
        col2.metric("Años", "5")
        
        st.markdown("---")
        st.info("💡 **Nota**: Los datos han sido estandarizados para una mejor comparación.")
    
    # Renderizar la página actual
    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "mapamundi":
        show_mapamundi(df_dict)
    elif st.session_state.page == "evolucion":
        show_evolucion(combined_df)
    elif st.session_state.page == "factores":
        show_factores(combined_df)
    elif st.session_state.page == "comparador":
        show_comparador(combined_df)

if __name__ == "__main__":
    main()
