# Databricks notebook source
# === PARÁMETROS ===
dbutils.widgets.text("container", "raw")
dbutils.widgets.text("catalogo", "catalog_proyectosmartdata")
dbutils.widgets.text("esquema", "bronze")
dbutils.widgets.text("storageName", "adlssmartdata2511")

container = dbutils.widgets.get("container")
catalogo = dbutils.widgets.get("catalogo")
esquema = dbutils.widgets.get("esquema")
storageName = dbutils.widgets.get("storageName")

# === IMPORTS ===
from pyspark.sql.functions import col, expr

# === LECTURA DEL CSV (con manejo de comillas) ===
ruta = f"abfss://{container}@{storageName}.dfs.core.windows.net/movies/FilmDetails.csv"
df_film = (spark.read.format("csv")
    .option("header", "true")
    .option("multiLine", "true")
    .option("quote", '"')
    .option("escape", '"')
    .load(ruta))  # SIN inferSchema — todo string

print(f"📥 Filas leídas: {df_film.count()}")

# === LIMPIEZA Y CASTEO TOLERANTE ===
df_film_final = df_film.selectExpr(
    "try_cast(id as int) as id",
    "director",
    "top_billed",
    "try_cast(budget_usd as double) as budget_usd",
    "try_cast(revenue_usd as double) as revenue_usd"
)

# Filtrar filas que sí tengan id válido
df_film_final = df_film_final.filter(col("id").isNotNull())

print(f"📊 Filas válidas tras limpieza: {df_film_final.count()}")
df_film_final.show(5)

# === ESCRITURA A BRONZE (saveAsTable es más tolerante) ===
df_film_final.write.mode("overwrite").format("delta").saveAsTable(f"{catalogo}.{esquema}.film_details")

# === VALIDACIÓN ===
total = spark.table(f"{catalogo}.{esquema}.film_details").count()
print(f"✅ Tabla {catalogo}.{esquema}.film_details cargada con {total} filas")
spark.table(f"{catalogo}.{esquema}.film_details").limit(5).display()
