import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA DE STREAMLIT
# ==============================================================================
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
# 1. FUNCIÓN DE CARGA Y LIMPIEZA DE DATOS (Pipeline Dinámico y Blindado)
# ----------------------------------------------------------------------------------
@st.cache_data
def load_and_clean_data(file_path="vgchartz-2024.csv"):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        df = pd.read_csv("Data/vgchartz-2024.csv")
        
    columnas_originales = df.columns.tolist()
    mapeo_columnas = {}
    
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
    
    # Sanitización de nulos y limpieza básica
    df = df.dropna(subset=['total_sales'])
    df = df[df['total_sales'] > 0]
    df['genre'] = df['genre'].fillna('Unknown')
    df['console'] = df['console'].fillna('Unknown')

    if 'release_date' in df.columns:
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    
    if 'year' not in df.columns or df['year'].isnull().all():
        if 'release_date' in df.columns:
            df['year'] = df['release_date'].dt.year

    df = df.dropna(subset=['year'])
    df['year'] = df['year'].astype(int)
    
    return df

# Carga global automática
df_raw_len = 64016  
df = load_and_clean_data()

img_col = next((c for c in df.columns if 'img' in c or 'image' in c or 'url' in c), 'img')
title_col = next((c for c in df.columns if 'title' in c or 'name' in c), 'title')
sales_col = next((c for c in df.columns if 'sales' in c or 'total' in c), 'total_sales')
console_col = next((c for c in df.columns if 'console' in c or 'platform' in c), 'console')
publisher_col = next((c for c in df.columns if 'pub' in c), 'publisher')

# ----------------------------------------------------------------------------------
# 2. BARRA LATERAL (Navegación limpia sin filtros a la izquierda)
# ----------------------------------------------------------------------------------
st.sidebar.title("Navegación")
st.sidebar.markdown("---")

# Mapeo seguro de secciones internas
SECCIONES_MAP = {
    "Dashboard General": "dashboard",
    "Buscador & Catálogo por Publisher": "search_and_catalog",
    "Títulos Líderes en el Mercado": "market_leaders",
    "Documentación Técnica": "docs"
}

seccion_seleccionada = st.sidebar.radio(
    "Selecciona la sección:",
    list(SECCIONES_MAP.keys())
)
app_mode = SECCIONES_MAP[seccion_seleccionada]

st.sidebar.markdown("---")
st.sidebar.info(
    "**Científico de Datos:** Álvaro Domingo Cordón\n\n"
    "[LinkedIn](http://www.linkedin.com/in/alvaro-domingo) | [GitHub](https://github.com/alvarodc093-pixel)"
)


# ==============================================================================
# 3. EJECUCIÓN DE SECCIONES
# ==============================================================================

# ------------------------------------------------------------------------------
# MODO A: DASHBOARD GENERAL (Primera Impresión Optimizada con tu gráfico integrado)
# ------------------------------------------------------------------------------
if app_mode == "dashboard":
    df_filtered = df.copy() # El dashboard opera sobre el histórico global completo
    
    st.title("🎮 Video Game Market Analytics")
    st.markdown("""
    ### **Transformando Big Data de VGChartz en Estrategia Comercial de Lanzamientos**
    *Un framework interactivo de Inteligencia de Negocio para mitigar riesgos financieros, mapear competidores AAA y optimizar ventanas globales de distribución.*
    """)
    st.markdown("---")
    
    tabs = st.tabs([
        "Introducción & Auditoría", 
        "Volumen vs Realidad Económica", 
        "Concentración de Mercados", 
        "Crítica Regresiva & Geografía", 
        "Ventanas Estratégicas (Timing)"
    ])
    
    # TAB 1: INTRODUCCIÓN Y AUDITORÍA
    with tabs[0]:
        st.markdown("## Contexto de Negocio y Calidad de la Información")
        kpi_a, kpi_b, kpi_c = st.columns(3)
        with kpi_a:
            st.metric(label="Universo de Datos Crudos Analizados", value=f"{df_raw_len:,}", delta="Dataset Global Completo")
        with kpi_b:
            st.metric(label="Registros Depurados Activos", value=f"{len(df):,}", delta="Con Tracción Comercial (>0)", delta_color="normal")
        with kpi_c:
            tasa_limpieza = ((df_raw_len - len(df)) / df_raw_len) * 100
            st.metric(label="Calidad del Pipeline de Datos", value=f"{100 - tasa_limpieza:.1f}% Reliable", delta=f"{df_raw_len - len(df):,} Inconsistencias Removidas", delta_color="inverse")
            
        st.markdown("---")
        col_izq, col_der = st.columns([5, 4])
        with col_izq:
            st.markdown("""
            ###La Problemática Comercial: Asimetría y Riesgo AAA
            El ecosistema de los videojuegos genera miles de millones de dólares anuales, pero se rige bajo una estricta distribución de **larga cola (Power Law)**. Lanzar un nuevo título al mercado implica inversiones de desarrollo que superan con frecuencia los **100 millones de USD**, acompañadas de ciclos de producción de hasta 7 años.
            
            Un error en la fecha elegida, ignorar las preferencias culturales de una región geográfica específica o seleccionar un género saturado puede comprometer permanentemente el retorno de inversión y llevar a un estudio a la quiebra.
            
            ### Objetivos del Framework Analítico
            Este panel interactivo da respuesta sistemática a las preguntas comerciales indispensables para directores de producto y editores:
            """)
            st.info("""
            * **1. Evolución Temporal:** Evaluación del crecimiento macroeconómico global frente a saturación de lanzamientos.
            * **2. Categorías Dominantes:** Identificación del monopolio comercial de consolas y géneros.
            * **3. Asimetría Cultural:** Segmentación precisa del consumo regional (Norteamérica, Europa y Japón).
            * **4. El Factor de la Crítica:** Análisis de regresión de la correlación real entre notas de prensa y éxito comercial.
            * **5. Estacionalidad Táctica:** Descubrimiento del momento exacto del año para lanzar según la eficiencia por título.
            """)
        with col_der:
            st.markdown("### Ficha Técnica del Pipeline de Ingeniería de Datos")
            with st.expander("Ver Procesamiento y Saneamiento ETL", expanded=True):
                st.markdown("""
                * **Filtrado Anti-Sesgo:** Eliminación de registros con facturación en cero o nula para proteger las medias financieras de distorsiones por software gratuito o descatalogado.
                * **Tratamiento de Datos Ausentes:** Los campos nulos en variables cualitativas críticas como *Género* o *Plataforma* se rellenaron con la categoría controlada `Unknown` para conservar el volumen poblacional real.
                * **Resolución Temporal Eficiente:** Reconstrucción de la dimensión temporal extrayendo el año nativo directo del objeto de marca de tiempo (`release_date`) cuando la columna analítica presentaba nulos.
                * **Estandarización Semántica:** Mapeo automatizado mediante coincidencia léxica para unificar variaciones de nombres de columnas presentes en entornos heterogéneos de extracción.
                """)
            st.success("**Estado:** Datos consolidados, auditados y listos para la toma de decisiones analíticas.")

    # TAB 2: VOLUMEN
    with tabs[1]:
        st.header("Distribución del Mercado: Volumen de Producción vs Éxito Real")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Volumen de Títulos por Género")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            order_genres = df_filtered["genre"].value_counts().index if not df_filtered.empty else []
            if len(order_genres) > 0:
                sns.countplot(data=df_filtered, y="genre", order=order_genres, palette="magma", hue="genre", legend=False, ax=ax1)
            st.pyplot(fig1)
        with col2:
            st.subheader("La Realidad del Éxito Comercial (Sesgo Exponencial)")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            if not df_filtered.empty:
                sns.histplot(data=df_filtered, x="total_sales", bins=50, kde=True, color="purple", ax=ax2)
                ax2.set_xscale("log")
            st.pyplot(fig2)

    # TAB 3: CONCENTRACIÓN
    with tabs[2]:
        st.header("Concentración de Ingresos: ¿Quién se queda con el Pastel?")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top 10 Consolas por Volumen de Facturación")
            if not df_filtered.empty:
                top_consoles = df_filtered.groupby("console")["total_sales"].sum().sort_values(ascending=False).head(10).reset_index()
                fig3, ax3 = plt.subplots(figsize=(10, 5))
                sns.barplot(data=top_consoles, x="total_sales", y="console", palette="Blues_r", hue="console", legend=False, ax=ax3)
                st.pyplot(fig3)
        with col2:
            st.subheader("Rendimiento Económico Acumulado por Género")
            if not df_filtered.empty:
                ventas_genero = df_filtered.groupby("genre")["total_sales"].sum().sort_values(ascending=False).reset_index()
                fig4, ax4 = plt.subplots(figsize=(10, 5))
                sns.barplot(data=ventas_genero, x="total_sales", y="genre", palette="viridis", hue="genre", legend=False, ax=ax4)
                st.pyplot(fig4)

    # TAB 4: CRÍTICA Y GEOGRAFÍA
    with tabs[3]:
        st.header("Factores de Éxito: El Peso de la Crítica y la Ubicación")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("¿Una buena crítica garantiza ventas masivas?")
            df_critics = df_filtered[df_filtered["critic_score"].notnull() & (df_filtered["critic_score"] > 0)] if not df_filtered.empty else pd.DataFrame()
            if not df_critics.empty:
                fig5, ax5 = plt.subplots(figsize=(10, 5))
                sns.scatterplot(data=df_critics, x="critic_score", y="total_sales", alpha=0.4, color="teal", ax=ax5)
                sns.regplot(data=df_critics, x="critic_score", y="total_sales", scatter=False, color="crimson", ax=ax5)
                ax5.set_yscale("log")
                st.pyplot(fig5)
            else:
                st.info("No hay suficientes datos críticos de análisis en este rango.")
        with col2:
            st.subheader("Segmentación Geográfica de los Ingresos")
            if not df_filtered.empty:
                regiones = {"Norteamérica (NA)": df_filtered["na_sales"].sum(), "Europa / PAL": df_filtered["pal_sales"].sum(), "Japón (JP)": df_filtered["jp_sales"].sum(), "Otros Mercados": df_filtered["other_sales"].sum()}
                df_regiones = pd.DataFrame(list(regiones.items()), columns=["Region", "Ventas"])
                fig6, ax6 = plt.subplots(figsize=(10, 5))
                sns.barplot(data=df_regiones, x="Region", y="Ventas", palette="autumn", hue="Region", legend=False, ax=ax6)
                st.pyplot(fig6)

    # TAB 5: ESTACIONALIDAD Y VENTANAS ESTRATÉGICAS (¡Integración completa de tu módulo de éxitos masivos!)
    with tabs[4]:
        st.header("Análisis Táctico de Estacionalidad: El 'Timing' Perfecto")
        
        df_season = df_filtered[df_filtered["release_date"].notnull()].copy() if not df_filtered.empty else pd.DataFrame()
        if not df_season.empty:
            df_season["month_num"] = df_season["release_date"].dt.month
            meses_es = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
            df_season["month_es"] = df_season["month_num"].map(meses_es)
            
            # --- Bloque 1: Comportamiento Promedio del Mercado ---
            st.subheader("1. Tendencia Macroeconómica General por Meses")
            df_monthly = df_season.groupby(["month_num", "month_es"]).agg(total_sales_millions=("total_sales", "sum"), titles_launched=("total_sales", "count"), avg_sales_per_title=("total_sales", "mean")).reset_index().sort_values("month_num")
            
            fig7, axes_s = plt.subplots(1, 2, figsize=(16, 5))
            sns.barplot(data=df_monthly, x="month_es", y="total_sales_millions", ax=axes_s[0], color="#4a90e2", alpha=0.8)
            axes_s[0].set_xticklabels(df_monthly["month_es"], rotation=45)
            axes_s[0].set_title("Ingresos Totales (Barras) vs Volumen de Lanzamientos (Línea)", fontweight="bold")
            ax0_2 = axes_s[0].twinx()
            sns.lineplot(data=df_monthly, x="month_es", y="titles_launched", ax=ax0_2, color="#d0021b", marker="o")
            
            sns.barplot(data=df_monthly, x="month_es", y="avg_sales_per_title", ax=axes_s[1], palette="Oranges_r", hue="month_es", legend=False)
            axes_s[1].set_xticklabels(df_monthly["month_es"], rotation=45)
            axes_s[1].set_title("Rendimiento Promedio de Eficiencia por Título", fontweight="bold")
            st.pyplot(fig7)
            
            # --- Bloque 2: Comportamiento Estratégico de Blockbusters (Tu Código Corporativo) ---
            st.markdown("---")
            st.subheader("2. Comportamiento Exclusivo de Títulos Masivos (Top 5% del Mercado)")
            
            # Lógica matemática idéntica a tu cuaderno
            df_hits = df_season.copy()
            df_hits["quarter"] = "Q" + df_hits["release_date"].dt.quarter.astype(str)
            
            umbral_top_5 = df_hits["total_sales"].quantile(0.95)
            df_blockbusters = df_hits[df_hits["total_sales"] >= umbral_top_5]
            
            # Indicadores Ejecutivos Rápidos
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.info(f"**Umbral de Entrada Corporativa (Percentil 95):** Requiere un récord superior a **${umbral_top_5:.2f}M USD** en ventas.")
            with col_b2:
                st.success(f"**Población de Superventas Identificada:** **{df_blockbusters.shape[0]} títulos** marcan la pauta élite de la industria.")
                
            orden_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            orden_trimestres = ["Q1", "Q2", "Q3", "Q4"]
            
            # Renderizado de Gráficas Corporativas Combinadas
            fig_hits, axes_hits = plt.subplots(1, 2, figsize=(18, 6))
            
            # Gráfica A: Distribución Mensual
            sns.countplot(data=df_blockbusters, x="month_es", order=orden_meses, palette="Purples_r", ax=axes_hits[0], hue="month_es", legend=False)
            axes_hits[0].set_title("Distribución Mensual de los Lanzamientos Más Masivos (Top 5%)", fontweight="bold", pad=15, fontsize=12)
            axes_hits[0].set_xlabel("Mes de Lanzamiento", fontweight="semibold")
            axes_hits[0].set_ylabel("Cantidad de Superventas Lanzados", fontweight="semibold")
            axes_hits[0].set_xticklabels(orden_meses, rotation=40)
            
            for p in axes_hits[0].patches:
                height = p.get_height()
                if height > 0:
                    axes_hits[0].annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height + 1),
                                        ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            # Gráfica B: Cuota por Trimestre Comercial
            conteo_q = df_blockbusters["quarter"].value_counts().reindex(orden_trimestres)
            axes_hits[1].pie(conteo_q, labels=conteo_q.index, autopct='%1.1f%%', startangle=90, 
                       colors=["#9dc6e0", "#a1dab4", "#feb24c", "#f03b20"], 
                       textprops={'fontsize': 12, 'fontweight': 'bold'},
                       wedgeprops={'edgecolor': 'white', 'linewidth': 2})
            axes_hits[1].set_title("Cuota por Trimestre de los Títulos con Mayores Ventas", fontweight="bold", pad=15, fontsize=12)
            
            plt.tight_layout()
            st.pyplot(fig_hits)
            
            # Tabla de Control Ejecutiva en Formato Streamlit Limpio
            st.markdown("#### 🏆 Muestra de Control: Top 5 Líderes Históricos del Segmento Élite")
            columnas_muestra = [c for c in ['title', 'name', 'console', 'platform', 'year', 'total_sales', 'month_es'] if c in df_blockbusters.columns]
            df_top_five = df_blockbusters.sort_values(by="total_sales", ascending=False)[columnas_muestra].head(5)
            st.dataframe(df_top_five, use_container_width=True)
            
        else:
            st.info("Sin registros de fecha válidos para calcular estacionalidad.")

# ------------------------------------------------------------------------------
# MODO B: SECCIÓN COMBINADA CON FILTROS INTEGRADOS EN LA PROPIA PÁGINA
# ------------------------------------------------------------------------------
elif app_mode == "search_and_catalog":
    st.title("🔍 Explorador Avanzado de Videojuegos")
    st.subheader("Auditoría individual y análisis de carteras corporativas")
    st.markdown("---")
    
    st.markdown("### Filtros de Segmentación de Catálogo")
    col_filtro_izq, col_filtro_der = st.columns(2)
    
    with col_filtro_izq:
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())
        year_range = st.slider("Rango de Años de Lanzamiento", min_value=min_year, max_value=max_year, value=(min_year, max_year), key="catalog_filter_year")
        
    with col_filtro_der:
        lista_generos = sorted(df['genre'].unique().tolist())
        generos_seleccionados = st.multiselect("Filtrar por Género Comercial", options=lista_generos, default=lista_generos, key="catalog_filter_genre")
    
    df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1]) & (df['genre'].isin(generos_seleccionados))]
    st.markdown("---")
    
    tab_buscador, tab_publisher, tab_plataforma = st.tabs(["🔍 Buscador Individual de Títulos", "🏢 Catálogo Corporativo por Publisher", "🎮 Catálogo por Plataforma / Consola"])
    
    with tab_buscador:
        st.markdown("### Inspección Detallada por Ficha de Producto")
        lista_titulos = sorted(df_filtered[title_col].dropna().unique()) if not df_filtered.empty else []
        if len(lista_titulos) > 0:
            titulo_seleccionado = st.selectbox("Seleccione el videojuego que desea auditar:", lista_titulos, key="search_individual_box")
            df_juego = df_filtered[df_filtered[title_col] == titulo_seleccionado]
            if not df_juego.empty:
                juego_data = df_juego.iloc[0]
                col_img, col_metrics = st.columns([1, 2])
                with col_img:
                    path_foto = str(juego_data[img_col]).strip()
                    url_final = f"https://www.vgchartz.com{path_foto}" if path_foto.startswith('/') else (path_foto if path_foto.startswith('http') else "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400")
                    try: st.image(url_final, use_container_width=True)
                    except Exception: st.image("https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400", use_container_width=True)
                with col_metrics:
                    st.markdown(f"## {juego_data[title_col]}")
                    c1, c2, c3 = st.columns(3)
                    c1.metric(" Plataforma", str(juego_data[console_col]).upper())
                    c2.metric(" Publisher / Editor", str(juego_data[publisher_col]))
                    c3.metric(" Desarrollador / Estudio", str(juego_data['developer']) if ('developer' in juego_data and pd.notna(juego_data['developer'])) else "No Disponible")
                    c4, c5, c6 = st.columns(3)
                    c4.metric(" Género Comercial", str(juego_data['genre']))
                    c5.metric(" Año de Estreno", f"{int(juego_data['year'])}")
                    c6.metric(" Facturación Global", f"{juego_data[sales_col]:.2f} M USD")
                    with st.expander("🌍 Distribución de Ventas por Mercado Geográfico"):
                        r1, r2, r3, r4 = st.columns(4)
                        r1.metric("🇺🇸 Norteamérica (NA)", f"{juego_data['na_sales']:.2f} M" if 'na_sales' in juego_data else "N/D")
                        r2.metric("🇪🇺 Europa / PAL", f"{juego_data['pal_sales']:.2f} M" if 'pal_sales' in juego_data else "N/D")
                        r3.metric("🇯🇵 Japón (JP)", f"{juego_data['jp_sales']:.2f} M" if 'jp_sales' in juego_data else "N/D")
                        r4.metric(" Otros Mercados", f"{juego_data['other_sales']:.2f} M" if 'other_sales' in juego_data else "N/D")
        else:
            st.warning(" No hay títulos que coincidan con los criterios de filtrado.")
            
    with tab_publisher:
        st.markdown("### Cartera de Productos por Compañía Editora")
        lista_publishers = sorted(df_filtered[publisher_col].dropna().unique()) if (publisher_col in df_filtered.columns and not df_filtered.empty) else []
        if len(lista_publishers) > 0:
            pub_seleccionado = st.selectbox("Seleccione el Publisher / Editor a auditar:", lista_publishers, key="search_publisher_box")
            df_pub = df_filtered[df_filtered[publisher_col] == pub_seleccionado].sort_values(by=sales_col, ascending=False)
            if not df_pub.empty:
                kpi1, kpi2, kpi3 = st.columns(3)
                kpi1.metric(" Títulos que cumplen el filtro", f"{len(df_pub)}")
                kpi2.metric(" Facturación en este segmento", f"${df_pub[sales_col].sum():.2f}M USD")
                kpi3.metric(" Líder del Filtro", f"{df_pub.iloc[0][title_col]}")
                st.markdown("---")
                max_mostrar = st.slider("Cantidad máxima de títulos a renderizar:", min_value=4, max_value=40, value=12, step=4, key="slider_pub_games")
                grid_cols = st.columns(4)
                for idx, (index, row) in enumerate(df_pub.head(max_mostrar).iterrows()):
                    col_target = idx % 4
                    with grid_cols[col_target]:
                        img_p = str(row[img_col]).strip()
                        url_img = f"https://www.vgchartz.com{img_p}" if img_p.startswith('/') else (img_p if img_p.startswith('http') else "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=200")
                        try: st.image(url_img, use_container_width=True)
                        except Exception: st.image("https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=200", use_container_width=True)
                        st.markdown(f"**{row[title_col]}**")
                        dev_info = str(row['developer']) if ('developer' in row and pd.notna(row['developer'])) else "Desconocido"
                        st.caption(f"🕹️ `{str(row[console_col]).upper()}` | 🎭 `{row['genre']}` | 📅 {int(row['year'])}")
                        st.markdown(f"📈 Total: **{row[sales_col]:.2f} M USD**")
                        st.markdown("---")
        else:
            st.warning(" No hay datos de Publishers disponibles.")

    with tab_plataforma:
        st.markdown("### Búsqueda y Exploración de Títulos por Consola")
        lista_consolas = sorted(df_filtered[console_col].dropna().unique()) if (console_col in df_filtered.columns and not df_filtered.empty) else []
        if len(lista_consolas) > 0:
            consola_seleccionada = st.selectbox("Seleccione la Plataforma / Consola a auditar:", lista_consolas, key="search_console_box")
            df_consola = df_filtered[df_filtered[console_col] == consola_seleccionada].sort_values(by=sales_col, ascending=False)
            if not df_consola.empty:
                kpi1, kpi2, kpi3 = st.columns(3)
                kpi1.metric("📦 Títulos detectados bajo el filtro", f"{len(df_consola)}")
                kpi2.metric("💰 Facturación de la plataforma", f"${df_consola[sales_col].sum():.2f}M USD")
                kpi3.metric("🔝 Más Vendido", f"{df_consola.iloc[0][title_col]}")
                st.markdown("---")
                max_mostrar_c = st.slider("Cantidad máxima de títulos a renderizar:", min_value=4, max_value=40, value=12, step=4, key="slider_console_games")
                grid_cols_c = st.columns(4)
                for idx, (index, row) in enumerate(df_consola.head(max_mostrar_c).iterrows()):
                    col_target = idx % 4
                    with grid_cols_c[col_target]:
                        img_p = str(row[img_col]).strip()
                        url_img = f"https://www.vgchartz.com{img_p}" if img_p.startswith('/') else (img_p if img_p.startswith('http') else "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=200")
                        try: st.image(url_img, use_container_width=True)
                        except Exception: st.image("https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=200", use_container_width=True)
                        st.markdown(f"**{row[title_col]}**")
                        st.caption(f"🏢 `{row[publisher_col]}` | 🎭 `{row['genre']}` | 📅 {int(row['year'])}")
                        st.markdown(f"📈 Total: **{row[sales_col]:.2f} M USD**")
                        st.markdown("---")
        else:
            st.warning(" No hay datos de Plataformas disponibles.")

# ------------------------------------------------------------------------------
# MODO C: SECCIÓN PROPIA DE TÍTULOS LÍDERES EN EL MERCADO (Histórico Global)
# ------------------------------------------------------------------------------
elif app_mode == "market_leaders":
    df_filtered = df.copy()
    st.title("🏆 Títulos Líderes en el Mercado")
    st.subheader("Clasificación de los videojuegos más vendidos a nivel histórico global")
    st.markdown("---")
    if not df_filtered.empty:
        top_n = st.slider("Seleccione el tamaño del ranking a evaluar:", min_value=5, max_value=50, value=10, step=5, key="leaders_top_slider")
        top_games = df_filtered.sort_values(by=sales_col, ascending=False).head(top_n)
        cols_per_row = 5
        for i in range(0, len(top_games), cols_per_row):
            chunk = top_games.iloc[i:i+cols_per_row]
            cols = st.columns(cols_per_row)
            for idx, (index, row) in enumerate(chunk.iterrows()):
                with cols[idx]:
                    st.markdown(f"### Ranking #{i + idx + 1}")
                    img_path = str(row[img_col]).strip()
                    url_final = f"https://www.vgchartz.com{img_path}" if img_path.startswith('/') else (img_path if img_path.startswith('http') else "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=200")
                    try: st.image(url_final, use_container_width=True)
                    except Exception: st.image("https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=200", use_container_width=True)
                    st.markdown(f"**{row[title_col]}**")
                    st.caption(f" `{str(row[console_col]).upper()}` |  `{row['genre']}` |  {int(row['year'])}")
                    st.markdown(f" Facturación: **{row[sales_col]:.2f} M**")
            st.markdown("---")

# ------------------------------------------------------------------------------
# MODO D: DOCUMENTACIÓN TÉCNICA
# ------------------------------------------------------------------------------
elif app_mode == "docs":
    st.title("Arquitectura del Proyecto & Ficha Técnica")
    st.markdown("---")
    st.markdown("""
    ### Resumen Técnico de Transformaciones (ETL)
    1. **Estandarización de Esquemas:** Mapeo automático de nombres de columnas mediante búsquedas de patrones semánticos.
    2. **Filtrado de Sesgo por Nulos:** Eliminación estricta de registros sin tracción económica o sin asignación temporal nítida.
    """)
    st.dataframe(df.head(20))