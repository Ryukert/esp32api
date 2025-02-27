from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, db

app = FastAPI()

# Cargar las credenciales desde el archivo JSON (debes subir este archivo a tu servidor)
cred = credentials.Certificate("triodeaceleradores-firebase-adminsdk-fbsvc-6448d15405.json")  # Nombre del archivo JSON con las credenciales
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://triodeaceleradores-default-rtdb.firebaseio.com/"
})

# Clase para definir los datos de aceleración
class Aceleracion(BaseModel):
    x: float
    y: float
    z: float

# Clase para definir los datos de cada sensor
class SensorData(BaseModel):
    sensor_id: str
    aceleracion: Aceleracion

# Clase para definir los datos de múltiples sensores
class Sensores(BaseModel):
    sensores: List[SensorData]

# Añadir datos de múltiples sensores
@app.post("/items")
def add_items(sensores: Sensores):
    ref = db.reference("/acelerometros/item")
    results = []

    for sensor in sensores.sensores:
        new_ref = ref.push({
            "SENSOR_ID": sensor.sensor_id,
            "ACELERACION": {
                "X": sensor.aceleracion.x,
                "Y": sensor.aceleracion.y,
                "Z": sensor.aceleracion.z
            }
        })
        results.append({"sensor_id": sensor.sensor_id, "key": new_ref.key})

    return {"results": results}
