import streamlit as st

st.title("🚀 Mi Dashboard para SAFIRE")
st.write("¡Hola! La aplicación ya está conectada y funcionando en la nube.")

# Un pequeño campo interactivo de prueba
nombre = st.text_input("Escribe tu nombre:", "Marcos")

if nombre:
    st.success(f"¡Bienvenido al sistema, {nombre}! El entorno está listo para meter los datos del challenge.")