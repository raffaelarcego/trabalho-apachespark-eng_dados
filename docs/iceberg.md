# Apache Iceberg

## O que é

O **Apache Iceberg** é um formato de tabela aberto criado pela **Netflix** (2017) e doado à Apache. Ele grava os dados em **Parquet** e organiza os metadados em camadas. Cada alteração gera um novo **snapshot**, ou seja, uma "foto" completa da tabela.

```
carros/
├── data/                         ← arquivos Parquet
└── metadata/
    ├── v1.metadata.json          ← schema, snapshots, versão atual
    ├── snap-....avro             ← manifest list (um por snapshot)
    └── ....avro                  ← manifests (lista de arquivos de dados)
```

Notebook: `notebooks/02_apache_iceberg.ipynb`

## Configuração

Usamos um **catálogo local do tipo `hadoop`** chamado `local`, que grava tudo em pastas, sem precisar de servidor:

```python
spark = (
    SparkSession.builder.appName("apache-iceberg")
    .master("local[*]")
    .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.9.2")
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.local.type", "hadoop")
    .config("spark.sql.catalog.local.warehouse", ".../warehouse/iceberg")
    .getOrCreate()
)
```

As tabelas são referenciadas como `catalogo.namespace.tabela`, por exemplo `local.seguradora.carros`.

## DDL

```sql
CREATE NAMESPACE IF NOT EXISTS local.seguradora;

CREATE TABLE local.seguradora.carros (
    placa STRING, modelo STRING, chassi STRING,
    marca STRING, ano INT, cor STRING
)
USING iceberg;

INSERT INTO local.seguradora.carros SELECT * FROM carros_csv;  -- carga inicial
```

## INSERT

```sql
INSERT INTO local.seguradora.carros
VALUES ('KLM2468', 'ONIX', '11223344556', 'GM', 2023, 'PRATA');
```

Gera um novo snapshot (`append`) apontando para o novo arquivo Parquet.

## UPDATE

```sql
UPDATE local.seguradora.carros SET cor = 'VERMELHO' WHERE placa = 'EEE1056';
```

Pela estratégia padrão (*copy-on-write*), o Iceberg reescreve o arquivo afetado e cria um snapshot `overwrite`.

## DELETE

```sql
DELETE FROM local.seguradora.carros WHERE ano < 2015;
```

Remove o CLIO e o PUNTO e cria mais um snapshot. Os snapshots anteriores continuam disponíveis.

## Snapshots e time travel

```sql
SELECT snapshot_id, committed_at, operation
FROM local.seguradora.carros.snapshots;
```

| operation | origem |
|---|---|
| append | carga inicial |
| append | INSERT |
| overwrite | UPDATE |
| overwrite / delete | DELETE |

```sql
SELECT * FROM local.seguradora.carros VERSION AS OF <snapshot_id>;
```

## Delta Lake x Iceberg

| | Delta Lake | Apache Iceberg |
|---|---|---|
| Criado por | Databricks | Netflix |
| Dados | Parquet | Parquet (também ORC e Avro) |
| Metadados | `_delta_log` (JSON) | `metadata/` (JSON + Avro) |
| Versões | número sequencial (0, 1, 2...) | `snapshot_id` |
| Time travel | `VERSION AS OF 1` | `VERSION AS OF <snapshot_id>` |
| Catálogo | catálogo do Spark | catálogo próprio (hadoop, hive, REST...) |
| `INSERT` / `UPDATE` / `DELETE` | ✅ | ✅ |
