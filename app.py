import streamlit as st
import pandas as pd
from datetime import datetime
import os
import io

st.title("📊 Generador de Cortes - APTOS")

# Subir archivo
archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)

    st.subheader("📋 Vista previa")
    st.dataframe(df)

    # Filtrar aptos
    aptos_actuales = df[df["ESTADO"] == "APTO"]

    archivo_base = "base_aptos.xlsx"

    # Verificar base
    if os.path.exists(archivo_base):
        base = pd.read_excel(archivo_base)
        base_dni = base["DNI"].tolist()

        nuevos_aptos = aptos_actuales[
            ~aptos_actuales["DNI"].isin(base_dni)
        ]

        st.success(f"🆕 Nuevos APTOS encontrados: {len(nuevos_aptos)}")

    else:
        st.info("📁 Primera ejecución: todos son nuevos")
        nuevos_aptos = aptos_actuales

    # Botón generar corte
    if st.button("🚀 Generar Corte"):
        hora_actual = datetime.now().strftime("%H-%M")
        nombre_archivo = f"CORTE - {hora_actual}.xlsx"

        if len(nuevos_aptos) > 0:
            # Crear archivo en memoria
            buffer = io.BytesIO()
            nuevos_aptos.to_excel(buffer, index=False)
            buffer.seek(0)

            st.success(f"📁 Archivo listo: {nombre_archivo}")

            # Botón de descarga
            st.download_button(
                label="📥 Descargar Corte",
                data=buffer,
                file_name=nombre_archivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Actualizar base
            aptos_actuales.to_excel(archivo_base, index=False)

        else:
            st.warning("⚠️ No hay nuevos aptos")