import streamlit as st
import math
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA WEB Y CONSTANTES
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Laboratorio de Espectroscopía",
    layout="wide"
)

hc_k = 1.438777  # Constante h*c/k en cm*K

# Base de datos espectroscópica exacta de la UAM
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

# --- FUNCIONES MATEMÁTICAS ---
def obtener_energia_vib(v, p):
    return p["we"]*(v + 0.5) - p["wexe"]*((v + 0.5)**2) + p["weye"]*((v + 0.5)**3)

def obtener_B_v(v, p):
    return p["Be"] - p["alpha"]*(v + 0.5)

def generar_rango(inicio, fin, pasos):
    paso = (fin - inicio) / (pasos - 1)
    return [inicio + i * paso for i in range(pasos)]

# Estilo CSS para vista de impresión limpia del informe
st.markdown("""
<style>
@media print {
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"], .stTabs [role="tablist"] {
        display: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. ENCABEZADO PRINCIPAL
# -----------------------------------------------------------------------------
st.title("LABORATORIO DE ESPECTROSCOPÍA")
st.markdown("""
Bienvenido/a al mundo de las moléculas y la luz.  
En este laboratorio interactivo aprenderás cómo las moléculas rotan y vibran cuando absorben luz.
""")

# Navegación por pestañas
tabs = st.tabs([
    "Módulo 1: Introducción",
    "Módulo 2: Efecto Isotópico",
    "Módulo 3: Simulador Completo",
    "Módulo 4: Evaluación y Entregable"
])

# -----------------------------------------------------------------------------
# MÓDULO 1: INTRODUCCIÓN
# -----------------------------------------------------------------------------
with tabs[0]:
    st.header("Introducción y Constantes Fundamentales")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Configuración Inicial")
        st.markdown("""
        En esta guía interactiva exploraremos la interacción entre la radiación electromagnética y la materia. 
        No se requiere experiencia previa en programación.
        """)

    with col2:
        st.subheader("Constantes Fundamentales")
        st.write("Valores universales de la naturaleza:")
        st.latex(r"h = 6.626 \times 10^{-34} \text{ J}\cdot\text{s} \quad (\text{Constante de Planck})")
        st.latex(r"c = 2.998 \times 10^{10} \text{ cm/s} \quad (\text{Velocidad de la luz})")
        st.latex(r"k = 1.381 \times 10^{-23} \text{ J/K} \quad (\text{Constante de Boltzmann})")

    st.info("""
    💡 **¿Sabías que?** Estas constantes aparecen en las ecuaciones porque la espectroscopía es cuantitativa y cuántica. 
    Los intercambios de energía ocurren en paquetes discretos llamados cuantos.
    """)

# -----------------------------------------------------------------------------
# MÓDULO 2: EFECTO ISOTÓPICO
# -----------------------------------------------------------------------------
with tabs[1]:
    st.header("Comparación Isotópica (H³⁵Cl vs H³⁷Cl)")
    
    modo_iso = st.radio("Modo de visualización:", ["Individual", "Superposición Directa"], horizontal=True)
    
    B0_35, B1_35, nu0_35 = 10.44, 10.136, 2885.9
    B0_37, B1_37, nu0_37 = 10.42, 10.120, 2883.8
    
    J_max = 12
    J_P, J_R = list(range(1, J_max)), list(range(0, J_max - 1))
    
    frec_P35 = [nu0_35 - (B1_35 + B0_35)*J + (B1_35 - B0_35)*(J**2) for J in J_P]
    frec_R35 = [nu0_35 + (B1_35 + B0_35)*(J + 1) + (B1_35 - B0_35)*((J + 1)**2) for J in J_R]
    frec_P37 = [nu0_37 - (B0_37 + B1_37)*J + (B1_37 - B0_37)*(J**2) for J in J_P]
    frec_R37 = [nu0_37 + (B0_37 + B1_37)*(J + 1) + (B1_37 - B0_37)*((J + 1)**2) for J in J_R]
    
    int_P = [1.0 / (J + 1) for J in J_P]
    int_R = [1.0 / (J + 2) for J in J_R]
    max_i = max(max(int_P), max(int_R))
    int_P = [v / max_i for v in int_P]
    int_R = [v / max_i for v in int_R]

    def agregar_stems(fig, x_vals, y_vals, color, dash='solid', symbol='circle', name=""):
        for x, y in zip(x_vals, y_vals):
            fig.add_trace(go.Scatter(x=[x, x], y=[0, y], mode='lines', line=dict(color=color, width=2, dash=dash), showlegend=False))
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='markers', marker=dict(color=color, size=7, symbol=symbol), name=name))

    fig2 = go.Figure()

    if modo_iso == "Individual":
        iso_select = st.selectbox("Seleccionar Isótopo:", ["H³⁵Cl", "H³⁷Cl"])
        if iso_select == "H³⁵Cl":
            agregar_stems(fig2, frec_P35, int_P, 'blue', dash='dot', symbol='circle', name="H³⁵Cl - Rama P")
            agregar_stems(fig2, frec_R35, int_R, 'blue', dash='solid', symbol='square', name="H³⁵Cl - Rama R")
        else:
            agregar_stems(fig2, frec_P37, int_P, 'red', dash='dot', symbol='circle', name="H³⁷Cl - Rama P")
            agregar_stems(fig2, frec_R37, int_R, 'red', dash='solid', symbol='square', name="H³⁷Cl - Rama R")
        fig2.update_layout(title=f"Espectro de {iso_select}", xaxis_title="Número de onda (cm⁻¹)", yaxis_title="Intensidad relativa")
    else:
        agregar_stems(fig2, frec_P35, [1.0]*len(frec_P35), 'blue', dash='dot', symbol='circle', name="H³⁵Cl - Rama P")
        agregar_stems(fig2, frec_R35, [1.0]*len(frec_R35), 'blue', dash='solid', symbol='square', name="H³⁵Cl - Rama R")
        agregar_stems(fig2, frec_P37, [0.7]*len(frec_P37), 'red', dash='dot', symbol='circle', name="H³⁷Cl - Rama P")
        agregar_stems(fig2, frec_R37, [0.7]*len(frec_R37), 'red', dash='solid', symbol='square', name="H³⁷Cl - Rama R")
        fig2.update_layout(title="COMPARACIÓN DIRECTA: H³⁵Cl (azul) vs H³⁷Cl (rojo)", xaxis_title="Número de onda (cm⁻¹)", yaxis_title="Intensidad (desplazada)")

    fig2.update_layout(xaxis=dict(range=[2800, 2960]), template="plotly_white", height=450)
    st.plotly_chart(fig2, use_container_width=True)

    st.info("""
    💡 **Dato teórico - Efecto Isotópico:**
    * **H³⁷Cl tiene MASAS más pesadas**, por lo que su espectro se desplaza ligeramente a **menores frecuencias**.
    * La forma general del espectro es **IDÉNTICA**.
    * La constante de fuerza del enlace **NO cambia** con el isótopo.
    """)

# -----------------------------------------------------------------------------
# MÓDULO 3: SIMULADOR COMPLETO (SISTEMA MATEMÁTICO UAM)
# -----------------------------------------------------------------------------
with tabs[2]:
    st.header("Simulador de Espectros de Rotación-Vibración")
    
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
        B0 = obtener_B_v(v0, p)
        B1 = obtener_B_v(v1, p)
        nu0 = abs(obtener_energia_vib(v1, p) - obtener_energia_vib(v0, p))
        
        st.info(f"""
        💡 **Parámetros de {mol_key}:**
        * $B_0 = {B0:.3f}\\text{{ cm}}^{{-1}}$
        * $B_1 = {B1:.3f}\\text{{ cm}}^{{-1}}$
        * $\\nu_0 = {nu0:.1f}\\text{{ cm}}^{{-1}}$
        """)

    with col_grafico:
        J_max = 40
        lineas_frec, lineas_int = [], []

        # Rama P (ΔJ = -1)
        for J in range(1, J_max):
            frec = nu0 - (B1 + B0)*J + (B1 - B0)*(J**2)
            pob = (2*J + 1) * math.exp(-B0 * J * (J + 1) * hc_k / max(T, 1.0))
            if pob > 1e-5:
                lineas_frec.append(frec)
                lineas_int.append(pob)

        # Rama R (ΔJ = +1)
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
            height=480
        )

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
# MÓDULO 4: EVALUACIÓN Y ENTREGABLE
# -----------------------------------------------------------------------------
with tabs[3]:
    st.header("Evaluación y Entregable Final")
    
    st.markdown("### Datos del Estudiante")
    col_est1, col_est2 = st.columns(2)
    with col_est1:
        nombre_alumno = st.text_input("Nombre y Apellido:", placeholder="Ingrese su nombre completo")
    with col_est2:
        legajo_alumno = st.text_input("Legajo / DNI:", placeholder="Ingrese su documento o legajo")

    st.divider()

    col_eval1, col_eval2 = st.columns(2)
    
    with col_eval1:
        st.subheader("Autoevaluación Conceptual")
        q1 = st.radio("1. ¿Qué movimiento estudia la espectroscopía ROTACIONAL?", ["a) Vibración de enlaces", "b) Rotación de la molécula completa", "c) Movimiento de electrones", "d) Traslación"])
        q2 = st.radio("2. En el espectro rotacional del CO, las líneas están:", ["a) A la misma frecuencia", "b) Igualmente espaciadas", "c) Más juntas a alta frecuencia", "d) Más separadas a alta frecuencia"])
        q3 = st.radio("3. La RAMA P en el espectro IR del HCl corresponde a:", ["a) ΔJ = +1", "b) ΔJ = -1", "c) ΔJ = 0", "d) Transición electrónica"])
        q4 = st.radio("4. Si aumentamos la temperatura:", ["a) Se desplazan a menor frecuencia", "b) Aparecen líneas con J más altos", "c) Desaparece la rama R", "d) No cambia"])
        q5 = st.radio("5. El H³⁷Cl tiene frecuencias menores que H³⁵Cl porque:", ["a) Menor constante de fuerza", "b) Mayor masa reducida", "c) Enlace más largo", "d) Es radiactivo"])
        
        score = 0
        if "b)" in q1: score += 20
        if "b)" in q2: score += 20
        if "b)" in q3: score += 20
        if "b)" in q4: score += 20
        if "b)" in q5: score += 20
        
        if st.button("Verificar Calificación"):
            st.success(f"Calificación: {score} / 100")

    with col_eval2:
        st.subheader("Tabla de Resultados Experimentales")
        st.write("Ingrese los valores obtenidos en sus experiencias simuladas:")

        v_co = st.text_input("CO — Longitud de enlace r (Å):", placeholder="Ej: 1.128")
        v_hcl_b0 = st.text_input("HCl — Constante B₀ (cm⁻¹):", placeholder="Ej: 10.44")
        v_hcl_b1 = st.text_input("HCl — Constante B₁ (cm⁻¹):", placeholder="Ej: 10.14")
        v_hcl_nu0 = st.text_input("HCl — Origen de banda ν₀ (cm⁻¹):", placeholder="Ej: 2886")
        v_iso_b0 = st.text_input("H³⁷Cl — Constante B₀ (cm⁻¹):", placeholder="Ej: 10.42")

        if st.button("Verificar Tabla"):
            aciertos = 0
            try:
                if v_co and abs(float(v_co.replace(',', '.')) - 1.128) < 0.05: aciertos += 1
                if v_hcl_b0 and abs(float(v_hcl_b0.replace(',', '.')) - 10.44) < 0.1: aciertos += 1
                if v_hcl_b1 and abs(float(v_hcl_b1.replace(',', '.')) - 10.14) < 0.1: aciertos += 1
                if v_hcl_nu0 and abs(float(v_hcl_nu0.replace(',', '.')) - 2886) < 10: aciertos += 1
                if v_iso_b0 and abs(float(v_iso_b0.replace(',', '.')) - 10.42) < 0.1: aciertos += 1

                if aciertos == 5:
                    st.success("Todos los parámetros coinciden correctamente.")
                else:
                    st.warning(f"Coinciden {aciertos} de 5 valores. Verifique sus mediciones.")
            except ValueError:
                st.error("Ingrese valores numéricos válidos.")

    st.divider()

    st.subheader("Pregunta Final")
    respuesta_final = st.text_area(
        "¿Por qué el CO tiene espectro rotacional pero el N₂ no? (Justifique considerando el momento dipolar):", 
        placeholder="Escriba su respuesta aquí..."
    )

    st.divider()

    st.subheader("Generación de Informe para el Docente")
    st.write("Haga clic en el botón para imprimir o guardar como PDF el informe de la evaluación con sus datos y resultados cargados.")

    st.components.v1.html(
        """
        <button onclick="window.parent.print()" style="
            background-color: #2e7d32;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            font-size: 15px;
            font-weight: bold;
            border-radius: 4px;
            cursor: pointer;
        ">
            Imprimir Informe de Resultados en PDF
        </button>
        """,
        height=50
    )