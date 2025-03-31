import ollama

def chat_with_ollama(messages, model_name="gemma3:1b"):
    try:
        response = ollama.chat(model=model_name, messages=messages)
        if "message" in response:
            return response["message"].get("content", "Respuesta vacía del modelo.")
        else:
            return "Error: La estructura de la respuesta no es válida."
    except Exception as e:
        return f"❌ Error al interactuar con el modelo: {e}"
