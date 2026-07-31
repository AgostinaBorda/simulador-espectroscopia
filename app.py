import streamlit as st
import math
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA WEB Y CONSTANTES
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulador de Espectroscopía Vibro-Rotacional",
    page_icon="🔬",
    layout="wide"
)

hc_k = 1.438777  # Constante h*c/k en cm*K

# Base de datos espectroscópica
PARAMETROS_UAM = {
    "DF":  {"we": 3000.25, "wexe": 47.33,  "weye": 0.0, "Be": 11.007, "alpha": 0.301, "nombre": "Fluoruro de Deuterio (DF)"},
    "CO":  {"we": 2169.81, "wexe": 13.288, "weye": 0.0, "Be": 1.931,  "alpha": 0.0175, "nombre": "Monóxido de Carbono (CO)"},
    "LiH": {"we": 1405.65, "wexe": 23.20,  "weye": 0.0, "Be": 7.513,  "alpha": 0.213, "nombre": "Hidruro de Litio (LiH)"},
    "HCl": {"we": 2990.95, "wexe": 52.819, "weye": 0.0, "Be": 10.593, "alpha": 0.307, "nombre": "Cloruro de Hidrógeno (HCl)"},
    "HF":  {"we": 4138.32, "wexe": 89.88,  "weye": 0.0, "Be": 20.956, "alpha": 0.798, "nombre": "Fluoruro de Hidrógeno (HF)"},
    "NO":  {"we": 1904.20, "wexe": 14.10,  "weye": 0.0, "Be": 1.705,  "alpha": 0.017, "nombre": "Monóxido de Nitrógeno (NO)"},
    "H2":  {"we": 4401.21, "wexe": 121.33, "weye": 0.0, "Be": 60.853, "alpha": 3.062, "nombre": "Hidrógeno Molecular (H₂)"},
    "N2":  {"we": 2358.57, "wexe": 14.324, "weye": 0.0, "Be": 1.998,  "alpha": 0.0173, "nombre": "Nitrógeno Molecular (N₂)"},
    "O2":  {"we": 1580.19, "wexe": 11.98,  "weye": 0.0, "Be": 1.438,  "alpha": 0.0158, "nombre": "Oxígeno Molecular (O₂)"},
    "I2":  {"we": 214.50,  "wexe": 0.61,   "weye": 0.0, "Be": 0.0373, "alpha": 0.00011, "nombre": "Yodo Molecular (I₂)"},
    "D2":  {"we": 3115.50, "wexe": 61.80,  "weye": 0.0, "Be": 30.443, "alpha": 1.078, "nombre": "Deuterio Molecular (D₂)"},
    "OH":  {"we": 3737.76, "wexe": 84.88,  "weye": 0.0, "Be": 18.910, "alpha": 0.724, "nombre": "Radical Hidroxilo (OH)"},
    "ICl": {"we": 384.20,  "wexe": 1.50,   "weye": 0.0, "Be": 0.114,  "alpha": 0.0005, "nombre": "Monocloruro de Yodo (ICl)"}
}

# --- FUNCIONES MATEMÁTICAS NATIVAS ---
def obtener_energia_vib(v, p):
    return p["we"]*(v + 0.5) - p["wexe"]*((v + 0.5)**2) + p["weye"]*((v + 0.5)**3)

def obtener_B_v(v, p):
    return p["Be"] - p["alpha"]*(v + 0.5)

def generar_rango(inicio, fin, pasos):
    paso = (fin - inicio) / (pasos - 1)
    return [inicio + i * paso for i in range(pasos)]

# -----------------------------------------------------------------------------
# 2. ENCABEZADO Y PESTAÑAS
# -----------------------------------------------------------------------------
st.title("🔬 Laboratorio Virtual de Espectroscopía Vibro-Rotacional")
st.markdown("Simulador didáctico de espectros de absorción infrarroja molecular.")

tab_sim, tab_quiz, tab_teoria = st.tabs(["📈 Simulador Interactivo", "📝 Cuestionario Evaluativo", "📖 Guía Teórica"])

# -----------------------------------------------------------------------------
# PESTAÑA 1: SIMULADOR INTERACTIVO
# -----------------------------------------------------------------------------
with tab_sim:
    col_panel, col_grafico = st.columns([1, 2.8])
    
    with col_panel:
        st.subheader("⚙️ Parámetros de Control")
        mol_key = st.selectbox(
            "Seleccionar Molécula:", 
            options=list(PARAMETROS_UAM.keys()),
            format_func=lambda x: f"{x} - {PARAMETROS_UAM[x]['nombre']}"
        )
        
        col_v0, col_v1 = st.columns(2)
        with col_v0:
            v0 = st.number_input("Nivel v''", min_value=0, max_value=20, value=0, step=1)
        with col_v1:
            v1 = st.number_input("---> Nivel v'", min_value=0, max_value=20, value=1, step=1)
            
        T = st.slider("Temperatura (K):", min_value=10.0, max_value=1000.0, value=298.0, step=5.0)
        gamma = st.slider("Ancho mitad de altura (γ):", min_value=0.01, max_value=5.0, value=1.0, step=0.05)
        
        p = PARAMETROS_UAM[mol_key]
        st.info(f"**Constantes de {mol_key}:**\n* $\omega_e = {p['we']}\text{{ cm}}^{{-1}}$\n* $B_e = {p['Be']}\text{{ cm}}^{{-1}}$")

    with col_grafico:
        # Lógica matemática
        B0 = obtener_B_v(v0, p)
        B1 = obtener_B_v(v1, p)
        nu0 = abs(obtener_energia_vib(v1, p) - obtener_energia_vib(v0, p))

        J_max = 40
        lineas_frec, lineas_int = [], []

        for J in range(1, J_max):
            frec = nu0 - (B1 + B0)*J + (B1 - B0)*(J**2)
            pob = (2*J + 1) * math.exp(-B0 * J * (J + 1) * hc_k / max(T, 1.0))
            if pob > 1e-5:
                lineas_frec.append(frec)
                lineas_int.append(pob)

        for J in range(0, J_max):
            frec = nu0 + (B1 + B0)*(J + 1) + (B1 - B0)*((J + 1)**2)
            pob = (2*J + 1) * math.exp(-B0 * J * (J + 1) * hc_k / max(T, 1.0))
            if pob > 1e-5:
                lineas_frec.append(frec)
                lineas_int.append(pob)

        if len(lineas_frec) == 0:
            lineas_frec, lineas_int = [nu0], [1.0]

        min_frec, max_frec = min(lineas_frec), max(lineas_frec)
        ancho_vista = max_frec - min_frec
        xmin = min_frec - max(ancho_vista * 0.12, 15.0)
        xmax = max_frec + max(ancho_vista * 0.12, 15.0)

        nu_eje = generar_rango(xmin, xmax, 3000)
        espectro = [0.0] * len(nu_eje)
        
        for frec, intens in zip(lineas_frec, lineas_int):
            for i, nu in enumerate(nu_eje):
                espectro[i] += intens * (gamma**2 / ((nu - frec)**2 + gamma**2))

        max_y = max(espectro) if espectro else 1.0

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=nu_eje, y=espectro,
            mode='lines',
            line=dict(color='purple', width=2),
            name='Espectro'
        ))

        fig.update_layout(
            title=f"Espectro de Rotación-Vibración para {mol_key} (v''={v0} → v'={v1})",
            xaxis_title="Número de onda (cm⁻¹)",
            yaxis_title="Intensidad",
            xaxis=dict(range=[xmin, xmax]),
            yaxis=dict(range=[0, max_y * 1.1 if max_y > 0 else 1]),
            template="plotly_white",
            height=500
        )

        # Muestra el gráfico y configura el botón de descarga del propio gráfico a PNG en alta calidad
        st.plotly_chart(
            fig, 
            use_container_width=True,
            config={
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'Espectro_{mol_key}_v{v0}_v{v1}',
                    'height': 600,
                    'width': 1000,
                    'scale': 3
                }
            }
        )

# -----------------------------------------------------------------------------
# PESTAÑA 2: CUESTIONARIO EVALUATIVO
# -----------------------------------------------------------------------------
with tab_quiz:
    st.header("📝 Cuestionario de Autoevaluación")
    st.write("Responde las siguientes preguntas conceptuales y presiona el botón para obtener tu nota.")

    p1 = st.radio(
        "1. ¿Qué representa la Rama P en el espectro de rotación-vibración?",
        ["Transiciones con ΔJ = +1", "Transiciones con ΔJ = -1", "Transiciones con ΔJ = 0"]
    )

    p2 = st.radio(
        "2. ¿Qué ocurre con la distribución de alturas de los picos al AUMENTAR la temperatura?",
        ["Los picos con J alto se vuelven más intensos", "Todos los picos desaparecen", "Solo aumenta la intensidad del pico central"]
    )

    p3 = st.radio(
        "3. ¿Por qué el Origen de la Banda (ν₀) no presenta un pico central en moléculas diatómicas homonucleares?",
        ["Porque ΔJ = 0 está prohibido por la regla de selección", "Porque la temperatura es muy baja", "Porque la constante de fuerza es cero"]
    )

    if st.button("Calcular Calificación"):
        score = 0
        if p1 == "Transiciones con ΔJ = -1":
            score += 33.3
        if p2 == "Los picos con J alto se vuelven más intensos":
            score += 33.3
        if p3 == "Porque ΔJ = 0 está prohibido por la regla de selección":
            score += 33.4

        st.divider()
        if score >= 70:
            st.success(f"🎉 ¡Excelente trabajo! Tu calificación es: {score:.1f} / 100")
        else:
            st.warning(f"✍️ Tu calificación es: {score:.1f} / 100. Revisa la guía teórica e inténtalo nuevamente.")

# -----------------------------------------------------------------------------
# PESTAÑA 3: GUÍA TEÓRICA
# -----------------------------------------------------------------------------
with tab_teoria:
    st.header("📖 Fundamentos Teóricos")
    st.markdown("""
    La **espectroscopía rotacional-vibracional** estudia los cambios simultáneos en los estados de energía vibracional y rotacional de una molécula cuando absorbe radiación infrarroja.

    ### 1. Reglas de Selección
    * **Vibracional:** $\Delta v = \pm 1, \pm 2, \dots$
    * **Rotacional:** $\Delta J = \pm 1$
      * **Rama P ($\Delta J = -1$):** Aparece a menores frecuencias que el origen de banda ($\nu < \nu_0$).
      * **Rama R ($\Delta J = +1$):** Aparece a mayores frecuencias que el origen de banda ($\nu > \nu_0$).

    ### 2. Cabeza de Banda (*Band Head*)
    Como la constante rotacional del estado excitado ($B_1$) es ligeramente menor que la del estado fundamental ($B_0$), los picos de la **Rama R** comienzan a amontonarse hasta colapsar en una frecuencia máxima.
    """)