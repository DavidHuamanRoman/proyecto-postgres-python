# 🛡️ Python & PostgreSQL Audit Toolkit

Este repositorio contiene un conjunto de herramientas modulares en **Python** diseñadas para conectar, auditar y explorar bases de datos **PostgreSQL** de manera segura y eficiente. 

El objetivo es automatizar la exploración de datos (Data Discovery) y la ingeniería inversa de esquemas, reemplazando consultas SQL manuales repetitivas con scripts de Python robustos.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Postgres](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge)

## 📂 Estructura del Proyecto

El proyecto está organizado en módulos con responsabilidades únicas (Separation of Concerns):

| Archivo | Descripción | Nivel |
| :--- | :--- | :--- |
| **`conexion.py`** | 🔌 **Motor Central.** Gestiona la conexión a la BD usando `SQLAlchemy`. Implementa seguridad vía variables de entorno (`.env`) para no exponer credenciales. | Core |
| **`ver_bases.py`** | 🌍 **Explorador de Servidor.** Se conecta a la base maestra para listar todas las bases de datos existentes en el servidor y su tamaño. | Server |
| **`mapear_db.py`** | 📋 **Analista de Datos.** Genera un "Diccionario de Datos" legible (Dataframe) de una base específica. Ideal para ver tablas y tipos de datos rápidamente. | Analysis |
| **`inspector_avanzado.py`** | ⚙️ **Ingeniero de Datos.** Utiliza `SQLAlchemy Inspector` para auditar relaciones complejas. Detecta **Claves Primarias (PK)** y **Claves Foráneas (FK)** automáticamente. | Engineering |
| **`.env`** | 🔐 **Credenciales.** Archivo de configuración local (ignorado por Git) para guardar usuario, contraseña y host. | Security |

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone [https://github.com/DavidHuamanRoman/proyecto-postgres-python.git](https://github.com/DavidHuamanRoman/proyecto-postgres-python.git)
cd proyecto-postgres-python
2. Preparar el entorno
Se recomienda usar un entorno virtual para no afectar tu instalación global de Python.

Bash

# Windows
python -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
3. Configuración de Seguridad (.env)
Este proyecto no "hardcodea" contraseñas. Debes crear un archivo llamado .env en la raíz del proyecto con tus credenciales:

Ini, TOML

DB_USER=postgres
DB_PASS=tu_password_secreto
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
🛠️ Uso de las Herramientas
A. Para ver qué bases de datos tienes en el servidor:
Bash

python ver_bases.py
Salida: Una tabla con nombres de DBs y su peso en disco.

B. Para obtener un diccionario de datos (Tablas y Columnas):
Edita mapear_db.py para elegir la base de datos y ejecuta:

Bash

python mapear_db.py
C. Para auditar relaciones y llaves (PK/FK):
Para ver la arquitectura interna y cómo se relacionan las tablas:

Bash

python inspector_avanzado.py
🔐 Buenas Prácticas Implementadas
Git Ignore: El archivo .gitignore está configurado para excluir .env y carpetas de entorno virtual (.venv), protegiendo información sensible.

Modularidad: La lógica de conexión está aislada, permitiendo reutilizar conexion.py en futuros scripts sin reescribir código.

ORM vs SQL: Uso híbrido de Pandas (para lectura rápida) y SQLAlchemy Inspector (para metadatos técnicos).

Desarrollado por David Fernando Huamán Román - Data Analyst