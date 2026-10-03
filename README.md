# Apache Spark com Delta Lake e Apache Iceberg

Ambiente **PySpark + JupyterLab** que demonstra `INSERT`, `UPDATE` e `DELETE` em tabelas **Delta Lake** e **Apache Iceberg**.

Trabalho de Engenharia de Dados (UNISATC), Prof. Jorge Luiz da Silva.

📖 **Documentação:** https://raffaelarcego.github.io/trabalho-apachespark-eng_dados/

**Integrantes:** Raffael · _Integrante 2_ · _Integrante 3_

## Pré-requisitos

- Windows 11 com **WSL 2 (Ubuntu)**
- **Java 17** (o Spark 3.5 não funciona com Java 21+)
- **[uv](https://docs.astral.sh/uv/)** (gerenciador de pacotes; ele também instala o Python 3.11)

| Biblioteca | Versão |
|---|---|
| pyspark | 3.5.x |
| delta-spark | 3.3.2 |
| iceberg-spark-runtime-3.5_2.12 | 1.9.2 |
| jupyterlab | 4.x |
| mkdocs-material | 9.x |

## Instalação

Todos os comandos são executados no **terminal do Ubuntu (WSL)**.

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

## Como executar

```bash
uv run jupyter lab
```

Abra o link `http://127.0.0.1:8888/...` que aparece no terminal e rode cada notebook com **Run All**:

- `notebooks/01_delta_lake.ipynb`
- `notebooks/02_apache_iceberg.ipynb`

> Para usar o VS Code em vez do JupyterLab: rode `code .` no Ubuntu e escolha o kernel `.venv`.
>
> Na primeira execução, o Spark baixa os JARs do Delta e do Iceberg pela internet.

## Documentação (MkDocs)

```bash
uv run mkdocs serve       # visualizar localmente em http://127.0.0.1:8000
uv run mkdocs gh-deploy   # publicar no GitHub Pages
```

## Problemas comuns

<details>
<summary><b>Sem internet no Ubuntu (WSL)</b>: <code>apt</code> ou <code>uv sync</code> falham com <i>Network is unreachable</i> ou <i>connection timed out</i></summary>

O modo de rede padrão do WSL (NAT) às vezes fica bloqueado. Para resolver, crie o arquivo `C:\Users\<seu-usuario>\.wslconfig` no Windows com:

```ini
[wsl2]
networkingMode=mirrored
dnsTunneling=true
autoProxy=true
```

Depois, no PowerShell, rode `wsl --shutdown`, abra o Ubuntu de novo e teste com:

```bash
curl -I https://pypi.org
```

</details>

<details>
<summary><b><code>JAVA_GATEWAY_EXITED</code></b> ao criar a SparkSession</summary>

O Java não está instalado ou a versão está errada. O Spark 3.5 precisa do **Java 17**:

```bash
java -version                              # deve mostrar 17
sudo update-alternatives --config java     # se houver mais de uma versão, escolha a 17
```

</details>

## Estrutura

```
├── data/carros.csv     # dataset (8 carros)
├── notebooks/          # Delta Lake e Apache Iceberg
├── docs/               # páginas do MkDocs
├── mkdocs.yml
└── pyproject.toml      # dependências (uv)
```
