import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA WEB
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Laboratorio Interactivo de Espectroscopía",
    page_icon="🔬",
    layout="wide"
)

# Constantes físicas
hc_k = 1.438777  # h*c/k en cm*K

# -----------------------------------------------------------------------------
# 2. ENCABEZADO Y NAVEGACIÓN
# -----------------------------------------------------------------------------
st.title("🔬 Laboratorio Interactivo de Espectroscopía Molecular")
st.markdown("Plataforma didáctica para la simulación de espectros de rotación y vibración-rotación.")

tabs = st.tabs([
    "🐍 Módulo 1: Introducción", 
    "🎨 Módulo 2: ¿Qué es un Espectro?", 
    "🌀 Módulo 3: Rotación (CO)", 
    "🧪 Módulo 4: Vibración-Rotación (HCl)", 
    "⚖️ Módulo 5: Efecto Isotópico", 
    "📝 Módulo 6: Autoevaluación"
])

# -----------------------------------------------------------------------------
# MÓDULO 1: PRIMEROS PASOS
# -----------------------------------------------------------------------------
with tabs[0]:
    st.header("🐍 Módulo 1: Introducción y Constantes Fundamentales")
    st.info("Bienvenido/a al laboratorio virtual. En esta sección repasamos las bases de la espectroscopía cuánctica.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📏 Constantes Fundamentales")
        st.latex(r"h = 6.626 \times 10^{-34} \text{ J}\cdot\text{s} \quad (\text{Planck})")
        st.latex(r"c = 2.998 \times 10^{10} \text{ cm/s} \quad (\text{Velocidad de la luz})")
        st.latex(r"k = 1.381 \times 10^{-23} \text{ J/K} \quad (\text{Boltzmann})")
    
    with col2:
        st.subheader("💡 ¿Sabías que?")
        st.markdown("""
        Estas constantes aparecen en las ecuaciones porque la espectroscopía es **cuántica**, no clásica.
        Los cambios de energía en las moléculas ocurren en paquetes discretos (cuantos).
        """)

# -----------------------------------------------------------------------------
# MÓDULO 2: ¿QUÉ ES UN ESPECTRO?
# -----------------------------------------------------------------------------
with tabs[1]:
    st.header("🎨 Módulo 2: Concepto de Espectro y Niveles de Energía")
    
    col_ctrl, col_plot = st.columns([1, 2.5])
    with col_ctrl:
        st.subheader("⚙️ Configuración")
        num_picos = st.slider("Número de transiciones (picos):", 1, 8, 5)
        separacion = st.slider("Espaciado entre picos:", 1.0, 5.0, 3.0)
    
    with col_plot:
        frecuencias = np.linspace(0, 30, 500)
        intensidad = np.zeros_like(frecuencias)
        
        fig = go.Figure()
        for i in range(num_picos):
            f_centro = (i + 1) * separacion
            amp = np.exp(-i * 0.2)
            intensidad += amp * np.exp(-((frecuencias - f_centro)**2) / 0.5)
            fig.add_vline(x=f_centro, line_dash="dash", line_color="red", opacity=0.4)
            fig.add_annotation(x=f_centro, y=amp + 0.05, text=f"J={i}", showarrow=False)

        fig.add_trace(go.Scatter(x=frecuencias, y=intensidad, mode='lines', fill='tozeroy', line=dict(color='purple', width=2), name="Espectro"))
        fig.update_layout(title="Simulación de un Espectro de Absorcón", xaxis_title="Frecuencia / Número de onda", yaxis_title="Intensidad", template="plotly_white", height=450)
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# MÓDULO 3: ESPECTROSCOPÍA ROTACIONAL (CO)
# -----------------------------------------------------------------------------
with tabs[2]:
    st.header("🌀 Módulo 3: Espectro Rotacional Puro (Microondas - CO)")
    
    col3_ctrl, col3_plot = st.columns([1, 2.5])
    with col3_ctrl:
        st.subheader("⚙️ Parámetros de Control")
        r_CO = st.slider("Longitud de enlace (Å):", min_value=0.8, max_value=1.5, value=1.128, step=0.005)
        T_CO = st.slider("Temperatura (K):", min_value=10, max_value=500, value=298, step=10, key="T_CO")
        
        # Cálculos de CO
        masa_C = 12.01 * 1.66054e-27
        masa_O = 16.00 * 1.66054e-27
        mu = (masa_C * masa_O) / (masa_C + masa_O)
        I = mu * (r_CO * 1e-10)**2
        B_GHz = (6.626e-34 / (8 * (np.pi**2) * I)) * 1e-9
        espaciado_CO = 2 * B_GHz
        
        st.info(f"**Constante Rotacional (B):** {B_GHz:.2f} GHz\n\n**Espaciado (2B):** {espaciado_CO:.2f} GHz")
    
    with col3_plot:
        J_vals = np.arange(0, 10)
        frec_rot = [2 * B_GHz * (J + 1) for J in J_vals]
        int_rot = [(2*J + 1) * np.exp(- (B_GHz * 1e9 * 6.626e-34 * J * (J + 1)) / (1.381e-23 * max(T_CO, 1))) for J in J_vals]
        int_rot = np.array(int_rot) / max(int_rot) if max(int_rot) > 0 else int_rot
        
        fig_rot = go.Figure()
        for f, i_val in zip(frec_rot, int_rot):
            fig_rot.add_trace(go.Scatter(x=[f, f], y=[0, i_val], mode='lines+markers', line=dict(color='purple', width=3), marker=dict(size=8, color='purple'), showlegend=False))
        
        fig_rot.update_layout(title=f"Espectro Rotacional del Monóxido de Carbono (CO) - r = {r_CO:.3f} Å", xaxis_title="Frecuencia (GHz)", yaxis_title="Intensidad Relativa", template="plotly_white", height=450)
        st.plotly_chart(fig_rot, use_container_width=True)

# -----------------------------------------------------------------------------
# MÓDULO 4: VIBRACIÓN-ROTACIÓN (HCl)
# -----------------------------------------------------------------------------
with tabs[3]:
    st.header("🧪 Módulo 4: Espectro Vibracional-Rotacional (IR - HCl)")
    
    col4_ctrl, col4_plot = st.columns([1, 2.5])
    with col4_ctrl:
        st.subheader("⚙️ Parámetros del HCl")
        B0_hcl = st.slider("B₀ (cm⁻¹):", 10.0, 10.8, 10.44, 0.01)
        B1_hcl = st.slider("B₁ (cm⁻¹):", 9.8, 10.5, 10.136, 0.01)
        nu0_hcl = st.slider("ν₀ (cm⁻¹):", 2800.0, 3000.0, 2885.9, 1.0)
        T_hcl = st.slider("Temperatura (K):", 10, 500, 298, 10, key="T_hcl")
        
    with col4_plot:
        J_max = 12
        J_P = np.arange(1, J_max)
        frec_P = nu0_hcl - (B1_hcl + B0_hcl)*J_P + (B1_hcl - B0_hcl)*(J_P**2)
        
        J_R = np.arange(0, J_max - 1)
        frec_R = nu0_hcl + (B1_hcl + B0_hcl)*(J_R + 1) + (B1_hcl - B0_hcl)*((J_R + 1)**2)
        
        int_P = [(2*J + 1) * np.exp(- B0_hcl * J * (J + 1) * hc_k / max(T_hcl, 1)) for J in J_P]
        int_R = [(2*J + 1) * np.exp(- B0_hcl * J * (J + 1) * hc_k / max(T_hcl, 1)) for J in J_R]
        
        max_int = max(max(int_P), max(int_R))
        int_P, int_R = np.array(int_P) / max_int, np.array(int_R) / max_int
        
        fig_hcl = go.Figure()
        # Rama P (roja)
        for f, i_val in zip(frec_P, int_P):
            fig_hcl.add_trace(go.Scatter(x=[f, f], y=[0, i_val], mode='lines+markers', line=dict(color='red', width=2, dash='dash'), marker=dict(symbol='circle', color='red'), name="Rama P (ΔJ=-1)", showlegend=False))
        # Rama R (azul)
        for f, i_val in zip(frec_R, int_R):
            fig_hcl.add_trace(go.Scatter(x=[f, f], y=[0, i_val], mode='lines+markers', line=dict(color='blue', width=2), marker=dict(symbol='square', color='blue'), name="Rama R (ΔJ=+1)", showlegend=False))
        
        fig_hcl.add_vline(x=nu0_hcl, line_dash="dot", line_color="black")
        fig_hcl.update_layout(title="Espectro Rovibracional del HCl (Ramas P y R)", xaxis_title="Número de onda (cm⁻¹)", yaxis_title="Intensidad Relativa", template="plotly_white", height=450)
        st.plotly_chart(fig_hcl, use_container_width=True)

# -----------------------------------------------------------------------------
# MÓDULO 5: EFECTO ISOTÓPICO
# -----------------------------------------------------------------------------
with tabs[4]:
    st.header("⚖️ Módulo 5: Comparación Isotópica (H³⁵Cl vs H³⁷Cl)")
    
    mode_iso = st.radio("Modo de visualización:", ["Individual", "Superposición Directa"], horizontal=True)
    
    # Parámetros de los isótopos
    B0_35, B1_35, nu0_35 = 10.44, 10.136, 2885.9
    B0_37, B1_37, nu0_37 = 10.42, 10.120, 2883.8
    
    J_max = 12
    J_P = np.arange(1, J_max)
    J_R = np.arange(0, J_max - 1)
    
    frec_P35 = nu0_35 - (B1_35 + B0_35)*J_P + (B1_35 - B0_35)*(J_P**2)
    frec_R35 = nu0_35 + (B1_35 + B0_35)*(J_R + 1) + (B1_35 - B0_35)*((J_R + 1)**2)
    
    frec_P37 = nu0_37 - (B1_37 + B0_37)*J_P + (B1_37 - B0_37)*(J_P**2)
    frec_R37 = nu0_37 + (B1_37 + B0_37)*(J_R + 1) + (B1_37 - B0_37)*((J_R + 1)**2)
    
    fig_iso = go.Figure()
    
    if mode_iso == "Individual":
        iso_select = st.selectbox("Seleccionar Isótopo:", ["H³⁵Cl (Azul)", "H³⁷Cl (Rojo)"])
        if "35" in iso_select:
            for f in frec_P35: fig_iso.add_trace(go.Scatter(x=[f, f], y=[0, 1], mode='lines+markers', line=dict(color='blue', dash='dot'), marker=dict(color='blue')))
            for f in frec_R35: fig_iso.add_trace(go.Scatter(x=[f, f], y=[0, 1], mode='lines+markers', line=dict(color='blue'), marker=dict(color='blue')))
        else:
            for f in frec_P37: fig_iso.add_trace(go.Scatter(x=[f, f], y=[0, 1], mode='lines+markers', line=dict(color='red', dash='dot'), marker=dict(color='red')))
            for f in frec_R37: fig_iso.add_trace(go.Scatter(x=[f, f], y=[0, 1], mode='lines+markers', line=dict(color='red'), marker=dict(color='red')))
    else:
        # Superposición
        for f in frec_P35: fig_iso.add_trace(go.Scatter(x=[f, f], y=[0, 1.0], mode='lines+markers', line=dict(color='blue', dash='dot'), marker=dict(color='blue'), showlegend=False))
        for f in frec_R35: fig_iso.add_trace(go.Scatter(x=[f, f], y=[0, 1.0], mode='lines+markers', line=dict(color='blue'), marker=dict(color='blue'), showlegend=False))
        
        for f in frec_P37: fig_iso.add_trace(go.Scatter(x=[f, f], y=[0, 0.7], mode='lines+markers', line=dict(color='red', dash='dot'), marker=dict(color='red'), showlegend=False))
        for f in frec_R37: fig_iso.add_trace(go.Scatter(x=[f, f], y=[0, 0.7], mode='lines+markers', line=dict(color='red'), marker=dict(color='red'), showlegend=False))

    fig_iso.update_layout(title="Comparación del Espectro por Efecto Isotópico", xaxis_title="Número de onda (cm⁻¹)", yaxis_title="Intensidad Relativa", template="plotly_white", height=450)
    st.plotly_chart(fig_iso, use_container_width=True)

# -----------------------------------------------------------------------------
# MÓDULO 6: AUTOEVALUACIÓN
# -----------------------------------------------------------------------------
with tabs[5]:
    st.header("📝 Módulo 6: Cuestionario de Autoevaluación")
    
    q1 = st.radio("1. ¿Qué tipo de movimiento molecular estudia la espectroscopía ROTACIONAL?", ["Vibración de los enlaces", "Rotación de la molécula como un todo", "Movimiento de los electrones", "Traslación de la molécula"])
    q2 = st.radio("2. En el espectro rotacional del CO, las líneas están:", ["Todas a la misma frecuencia", "Igualmente espaciadas", "Más juntas a altas frecuencias", "Más separadas a altas frecuencias"])
    q3 = st.radio("3. La RAMA P en el espectro IR del HCl corresponde a:", ["ΔJ = +1 (aumenta la rotación)", "ΔJ = -1 (disminuye la rotación)", "ΔJ = 0 (no cambia la rotación)", "Transiciones electrónicas"])
    
    if st.button("Calcular Calificación"):
        score = 0
        if q1 == "Rotación de la molécula como un todo": score += 33.3
        if q2 == "Igualmente espaciadas": score += 33.3
        if q3 == "ΔJ = -1 (disminuye la rotación)": score += 33.4
        
        if score >= 70:
            st.success(f"🎉 ¡Excelente resultado! Calificación: {score:.1f} / 100")
        else:
            st.warning(f"✍️ Calificación: {score:.1f} / 100. Revisa los módulos teóricos e inténtalo nuevamente.")