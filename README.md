# 🌍 World Happiness Dashboard

Un dashboard profesional interactivo para visualizar y analizar datos de felicidad mundial (2015-2019) con interfaz de navegación moderna por páginas.

## ✨ Características Destacadas

### 🏠 Interfaz Moderna con Navegación

- **Página de inicio limpia y elegante** con tarjetas de navegación
- **Sistema de navegación múltiple**: botones en página principal y sidebar
- **Diseño con gradientes modernos** en cada sección
- **Carga bajo demanda**: cada visualización se genera solo cuando la visitas
- **Experiencia de usuario optimizada**: navegación intuitiva y fluida

### 📊 Tres Visualizaciones Principales

#### 🗺️ **1. Mapamundi Interactivo**
   - **Visualización geográfica completa** con Plotly
   - Países más felices en **rojo oscuro**, menos felices en **azul**
   - **Hover interactivo**: pasa el ratón sobre cualquier país para ver:
     - Nombre del país
     - Puntuación de felicidad
     - Ranking mundial
   - **Control deslizante** para cambiar entre años (2015-2019)
   - Proyección Natural Earth para representación realista
   - Estadísticas del año seleccionado

#### 📈 **2. Evolución Temporal**
   - **Gráfico de líneas** con países representativos de diferentes regiones
   - Comparación con la **media global**
   - **Violin plots** mostrando la distribución completa por año
   - Análisis de tendencias a lo largo del tiempo (2015-2019)
   - Insights sobre tendencias positivas y áreas de atención

#### 🎯 **3. Análisis de Factores**
   - **Correlación de Pearson** de cada factor con la felicidad
   - **Valores promedio** con desviación estándar
   - Visualización dual: correlaciones + promedios
   - **Análisis detallado** de los 6 factores clave:
     - 💰 Economía (PIB per cápita)
     - 👨‍👩‍👧‍👦 Familia y apoyo social
     - 🏥 Salud y esperanza de vida
     - 🕊️ Libertad para tomar decisiones
     - 🤝 Generosidad
     - 🏛️ Confianza en el gobierno

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

- **Streamlit** - Framework para el dashboard web interactivo
- **Plotly** - Mapamundi interactivo con hover tooltips
- **Matplotlib** - Visualizaciones estáticas profesionales
- **Seaborn** - Visualizaciones estadísticas avanzadas
- **Pandas** - Manipulación y análisis de datos
- **NumPy** - Operaciones numéricas y procesamiento
- **scikit-learn** - Estandarización de datos

## � Características Profesionales

### Diseño y UX
- ✅ **Interfaz de navegación por páginas** con estado de sesión
- ✅ **Diseño responsivo** y moderno con gradientes
- ✅ **Tarjetas de navegación** con colores distintivos
- ✅ **Sidebar persistente** con navegación rápida
- ✅ **Botones de regreso** en cada página

### Visualizaciones
- ✅ **Mapamundi interactivo** con Plotly (hover, zoom, pan)
- ✅ **Gráficos duales** para análisis completo
- ✅ **Paletas de colores personalizadas** profesionales
- ✅ **Violin plots** para distribuciones
- ✅ **Heatmaps** con valores numéricos

### Rendimiento
- ✅ **Carga de datos optimizada** con `@st.cache_data`
- ✅ **Carga bajo demanda** de visualizaciones
- ✅ **Spinners con mensajes** durante procesamiento
- ✅ **Gestión de estado** eficiente con `session_state`

### Contenido
- ✅ **Métricas en tiempo real** con `st.metric`
- ✅ **Insights automáticos** organizados por sección
- ✅ **Descripciones contextuales** en cada visualización
- ✅ **Cajas de información** con bordes de color
- ✅ **Documentación completa** (README + INTERFAZ.md)

## 🧭 Navegación del Dashboard

### Tres Formas de Navegar:

1. **Página de Inicio**: Click en las tarjetas de colores con gradientes
2. **Sidebar**: Botones de navegación siempre visibles
3. **Botones de Regreso**: "⬅️ Volver al Inicio" en cada página

### Flujo de Usuario:

```
🏠 Inicio
   ↓
   ├─→ 🗺️ Mapamundi → Explora países → 🏠 Volver
   ├─→ 📈 Evolución → Analiza tendencias → 🏠 Volver
   └─→ 🎯 Factores → Descubre impactos → 🏠 Volver
```

## 🔍 Insights Principales

### Factores de Felicidad (Orden de Impacto):

1. **💰 Economía (PIB per cápita)** - Mayor correlación con felicidad
2. **👨‍👩‍👧‍👦 Familia y apoyo social** - Segundo factor más importante
3. **🏥 Salud (esperanza de vida)** - Impacto significativo en bienestar
4. **🕊️ Libertad** - Importante para decisiones de vida
5. **🏛️ Confianza (gobierno)** - Afecta percepción general
6. **🤝 Generosidad** - Menor correlación pero presente

### Tendencias Temporales:

- 📊 La media global se mantiene relativamente **estable** (2015-2019)
- 🌍 Existe **variación considerable** entre regiones
- 🇫🇮 **Finlandia** lidera como país más feliz en 2019
- 📈 Países desarrollados mantienen **consistencia** en el top

### Geografía de la Felicidad:

- 🔴 **Europa Nórdica**: Consistentemente más feliz (rojo oscuro en mapa)
- 🟡 **América y Asia**: Niveles medios de felicidad
- 🔵 **África Subsahariana**: Desafíos en indicadores de felicidad

## 📝 Archivos de Documentación

- **README.md** (este archivo): Documentación general del proyecto
- **INTERFAZ.md**: Detalles de la nueva interfaz y navegación
- **pyproject.toml**: Configuración de dependencias con uv

## 🤝 Contribución

Este proyecto es parte de prácticas académicas. Para mejoras o sugerencias:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📜 Licencia

Proyecto académico - Master AVPD

---

**✨ Creado con ❤️ usando Streamlit, Plotly, Matplotlib y Seaborn**

**📊 Datos: World Happiness Report (2015-2019)**
