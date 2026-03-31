import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Gestión de Stock LATAM - SOP", layout="wide")

st.title("🏠 Sistema de Gestión de Stock – Gabinetes PRIME & FANTASY")
st.markdown("---")

# --- BLOQUE 1: CONFIGURACIÓN GLOBAL ---
st.sidebar.header("⚙️ CONFIGURACIÓN GLOBAL")
with st.sidebar:
    lead_time = st.number_input("Lead Time de Fabricación (semanas)", min_value=1, value=4)
    nivel_servicio = st.slider("Nivel de Servicio Objetivo (%)", 0.90, 0.99, 0.97)
    escenario_activo = st.selectbox("Seleccionar Escenario Activo", ["A", "B", "C"], index=1)
    fecha_revision = st.date_input("Fecha Última Revisión")
    periodo_analisis = st.text_input("Período de Análisis", "Q2 2026 (Abr–Jun)")

# --- BLOQUE 2: PARÁMETROS POR ESCENARIO (PRIME & FANTASY) ---
st.header("📐 Configuración de Escenarios")
col1, col2 = st.columns(2)

def calc_parametros(base, ajuste, seguridad, maximo, lt):
    ajustada = base * (1 + (ajuste / 100))
    rop = seguridad + (ajustada * lt)
    estandar = maximo - rop
    return ajustada, rop, estandar

# Diccionario para almacenar parámetros
params = {
    "PRIME": {"A": {}, "B": {}, "C": {}},
    "FANTASY": {"A": {}, "B": {}, "C": {}}
}

with col1:
    st.subheader("▌ PARÁMETROS — PRIME")
    for esc in ["A", "B", "C"]:
        with st.expander(f"Escenario {esc}"):
            # Valores por defecto basados en el Excel original
            def_base = 42.0
            def_ajuste = 0.0 if esc == "A" else (20.0 if esc == "B" else 55.0)
            def_ss = 25 if esc == "A" else (35 if esc == "B" else 50)
            def_max = 250 if esc == "A" else (300 if esc == "B" else 380)
            
            p_base = st.number_input(f"Demanda Base - {esc} (PRIME)", value=def_base, key=f"p_b_{esc}")
            p_ajuste = st.number_input(f"Ajuste % - {esc} (PRIME)", value=def_ajuste, key=f"p_a_{esc}")
            p_ss = st.number_input(f"Stock Seguridad - {esc} (PRIME)", value=def_ss, key=f"p_s_{esc}")
            p_max = st.number_input(f"Stock Máximo - {esc} (PRIME)", value=def_max, key=f"p_m_{esc}")
            
            ajust, rop, std = calc_parametros(p_base, p_ajuste, p_ss, p_max, lead_time)
            params["PRIME"][esc] = {"ajustada": ajust, "rop": rop, "max": p_max, "ss": p_ss}
            st.caption(f"ROP calculado: {rop:.1f} | Orden Estándar: {std:.1f}")

with col2:
    st.subheader("▌ PARÁMETROS — FANTASY")
    for esc in ["A", "B", "C"]:
        with st.expander(f"Escenario {esc}"):
            # Valores por defecto basados en el Excel original
            def_base_f = 16.0 if esc == "A" else 21.0
            def_ajuste_f = 10.0 if esc == "A" else (20.0 if esc == "B" else 65.0)
            def_ss_f = 12 if esc == "A" else (20 if esc == "B" else 28)
            def_max_f = 100 if esc == "A" else (130 if esc == "B" else 200)

            f_base = st.number_input(f"Demanda Base - {esc} (FANTASY)", value=def_base_f, key=f"f_b_{esc}")
            f_ajuste = st.number_input(f"Ajuste % - {esc} (FANTASY)", value=def_ajuste_f, key=f"f_a_{esc}")
            f_ss = st.number_input(f"Stock Seguridad - {esc} (FANTASY)", value=def_ss_f, key=f"f_s_{esc}")
            f_max = st.number_input(f"Stock Máximo - {esc} (FANTASY)", value=def_max_f, key=f"f_m_{esc}")
            
            ajust, rop, std = calc_parametros(f_base, f_ajuste, f_ss, f_max, lead_time)
            params["FANTASY"][esc] = {"ajustada": ajust, "rop": rop, "max": f_max, "ss": f_ss}
            st.caption(f"ROP calculado: {rop:.1f} | Orden Estándar: {std:.1f}")

# --- BLOQUE 3: ENTRADA MANUAL DE STOCK ACTUAL ---
st.markdown("---")
st.header("▌ STOCK ACTUAL Y FABRICACIONES PENDIENTES")
c1, c2 = st.columns(2)

with c1:
    st.subheader("Gabinete PRIME")
    st_fisico_p = st.number_input("Stock Físico Actual (PRIME)", min_value=0, value=0)
    st_fab_p = st.number_input("Fabricaciones Pendientes (PRIME)", min_value=0, value=0)
    st_pedidos_p = st.number_input("Pedidos en Firme (PRIME)", min_value=0, value=0)
    st_forecast_p = st.number_input("Forecast del Período (PRIME)", min_value=0, value=0)

with c2:
    st.subheader("Gabinete FANTASY")
    st_fisico_f = st.number_input("Stock Físico Actual (FANTASY)", min_value=0, value=0)
    st_fab_f = st.number_input("Fabricaciones Pendientes (FANTASY)", min_value=0, value=0)
    st_pedidos_f = st.number_input("Pedidos en Firme (FANTASY)", min_value=0, value=0)
    st_forecast_f = st.number_input("Forecast del Período (FANTASY)", min_value=0, value=0)

# --- BLOQUE 4: CÁLCULOS DEL PANEL DE CONTROL ---
def generar_analisis(producto, fisico, pendientes, pedidos, forecast, p_dict):
    disp = fisico + pendientes - pedidos
    rop = p_dict["rop"]
    max_st = p_dict["max"]
    ss = p_dict["ss"]
    dem_sem = p_dict["ajustada"]
    
    # Lógica de Alertas
    if disp <= ss:
        estado = "🔴 ALERTA ROJA"
        color = "red"
    elif disp <= rop:
        estado = "🟡 REAPROVISIONAR"
        color = "orange"
    else:
        estado = "✅ STOCK OK"
        color = "green"
        
    sug_orden = max(0, max_st - disp) if disp <= rop else 0
    cobertura = disp / dem_sem if dem_sem > 0 else 0
    
    return {
        "Inventario Disponible": disp,
        "ROP": rop,
        "Stock Máximo": max_st,
        "Stock Seguridad": ss,
        "Exceso/Déficit vs ROP": disp - rop,
        "Orden Sugerida": sug_orden,
        "Estado": estado,
        "Color": color,
        "Cobertura (sem)": cobertura
    }

analisis_p = generar_analisis("PRIME", st_fisico_p, st_fab_p, st_pedidos_p, st_forecast_p, params["PRIME"][escenario_activo])
analisis_f = generar_analisis("FANTASY", st_fisico_f, st_fab_f, st_pedidos_f, st_forecast_f, params["FANTASY"][escenario_activo])

# --- BLOQUE 5: VISUALIZACIÓN DE RESULTADOS ---
st.markdown("---")
st.header(f"📊 PANEL DE CONTROL - ESCENARIO {escenario_activo}")

res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric("Inv. Disponible PRIME", f"{analisis_p['Inventario Disponible']} u.")
    st.markdown(f"**Estado:** :{analisis_p['Color']}[{analisis_p['Estado']}]")
    st.write(f"**Cobertura:** {analisis_p['Cobertura (sem)']:.1f} semanas")
    if analisis_p['Orden Sugerida'] > 0:
        st.warning(f"Lanzar fabricación de: {analisis_p['Orden Sugerida']:.0f} unidades")

with res_col2:
    st.metric("Inv. Disponible FANTASY", f"{analisis_f['Inventario Disponible']} u.")
    st.markdown(f"**Estado:** :{analisis_f['Color']}[{analisis_f['Estado']}]")
    st.write(f"**Cobertura:** {analisis_f['Cobertura (sem)']:.1f} semanas")
    if analisis_f['Orden Sugerida'] > 0:
        st.warning(f"Lanzar fabricación de: {analisis_f['Orden Sugerida']:.0f} unidades")

# Tabla comparativa final
st.subheader("Resumen de Parámetros Activos")
df_resumen = pd.DataFrame({
    "Indicador": ["Demanda Semanal Ajustada", "Stock Seguridad", "ROP", "Stock Máximo"],
    "PRIME": [params["PRIME"][escenario_activo]["ajustada"], params["PRIME"][escenario_activo]["ss"], params["PRIME"][escenario_activo]["rop"], params["PRIME"][escenario_activo]["max"]],
    "FANTASY": [params["FANTASY"][escenario_activo]["ajustada"], params["FANTASY"][escenario_activo]["ss"], params["FANTASY"][escenario_activo]["rop"], params["FANTASY"][escenario_activo]["max"]]
})
st.table(df_resumen)
# --- BLOQUE 6: EVOLUCIÓN SEMANAL CON ENTRADAS PROGRAMADAS ---
st.markdown("---")
st.header("📈 PROYECCIÓN DE EVOLUCIÓN SEMANAL")
st.info("Introduce las unidades que esperas recibir cada semana (entradas de fábrica/importación).")

num_semanas = st.slider("Semanas a proyectar", 4, 12, 8)

col_ent1, col_ent2 = st.columns(2)

with col_ent1:
    st.subheader("Entradas Programadas - PRIME")
    # Creamos una fila de inputs horizontales para las entradas semanales
    entradas_p = [st.number_input(f"Sem +{i} (P)", min_value=0, value=0, key=f"ep_{i}") for i in range(1, num_semanas + 1)]

with col_ent2:
    st.subheader("Entradas Programadas - FANTASY")
    entradas_f = [st.number_input(f"Sem +{i} (F)", min_value=0, value=0, key=f"ef_{i}") for i in range(1, num_semanas + 1)]

def proyectar_stock_con_entradas(inicio, dem_ajustada, rop, ss, lista_entradas):
    proyeccion = []
    stock_iter = inicio
    for i, entrada in enumerate(lista_entradas):
        # El stock de la semana es: Stock Anterior - Demanda + Entrada programada
        stock_iter = stock_iter - dem_ajustada + entrada
        proyeccion.append({
            "Semana": f"Sem +{i+1}",
            "Stock Proyectado": round(max(0, stock_iter), 1),
            "Punto Pedido (ROP)": rop,
            "Seguridad (SS)": ss
        })
    return pd.DataFrame(proyeccion)

# --- Visualización de Gráficos ---
c_g1, c_g2 = st.columns(2)

with c_g1:
    df_p = proyectar_stock_con_entradas(
        analisis_p['Inventario Disponible'], 
        params["PRIME"][escenario_activo]["ajustada"],
        params["PRIME"][escenario_activo]["rop"],
        params["PRIME"][escenario_activo]["ss"],
        entradas_p
    )
    st.line_chart(df_p.set_index("Semana"))
    
    # Lógica de alertas preventivas
    if (df_p["Stock Proyectado"] < params["PRIME"][escenario_activo]["ss"]).any():
        sem_critica = df_p[df_p["Stock Proyectado"] < params["PRIME"][escenario_activo]["ss"]].iloc[0]["Semana"]
        st.error(f"🚨 PRIME: Rotura de Stock de Seguridad en {sem_critica}")

with c_g2:
    df_f = proyectar_stock_con_entradas(
        analisis_f['Inventario Disponible'], 
        params["FANTASY"][escenario_activo]["ajustada"],
        params["FANTASY"][escenario_activo]["rop"],
        params["FANTASY"][escenario_activo]["ss"],
        entradas_f
    )
    st.line_chart(df_f.set_index("Semana"))
    
    if (df_f["Stock Proyectado"] < params["FANTASY"][escenario_activo]["ss"]).any():
        sem_critica_f = df_f[df_f["Stock Proyectado"] < params["FANTASY"][escenario_activo]["ss"]].iloc[0]["Semana"]
        st.error(f"🚨 FANTASY: Rotura de Stock de Seguridad en {sem_critica_f}")

# Tabla de resumen para exportar o revisar
with st.expander("📄 Ver detalle de datos proyectados"):
    st.write("Datos calculados (Stock Final de cada semana)")
    col_t1, col_t2 = st.columns(2)
    col_t1.dataframe(df_p)
    col_t2.dataframe(df_f)
