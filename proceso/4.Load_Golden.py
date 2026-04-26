# Databricks notebook source
# === PARÁMETROS ===
dbutils.widgets.text("catalogo", "catalog_proyectosmartdata")
dbutils.widgets.text("esquema_source", "silver")
dbutils.widgets.text("esquema_sink", "golden")

catalogo = dbutils.widgets.get("catalogo")
esquema_source = dbutils.widgets.get("esquema_source")
esquema_sink = dbutils.widgets.get("esquema_sink")

# === IMPORTS ===
from pyspark.sql.functions import col, count, sum as spark_sum, avg, round as spark_round

# === LECTURA SILVER ===
df_silver = spark.table(f"{catalogo}.{esquema_source}.movies_enriched")
print(f"📥 Silver: {df_silver.count()} filas")

# ============================================================
# KPI 1 — Por Director
# ============================================================
df_kpi_director = (df_silver
    .filter(col("director").isNotNull())
    .groupBy("director")
    .agg(
        count("id").cast("int").alias("cantidad_peliculas"),
        spark_sum("revenue_usd").cast("double").alias("revenue_total"),
        spark_sum("budget_usd").cast("double").alias("budget_total"),
        spark_sum("profit_usd").cast("double").alias("profit_total"),
        spark_round(avg("user_score"), 2).cast("double").alias("score_promedio")
    )
    .filter(col("cantidad_peliculas") >= 2)
    .orderBy(col("revenue_total").desc())
)

print(f"📊 KPI Director: {df_kpi_director.count()} directores")
df_kpi_director.show(10, truncate=False)

(df_kpi_director.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .format("delta")
    .saveAsTable(f"{catalogo}.{esquema_sink}.kpi_por_director"))

# ============================================================
# KPI 2 — Por Género
# ============================================================
df_kpi_genero = (df_silver
    .filter(col("genre_principal").isNotNull())
    .groupBy("genre_principal")
    .agg(
        count("id").cast("int").alias("cantidad_peliculas"),
        spark_round(avg("revenue_usd"), 2).cast("double").alias("revenue_promedio"),
        spark_round(avg("user_score"), 2).cast("double").alias("score_promedio")
    )
    .orderBy(col("cantidad_peliculas").desc())
)

print(f"📊 KPI Género: {df_kpi_genero.count()} géneros")
df_kpi_genero.show(20, truncate=False)

(df_kpi_genero.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .format("delta")
    .saveAsTable(f"{catalogo}.{esquema_sink}.kpi_por_genero"))

# === VALIDACIÓN ===
print("\n✅ KPIs golden cargados correctamente")
print(f"   → {catalogo}.{esquema_sink}.kpi_por_director")
print(f"   → {catalogo}.{esquema_sink}.kpi_por_genero")
