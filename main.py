import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
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

def create_custom_cmap():
    """Crea un mapa de colores personalizado para el heatmap"""
    colors = ['#d73027', '#fc8d59', '#fee090', '#e0f3f8', '#91bfdb', '#4575b4']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)
    return cmap

def plot_happiness_heatmap(df_dict, selected_year):
    """
    Visualización 1: Mapa de calor de países más y menos felices
    Diseño profesional con gradientes y etiquetas optimizadas
    """
    df = df_dict[selected_year].copy()
    
    # Ordenar por Happiness Score
    df = df.sort_values('Happiness Score', ascending=False)
    
    # Seleccionar top 20 y bottom 20 países
    top_countries = df.head(20)
    bottom_countries = df.tail(20)
    selected_countries = pd.concat([top_countries, bottom_countries])
    
    # Preparar datos para el heatmap
    variables = ['Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)', 
                 'Freedom', 'Trust (Government Corruption)', 'Generosity']
    
    heatmap_data = selected_countries[variables].values
    countries = selected_countries['Country'].values
    
    # Crear figura con diseño profesional
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Crear heatmap con estilo personalizado
    cmap = create_custom_cmap()
    im = ax.imshow(heatmap_data, aspect='auto', cmap=cmap, interpolation='nearest')
    
    # Configurar ejes
    ax.set_xticks(np.arange(len(variables)))
    ax.set_yticks(np.arange(len(countries)))
    ax.set_xticklabels(variables, rotation=45, ha='right', fontsize=10, fontweight='bold')
    ax.set_yticklabels(countries, fontsize=9)
    
    # Añadir línea separadora entre top y bottom
    ax.axhline(y=19.5, color='white', linewidth=3, linestyle='--', alpha=0.7)
    
    # Añadir valores en las celdas
    for i in range(len(countries)):
        for j in range(len(variables)):
            text = ax.text(j, i, f'{heatmap_data[i, j]:.2f}',
                          ha="center", va="center", color="white", 
                          fontsize=7, fontweight='bold',
                          bbox=dict(boxstyle='round', facecolor='black', alpha=0.3))
    
    # Barra de color profesional
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Valor Estandarizado', rotation=270, labelpad=20, fontsize=11, fontweight='bold')
    cbar.ax.tick_params(labelsize=9)
    
    # Título y subtítulo
    ax.set_title(f'Análisis de Felicidad por País - {selected_year}\n' + 
                 'Top 20 Países (Arriba) vs Bottom 20 Países (Abajo)',
                 fontsize=16, fontweight='bold', pad=20)
    
    # Añadir anotaciones
    ax.text(-0.5, 10, 'MÁS\nFELICES', fontsize=12, fontweight='bold', 
            color=COLORS['success'], rotation=90, va='center')
    ax.text(-0.5, 30, 'MENOS\nFELICES', fontsize=12, fontweight='bold', 
            color=COLORS['danger'], rotation=90, va='center')
    
    plt.tight_layout()
    return fig

def plot_happiness_evolution(combined_df):
    """
    Visualización 2: Evolución de la felicidad a lo largo de los años
    Gráfico de líneas con múltiples países destacados
    """
    # Calcular la media global por año
    global_avg = combined_df.groupby('Year')['Happiness Score'].mean().reset_index()
    
    # Seleccionar países representativos de diferentes regiones
    countries_to_plot = ['Switzerland', 'United States', 'Brazil', 'Japan', 
                        'Germany', 'Australia', 'South Africa', 'India']
    
    # Crear figura con diseño profesional
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), 
                                    gridspec_kw={'height_ratios': [2, 1]})
    
    # Gráfico superior: Evolución de países seleccionados
    colors_palette = sns.color_palette("husl", len(countries_to_plot))
    
    for idx, country in enumerate(countries_to_plot):
        country_data = combined_df[combined_df['Country'] == country]
        if not country_data.empty:
            ax1.plot(country_data['Year'], country_data['Happiness Score'], 
                    marker='o', linewidth=2.5, markersize=8, label=country,
                    color=colors_palette[idx], alpha=0.8)
    
    # Línea de media global con estilo especial
    ax1.plot(global_avg['Year'], global_avg['Happiness Score'], 
            linestyle='--', linewidth=3, color='black', 
            label='Media Global', alpha=0.6, marker='s', markersize=10)
    
    # Configuración del gráfico superior
    ax1.set_xlabel('Año', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Puntuación de Felicidad (Estandarizada)', fontsize=12, fontweight='bold')
    ax1.set_title('Evolución de la Felicidad Mundial (2015-2019)\nPaíses Representativos', 
                 fontsize=16, fontweight='bold', pad=20)
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10, framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle=':', linewidth=1)
    ax1.set_xticks([2015, 2016, 2017, 2018, 2019])
    
    # Gráfico inferior: Distribución de felicidad por año (violin plot)
    years = sorted(combined_df['Year'].unique())
    positions = range(len(years))
    
    violin_parts = ax2.violinplot([combined_df[combined_df['Year'] == year]['Happiness Score'].values 
                                   for year in years],
                                  positions=positions, widths=0.7,
                                  showmeans=True, showmedians=True)
    
    # Colorear los violin plots
    colors_violin = plt.cm.viridis(np.linspace(0, 1, len(years)))
    for idx, pc in enumerate(violin_parts['bodies']):
        pc.set_facecolor(colors_violin[idx])
        pc.set_alpha(0.7)
        pc.set_edgecolor('black')
        pc.set_linewidth(1.5)
    
    # Configuración del gráfico inferior
    ax2.set_xlabel('Año', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Distribución de Felicidad', fontsize=12, fontweight='bold')
    ax2.set_title('Distribución Global de Felicidad por Año', 
                 fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(positions)
    ax2.set_xticklabels(years)
    ax2.grid(True, alpha=0.3, axis='y', linestyle=':', linewidth=1)
    
    plt.tight_layout()
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

def main():
    # Cargar datos
    df_dict, combined_df = load_data()
    
    # Header principal
    st.markdown("""
        <h1 style='text-align: center; color: #1f77b4; padding: 20px;'>
            🌍 World Happiness Dashboard 😊
        </h1>
        <p style='text-align: center; font-size: 18px; color: #666;'>
            Análisis Profesional de Felicidad Mundial (2015-2019)
        </p>
        <hr style='border: 2px solid #1f77b4;'>
    """, unsafe_allow_html=True)
    
    # Sidebar con información
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f30d.png", width=100)
        st.title("📊 Panel de Control")
        st.markdown("---")
        
        # Métricas generales
        st.subheader("📈 Estadísticas Globales")
        total_countries = combined_df['Country'].nunique()
        avg_happiness = combined_df['Happiness Score'].mean()
        
        col1, col2 = st.columns(2)
        col1.metric("Países", total_countries)
        col2.metric("Años", "5")
        
        st.markdown("---")
        st.info("💡 **Nota**: Los datos han sido estandarizados para una mejor comparación.")
        
    # Visualización 1: Mapa de Calor
    st.header("🗺️ Mapa de Calor de Felicidad por País")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        Este mapa de calor muestra los **20 países más felices** (arriba) y los **20 países menos felices** (abajo),
        analizando las diferentes variables que componen el índice de felicidad.
        """)
    
    with col2:
        selected_year = st.select_slider(
            "📅 Selecciona el año:",
            options=[2015, 2016, 2017, 2018, 2019],
            value=2019
        )
    
    with st.spinner('Generando mapa de calor...'):
        fig1 = plot_happiness_heatmap(df_dict, selected_year)
        st.pyplot(fig1)
        plt.close()
    
    st.markdown("---")
    
    # Visualización 2: Evolución Temporal
    st.header("📈 Evolución de la Felicidad a lo Largo del Tiempo")
    st.markdown("""
    Análisis de la evolución temporal de la felicidad en países representativos de diferentes regiones del mundo,
    comparados con la **media global**.
    """)
    
    with st.spinner('Generando gráfico de evolución...'):
        fig2 = plot_happiness_evolution(combined_df)
        st.pyplot(fig2)
        plt.close()
    
    st.markdown("---")
    
    # Visualización 3: Importancia de Variables
    st.header("🎯 Variables que Más Afectan a la Felicidad")
    st.markdown("""
    Análisis de **correlación** y **valores promedio** de los factores que influyen en la felicidad mundial.
    Las correlaciones positivas más altas indican mayor impacto en la felicidad.
    """)
    
    with st.spinner('Generando análisis de variables...'):
        fig3 = plot_feature_importance(combined_df)
        st.pyplot(fig3)
        plt.close()
    
    # Footer con insights
    st.markdown("---")
    st.subheader("🔍 Insights Clave")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **💰 Economía**
        - Factor con mayor correlación
        - El PIB per cápita es fundamental
        """)
    
    with col2:
        st.markdown("""
        **👨‍👩‍👧‍👦 Familia**
        - Segundo factor más importante
        - Apoyo social crucial
        """)
    
    with col3:
        st.markdown("""
        **🏥 Salud**
        - Esperanza de vida vital
        - Correlación muy positiva
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <p style='text-align: center; color: #888; font-size: 14px;'>
            Dashboard creado con ❤️ usando Streamlit, Matplotlib y Seaborn | 
            Datos: World Happiness Report
        </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
