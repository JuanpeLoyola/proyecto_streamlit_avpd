# 🌍 World Happiness Dashboard

Un dashboard profesional interactivo para visualizar y analizar datos de felicidad mundial (2015-2019).

## 🎯 Características

### 📊 Visualizaciones Principales

1. **Mapa de Calor Interactivo**
   - Compara los 20 países más felices vs los 20 menos felices
   - Control deslizante para cambiar entre años (2015-2019)
   - Visualización detallada de todas las variables de felicidad
   - Diseño profesional con gradientes de color personalizados

2. **Gráfico de Evolución Temporal**
   - Seguimiento de la felicidad en países representativos
   - Comparación con la media global
   - Violin plots para mostrar distribución por año
   - Análisis de tendencias a lo largo del tiempo

3. **Análisis de Variables Clave**
   - Correlación de cada factor con la felicidad
   - Valores promedio con desviación estándar
   - Identificación de los factores más influyentes
   - Visualización dual para análisis completo

## 🚀 Instalación

```bash
# Las dependencias ya están instaladas con uv
uv sync
```

## 💻 Uso

```bash
# Ejecutar el dashboard
uv run streamlit run main.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
proyecto_streamlit/
├── main.py                 # Dashboard principal de Streamlit
├── data/
│   ├── 2015_processed.csv # Datos procesados 2015
│   ├── 2016_processed.csv # Datos procesados 2016
│   ├── 2017_processed.csv # Datos procesados 2017
│   ├── 2018_processed.csv # Datos procesados 2018
│   └── 2019_processed.csv # Datos procesados 2019
└── notebooks/
    └── preprocessing.ipynb # Notebook de preprocesamiento
```

## 📊 Datos

Los datos provienen del World Happiness Report y han sido preprocesados para incluir:

- **Country**: Nombre del país
- **Happiness Rank**: Ranking de felicidad
- **Happiness Score**: Puntuación de felicidad
- **Economy (GDP per Capita)**: PIB per cápita
- **Family**: Apoyo social/familiar
- **Health (Life Expectancy)**: Esperanza de vida saludable
- **Freedom**: Libertad para tomar decisiones
- **Trust (Government Corruption)**: Confianza en el gobierno
- **Generosity**: Generosidad

## 🎨 Tecnologías Utilizadas

- **Streamlit**: Framework para el dashboard web
- **Matplotlib**: Visualizaciones estáticas profesionales
- **Seaborn**: Visualizaciones estadísticas avanzadas
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Operaciones numéricas

## 👨‍💻 Características Profesionales

- ✅ Diseño responsivo y moderno
- ✅ Paletas de colores personalizadas
- ✅ Visualizaciones interactivas
- ✅ Carga de datos optimizada con caché
- ✅ Métricas y estadísticas en tiempo real
- ✅ Insights automáticos
- ✅ Documentación completa

## 🔍 Insights Principales

1. La **economía (PIB)** es el factor con mayor correlación con la felicidad
2. El **apoyo familiar/social** es el segundo factor más importante
3. La **salud y esperanza de vida** tienen un impacto significativo
4. Existe variación considerable en la felicidad entre regiones

---

**Creado con ❤️ usando Streamlit, Matplotlib y Seaborn**
