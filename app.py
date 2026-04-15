import streamlit as st
import pandas as pd
from datetime import datetime
import io
import pytz

st.title("📊 Sistema de Procesamiento de Registros")
st.markdown("### 🔍 Filtrado, validación y generación de cortes en tiempo real")
zona_peru = pytz.timezone("America/Lima")
hora_actual = datetime.now(zona_peru).strftime("%d/%m/%y %H:%M")

st.metric("🕒 Hora actual (Perú)", hora_actual)

# 📄 PLANTILLA
st.subheader("📄 Descargar plantilla base")

plantilla = pd.DataFrame({
    "DNI": ["12345678"],
    "NOMBRE": ["Juan"],
    "APELLIDO": ["Perez"],
    "CORREO": ["juan@email.com"],
    "CELULAR": ["987654321"],
    "ESTADO": ["APTO"]
})

buffer_plantilla = io.BytesIO()
plantilla.to_excel(buffer_plantilla, index=False)
buffer_plantilla.seek(0)

st.download_button(
    label="📥 Descargar plantilla Excel",
    data=buffer_plantilla,
    file_name="plantilla_registros.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Subir archivo
archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])
st.info("📁 Sube un archivo Excel con las columnas: DNI y ESTADO (valores: APTO / NO APTO)")

if archivo:
    df = pd.read_excel(archivo)

    st.subheader("📋 Vista previa")
    st.dataframe(df)

    # 🔹 Validar columnas necesarias
    if "DNI" not in df.columns or "ESTADO" not in df.columns:
        st.error("❌ El archivo debe contener las columnas 'DNI' y 'ESTADO'")
    else:
        # 🔹 Filtrar solo APTOS
        aptos_actuales = df[df["ESTADO"] == "APTO"]

        # 🔹 Conteo antes de limpiar
        total_aptos = len(aptos_actuales)

        # 🔹 Eliminar duplicados por DNI
        aptos_sin_duplicados = aptos_actuales.drop_duplicates(subset=["DNI"])

        # 🔹 Conteo después
        total_limpios = len(aptos_sin_duplicados)

        # 🔹 Duplicados encontrados
        duplicados = total_aptos - total_limpios

        # 🔹 Mostrar resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("✅ APTOS LIMPIOS", total_limpios)

        with col2:
            st.metric("⚠️ DUPLICADOS", duplicados)

            st.success(f"Se encontraron {total_limpios} registros aptos únicos y {duplicados} duplicados.")

        # 🔹 Botón generar corte
        if st.button("🚀 Generar Corte"):
            zona_peru = pytz.timezone("America/Lima")
            fecha_hora = datetime.now(zona_peru).strftime("%d-%m-%y_%H-%M")
            nombre_archivo = f"CORTE - {fecha_hora}.xlsx"

            if total_limpios > 0:
                # Crear archivo en memoria
                buffer = io.BytesIO()
                aptos_sin_duplicados.to_excel(buffer, index=False)
                buffer.seek(0)

                st.success(f"📂 Archivo generado correctamente: {nombre_archivo}")

                # Botón de descarga
                st.download_button(
                    label="📥 Descargar Corte",
                    data=buffer,
                    file_name=nombre_archivo,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("⚠️ No hay registros APTOS")
