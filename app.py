import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Laboratorio de Espectroscopía",
    layout="wide"
)

# Constantes físicas universales
h = 6.626e-34      # J·s (Planck)
c = 2.998e10       # cm/s (Velocidad de la luz)
k = 1.381e-23      # J/K (Boltzmann)
hc_k = 1.438777    # cm·K

# Base de datos completa de moléculas (Replicación UAM)
# Formato: { "Nombre": (B_e, alpha_e, omega_e, omega_x_e, mu_amu) }
MOLECULAS_UAM = {
    "DF":  (15.910, 0.570, 2998.25, 45.71),
    "CO":  (1.931,  0.018, 2169.81, 13.29),
    "LiH": (7.513,  0.213, 1405.65, 23.20),
    "HCl": (10.593, 0.307, 2990.95, 52.82),
    "HF":  (20.956, 0.796, 4138.32, 89.88),
    "NO":  (1.705,  0.017, 1904.20, 14.10),
    "HH":  (60.853, 3.062, 4401.21, 121.34),
    "NN":  (1.998,  0.017, 2358.57, 14.32),
    "OO":  (1.438,  0.016, 1580.19, 11.98),
    "II":  (0.037,  0.0001, 214.50,  0.61),
    "DD":  (30.443, 1.078, 3115.50, 61.80),
    "OH":  (18.911, 0.724, 3737.76, 84.88),
    "ICl": (0.114,  0.0005, 384.29,  1.50)
}

# Estilo CSS para impresión limpia
st.markdown("""
<style>
@media print {
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"], .stTabs [role="tablist"] {
        display: none !important;
    }
    .report-container {
        font-family: Arial, sans-serif;
        padding: 20px;
        color: #000;
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
        st.latex(rf"h = {h:.3e} \text{{ J}}\cdot\text{{s}} \quad (\text{{Constante de Planck}})")
        st.latex(rf"c = {c:.3e} \text{{ cm/s}} \quad (\text{{Velocidad de la luz}})")
        st.latex(rf"k = {k:.3e} \text{{ J/K}} \quad (\text{{Constante de Boltzmann}})")

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
    
    # Constantes espectroscópicas
    B0_35, B1_35, nu0_35 = 10.44, 10.136, 2885.9
    B0_37, B1_37, nu0_37 = 10.42, 10.120, 2883.8
    
    J_max = 12
    J_P, J_R = np.arange(1, J_max), np.arange(0, J_max - 1)
    
    frec_P35 = nu0_35 - (B1_35 + B0_35)*J_P + (B1_35 - B0_35)*(J_P**2)
    frec_R35 = nu0_35 + (B1_35 + B0_35)*(J_R + 1) + (B1_35 - B0_35)*((J_R + 1)**2)
    frec_P37 = nu0_37 - (B0_37 + B1_37)*J_P + (B1_37 - B0_37)*(J_P**2)
    frec_R37 = nu0_37 + (B0_37 + B1_37)*(J_R + 1) + (B1_37 - B0_37)*((J_R + 1)**2)
    
    int_P = np.array([1.0 / (J + 1) for J in J_P])
    int_R = np.array([1.0 / (J + 2) for J in J_R])
    max_i = max(max(int_P), max(int_R))
    int_P, int_R = int_P / max_i, int_R / max_i

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
# MÓDULO 3: SIMULADOR COMPLETO (REPLICACIÓN EXACTA UAM)
# -----------------------------------------------------------------------------
with tabs[2]:
    st.header("Simulador de Espectros de Rotación-Vibración")
    
    col_ctrl, col_plot = st.columns([1, 2.3])
    
    with col_ctrl:
        st.subheader("Parámetros de Simulación")
        
        molecula_sel = st.selectbox("Molécula:", list(MOLECULAS_UAM.keys()), index=1) # CO por defecto
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            v_lower = st.slider("v''", min_value=0, max_value=2, value=1)
        with col_v2:
            v_upper = st.slider("v'", min_value=1, max_value=3, value=2)
            
        T_val = st.slider("Temperatura", min_value=10.0, max_value=500.0, value=150.0, step=1.0)
        ancho_mitad = st.slider("Ancho mitad", min_value=0.1, max_value=3.0, value=0.4, step=0.1)
        
        # Constantes espectroscópicas
        B_e, alpha_e, omega_e, omega_x_e = MOLECULAS_UAM[molecula_sel]
        
        B0 = B_e - alpha_e * (v_lower + 0.5)
        B1 = B_e - alpha_e * (v_upper + 0.5)
        
        G_v_lower = omega_e * (v_lower + 0.5) - omega_x_e * ((v_lower + 0.5)**2)
        G_v_upper = omega_e * (v_upper + 0.5) - omega_x_e * ((v_upper + 0.5)**2)
        nu0 = G_v_upper - G_v_lower

        st.info(f"""
        💡 **Parámetros físicos para {molecula_sel}:**
        * B₀ = {B0:.3f} cm⁻¹
        * B₁ = {B1:.3f} cm⁻¹
        * ν₀ = {nu0:.1f} cm⁻¹
        """)

    with col_plot:
        J_max = 30
        J_P = np.arange(1, J_max)
        frec_P = nu0 - (B1 + B0)*J_P + (B1 - B0)*(J_P**2)
        
        J_R = np.arange(0, J_max - 1)
        frec_R = nu0 + (B1 + B0)*(J_R + 1) + (B1 - B0)*((J_R + 1)**2)
        
        # Factor de Boltzmann e intensidades
        int_P = [(2*J + 1) * np.exp(-B0 * J * (J + 1) * hc_k / max(T_val, 1.0)) for J in J_P]
        int_R = [(2*J + 1) * np.exp(-B0 * J * (J + 1) * hc_k / max(T_val, 1.0)) for J in J_R]
        
        # Malla de alta resolución centrada ajustada a la banda (rango +- 100 cm-1)
        x_min_crop = max(0, nu0 - 100)
        x_max_crop = nu0 + 100
        x_grid = np.linspace(x_min_crop, x_max_crop, 2000)
        y_grid = np.zeros_like(x_grid)
        
        # Suma de perfiles gaussianos
        for f, iv in zip(frec_P, int_P):
            y_grid += iv * np.exp(-((x_grid - f)**2) / (2 * (ancho_mitad**2)))
        for f, iv in zip(frec_R, int_R):
            y_grid += iv * np.exp(-((x_grid - f)**2) / (2 * (ancho_mitad**2)))

        # Escala de intensidad idéntica a la UAM (máximo relativo en ~42)
        if max(y_grid) > 0:
            y_grid = (y_grid / max(y_grid)) * 41.5

        fig_uam = go.Figure()
        fig_uam.add_trace(go.Scatter(
            x=x_grid, 
            y=y_grid, 
            mode='lines', 
            line=dict(color='purple', width=1.8), 
            name="Espectro"
        ))
        
        fig_uam.update_layout(
            title="Simulador de Espectros de Rotación Vibración",
            xaxis_title="Numero de onda (cm-1)",
            yaxis_title="Intensidad",
            template="plotly_white",
            height=450,
            xaxis=dict(range=[x_min_crop, x_max_crop], showgrid=True),
            yaxis=dict(range=[0, 45], showgrid=True)
        )
        st.plotly_chart(fig_uam, use_container_width=True)

        st.components.v1.html(
            """
            <button onclick="window.print()" style="
                background-color: #2b5797;
                border: none;
                color: white;
                padding: 8px 16px;
                text-align: center;
                font-size: 14px;
                border-radius: 4px;
                cursor: pointer;
            ">
                Espectro en pdf
            </button>
            """,
            height=45
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