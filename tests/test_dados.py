import csv
from pathlib import Path

CSV = Path(__file__).parent.parent / 'data' / 'carros.csv'
COLUNAS = ['placa', 'modelo', 'chassi', 'marca', 'ano', 'cor']


def ler_carros() -> list[dict[str, str]]:
    with CSV.open(encoding='utf-8') as arquivo:
        return list(csv.DictReader(arquivo))


def test_csv_tem_as_colunas_esperadas():
    with CSV.open(encoding='utf-8') as arquivo:
        assert next(csv.reader(arquivo)) == COLUNAS


def test_csv_tem_8_carros():
    assert len(ler_carros()) == 8


def test_placas_sao_unicas():
    placas = [carro['placa'] for carro in ler_carros()]

    assert len(placas) == len(set(placas))
