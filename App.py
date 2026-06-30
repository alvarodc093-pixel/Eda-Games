import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Video Game Market | Dashboard Ejecutivo",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo general de gráficos
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'figure.max_open_warning': 0})

# ----------------------------------------------------------------------------------
# 1. FUNCIÓN DE CARGA Y LIMPIEZA DE DATOS (Mismo pipeline del Jupyter Notebook)
# ----------------------------------------------------------------------------------
@st.cache_data
def load_and_clean_data(file_path="vgchartz-2024.csv"):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        # Intento de ruta alternativa si se ejecuta en subcarpetas
        df = pd.read_csv("Data/vgchartz-2024.csv")
        
    columnas_originales = df.columns.tolist()
    mapeo_columnas = {}
    
    # Mapeo dinámico para robustez ante variaciones del archivo
    for col in columnas_originales:
        col_low = col.lower().strip()
        if col_low in ['year', 'year_of_release', 'release_year']: mapeo_columnas[col] = 'year'
        elif col_low in ['total_sales', 'global_sales', 'sales', 'total_sales_millions']: mapeo_columnas[col] = 'total_sales'
        elif col_low in ['genre', 'genero']: mapeo_columnas[col] = 'genre'
        elif col_low in ['console', 'platform', 'plataforma']: mapeo_columnas[col] = 'console'
        elif col_low in ['critic_score', 'score', 'critic']: mapeo_columnas[col] = 'critic_score'
        elif col_low in ['release_date', 'date', 'fecha']: mapeo_columnas[col] = 'release_date'
        elif col_low in ['na_sales', 'na_sales_millions']: mapeo_columnas[col] = 'na_sales'
        elif col_low in ['jp_sales', 'jp_sales_millions']: mapeo_columnas[col] = 'jp_sales'
        elif col_low in ['pal_sales', 'eu_sales', 'europe_sales']: mapeo_columnas[col] = 'pal_sales'
        elif col_low in ['other_sales', 'others_sales']: mapeo_columnas[col] = 'other_sales'

    df = df.rename(columns=mapeo_columnas)

    # Limpieza A: Filtrado de variable objetivo (Ventas válidas)
    df = df.dropna(subset=['total_sales'])
    df = df[df['total_sales'] > 0]

    # Limpieza B: Normalización de categóricos
    df['genre'] = df['genre'].fillna('Unknown')
    df['console'] = df['console'].fillna('Unknown')

    # Limpieza C: Conversión segura de Fechas y Años
    if 'release_date' in df.columns:
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    
    if 'year' not in df.columns or df['year'].isnull().all():
        df['year'] = df['release_date'].dt.year
        
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    
    return df

# Carga de datos
df_raw_len = 64016  # Guardamos la métrica inicial como referencia histórica
df = load_and_clean_data()

# ----------------------------------------------------------------------------------
# 2. BARRA LATERAL (Filtros Globales e Información del Portafolio)
# ----------------------------------------------------------------------------------
st.sidebar.title("Navegación y Filtros")
st.sidebar.markdown("---")

# Selector de Modo de Visualización
app_mode = st.sidebar.radio(
    "Selecciona la sección:",
    ["Dashboard", "Documentación Técnica"]
)

if app_mode == "Dashboard":
    st.sidebar.subheader("Filtros Globales")
    
    # Filtro de Años
    min_year = int(df['year'].dropna().min())
    max_year = int(df['year'].dropna().max())
    year_range = st.sidebar.slider(
        "Rango de Años de Lanzamiento",
        min_value=min_year,
        max_value=max_year,
        value=(1985, 2023)
    )
    
    # Filtro de Géneros
    lista_generos = sorted(df['genre'].unique().tolist())
    generos_seleccionados = st.sidebar.multiselect(
        "Filtrar por Género Comercial",
        options=lista_generos,
        default=lista_generos
    )
    
    # Aplicación de filtros al dataframe de trabajo
    df_filtered = df[
        (df['year'] >= year_range[0]) & 
        (df['year'] <= year_range[1]) & 
        (df['genre'].isin(generos_seleccionados))
    ]
else:
    df_filtered = df.copy()

st.sidebar.markdown("---")
st.sidebar.info(
    "**Científico de Datos:** Álvaro Domingo Cordón\n\n"
    "[LinkedIn](http://www.linkedin.com/in/alvaro-domingo)\n"
    "[GitHub](https://github.com/alvarodc093-pixel)"
)

# ----------------------------------------------------------------------------------
# 3. SECCIÓN: DASHBOARD DE STORYTELLING (Estructura de 15 Minutos)
# ----------------------------------------------------------------------------------
if app_mode == "Dashboard":
    
    # Encabezado Principal
    st.title("🎮 Video Game Market")
    st.subheader("Transformando Datos de VGChartz en Estrategia Comercial de Lanzamientos")
    st.markdown("---")
    
    # Estructura del Storytelling en Tabs Cronometrados
    tabs = st.tabs([
        "Apertura & Calidad",
        "Volumen vs Realidad",
        "Monopolios Comerciales",
        "Crítica & Geografía",
        "Ventanas Estratégicas"
    ])
    
    # ------------------------------------------------------------------------------
    # TAB 1: APERTURA, AUDITORÍA Y CALIDAD DE DATOS
    # ------------------------------------------------------------------------------
    with tabs[0]:
        st.header("Contexto de Negocio y Auditoría de Datos")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### El Gancho y la Problemática
            La industria global de videojuegos genera miles de millones de dólares anualmente, pero es un mercado **altamente asimétrico y riesgoso**. El coste de desarrollo de un título AAA puede superar los 100 millones de USD, haciendo que un fracaso comercial ponga en riesgo la supervivencia de un estudio.
            
            **Nuestra Misión Corporativa:** Responder a 5 preguntas críticas de negocio a través de la evidencia estadística:
            1. **Tendencia Temporal:** ¿Sigue el mercado en expansión de ingresos o nos enfrentamos a una saturación?
            2. **Segmentos Dominantes:** ¿Dónde se concentra el dinero real (Plataformas y Géneros)?
            3. **Asimetría Geográfica:** ¿Cómo debemos adaptar el presupuesto de marketing según la región?
            4. **Rentabilidad de la Crítica:** ¿Garantiza una excelente puntuación de los analistas un éxito comercial masivo?
            5. **Estacionalidad Táctica:** ¿Cuál es el mes óptimo para el lanzamiento del producto?
            """)
        
        with col2:
            st.markdown("### Resumen")
            st.metric(label="Registros Brutos Recibidos", value=f"{df_raw_len:,}")
            st.metric(label="Registros Válidos con Ventas (>0)", value=f"{len(df):,}")
            st.error(f"Filas Removidas por Inconsistencia: {df_raw_len - len(df):,}")
            st.caption("Nota: Se eliminó el 72.6% de los datos debido a la falta de la variable objetivo económica.")

    # ------------------------------------------------------------------------------
    # TAB 2: ANÁLISIS UNIVARIANTE - VOLUMEN VS REALIDAD
    # ------------------------------------------------------------------------------
    with tabs[1]:
        st.header("Distribución del Mercado: Volumen de Producción vs Éxito Real")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Volumen de Títulos por Género")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            order_genres = df_filtered["genre"].value_counts().index
            sns.countplot(data=df_filtered, y="genre", order=order_genres, palette="magma", hue="genre", legend=False, ax=ax1)
            ax1.set_xlabel("Cantidad Total de Títulos Desarrollados")
            ax1.set_ylabel("Género Comercial")
            st.pyplot(fig1)
            st.info("Los géneros de Acción, Deportes y Misiones lideran la capacidad operativa de las desarrolladoras.")
            
        with col2:
            st.subheader("La Realidad del Éxito Comercial (Sesgo Exponencial)")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            sns.histplot(data=df_filtered, x="total_sales", bins=50, kde=True, color="purple", ax=ax2)
            ax2.set_xscale("log")
            ax2.set_xlabel("Ventas Globales (Millones USD) - Escala Logarítmica")
            ax2.set_ylabel("Cantidad de Videojuegos")
            st.pyplot(fig2)
            
            # Métricas descriptivas impresas
            mean_v = df_filtered['total_sales'].mean()
            median_v = df_filtered['total_sales'].median()
            skew_v = df_filtered['total_sales'].skew()
            
            subc1, subc2, subc3 = st.columns(3)
            subc1.metric("Venta Media", f"${mean_v:.2f}M USD")
            subc2.metric("Venta Mediana", f"${median_v:.2f}M USD")
            subc3.metric("Asimetría (Skewness)", f"{skew_v:.2f}")

    # ------------------------------------------------------------------------------
    # TAB 3: MONOPOLIOS COMERCIALES - GÉNEROS Y PLATAFORMAS LÍDERES
    # ------------------------------------------------------------------------------
    with tabs[2]:
        st.header("Concentración de Ingresos: ¿Quién se queda con el Pastel?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Consolas por Volumen de Facturación")
            top_consoles = df_filtered.groupby("console")["total_sales"].sum().sort_values(ascending=False).head(10).reset_index()
            
            fig3, ax3 = plt.subplots(figsize=(10, 5))
            sns.barplot(data=top_consoles, x="total_sales", y="console", palette="Blues_r", hue="console", legend=False, ax=ax3)
            ax3.set_xlabel("Ventas Totales Acumuladas (Millones de USD)")
            ax3.set_ylabel("Plataforma")
            for index, value in enumerate(top_consoles["total_sales"]):
                ax3.text(value + 0.5, index, f"${value:,.0f}M", va="center", ha="left", fontsize=9, fontweight="bold")
            st.pyplot(fig3)
            st.caption("El ecosistema PlayStation (PS2, PS3, PS4) junto a Xbox 360 y Wii concentran el dominio histórico de hardware.")
            
        with col2:
            st.subheader("Rendimiento Económico Acumulado por Género")
            ventas_genero = df_filtered.groupby("genre")["total_sales"].sum().sort_values(ascending=False).reset_index()
            
            fig4, ax4 = plt.subplots(figsize=(10, 5))
            sns.barplot(data=ventas_genero, x="total_sales", y="genre", palette="viridis", hue="genre", legend=False, ax=ax4)
            ax4.set_xlabel("Ingresos Totales Acumulados (Millones de USD)")
            ax4.set_ylabel("Género")
            for index, value in enumerate(ventas_genero["total_sales"]):
                ax4.text(value + 1.0, index, f"${value:,.0f}M", va="center", ha="left", fontsize=8)
            st.pyplot(fig4)

    # ------------------------------------------------------------------------------
    # TAB 4: IMPACTO DE LA CRÍTICA Y ASIMETRÍA GEOGRÁFICA
    # ------------------------------------------------------------------------------
    with tabs[3]:
        st.header("Factores de Éxito: El Peso de la Crítica y la Ubicación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("¿Una buena crítica garantiza ventas masivas?")
            df_critics = df_filtered[df_filtered["critic_score"].notnull() & (df_filtered["critic_score"] > 0)]
            
            if not df_critics.empty:
                fig5, ax5 = plt.subplots(figsize=(10, 5))
                sns.scatterplot(data=df_critics, x="critic_score", y="total_sales", alpha=0.4, color="teal", ax=ax5)
                sns.regplot(data=df_critics, x="critic_score", y="total_sales", scatter=False, color="crimson", line_kws={"linewidth": 2, "linestyle": "--"}, ax=ax5)
                ax5.set_yscale("log")
                ax5.set_xlabel("Calificación de la Crítica (Escala 1 al 10)")
                ax5.set_ylabel("Ventas Mundiales (Millones USD) - Escala Logarítmica")
                
                correlacion = df_critics["critic_score"].corr(df_critics["total_sales"])
                ax5.set_title(f"Coeficiente de Correlación de Pearson r = {correlacion:.2f}", fontsize=11, color="darkred")
                st.pyplot(fig5)
            else:
                st.warning("No hay suficientes datos de críticas para este rango de filtros.")
                
            st.info("Fuerte dispersión: Un puntaje alto (>8.5) es necesario para un Blockbuster, pero no lo garantiza automáticamente.")
            
        with col2:
            st.subheader("Segmentación Geográfica de los Ingresos")
            regiones = {
                "Norteamérica (NA)": df_filtered["na_sales"].sum(),
                "Europa / PAL": df_filtered["pal_sales"].sum(),
                "Japón (JP)": df_filtered["jp_sales"].sum(),
                "Otros Mercados": df_filtered["other_sales"].sum()
            }
            df_regiones = pd.DataFrame(list(regiones.items()), columns=["Region", "Ventas"]).sort_values(by="Ventas", ascending=False)
            
            fig6, ax6 = plt.subplots(figsize=(10, 5))
            sns.barplot(data=df_regiones, x="Region", y="Ventas", palette="autumn", hue="Region", legend=False, ax=ax6)
            ax6.set_xlabel("Región Económica")
            ax6.set_ylabel("Volumen de Ventas (Millones de USD)")
            st.pyplot(fig6)
            
            # KPI Porcentual
            total_r = df_regiones["Ventas"].sum()
            na_pct = (regiones["Norteamérica (NA)"] / total_r) * 100
            st.metric("Dominio de Norteamérica (NA Sales)", f"{na_pct:.1f}% del Mercado Global")

    # ------------------------------------------------------------------------------
    # TAB 5: ESTACIONALIDAD Y VENTANAS ESTRATÉGICAS DE LANZAMIENTO
    # ------------------------------------------------------------------------------
    with tabs[4]:
        st.header("Análisis Táctico de Estacionalidad: El 'Timing' Perfecto")
        
        # Filtro local para asegurar fechas válidas de estacionalidad
        df_season = df_filtered[df_filtered["release_date"].notnull()].copy()
        df_season["month_num"] = df_season["release_date"].dt.month
        meses_es = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
                    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
        df_season["month_es"] = df_season["month_num"].map(meses_es)
        
        df_monthly = df_season.groupby(["month_num", "month_es"]).agg(
            total_sales_millions=("total_sales", "sum"),
            titles_launched=("total_sales", "count"),
            avg_sales_per_title=("total_sales", "mean")
        ).reset_index().sort_values("month_num")
        
        if not df_monthly.empty:
            fig7, axes = plt.subplots(1, 2, figsize=(16, 5))
            
            # Subplot A: Ventas Totales vs Competencia
            color_bar = "#4a90e2"
            color_line = "#d0021b"
            sns.barplot(data=df_monthly, x="month_es", y="total_sales_millions", ax=axes[0], color=color_bar, alpha=0.8)
            axes[0].set_title("Volumen Total Facturado vs Títulos en Mercado", fontweight="bold")
            axes[0].set_xlabel("Mes de Lanzamiento")
            axes[0].set_ylabel("Ventas Acumuladas (Millones USD)", color=color_bar)
            axes[0].tick_params(axis='y', labelcolor=color_bar)
            axes[0].set_xticklabels(df_monthly["month_es"], rotation=45)
            
            ax0_2 = axes[0].twinx()
            sns.lineplot(data=df_monthly, x="month_es", y="titles_launched", ax=ax0_2, color=color_line, marker="o", linewidth=2, sort=False)
            ax0_2.set_ylabel("Cantidad de Títulos (Competencia)", color=color_line)
            ax0_2.tick_params(axis='y', labelcolor=color_line)
            ax0_2.grid(False)
            
            # Subplot B: Eficiencia Unitaria
            sns.barplot(data=df_monthly, x="month_es", y="avg_sales_per_title", ax=axes[1], palette="Oranges_r", hue="month_es", legend=False)
            axes[1].set_title("Eficiencia Unitaria: Ventas Promedio por Juego", fontweight="bold")
            axes[1].set_xlabel("Mes de Lanzamiento")
            axes[1].set_ylabel("Ventas Promedio por Título (Millones USD)")
            axes[1].set_xticklabels(df_monthly["month_es"], rotation=45)
            
            st.pyplot(fig7)
            
            # KPIs Ejecutivos Dinámicos
            top_mes_vol = df_monthly.loc[df_monthly["total_sales_millions"].idxmax()]
            top_mes_eff = df_monthly.loc[df_monthly["avg_sales_per_title"].idxmax()]
            
            c_kpi1, c_kpi2 = st.columns(2)
            c_kpi1.metric("Mayor Volumen de Mercado (Océano Rojo)", f"{top_mes_vol['month_es']}", f"${top_mes_vol['total_sales_millions']:.1f}M Totales")
            c_kpi2.metric("Ventana de Alta Eficiencia (Océano Azul)", f"{top_mes_eff['month_es']}", f"${top_mes_eff['avg_sales_per_title']:.3f}M Promedio por Juego")
        else:
            st.warning("No hay suficientes datos temporales para calcular la estacionalidad.")

        st.markdown("""
        ### Conclusión del Cierre 
        1. **Noviembre** es el mes con mayor volumen total de ingresos en la industria debido a la campaña navideña, pero viene acompañado de una saturación brutal de competencia (Línea roja al máximo).
        2. **Ventana Estratégica Escondida:** Analizando la **Eficiencia Unitaria**, descubrimos meses como **Enero o Mayo** donde, a pesar de haber menos ventas absolutas totales, la competencia cae tanto que la ratio de *ventas promedio por juego lanzado* se maximiza drásticamente. 
        
        **Recomendación del Analista:** Si eres un estudio independiente o con presupuesto mediano, evita Noviembre. Lanza tu juego en ventanas de alta eficiencia unitaria para evitar ser aplastado por los grandes monopolios.
        """)

# ----------------------------------------------------------------------------------
# 4. SECCIÓN: DOCUMENTACIÓN TÉCNICA Y RESUMEN GENERAL DEL PROYECTO
# ----------------------------------------------------------------------------------
elif app_mode == "Documentación Técnica":
    st.title("Arquitectura del Proyecto & Ficha Técnica")
    st.markdown("---")
    
    st.markdown("""
    ### Origen de los Datos
    El dataset utilizado proviene del histórico de raspado web (*web scraping*) de la plataforma **VGChartz (Edición 2024)**. Contiene información detallada sobre la distribución comercial de software interactivo desde los años 80 hasta la actualidad.
    
    ### Resumen Técnico de Transformaciones (ETL)
    1. **Estandarización de Esquemas:** Mapeo automático de nombres de columnas mediante búsquedas de patrones semánticos por si el archivo de entrada cambia (`global_sales` -> `total_sales`, etc.).
    2. **Filtrado de Sesgo por Nulos:** Eliminación estricta de registros sin tracción económica (Ventas NaN o <= 0) para limpiar la variable objetivo.
    3. **Tratamiento Temporal:** Parseo seguro de formatos de texto `string` a objetos nativos `datetime` de Pandas, aislando la estacionalidad mensual y anual de forma limpia.
    4. **Imputación Categórica:** Sustitución de valores nulos en Género y Consola por la etiqueta controlada `'Unknown'` para salvaguardar el resto de campos financieros de la fila.
    """)
    st.dataframe(df.head(20))