CREATE SCHEMA IF NOT EXISTS "ml";

DROP TABLE IF EXISTS "ml"."metrics";
CREATE TABLE IF NOT EXISTS "ml"."metrics" (
    "data" date NOT NULL,
    "mse" double precision NOT NULL,
    "rmse" double precision NOT NULL,
    "mape" double precision NOT NULL,
    CONSTRAINT "metrics_data" PRIMARY KEY ("data")
) WITH (oids = false);

DROP TABLE IF EXISTS "ml"."raw_data";
CREATE TABLE IF NOT EXISTS "ml"."raw_data" (
    "codigo" character(10) NOT NULL,
    "acao" text NOT NULL,
    "tipo" text NOT NULL,
    "qtdeteorica" bigint NOT NULL,
    "part" double precision NOT NULL,
    "data" date NOT NULL
) WITH (oids = false);
