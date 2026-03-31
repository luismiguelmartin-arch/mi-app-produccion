import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Gestor de Producción y Stock", layout="wide")

st.title("🚀 Sistema de Gestión de Fabricación")

# --- BARRA LATERAL (NAVEGACIÓN) ---
menu = st.sidebar.selectbox("Seleccionar Pestaña", ["Parámetros", "Panel de Control"])

# --- PESTAÑA 1: PARÁMETROS ---
if menu == "Parámetros":
    st.header("⚙️ Configuración de Parámetros")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Valores Generales")
        d17 = st.number_input("Parámetro D17", value=0.0)
        d18 = st.number_input("Parámetro D18", value=0.0)
        d19 = st.number_input("Parámetro D19", value=0.0)
        d20 = st.number_input("Parámetro D20", value=0.0)
        d21 = st.number_input("Parámetro D21", value=0.0)

    with col2:
        st.subheader("Bloque de Control A")
        # Agrupamos D, E, F para las filas 26, 27, 29, 31
        for fila in [26, 27, 29, 31]:
            c1, c2, c3 = st.columns(3)
            globals()[f"d{fila}"] = c1.number_input(f"D{fila}", value=0.0, key=f"d{fila}")
            globals()[f"e{fila}"] = c2.number_input(f"E{fila}", value=0.0, key=f"e{fila}")
            globals()[f"f{fila}"] = c3.number_input(f"F{fila}", value=0.0, key=f"f{fila}")

    with col3:
        st.subheader("Bloque de Control B")
        # Agrupamos D, E, F para las filas 36, 37, 39, 41
        for fila in [36, 37, 39, 41]:
            c1, c2, c3 = st.columns(3)
            globals()[f"d{fila}"] = c1.number_input(f"D{fila}", value=0.0, key=f"d{fila}")
            globals()[f"e{fila}"] = c2.number_input(f"E{fila}", value=0.0, key=f"e{fila}")
            globals()[f"f{fila}"] = c3.number_input(f"F{fila}", value=0.0, key=f"f{fila}")

# --- PESTAÑA 2: PANEL DE CONTROL ---
elif menu == "Panel de Control":
    st.header("📊 Panel de Control")
    
    st.subheader("▌ STOCK ACTUAL Y FABRICACIONES PENDIENTES (Entrada Manual)")
    
    # Creamos una tabla editable para el stock
    data_stock = {
        "Producto/Referencia": ["Prod A", "Prod B", "Prod C", "Prod D"],
        "Stock Actual": [0, 0, 0, 0],
        "Fabricaciones Pendientes": [0, 0, 0, 0]
    }
    df_stock = pd.DataFrame(data_stock)
    
    # El componente experimental_data_editor permite editar como en Excel
    df_editado = st.data_editor(df_stock, num_rows="dynamic", use_container_width=True)

    # --- LÓGICA DE CÁLCULO ---
    st.divider()
    if st.button("Calcular Necesidades"):
        # Aquí deberás programar las fórmulas que tenía tu Excel
        # Ejemplo simple:
        stock_total = df_editado["Stock Actual"].sum()
        st.success(f"Cálculo completado. El stock total procesado es: {stock_total}")
        
        # Aquí puedes añadir gráficos
        st.bar_chart(df_editado.set_index("Producto/Referencia")["Stock Actual"])
