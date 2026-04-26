# Databricks notebook source
# === ORQUESTADOR DEL PIPELINE ETL ===
# Ejecuta los notebooks en orden: Preparación → Ingesta → Transform → Load

RUTA_BASE = "/Users/ajuarezm88@gmail.com/proyectosmartdata/ETL"

# === PARÁMETROS GLOBALES ===
catalogo = "catalog_proyectosmartdata"
storageName = "adlssmartdata2511"
container = "raw"

# === 1. PREPARACIÓN AMBIENTE ===
print("=" * 60)
print("🔧 1. Preparación de ambiente")
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
print("✅ Preparación de ambiente completada")

# === 2. INGESTA MOVIES ===
print("=" * 60)
print("📥 2. Ingesta Movies (RAW → BRONZE)")
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
print("✅ Ingesta Movies completada")

# === 3. INGESTA FILM DETAILS ===
print("=" * 60)
print("📥 3. Ingesta FilmDetails (RAW → BRONZE)")
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
print("✅ Ingesta FilmDetails completada")

# === 4. TRANSFORMACIÓN SILVER ===
print("=" * 60)
print("🔄 4. Transform Silver (BRONZE → SILVER)")
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
print("✅ Transform Silver completada")

# === 5. LOAD GOLDEN ===
print("=" * 60)
print("🏆 5. Load Golden (SILVER → GOLDEN)")
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
print("✅ Load Golden completada")

print("\n" + "=" * 60)
print("🎉 PIPELINE ETL COMPLETO — TODOS LOS NOTEBOOKS EJECUTADOS")
print("=" * 60)
