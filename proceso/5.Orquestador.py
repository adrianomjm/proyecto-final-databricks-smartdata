# Databricks notebook source
# === ORQUESTADOR DEL PIPELINE ETL ===
# Ejecuta los notebooks en orden: Preparacion -> Ingesta -> Transform -> Load
# Detecta automaticamente la ruta donde esta este notebook
# Funciona en cualquier workspace (DEV, PROD, /Users/, /Shared/, etc.)

import os

RUTA_BASE = os.path.dirname(
    dbutils.notebook.entry_point.getDbutils()
    .notebook().getContext().notebookPath().get()
)
print(f"RUTA_BASE detectada: {RUTA_BASE}")

# === PARAMETROS GLOBALES ===
catalogo = "catalog_proyectosmartdata"
storageName = "adlssmartdata2511"
container = "raw"

# COMMAND ----------

# === 1. PREPARACION AMBIENTE ===
print("=" * 60)
print("1. Preparacion de ambiente")
print("=" * 60)
dbutils.notebook.run(
    f"{RUTA_BASE}/1.Preparacion_Ambiente",
    timeout_seconds=600,
    arguments={
        "catalogo": catalogo,
        "esquema_bronze": "bronze",
        "esquema_silver": "silver",
        "esquema_golden": "golden",
        "storageName": storageName
    }
)
print("OK Preparacion de ambiente completada")

# COMMAND ----------

# === 2. INGESTA MOVIES ===
print("=" * 60)
print("2. Ingesta Movies (RAW -> BRONZE)")
print("=" * 60)
dbutils.notebook.run(
    f"{RUTA_BASE}/2.Ingest_Movies",
    timeout_seconds=600,
    arguments={
        "container": container,
        "catalogo": catalogo,
        "esquema": "bronze",
        "storageName": storageName
    }
)
print("OK Ingesta Movies completada")

# COMMAND ----------

# === 3. INGESTA FILM DETAILS ===
print("=" * 60)
print("3. Ingesta FilmDetails (RAW -> BRONZE)")
print("=" * 60)
dbutils.notebook.run(
    f"{RUTA_BASE}/2.Ingest_FilmDetails",
    timeout_seconds=600,
    arguments={
        "container": container,
        "catalogo": catalogo,
        "esquema": "bronze",
        "storageName": storageName
    }
)
print("OK Ingesta FilmDetails completada")

# COMMAND ----------

# === 4. TRANSFORMACION SILVER ===
print("=" * 60)
print("4. Transform Silver (BRONZE -> SILVER)")
print("=" * 60)
dbutils.notebook.run(
    f"{RUTA_BASE}/3.Transform_Silver",
    timeout_seconds=600,
    arguments={
        "catalogo": catalogo,
        "esquema_source": "bronze",
        "esquema_sink": "silver"
    }
)
print("OK Transform Silver completada")

# COMMAND ----------

# === 5. LOAD GOLDEN ===
print("=" * 60)
print("5. Load Golden (SILVER -> GOLDEN)")
print("=" * 60)
dbutils.notebook.run(
    f"{RUTA_BASE}/4.Load_Golden",
    timeout_seconds=600,
    arguments={
        "catalogo": catalogo,
        "esquema_source": "silver",
        "esquema_sink": "golden"
    }
)
print("OK Load Golden completada")

# COMMAND ----------

print("\n" + "=" * 60)
print("PIPELINE ETL COMPLETO - TODOS LOS NOTEBOOKS EJECUTADOS")
print("=" * 60)
