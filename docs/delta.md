# Delta Lake

## O que é

O **Delta Lake** é um formato de tabela aberto criado pela **Databricks** (2019). Ele grava os dados em **Parquet** e registra cada alteração em um **log de transações** (`_delta_log`). É esse log que garante ACID, histórico e *time travel*.

```
carros/
├── part-00000-....snappy.parquet      ← dados
└── _delta_log/
    ├── 00000000000000000000.json      ← versão 0 (CREATE TABLE)
    ├── 00000000000000000001.json      ← versão 1 (carga)
    └── ...
```

Notebook: `notebooks/01_delta_lake.ipynb`

## Configuração

```python
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

builder = (
    SparkSession.builder.appName("delta-lake")
    .master("local[*]")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)
spark = configure_spark_with_delta_pip(builder).getOrCreate()
```

## DDL

```sql
CREATE TABLE carros (
    placa STRING, modelo STRING, chassi STRING,
    marca STRING, ano INT, cor STRING
)
USING delta
LOCATION '.../warehouse/delta/carros';

INSERT INTO carros SELECT * FROM carros_csv;  -- carga inicial (8 carros)
```

## INSERT

```sql
INSERT INTO carros VALUES ('KLM2468', 'ONIX', '11223344556', 'GM', 2023, 'PRATA');
```

O Delta grava um **novo arquivo Parquet** só com a linha nova e registra a versão 2 no log.

## UPDATE

```sql
UPDATE carros SET cor = 'VERMELHO' WHERE placa = 'EEE1056';
```

Parquet não pode ser editado. O Delta então **reescreve o arquivo** que contém a linha alterada e marca o arquivo antigo como removido no log (versão 3).

## DELETE

```sql
DELETE FROM carros WHERE ano < 2015;
```

Remove o CLIO (2011) e o PUNTO (2013) da mesma forma: reescreve os arquivos afetados (versão 4). Os arquivos antigos continuam no disco, e é isso que permite o *time travel*.

## Histórico e time travel

```sql
DESCRIBE HISTORY carros;
```

| version | operation |
|---|---|
| 0 | CREATE TABLE |
| 1 | WRITE (carga inicial) |
| 2 | WRITE (INSERT) |
| 3 | UPDATE |
| 4 | DELETE |

```sql
SELECT * FROM carros VERSION AS OF 1;  -- tabela original, com 8 carros
```
