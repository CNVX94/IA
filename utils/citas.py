import json
import os

def guardar_cita(nombre, fecha, hora, descripcion):
    cita = {
        "nombre": nombre,
        "fecha": fecha,
        "hora": hora,
        "descripcion": descripcion
    }
    citas = []
    if os.path.exists("citas.json"):
        with open("citas.json", "r") as file:
            citas = json.load(file)
    citas.append(cita)
    with open("citas.json", "w") as file:
        json.dump(citas, file, indent=4)

def consultar_citas(nombre):
    if not os.path.exists("citas.json"):
        return []
    with open("citas.json", "r") as file:
        citas = json.load(file)
    return [c for c in citas if c["nombre"].lower() == nombre.lower()]
