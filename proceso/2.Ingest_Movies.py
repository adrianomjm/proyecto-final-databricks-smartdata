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
from pyspark.sql.functions import col, split, hour, minute, to_timestamp, year
from pyspark.sql.types import IntegerType, FloatType

# === LECTURA DEL CSV ===
ruta_movies = f"abfss://{container}@{storageName}.dfs.core.windows.net/movies/Movies.csv"
df_movies = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(ruta_movies)

print(f"📥 Filas leídas: {df_movies.count()}")
df_movies.printSchema()

# COMMAND ----------

# === ESCRITURA A BRONZE ===
df_movies_final = df_movies.select(
    col("id").cast("int"),
    col("title"),
    col("genres"),
    col("language"),
    col("user_score").cast("float"),
    col("runtime_hour").cast("int"),
    col("runtime_min").cast("int"),
    col("release_date").cast("string"),
    col("vote_count").cast("int")
)

df_movies_final.write.mode("overwrite").insertInto(f"{catalogo}.{esquema}.movies")

# Validación
total = spark.table(f"{catalogo}.{esquema}.movies").count()
print(f"✅ Tabla {catalogo}.{esquema}.movies cargada con {total} filas")
spark.table(f"{catalogo}.{esquema}.movies").limit(5).display()
