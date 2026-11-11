"""
Verificador do Projeto 1. NÃO precisa editar este arquivo.

Rode:  python verificar.py
Ele confere o arquivo saida/notas_limpas.csv gerado pelo seu limpeza.py.
"""
import csv
import re
from pathlib import Path

ESPERADO = {
    "linhas": 310,
    "soma_valor_total": 3924451.44,
    "soma_autorizadas": 3626722.10,
    "canceladas": 26,
}
COLUNAS = ["numero_nf", "data_emissao", "cnpj_emitente", "razao_social",
           "uf", "valor_total", "valor_icms", "situacao"]

arquivo = Path(__file__).parent / "saida" / "notas_limpas.csv"
ok = 0
falhas = 0


def checar(nome, condicao, dica):
    global ok, falhas
    if condicao:
        ok += 1
        print(f"  [OK]    {nome}")
    else:
        falhas += 1
        print(f"  [FALHA] {nome}\n          dica: {dica}")


print(f"\nVerificando {arquivo}\n")
if not arquivo.exists():
    print("  [FALHA] arquivo não encontrado. Rode primeiro: python limpeza.py")
    raise SystemExit(1)

with open(arquivo, encoding="utf-8") as f:
    leitor = csv.DictReader(f)
    colunas = leitor.fieldnames or []
    linhas = list(leitor)

checar("colunas na ordem certa", colunas == COLUNAS,
       f"esperado {COLUNAS}, encontrado {colunas}. O separador da saída deve ser vírgula.")
checar(f"quantidade de linhas = {ESPERADO['linhas']}", len(linhas) == ESPERADO["linhas"],
       f"encontrei {len(linhas)}. Removeu linhas vazias, duplicadas e sem valor_total?")

nfs = [l.get("numero_nf", "") for l in linhas]
checar("sem notas duplicadas", len(nfs) == len(set(nfs)), "use drop_duplicates(subset='numero_nf')")

checar("datas no formato AAAA-MM-DD",
       all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", l.get("data_emissao", "")) for l in linhas),
       "existem 3 formatos de data no arquivo bruto. Veja pd.to_datetime com format= e dayfirst=")

checar("CNPJ com 14 dígitos, só números",
       all(re.fullmatch(r"\d{14}", l.get("cnpj_emitente", "")) for l in linhas),
       "remova pontos, barra e traço, e complete zeros à esquerda (str.zfill(14)). Leia o CSV com dtype=str!")

checar("UF com 2 letras maiúsculas",
       all(re.fullmatch(r"[A-Z]{2}", l.get("uf", "")) for l in linhas),
       "str.strip() e str.upper()")

checar("razão social sem espaços sobrando e em maiúsculas",
       all(l.get("razao_social", "") == l.get("razao_social", "").strip().upper() for l in linhas),
       "str.strip() e str.upper()")

checar("situação só 'autorizada' ou 'cancelada'",
       all(l.get("situacao") in ("autorizada", "cancelada") for l in linhas),
       "str.strip() e str.lower()")


def numero(txt):
    try:
        return float(txt)
    except (TypeError, ValueError):
        return None


valores = [numero(l.get("valor_total")) for l in linhas]
icms = [numero(l.get("valor_icms")) for l in linhas]
checar("valores numéricos com ponto decimal (ex.: 1234.56)",
       all(v is not None for v in valores + icms),
       "tire 'R$ ', remova o ponto de milhar e troque a vírgula por ponto, nessa ordem. Cuidado com valores que já vêm como 1234.56")

if all(v is not None for v in valores):
    soma = round(sum(valores), 2)
    checar(f"soma de valor_total = {ESPERADO['soma_valor_total']:,.2f}",
           abs(soma - ESPERADO["soma_valor_total"]) < 0.01,
           f"sua soma deu {soma:,.2f}. Algum formato de valor está sendo convertido errado?")
    aut = round(sum(v for v, l in zip(valores, linhas) if l.get("situacao") == "autorizada"), 2)
    checar(f"soma das autorizadas = {ESPERADO['soma_autorizadas']:,.2f}",
           abs(aut - ESPERADO["soma_autorizadas"]) < 0.01, f"sua soma deu {aut:,.2f}")

canc = sum(1 for l in linhas if l.get("situacao") == "cancelada")
checar(f"{ESPERADO['canceladas']} notas canceladas", canc == ESPERADO["canceladas"], f"encontrei {canc}")

relatorio = Path(__file__).parent / "saida" / "relatorio.txt"
checar("relatório gerado em saida/relatorio.txt", relatorio.exists(), "veja a Missão 6 do README")

print(f"\nResultado: {ok} de {ok + falhas} verificações passaram.")
if falhas == 0:
    print("Projeto 1 concluído! Faça o commit e marque o item na sua trilha.\n")
