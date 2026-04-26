# Databricks notebook source
# MAGIC %md
# MAGIC # Preparación del Ambiente
# MAGIC Crea esquemas y tablas vacías en bronze, silver y golden

# COMMAND ----------

# MAGIC %md
# MAGIC Widgets

# COMMAND ----------

dbutils.widgets.text("catalogo", "catalog_proyectosmartdata")
dbutils.widgets.text("esquema_bronze", "bronze")
dbutils.widgets.text("esquema_silver", "silver")
dbutils.widgets.text("esquema_golden", "golden")
dbutils.widgets.text("storageName", "adlssmartdata2511")

catalogo = dbutils.widgets.get("catalogo")
esquema_bronze = dbutils.widgets.get("esquema_bronze")
esquema_silver = dbutils.widgets.get("esquema_silver")
esquema_golden = dbutils.widgets.get("esquema_golden")
storageName = dbutils.widgets.get("storageName")

# COMMAND ----------

# MAGIC %md
# MAGIC Tablas Bronze

# COMMAND ----------

spark.sql(f"DROP TABLE IF EXISTS {catalogo}.{esquema_bronze}.movies")
spark.sql(f"""
CREATE TABLE {catalogo}.{esquema_bronze}.movies (
    id INT,
    title STRING,
    genres STRING,
    language STRING,
    user_score FLOAT,
    runtime_hour INT,
    runtime_min INT,
    release_date STRING,
    vote_count INT
) USING DELTA
""")

spark.sql(f"DROP TABLE IF EXISTS {catalogo}.{esquema_bronze}.film_details")
spark.sql(f"""
CREATE TABLE {catalogo}.{esquema_bronze}.film_details (
    id INT,
    director STRING,
    top_billed STRING,
    budget_usd DOUBLE,
    revenue_usd DOUBLE
) USING DELTA
""")

# COMMAND ----------

# MAGIC %md
# MAGIC Tabla Silver

# COMMAND ----------

spark.sql(f"DROP TABLE IF EXISTS {catalogo}.{esquema_silver}.movies_enriched")
spark.sql(f"""
CREATE TABLE {catalogo}.{esquema_silver}.movies_enriched (
    id INT,
    title STRING,
    genre_principal STRING,
    language STRING,
    user_score FLOAT,
    runtime_min_total INT,
    release_year INT,
    director STRING,
    budget_usd DOUBLE,
    revenue_usd DOUBLE,
    profit_usd DOUBLE,
    roi_pct DOUBLE,
    vote_count INT
) USING DELTA
""")

# COMMAND ----------

# MAGIC %md
# MAGIC Tablas Golden

# COMMAND ----------

spark.sql(f"DROP TABLE IF EXISTS {catalogo}.{esquema_golden}.kpi_por_director")
spark.sql(f"""
CREATE TABLE {catalogo}.{esquema_golden}.kpi_por_director (
    director STRING,
    cantidad_peliculas INT,
    revenue_total DOUBLE,
    budget_total DOUBLE,
    profit_total DOUBLE,
    score_promedio DOUBLE
) USING DELTA
""")

spark.sql(f"DROP TABLE IF EXISTS {catalogo}.{esquema_golden}.kpi_por_genero")
spark.sql(f"""
CREATE TABLE {catalogo}.{esquema_golden}.kpi_por_genero (
    genre_principal STRING,
    cantidad_peliculas INT,
    revenue_promedio DOUBLE,
    score_promedio DOUBLE
) USING DELTA
""")

print("✅ Tablas creadas correctamente")
