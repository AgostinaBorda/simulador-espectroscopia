import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Laboratorio Interactivo de Espectroscopía",
    page_icon="🔬",
    layout="wide"
)

# Constantes físicas
h = 6.626e-34      # J·s (Planck)
c = 2.998e10       # cm/s (Velocidad de la luz)
k = 1.381e-23      # J/K (Boltzmann)
hc_k = 1.438777    # cm·K

# -----------------------------------------------------------------------------
# 2. ENCABEZADO PRINCIPAL
# -----------------------------------------------------------------------------
st.title("🎓 LABORATORIO DE ESPECTROSCOPÍA PARA PRINCIPIANTES")
st.markdown("""
**Bienvenido/a al mundo de las moléculas y la luz.**  
En este laboratorio interactivo aprenderás cómo las moléculas "bailan" (rotan) y "vibran" cuando absorben luz.
""")

# Navegación por Módulos
tabs = st.tabs([
    "🚀 Módulo 1: Primeros Pasos",
    "🌈 Módulo 2: ¿Qué es un Espectro?",
    "🔄 Módulo 3: Rotación (CO)",
    "🌡️ Módulo 4: Vibración-Rotación (HCl)",
    "⚖️ Módulo 5: Efecto Isotópico",
    "📝 Módulo 6: Evaluación y Entregable"
])

# -----------------------------------------------------------------------------
# MÓDULO 1: PRIMEROS PASOS
# -----------------------------------------------------------------------------
with tabs[0]:
    st.header("🚀 Módulo 1: Configuración Inicial y Constantes")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📌 Celda 1: Bienvenida al Entorno")
        st.success("✅ Entorno interactivo y librerías numéricas cargadas correctamente.")
        st.markdown("""
        En esta guía interactiva exploraremos la interacción entre la radiación electromagnética y la materia. 
        No se requiere experiencia en programación.
        """)

    with col2:
        st.subheader("📏 Celda 2: Las Constantes de la Naturaleza")
        st.write("Estos números no cambian **NUNCA** en todo el universo:")
        st.latex(rf"h = {h:.3e} \text{{ J}}\cdot\text{{s}} \quad (\text{{Planck}})")
        st.latex(rf"c = {c:.3e} \text{{ cm/s}} \quad (\text{{Velocidad de la luz}})")
        st.latex(rf"k = {k:.3e} \text{{ J/K}} \quad (\text{{Boltzmann}})")

    st.info("""
    💡 **¿Sabías que?** Estas constantes aparecen en las ecuaciones porque la espectroscopía es **CUÁNTICA**, no clásica. 
    Los intercambios de energía ocurren en paquetes discretos llamados *cuantos*.
    """)

# -----------------------------------------------------------------------------
# MÓDULO 2: ¿QUÉ ES UN ESPECTRO?
# -----------------------------------------------------------------------------
with tabs[1]:
    st.header("🌈 Módulo 2: Visualizando Frecuencias y Transiciones")
    
    col_ctrl2, col_plot2 = st.columns([1, 2.2])
    
    with col_ctrl2:
        st.subheader("⚙️ Configuración del Espectro")
        modo_espectro = st.radio("Seleccionar Celda:", ["Celda 3: Un solo pico", "Celda 4: Múltiples líneas (J=0,1,2...)"])
        
        st.markdown("""
        📝 **ANOTA EN TU CUADERNO:**
        1. El eje X es la **FRECUENCIA** (o número de onda) de la luz.
        2. El eje Y es la **INTENSIDAD** (cuánta luz absorbe).
        3. Cada **PICO** significa que la molécula absorbió luz al cambiar de estado.
        """)

    with col_plot2:
        fig2 = go.Figure()
        
        if modo_espectro == "Celda 3: Un solo pico":
            frec = np.linspace(0, 10, 200)
            intens = np.exp(-((frec - 5)**2))
            fig2.add_trace(go.Scatter(x=frec, y=intens, mode='lines', fill='tozeroy', line=dict(color='purple', width=3), name="Transición única"))
            fig2.update_layout(title="Ejemplo de ESPECTRO: Un solo pico = una transición", xaxis_title="Frecuencia", yaxis_title="Intensidad")
        else:
            frec = np.linspace(0, 20, 300)
            picos = [3, 6, 9, 12, 15]
            intens = sum(0.8**(i) * np.exp(-((frec - x)**2)) for i, x in enumerate(picos))
            fig2.add_trace(go.Scatter(x=frec, y=intens, mode='lines', fill='tozeroy', line=dict(color='purple', width=2), name="Espectro Múltiple"))
            for i, x in enumerate(picos):
                fig2.add_vline(x=x, line_dash="dash", line_color="red", opacity=0.5)
                fig2.add_annotation(x=x, y=0.8**(i) + 0.08, text=f"J={i}", showarrow=False)
            fig2.update_layout(title="Espectro con MÚLTIPLES transiciones", xaxis_title="Frecuencia", yaxis_title="Intensidad")

        fig2.update_layout(template="plotly_white", height=450)
        st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------------------------------------------
# MÓDULO 3: ESPECTROSCOPÍA ROTACIONAL (CO)
# -----------------------------------------------------------------------------
with tabs[2]:
    st.header("🔄 Módulo 3: Espectroscopía Rotacional (La que hace girar)")
    
    col_ctrl3, col_plot3 = st.columns([1, 2.2])
    
    with col_ctrl3:
        st.subheader("⚙️ Celda 5: Simulador de CO")
        r_CO = st.slider("Longitud de enlace (Å):", min_value=0.80, max_value=1.50, value=1.128, step=0.001)
        T_CO = st.slider("Temperatura (K):", min_value=10, max_value=500, value=298, step=10, key="t_co")
        
        # Cálculos físicos del CO
        masa_C = 12.01 * 1.66e-27
        masa_O = 16.00 * 1.66e-27
        mu_CO = (masa_C * masa_O) / (masa_C + masa_O)
        I_CO = mu_CO * (r_CO * 1e-10)**2
        B_CO_GHz = (h / (8 * (np.pi**2) * I_CO)) * 1e-9
        espaciado_CO = 2 * B_CO_GHz
        
        st.info(f"""
        📊 **RESULTADOS DE LA MOLÉCULA:**
        * **Constante rotacional B:** {B_CO_GHz:.3f} GHz
        * **Espaciado entre líneas (2B):** {espaciado_CO:.3f} GHz
        * **Longitud ajustada (r):** {r_CO:.3f} Å
        """)

    with col_plot3:
        J_vals = np.arange(0, 8)
        frec_rot = [2 * B_CO_GHz * (J + 1) for J in J_vals]
        int_rot = [(2*J + 1) * np.exp(-(B_CO_GHz * 1e9 * h * J * (J + 1)) / (k * max(T_CO, 1.0))) for J in J_vals]
        int_rot = np.array(int_rot) / max(int_rot) if max(int_rot) > 0 else int_rot
        
        fig3 = go.Figure()
        for f, iv in zip(frec_rot, int_rot):
            fig3.add_trace(go.Scatter(x=[f, f], y=[0, iv], mode='lines+markers', line=dict(color='purple', width=3), marker=dict(size=8, color='red'), showlegend=False))
            
        fig3.update_layout(
            title=f"Espectro ROTACIONAL del CO — Longitud = {r_CO:.3f} Å",
            xaxis_title="Frecuencia (GHz)",
            yaxis_title="Intensidad relativa",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📝 Celda 6: Preguntas Guiadas (Responde en tu cuaderno)")
    st.markdown("""
    1. **¿Qué pasa con las líneas cuando AUMENTAS la longitud de enlace?** ¿Se separan o se juntan? ¿Por qué crees?
    2. **¿Qué pasa con las líneas cuando DISMINUYES la temperatura?** ¿Alguna línea desaparece? ¿Cuál?
    3. **Para CO real, el espaciado es 115.3 GHz.** ¿Qué longitud de enlace obtienes en el simulador? *(Valor bibliográfico: 1.128 Å)*.
    4. **Si duplicaras la masa del carbono**, ¿el espaciado aumentaría o disminuiría?
    """)

# -----------------------------------------------------------------------------
# MÓDULO 4: ESPECTROSCOPÍA VIBRACIONAL-ROTACIONAL (HCl)
# -----------------------------------------------------------------------------
with tabs[3]:
    st.header("🧪 Módulo 4: Espectro Vibracional-Rotacional (HCl)")
    
    col_ctrl4, col_plot4 = st.columns([1, 2.3])
    
    with col_ctrl4:
        st.subheader("⚙️ Parámetros de Simulación")
        
        molecula = st.selectbox("Molécula:", ["HCl (Cloro-35)", "CO (Monóxido de Carbono)"])
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            v_lower = st.slider("v''", min_value=0, max_value=2, value=0)
        with col_v2:
            v_upper = st.slider("v'", min_value=1, max_value=3, value=1)
            
        T_hcl = st.slider("Temperatura (K):", min_value=10.0, max_value=500.0, value=298.0, step=10.0)
        ancho_mitad = st.slider("Ancho a la mitad (Gausiana):", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
        
        # Asignación de constantes físicas del documento del docente (Celda 7)
        if "HCl" in molecula:
            B0 = 10.44      # cm⁻¹ (Docente Celda 7)
            B1 = 10.136     # cm⁻¹ (Docente Celda 7)
            nu0 = 2885.9    # cm⁻¹ (Docente Celda 7)
        else:
            B0 = 1.931
            B1 = 1.913
            nu0 = 2143.2

        st.info(f"""
        📖 **Valores del docente para {molecula}:**
        * $B_0 = {B0}\\text{{ cm}}^{{-1}}$ (Estado fundamental $v''={v_lower}$)
        * $B_1 = {B1}\\text{{ cm}}^{{-1}}$ (Estado excitado $v'={v_upper}$)
        * $\\nu_0 = {nu0}\\text{{ cm}}^{{-1}}$ (Origen de la banda)
        """)

    with col_plot4:
        J_max = 15
        
        # Ramas P (ΔJ = -1) y R (ΔJ = +1)
        J_P = np.arange(1, J_max)
        frec_P = nu0 - (B1 + B0)*J_P + (B1 - B0)*(J_P**2)
        
        J_R = np.arange(0, J_max - 1)
        frec_R = nu0 + (B1 + B0)*(J_R + 1) + (B1 - B0)*((J_R + 1)**2)
        
        # Intensidades de Boltzmann
        int_P = [(2*J + 1) * np.exp(-B0 * J * (J + 1) * hc_k / max(T_hcl, 1.0)) for J in J_P]
        int_R = [(2*J + 1) * np.exp(-B0 * J * (J + 1) * hc_k / max(T_hcl, 1.0)) for J in J_R]
        
        # Generación de perfil continuo suavizado (Estilo UAM)
        x_grid = np.linspace(nu0 - 250, nu0 + 250, 1000)
        y_grid = np.zeros_like(x_grid)
        
        for f, iv in zip(frec_P, int_P):
            y_grid += iv * np.exp(-((x_grid - f)**2) / (2 * (ancho_mitad**2)))
        for f, iv in zip(frec_R, int_R):
            y_grid += iv * np.exp(-((x_grid - f)**2) / (2 * (ancho_mitad**2)))
            
        if max(y_grid) > 0:
            y_grid = (y_grid / max(y_grid)) * 4.0  # Escala similar a la UAM (0 a 4.0)

        fig_uam = go.Figure()
        fig_uam.add_trace(go.Scatter(
            x=x_grid, 
            y=y_grid, 
            mode='lines', 
            line=dict(color='purple', width=2), 
            fill='tozeroy',
            fillcolor='rgba(128, 0, 128, 0.05)',
            name="Espectro continuo"
        ))
        
        fig_uam.update_layout(
            title=f"Simulador de Espectros de Rotación-Vibración ({molecula})",
            xaxis_title="Número de onda (cm⁻¹)",
            yaxis_title="Intensidad",
            template="plotly_white",
            height=450,
            xaxis=dict(range=[nu0 - 250, nu0 + 250])
        )
        st.plotly_chart(fig_uam, use_container_width=True)

    # -------------------------------------------------------------------------
    # CELDA 8 DEL DOCENTE: APRENDIENDO A LEER EL ESPECTRO
    # -------------------------------------------------------------------------
    st.divider()
    st.subheader("🔍 Celda 8: Identificador de Líneas (Pista Práctica)")
    
    col_p, col_r = st.columns(2)
    with col_p:
        st.markdown("**RAMA P ($\Delta J = -1$)**")
        for J in range(1, 6):
            f_val = nu0 - (B1 + B0)*J + (B1 - B0)*(J**2)
            st.code(f"P({J}) → {f_val:.2f} cm⁻¹", language="text")

    with col_r:
        st.markdown("**RAMA R ($\Delta J = +1$)**")
        for J in range(0, 5):
            f_val = nu0 + (B1 + B0)*(J + 1) + (B1 - B0)*((J + 1)**2)
            st.code(f"R({J}) → {f_val:.2f} cm⁻¹", language="text")

    r0_val = nu0 + (B1 + B0)*(1) + (B1 - B0)*(1**2)
    p2_val = nu0 - (B1 + B0)*2 + (B1 - B0)*(2**2)
    
    st.info(f"""
    🧪 **EXPERIMENTO DE LA GUÍA:**
    * Línea $R(0) = {r0_val:.2f}\\text{{ cm}}^{{-1}}$
    * Línea $P(2) = {p2_val:.2f}\\text{{ cm}}^{{-1}}$
    * $(R(0) - P(2)) / 4 = {((r0_val - p2_val)/4):.2f}\\text{{ cm}}^{{-1}}$ (Coincide exactamente con $B_0 = {B0}\\text{{ cm}}^{{-1}}$)
    """)

# -----------------------------------------------------------------------------
# MÓDULO 5: EFECTO ISOTÓPICO
# -----------------------------------------------------------------------------
with tabs[4]:
    st.header("⚖️ Módulo 5: Efecto Isotópico (H³⁵Cl vs H³⁷Cl)")
    
    modo_iso = st.radio("Seleccionar Celda de Estudio:", ["Celda 9: Isótopo Individual", "Celda 10: Superposición para Comparación Directa"], horizontal=True)
    
    B0_35, B1_35, nu0_35 = 10.44, 10.136, 2885.9
    B0_37, B1_37, nu0_37 = 10.42, 10.120, 2883.8
    
    J_max = 12
    J_P, J_R = np.arange(1, J_max), np.arange(0, J_max - 1)
    
    frec_P35 = nu0_35 - (B1_35 + B0_35)*J_P + (B1_35 - B0_35)*(J_P**2)
    frec_R35 = nu0_35 + (B1_35 + B0_35)*(J_R + 1) + (B1_35 - B0_35)*((J_R + 1)**2)
    frec_P37 = nu0_37 - (B1_37 + B0_37)*J_P + (B1_37 - B0_37)*(J_P**2)
    frec_R37 = nu0_37 + (B1_37 + B0_37)*(J_R + 1) + (B1_37 - B0_37)*((J_R + 1)**2)
    
    int_P = np.array([1.0 / (J + 1) for J in J_P])
    int_R = np.array([1.0 / (J + 2) for J in J_R])
    max_i = max(max(int_P), max(int_R))
    int_P, int_R = int_P / max_i, int_R / max_i

    def agregar_stems(fig, x_vals, y_vals, color, dash='solid', symbol='circle', name=""):
        for x, y in zip(x_vals, y_vals):
            fig.add_trace(go.Scatter(x=[x, x], y=[0, y], mode='lines', line=dict(color=color, width=2, dash=dash), showlegend=False))
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='markers', marker=dict(color=color, size=7, symbol=symbol), name=name))

    fig5 = go.Figure()

    if modo_iso == "Celda 9: Isótopo Individual":
        iso_select = st.selectbox("Seleccionar Isótopo (Celda 9):", ["H³⁵Cl", "H³⁷Cl"])
        if iso_select == "H³⁵Cl":
            agregar_stems(fig5, frec_P35, int_P, 'blue', dash='dot', symbol='circle', name="H³⁵Cl - Rama P")
            agregar_stems(fig5, frec_R35, int_R, 'blue', dash='solid', symbol='square', name="H³⁵Cl - Rama R")
        else:
            agregar_stems(fig5, frec_P37, int_P, 'red', dash='dot', symbol='circle', name="H³⁷Cl - Rama P")
            agregar_stems(fig5, frec_R37, int_R, 'red', dash='solid', symbol='square', name="H³⁷Cl - Rama R")
        fig5.update_layout(title=f"Espectro de {iso_select}", xaxis_title="Número de onda (cm⁻¹)", yaxis_title="Intensidad relativa")
    else:
        agregar_stems(fig5, frec_P35, [1.0]*len(frec_P35), 'blue', dash='dot', symbol='circle', name="H³⁵Cl - Rama P")
        agregar_stems(fig5, frec_R35, [1.0]*len(frec_R35), 'blue', dash='solid', symbol='square', name="H³⁵Cl - Rama R")
        agregar_stems(fig5, frec_P37, [0.7]*len(frec_P37), 'red', dash='dot', symbol='circle', name="H³⁷Cl - Rama P")
        agregar_stems(fig5, frec_R37, [0.7]*len(frec_R37), 'red', dash='solid', symbol='square', name="H³⁷Cl - Rama R")
        fig5.update_layout(title="COMPARACIÓN DIRECTA: H³⁵Cl (azul) vs H³⁷Cl (rojo)", xaxis_title="Número de onda (cm⁻¹)", yaxis_title="Intensidad (desplazada)")

    fig5.update_layout(xaxis=dict(range=[2800, 2960]), template="plotly_white", height=450)
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("""
    🔬 **¿QUÉ OBSERVAS EN EL EFECTO ISOTÓPICO?**
    * **H³⁷Cl tiene MASAS más pesadas**, por lo que se desplaza ligeramente a **menores frecuencias**.
    * La forma general del espectro es **IDÉNTICA**.
    * La constante de fuerza del enlace **NO cambia** con el isótopo.
    """)

# -----------------------------------------------------------------------------
# MÓDULO 6: MINI-EVALUACIÓN Y ENTREGABLE
# -----------------------------------------------------------------------------
with tabs[5]:
    st.header("📝 Módulo 6: Mini-Evaluación y Entregable Final")
    
    col_eval1, col_eval2 = st.columns(2)
    
    with col_eval1:
        st.subheader("📝 Celda 11: Autoevaluación")
        q1 = st.radio("1️⃣ ¿Qué movimiento estudia la espectroscopía ROTACIONAL?", ["a) Vibración de enlaces", "b) Rotación de la molécula completa", "c) Movimiento de electrones", "d) Traslación"])
        q2 = st.radio("2️⃣ En el espectro rotacional del CO, las líneas están:", ["a) A la misma frecuencia", "b) Igualmente espaciadas", "c) Más juntas a alta frecuencia", "d) Más separadas a alta frecuencia"])
        q3 = st.radio("3️⃣ La RAMA P en el espectro IR del HCl corresponde a:", ["a) ΔJ = +1", "b) ΔJ = -1", "c) ΔJ = 0", "d) Transición electrónica"])
        q4 = st.radio("4️⃣ Si aumentamos la temperatura:", ["a) Se desplazan a menor frecuencia", "b) Aparecen líneas con J más altos", "c) Desaparece la rama R", "d) No cambia"])
        q5 = st.radio("5️⃣ El H³⁷Cl tiene frecuencias menores que H³⁵Cl porque:", ["a) Menor constante de fuerza", "b) Mayor masa reducida", "c) Enlace más largo", "d) Es radiactivo"])
        
        if st.button("Verificar Respuestas"):
            score = 0
            if "b)" in q1: score += 20
            if "b)" in q2: score += 20
            if "b)" in q3: score += 20
            if "b)" in q4: score += 20
            if "b)" in q5: score += 20
            
            st.success(f"🎉 Tu calificación es: {score} / 100")
            st.info("Respuestas correctas: 1-b, 2-b, 3-b, 4-b, 5-b")

    with col_eval2:
        st.subheader("📋 Celda 12: Tabla de Resultados")
        st.markdown("""
        Completa los siguientes valores obtenidos durante el laboratorio:

        | Molécula | Parámetro | Valor Obtenido | Valor Real |
        | :--- | :--- | :--- | :--- |
        | **CO** | Longitud de enlace r (Å) | `______` | **1.128 Å** |
        | **HCl** | Constante B₀ (cm⁻¹) | `______` | **10.44 cm⁻¹** |
        | **HCl** | Constante B₁ (cm⁻¹) | `______` | **10.14 cm⁻¹** |
        | **HCl** | Origen de banda ν₀ (cm⁻¹) | `______` | **2886 cm⁻¹** |
        | **H³⁷Cl** | Constante B₀ (cm⁻¹) | `______` | **10.42 cm⁻¹** |
        """)
        
        st.subheader("🎯 Pregunta Final del Docente")
        st.text_area("¿Por qué el CO tiene espectro rotacional pero el N₂ no? (Pista: busca 'momento dipolar'):", placeholder="Escribe tu respuesta aquí...")