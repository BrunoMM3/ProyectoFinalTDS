from pymongo import MongoClient
from datetime import datetime
import random

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["gestion_activos"]  # Nombre de la base de datos
coleccion = db["activos"]       # Nombre de la colección

# Datos de ejemplo
nombres = ["Laptop", "Monitor", "Impresora", "Proyector", "Switch", "Router"]
marcas = ["Dell", "HP", "Lenovo", "Asus", "Cisco", "Epson"]
estados = ["operativo", "en reparación", "dado de baja"]
categorias = ["Computadora portátil", "Periférico", "Red", "Proyección", "Impresión"]

# Generar un activo con los campos requeridos por tu tabla
def generar_activo(i):
    nombre = random.choice(nombres)
    marca = random.choice(marcas)
    estado = random.choice(estados)
    categoria = random.choice(categorias)
    codigo = f"{nombre[:3].upper()}-2024-{i:03}"

    return {
        "nombre": f"{nombre} {marca} {i}",
        "descripcion": f"{nombre} modelo {i} para uso institucional",
        "codigo_interno": codigo,
        "categoria": categoria,
        "marca": marca,
        "modelo": f"Modelo-{i}",
        "numero_serie": f"SN{i:09}",
        "estado": estado,
        "fecha_adquisicion": datetime(
            year=2023,
            month=random.randint(1, 12),
            day=random.randint(1, 28)
        ),
        "valor": round(random.uniform(5000, 20000), 2),
        "quien_registro": "admin"  # Puedes cambiarlo por otro nombre si lo deseas
    }

# Insertar 50 activos únicos basados en el código interno
insertados = 0
for i in range(1, 51):
    activo = generar_activo(i)
    if not coleccion.find_one({"codigo_interno": activo["codigo_interno"]}):
        coleccion.insert_one(activo)
        insertados += 1

print(f"Se insertaron {insertados} activos nuevos.")