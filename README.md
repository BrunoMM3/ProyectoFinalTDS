﻿# ProyectoFinalTDS
# 🧾 Gestión de Activos Fijos Menores

Aplicación de escritorio desarrollada en **Python** con **Tkinter** y **MongoDB**, diseñada para gestionar activos fijos menores como proyectores, laptops, cámaras, etc. Permite registrar, asignar, ubicar y realizar mantenimiento a estos activos dentro de un departamento o institución.

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Tkinter** - Interfaz gráfica de usuario (GUI)
- **MongoDB** - Base de datos NoSQL
- **pymongo** - Conector entre Python y MongoDB

---

## 📁 Estructura del proyecto
```bash
gestion_activos/
├── app/ # Punto de entrada de la aplicación
├── controllers/ # Lógica de control entre GUI y servicios
├── gui/ # Ventanas de Tkinter
├── models/ # Definiciones de entidades (activos, usuarios, etc.)
├── repositories/ # Conexión a MongoDB y operaciones de datos
├── requirements.txt # Dependencias del proyecto
└── README.md
```

---

## ✅ Funcionalidades principales

- 🔐 **Login de usuarios**
- 🆕 **Registro y edición de activos**
- 📍 **Asignación de activos por ubicación/persona**
- 🛠️ **Historial de mantenimiento**
- 🔍 **Consultas avanzadas** (por ubicación, estado, asignación)
- 📊 **Organización modular y mantenible**

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/BrunoMM3/ProyectoFinalTDS.git
cd ProyectoFinalTDS
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Linux/macOS
venv\Scripts\activate     # En Windows
```
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 🚀 Ejecutar la aplicación
 ```bash
python app/main.py
```


