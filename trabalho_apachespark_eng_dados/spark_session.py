from pathlib import Path

from pyspark.sql import SparkSession

ICEBERG_PACKAGE = 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.9.2'


def delta_configs() -> dict[str, str]:
    return {
        'spark.sql.extensions': 'io.delta.sql.DeltaSparkSessionExtension',
        'spark.sql.catalog.spark_catalog': (
            'org.apache.spark.sql.delta.catalog.DeltaCatalog'
        ),
    }


def iceberg_configs(warehouse: Path) -> dict[str, str]:
    return {
        'spark.jars.packages': ICEBERG_PACKAGE,
        'spark.sql.extensions': (
            'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions'
        ),
        'spark.sql.catalog.local': 'org.apache.iceberg.spark.SparkCatalog',
        'spark.sql.catalog.local.type': 'hadoop',
        'spark.sql.catalog.local.warehouse': str(warehouse),
    }


def create_delta_session() -> SparkSession:
    from delta import configure_spark_with_delta_pip

    builder = SparkSession.builder.appName('delta-lake').master('local[*]')
    for chave, valor in delta_configs().items():
        builder = builder.config(chave, valor)
    return configure_spark_with_delta_pip(builder).getOrCreate()


def create_iceberg_session(warehouse: Path) -> SparkSession:
    builder = SparkSession.builder.appName('apache-iceberg').master('local[*]')
    for chave, valor in iceberg_configs(warehouse).items():
        builder = builder.config(chave, valor)
    return builder.getOrCreate()
