# Apache Spark com Delta Lake e Apache Iceberg

## Descrição

Ambiente **PySpark + JupyterLab** que demonstra `INSERT`, `UPDATE` e `DELETE` em tabelas **Delta Lake** e **Apache Iceberg**, a partir de um dataset de carros (`data/carros.csv`).

Trabalho de Engenharia de Dados (UNISATC), Prof. Jorge Luiz da Silva.

**Integrantes:** Raffael Michels Arcego · Isabelle Luiz Feltrin

📖 **Documentação completa:** https://raffaelarcego.github.io/trabalho-apachespark-eng_dados/

## Disclaimer

- O Spark 3.5 exige **Java 17**. Versões 21 ou superiores não funcionam.
- Na primeira execução, o Spark baixa os JARs do Delta e do Iceberg pela internet.
- Os comandos são executados no **terminal do Ubuntu (WSL)**, e não no PowerShell.

## Pré-requisitos

- Windows 11 com **WSL 2 (Ubuntu)**
- **Java 17**
- **[uv](https://docs.astral.sh/uv/)** (gerenciador de pacotes; ele também instala o Python 3.11)

| Biblioteca                         | Versão                         |
| ---------------------------------- | ------------------------------ |
| pyspark                            | 3.5.x                          |
| delta-spark                        | 3.3.2                          |
| iceberg-spark-runtime-3.5_2.12     | 1.9.2                          |
| jupyterlab                         | 4.x                            |
| mkdocs-material                    | 9.x                            |
| pytest, ruff, blue, isort, taskipy | ferramentas de desenvolvimento |

## Instalação

```bash
# 1. Java 17
sudo apt update && sudo apt install -y openjdk-17-jdk-headless

# 2. uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# 3. Projeto
cd ~
git clone https://github.com/raffaelarcego/trabalho-apachespark-eng_dados.git
cd trabalho-apachespark-eng_dados
uv sync
```

## Howto

```bash
uv run jupyter lab
```

Abra o link `http://127.0.0.1:8888/...` que aparece no terminal e rode cada notebook com **Run All**:

- `notebooks/01_delta_lake.ipynb`
- `notebooks/02_apache_iceberg.ipynb`

Cada notebook cria a tabela `carros` e executa `INSERT`, `UPDATE`, `DELETE` e _time travel_.

> Para usar o VS Code em vez do JupyterLab: rode `code .` no Ubuntu e escolha o kernel `.venv`.

## Testes

```bash
uv run task test    # pytest com cobertura
uv run task lint    # ruff, blue e isort
uv run task format  # corrige a formatação
```

## Documentação

Site publicado: https://raffaelarcego.github.io/trabalho-apachespark-eng_dados/

```bash
uv run mkdocs serve       # visualizar localmente em http://127.0.0.1:8000
uv run mkdocs gh-deploy   # publicar no GitHub Pages
```

## Estrutura

```
├── trabalho_apachespark_eng_dados/   # pacote Python (SparkSession Delta e Iceberg)
├── tests/                            # testes com pytest
├── notebooks/                        # Delta Lake e Apache Iceberg
├── data/carros.csv                   # dataset (8 carros)
├── docs/                             # páginas do MkDocs
├── mkdocs.yml
└── pyproject.toml                    # dependências e tarefas (uv + taskipy)
```

## Problemas comuns

<details>
<summary><b>Sem internet no Ubuntu (WSL)</b>: <code>apt</code> ou <code>uv sync</code> falham com <i>Network is unreachable</i></summary>

Crie o arquivo `C:\Users\<seu-usuario>\.wslconfig` no Windows com:

```ini
[wsl2]
networkingMode=mirrored
dnsTunneling=true
autoProxy=true
```

Depois, no PowerShell, rode `wsl --shutdown`, abra o Ubuntu de novo e teste com `curl -I https://pypi.org`.

</details>

<details>
<summary><b><code>JAVA_GATEWAY_EXITED</code></b> ou <b><code>JAVA_HOME is not set</code></b></summary>

O Java não está instalado ou a versão está errada:

```bash
java -version                              # deve mostrar 17
sudo update-alternatives --config java     # se houver mais de uma versão, escolha a 17
```

</details>

## Referências

- Canal [DataWay BR](https://www.youtube.com/@DataWayBR)
- [jlsilva01/spark-delta](https://github.com/jlsilva01/spark-delta) e [jlsilva01/spark-iceberg](https://github.com/jlsilva01/spark-iceberg)
- [Delta Lake](https://docs.delta.io/) · [Apache Iceberg](https://iceberg.apache.org/docs/latest/) · [Apache Spark](https://spark.apache.org/docs/3.5.3/)

## Uso de IA

O Claude (Anthropic) foi usado como apoio para revisar código e documentação e resolver problemas de ambiente. O grupo executou, conferiu e revisou tudo.
