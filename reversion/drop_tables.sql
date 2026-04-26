-- =========================================================
-- REVERSIÓN: Elimina tablas y esquemas del proyecto
-- Ejecutar para limpiar el ambiente completamente
-- =========================================================

USE CATALOG catalog_proyectosmartdata;

-- Tablas Golden
DROP TABLE IF EXISTS catalog_proyectosmartdata.golden.kpi_por_director;
DROP TABLE IF EXISTS catalog_proyectosmartdata.golden.kpi_por_genero;

-- Tabla Silver
DROP TABLE IF EXISTS catalog_proyectosmartdata.silver.movies_enriched;

-- Tablas Bronze
DROP TABLE IF EXISTS catalog_proyectosmartdata.bronze.movies;
DROP TABLE IF EXISTS catalog_proyectosmartdata.bronze.film_details;

-- Esquemas
DROP SCHEMA IF EXISTS catalog_proyectosmartdata.golden CASCADE;
DROP SCHEMA IF EXISTS catalog_proyectosmartdata.silver CASCADE;
DROP SCHEMA IF EXISTS catalog_proyectosmartdata.bronze CASCADE;

-- Catálogo (descomentar si se desea eliminar todo)
-- DROP CATALOG IF EXISTS catalog_proyectosmartdata CASCADE;
