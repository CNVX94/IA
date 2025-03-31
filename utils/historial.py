import os
import time

def guardar_historial_txt(historial):
    carpeta = "historiales"
    os.makedirs(carpeta, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    archivo = os.path.join(carpeta, f"chat_{timestamp}.txt")
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(f"🕒 Conversación iniciada: {timestamp}\n\n")
        for mensaje in historial:
            rol = "Tú" if mensaje["role"] == "user" else "Bot"
            f.write(f"{rol}: {mensaje['content']}\n")
        f.write("\n" + "-" * 40 + "\n")
