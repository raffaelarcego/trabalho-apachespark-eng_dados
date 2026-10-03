from pathlib import Path

from trabalho_apachespark_eng_dados.spark_session import (
    ICEBERG_PACKAGE,
    delta_configs,
    iceberg_configs,
)


def test_delta_configs_tem_extensao_e_catalogo():
    configs = delta_configs()

    assert configs['spark.sql.extensions'] == (
        'io.delta.sql.DeltaSparkSessionExtension'
    )
    assert 'DeltaCatalog' in configs['spark.sql.catalog.spark_catalog']


def test_iceberg_configs_usa_catalogo_hadoop_local():
    configs = iceberg_configs(Path('/tmp/warehouse'))

    assert configs['spark.jars.packages'] == ICEBERG_PACKAGE
    assert configs['spark.sql.catalog.local.type'] == 'hadoop'
    assert configs['spark.sql.catalog.local.warehouse'] == '/tmp/warehouse'
