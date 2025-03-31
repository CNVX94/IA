import streamlit as st
import time
import sqlite3

# Importamos las funciones de los módulos
from utils.ollama_utils import chat_with_ollama
from utils.citas import guardar_cita, consultar_citas
from utils.historial import guardar_historial_txt
from utils.database import init_db, get_store_info, guardar_historial_db

# Información del negocio para el chatbot
informacion_negocio = """
Eres un asistente virtual para clientes de TechFix Izcalli, un taller de reparación de computadoras.

Tu objetivo es:
- Dar respuestas claras, breves y útiles.
- Mostrar confianza y profesionalismo.
- Evitar pedir información que ya tienes.
- Sugerir agendar cita si el usuario tiene un problema técnico.
- Solo brindar ayuda relacionada con el servicio técnico.
- No respondas preguntas sobre videojuegos, recetas, películas u otros temas ajenos al servicio técnico.
- Si te preguntan algo fuera de contexto, rechaza amablemente y vuelve al tema del servicio técnico.
- Si el usuario quiere agendar una cita, invítalo a rellenar el formulario correspondiente.

📍 Info del negocio:
- Ubicación: Izcalli, C.P. 54720
- Horario: Lunes a viernes de 10:00 a.m. a 7:00 p.m.
- Teléfono: 55 1234 5678

🎯 Servicios:
- Reparación y mantenimiento de laptops/PC
- Formateo, limpieza, eliminación de virus
- Diagnóstico gratuito, recuperación de datos

🎉 Promos activas:
- Mantenimiento a $299
- 10% en formateo esta semana
- 15% en accesorios
"""

# Integrar información local de la tienda desde la base de datos
conn = init_db()
store_info = get_store_info(conn)
conn.close()

if store_info:
    detalles = "\n".join([f"{k}: {v}" for k, v in store_info.items()])
    informacion_negocio += "\nInformación adicional de la tienda:\n" + detalles

# Configuración de la página
st.set_page_config(page_title="Asistente Técnico", page_icon="🛠️")
st.markdown("""
# 🤖 Chatbot Servicio Técnico
Bienvenido al asistente virtual de **TechFix Izcalli**. Estoy aquí para ayudarte con consultas sobre servicios técnicos o para agendar tu cita.
""")

model_name = "gemma3:1b"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": informacion_negocio}
    ]

# Sección de preguntas frecuentes (FAQ)
with st.expander("📚 Preguntas frecuentes (FAQ)"):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛠️ ¿Qué servicios ofrecen?"):
            st.session_state.messages.append({"role": "assistant", "content": "Ofrecemos reparación y mantenimiento de laptops y PCs, formateo, limpieza interna, eliminación de virus, recuperación de datos y diagnóstico gratuito."})
        if st.button("🕒 ¿Cuál es el horario?"):
            st.session_state.messages.append({"role": "assistant", "content": "Nuestro horario es de lunes a viernes, de 10:00 a.m. a 7:00 p.m."})
    with col2:
        if st.button("💸 ¿Cuánto cuesta el mantenimiento?"):
            st.session_state.messages.append({"role": "assistant", "content": "El mantenimiento tiene una promoción activa de $299."})
        if st.button("📍 ¿Dónde están ubicados?"):
            st.session_state.messages.append({"role": "assistant", "content": "Estamos en Izcalli, C.P. 54720. ¡Te esperamos!"})
# 📥 Insertar FAQs
# if st.button("📥 Insertar FAQs"):

# Entrada de usuario
user_input = st.text_input("✍️ Escribe tu mensaje:", placeholder="Ej: Mi computadora no prende, ¿qué hago?")

if st.button("📨 Enviar"):
    if user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("💬 El asistente está procesando tu mensaje..."):
            time.sleep(1)
            response = chat_with_ollama(st.session_state.messages, model_name)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Guardar historial en archivo y en la base de datos
        guardar_historial_txt(st.session_state.messages)
        conn = init_db()
        guardar_historial_db(conn, st.session_state.messages)
        conn.close()
    else:
        st.warning("⚠️ Escribe algo para poder enviarlo.")

# Mostrar historial de mensajes
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**🧑 Tú:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**🤖 Bot:** {message['content']}")

# Sección para agendar citas
with st.expander("📅 Haz clic aquí para agendar una cita"):
    with st.form("form_cita"):
        nombre = st.text_input("👤 Tu nombre")
        fecha = st.date_input("📆 Fecha deseada")
        hora = st.time_input("⏰ Hora deseada")
        descripcion = st.text_area("🛠️ Descripción del problema", placeholder="Ej: Mi computadora no enciende...")
        enviar_cita = st.form_submit_button("✅ Agendar cita")
        if enviar_cita:
            if nombre and descripcion:
                guardar_cita(nombre, str(fecha), str(hora), descripcion)
                st.success("🎉 Tu cita ha sido agendada con éxito.")
            else:
                st.warning("⚠️ Por favor completa todos los campos.")

# Sección para consultar citas agendadas
with st.expander("🔍 Consultar citas agendadas"):
    nombre_consulta = st.text_input("👤 Ingresa tu nombre para buscar tus citas")
    if st.button("📋 Mostrar citas"):
        citas_encontradas = consultar_citas(nombre_consulta)
        if citas_encontradas:
            for c in citas_encontradas:
                st.info(f"📆 {c['fecha']} a las {c['hora']} - {c['descripcion']}")
        else:
            st.warning("⚠️ No se encontraron citas con ese nombre.")

# Botón para reiniciar la conversación
if st.button("🔄 Reiniciar conversación"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("✅ Conversación reiniciada. Puedes comenzar de nuevo.")
    st.stop()

# Add JavaScript for auto-scrolling
st.components.v1.html(f"""
<script>
    window.parent.document.querySelector('section.main').scrollTo(0, window.parent.document.querySelector('section.main').scrollHeight);
</script>
""", height=0)
