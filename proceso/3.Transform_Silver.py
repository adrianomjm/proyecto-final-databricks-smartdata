# Databricks notebook source
# === PARÁMETROS ===
dbutils.widgets.text("catalogo", "catalog_proyectosmartdata")
dbutils.widgets.text("esquema_source", "bronze")
dbutils.widgets.text("esquema_sink", "silver")

catalogo = dbutils.widgets.get("catalogo")
esquema_source = dbutils.widgets.get("esquema_source")
esquema_sink = dbutils.widgets.get("esquema_sink")

# === IMPORTS ===
from pyspark.sql.functions import col, split, year, to_date, when, round as spark_round, lit

# === LECTURA DE BRONZE ===
df_movies = spark.table(f"{catalogo}.{esquema_source}.movies")
df_film = spark.table(f"{catalogo}.{esquema_source}.film_details")

print(f"📥 Movies bronze: {df_movies.count()} filas")
print(f"📥 FilmDetails bronze: {df_film.count()} filas")

# === TRANSFORMACIÓN ===
# Calcular runtime total en minutos
df_movies_t = df_movies.withColumn(
    "runtime_min_total",
    (col("runtime_hour") * 60 + col("runtime_min"))
).withColumn(
    "release_year",
    year(to_date(col("release_date"), "yyyy-MM-dd"))
).withColumn(
    "genre_principal",
    split(col("genres"), ",").getItem(0)
)

# === JOIN ENTRE LAS 2 FUENTES ===
df_silver = df_movies_t.alias("m").join(
    df_film.alias("f"),
    col("m.id") == col("f.id"),
    "inner"
).select(
    col("m.id"),
    col("m.title"),
    col("m.genre_principal"),
    col("m.language"),
    col("m.user_score"),
    col("m.runtime_min_total"),
    col("m.release_year"),
    col("f.director"),
    col("f.budget_usd"),
    col("f.revenue_usd"),
    (col("f.revenue_usd") - col("f.budget_usd")).alias("profit_usd"),
    when(col("f.budget_usd") > 0,
         spark_round((col("f.revenue_usd") - col("f.budget_usd")) / col("f.budget_usd") * 100, 2)
    ).otherwise(lit(None)).alias("roi_pct"),
    col("m.vote_count")
)

# Filtrar registros con datos clave
df_silver = df_silver.filter(col("director").isNotNull())

print(f"📊 Filas tras JOIN: {df_silver.count()}")
df_silver.show(5, truncate=False)

# === ESCRITURA A SILVER ===
df_silver.write.mode("overwrite").format("delta").saveAsTable(
    f"{catalogo}.{esquema_sink}.movies_enriched"
)

# === VALIDACIÓN ===
total = spark.table(f"{catalogo}.{esquema_sink}.movies_enriched").count()
print(f"✅ Tabla {catalogo}.{esquema_sink}.movies_enriched cargada con {total} filas")
spark.table(f"{catalogo}.{esquema_sink}.movies_enriched").limit(5).display()
