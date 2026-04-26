-- =========================================================
-- SEGURIDAD: GRANTs sobre catálogo, esquemas y tablas
-- =========================================================

GRANT USE CATALOG ON CATALOG catalog_proyectosmartdata TO `account users`;

-- BRONZE: Solo Data Engineers
GRANT USE SCHEMA ON SCHEMA catalog_proyectosmartdata.bronze TO `data_engineers`;
GRANT MODIFY, SELECT ON SCHEMA catalog_proyectosmartdata.bronze TO `data_engineers`;

-- SILVER: Engineers + Analysts (lectura)
GRANT USE SCHEMA ON SCHEMA catalog_proyectosmartdata.silver TO `data_engineers`;
GRANT MODIFY, SELECT ON SCHEMA catalog_proyectosmartdata.silver TO `data_engineers`;
GRANT USE SCHEMA ON SCHEMA catalog_proyectosmartdata.silver TO `data_analysts`;
GRANT SELECT ON SCHEMA catalog_proyectosmartdata.silver TO `data_analysts`;

-- GOLDEN: Lectura amplia para BI
GRANT USE SCHEMA ON SCHEMA catalog_proyectosmartdata.golden TO `data_engineers`;
GRANT MODIFY, SELECT ON SCHEMA catalog_proyectosmartdata.golden TO `data_engineers`;
GRANT USE SCHEMA ON SCHEMA catalog_proyectosmartdata.golden TO `data_analysts`;
GRANT SELECT ON SCHEMA catalog_proyectosmartdata.golden TO `data_analysts`;
GRANT USE SCHEMA ON SCHEMA catalog_proyectosmartdata.golden TO `bi_consumers`;
GRANT SELECT ON SCHEMA catalog_proyectosmartdata.golden TO `bi_consumers`;

-- Tablas específicas para usuarios externos
GRANT SELECT ON TABLE catalog_proyectosmartdata.golden.kpi_por_director TO `external_users`;
GRANT SELECT ON TABLE catalog_proyectosmartdata.golden.kpi_por_genero TO `external_users`;
