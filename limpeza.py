"""
Projeto 1: limpeza de notas fiscais.

Lê dados/notas_fiscais_brutas.csv, limpa e grava:
  - saida/notas_limpas.csv
  - saida/relatorio.txt

Siga as missões do README.md. Cada função abaixo é uma missão.
Rode com:  python limpeza.py
Confira com:  python verificar.py
"""
from pathlib import Path

import pandas as pd

PASTA = Path(__file__).parent
ENTRADA = PASTA / "dados" / "notas_fiscais_brutas.csv"
SAIDA = PASTA / "saida"


def ler_dados() -> pd.DataFrame:
    """Missão 2: ler o CSV bruto.
     Dicas:
    - o separador é ponto e vírgula (sep=";")
    - leia TUDO como texto (dtype=str), senão o pandas come os zeros
      à esquerda do CNPJ, exatamente como o Excel faz.
    """

    df = pd.read_csv(ENTRADA, sep=";", dtype=str)
    return df

 


def remover_lixo(df: pd.DataFrame) -> pd.DataFrame:
    """Missão 3: remover linhas vazias e notas duplicadas.

    Dicas: df.dropna(how="all") e df.drop_duplicates(subset="numero_nf")
    Pense em SQL: é um SELECT DISTINCT com WHERE numero_nf IS NOT NULL.
    """
    
    df = df.dropna(how="all")
    df = df.drop_duplicates(subset="numero_nf")
    
    return df



def padronizar_textos(df: pd.DataFrame) -> pd.DataFrame:
    """Missão 4: padronizar razao_social, uf, situacao e cnpj_emitente.

    Dicas:
    - df["uf"] = df["uf"].str.strip().str.upper()   (equivale a UPPER(TRIM(uf)))
    - situacao em minúsculas
    - CNPJ: remover tudo que não é dígito com .str.replace(r"\\D", "", regex=True)
      e depois .str.zfill(14)
    """
    # TODO
    return df


def converter_valor(texto):
    """Missão 5a: converter UM valor em texto para número (float).

    Formatos que aparecem no arquivo:
        "R$ 1.234,56"   "1.234,56"   "1234.56"   "" (vazio)
    Retorne None quando estiver vazio.

    Teste no terminal antes de seguir:
        python -c "from limpeza import converter_valor as c; print(c('R$ 1.234,56'), c('1234.56'))"
    """
    # TODO
    return texto


def converter_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """Missão 5b: converter valores e datas.

    - valor_total e valor_icms: use df["valor_total"].apply(converter_valor)
    - depois remova as linhas sem valor_total
    - data_emissao tem 3 formatos (AAAA-MM-DD, DD/MM/AAAA, DD-MM-AAAA).
      Uma saída: converter cada formato separadamente com
      pd.to_datetime(..., format="%d/%m/%Y", errors="coerce") e combinar com .fillna()
      No final, deixe como texto AAAA-MM-DD: .dt.strftime("%Y-%m-%d")
    """
    # TODO
    return df


def gerar_relatorio(df: pd.DataFrame) -> str:
    """Missão 6: montar um texto com:
    - quantidade de notas e valor total
    - valor total por UF (groupby, igual ao GROUP BY do SQL)
    - quantidade de canceladas
    - top 5 emitentes por valor, só notas autorizadas
    """
    # TODO
    return "Relatório ainda não implementado\n"


def main():
    df = ler_dados()
    print(f"Linhas lidas: {len(df)}")

    df = remover_lixo(df)
    df = padronizar_textos(df)
    df = converter_tipos(df)
    print(f"Linhas após limpeza: {len(df)}")

    SAIDA.mkdir(exist_ok=True)
    df.to_csv(SAIDA / "notas_limpas.csv", index=False, encoding="utf-8")
    (SAIDA / "relatorio.txt").write_text(gerar_relatorio(df), encoding="utf-8")
    print("Arquivos gravados em saida/")


if __name__ == "__main__":
    main()
