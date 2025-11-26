# 🛡️ Python & PostgreSQL Audit Toolkit

Este repositorio contiene un conjunto de herramientas modulares en **Python** diseñadas para conectar, auditar y explorar bases de datos **PostgreSQL** de manera segura y eficiente.

El objetivo es automatizar la exploración de datos (Data Discovery) y la ingeniería inversa de esquemas, reemplazando consultas SQL manuales repetitivas con scripts de Python robustos.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Postgres](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge)

## 📂 Arquitectura del Proyecto

```text
📦 proyecto-postgres-python
 ┣ 📂 .venv/                 # Entorno virtual (Ignorado por Git)
 ┣ 📜 .env                   # Variables de entorno (Ignorado por Git)
 ┣ 📜 .gitignore             # Configuración de exclusiones
 ┣ 📜 conexion.py            # 🔌 Core: Motor de conexión seguro
 ┣ 📜 ver_bases.py           # 🌍 Server: Listado de bases de datos
 ┣ 📜 mapear_db.py           # 📋 Analysis: Diccionario de tablas
 ┣ 📜 inspector_avanzado.py  # ⚙️ Engineering: Auditoría de PK/FKs
 ┣ 📜 README.md              # Documentación
 ┗ 📜 requirements.txt       # Dependencias
```
| Archivo | Nivel | Responsabilidad |
| :--- | :--- | :--- |
| `conexion.py` | Core | Gestiona la conexión a la BD usando `SQLAlchemy`. Implementa seguridad vía variables de entorno (`.env`) para no exponer credenciales. |
| `ver_bases.py` | Server | Se conecta a la base maestra para listar todas las bases de datos existentes en el servidor y su tamaño. |
| `mapear_db.py` | Analysis | Genera un "Diccionario de Datos" legible (Dataframe) de una base específica. Ideal para ver tablas y tipos de datos rápidamente. |
| `inspector_avanzado.py` | Eng | Utiliza `SQLAlchemy Inspector` para auditar relaciones complejas. Detecta **Claves Primarias (PK)** y **Claves Foráneas (FK)** automáticamente. |

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/DavidHuamanRoman/proyecto-postgres-python.git
cd proyecto-postgres-python
```
### 2. Preparar el entorno

Se recomienda usar un entorno virtual para mantener las dependencias aisladas.

```bash
# Crear entorno virtual (Windows)
python -m venv .venv

# Activar entorno
.venv\Scripts\activate

# Instalar librerías
pip install -r requirements.txt
```
### 3. Configuración de Seguridad (.env)
Este proyecto no "hardcodea" contraseñas. Debes crear un archivo llamado .env en la raíz del proyecto y definir tus credenciales:

```bash
DB_USER=postgres
DB_PASS=tu_password_secreto
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
```
## 🛠️ Uso de las Herramientas

### A. Auditoría de Servidor
Para ver qué bases de datos existen en tu instancia de Postgres:

```bash
python ver_bases.py
```
*Salida: Tabla con nombres de DBs y su tamaño en disco*

### B. Mapeo de una Base de Datos
Genera un reporte limpio de las tablas para análisis.

Tip: Puedes editar mapear_db.py para cambiar la base de datos objetivo si no quieres usar la default.

```bash
python mapear_db.py
```
*Salida: Dataframe con tablas y tipos de datos*

### C. Auditoría Avanzada de Esquema
Para auditar la arquitectura interna, llaves primarias y relaciones entre tablas:

```bash
python inspector_avanzado.py
```
*Salida: Reporte detallado de relaciones entre tablas*

## 🔐 Buenas Prácticas Implementadas

* **Seguridad:** El archivo `.gitignore` excluye explícitamente `.env` y la carpeta `.venv`, preveniendo fugas de credenciales.
* **Modularidad:** Principio de responsabilidad única. La lógica de conexión está desacoplada de la lógica de negocio.
* **Abstracción:** Uso híbrido de `Pandas` (para lectura visual rápida) y `SQLAlchemy Inspector` (para obtención de metadatos técnicos agnósticos de la base de datos).


## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si deseas mejorar las herramientas o agregar nuevas funcionalidades, por favor sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m 'Agrega nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
---
Hecho con ❤️ por David Huamán Román


