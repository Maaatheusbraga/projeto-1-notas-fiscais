# Projeto 1: Limpeza de notas fiscais

Um cliente mandou um export de notas fiscais **todo bagunçado**: três formatos de data, CNPJ com e sem máscara (e alguns sem o zero à esquerda), valores com `R$`, vírgula ou ponto, UF minúscula, linhas vazias e notas duplicadas.

Seu trabalho é transformar isso num arquivo limpo e num relatório. É o mesmo problema do seu trabalho, agora resolvido em Python.

## Estrutura

```
projeto-1-notas-fiscais/
├── dados/notas_fiscais_brutas.csv   ← entrada (341 linhas, separador ;)
├── limpeza.py                       ← você escreve aqui
├── verificar.py                     ← confere seu resultado (não edite)
└── saida/                           ← criada pelo script
```

## Como trabalhar

1. Faça **uma missão por vez**.
2. Depois de cada missão, rode `python limpeza.py` e `python verificar.py`.
3. Cada `[FALHA]` traz uma dica. Tente sozinho por pelo menos 20 minutos antes de pesquisar.
4. Missão concluída → `git commit`.

---

## Missão 0: Preparar o ambiente

No terminal do VS Code, dentro desta pasta:

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install pandas
```

```bash
pip freeze > requirements.txt
```

**Para entender:** o que é um ambiente virtual e por que cada projeto tem o seu?

## Missão 1: Versionar desde o início

```bash
git init
```

Crie um arquivo `.gitignore` com as linhas `.venv/` e `saida/`. Depois:

```bash
git add .
```

```bash
git commit -m "Projeto 1: estrutura inicial"
```

Crie um repositório no GitHub chamado `projeto-1-notas-fiscais` e faça o push (o GitHub mostra os comandos).

## Missão 2: Ler os dados

A função `ler_dados()` já está pronta. Rode `python limpeza.py`, depois abra o terminal Python (`python`) e explore:

```python
import pandas as pd
df = pd.read_csv("dados/notas_fiscais_brutas.csv", sep=";", dtype=str)
df.head(10)
df.info()
df["uf"].value_counts()
df["situacao"].value_counts()
```

**Anote no diário:** quais problemas você encontrou em cada coluna?

## Missão 3: Remover linhas vazias e duplicadas

Implemente `remover_lixo()`. Ponte com o SQL: é um `SELECT DISTINCT` com `WHERE numero_nf IS NOT NULL`.

## Missão 4: Padronizar textos

Implemente `padronizar_textos()`. `TRIM`, `UPPER` e `LOWER` existem no pandas como `.str.strip()`, `.str.upper()` e `.str.lower()`.

## Missão 5: Converter valores e datas

Esta é a missão mais difícil.

- **5a.** Implemente `converter_valor()` para **um** valor e teste no terminal antes de aplicar na tabela.
- **5b.** Implemente `converter_tipos()`.

Cuidado: `"1234.56"` e `"1.234,56"` exigem tratamentos diferentes. Como saber qual é qual?

## Missão 6: Relatório

Implemente `gerar_relatorio()`. Use `groupby`, que é o `GROUP BY` do pandas. Ponto extra: grave também o relatório em CSV.

## Missão 7: Fechamento

- [ ] `python verificar.py` com todas as verificações OK
- [ ] README do seu repositório explicando: problema, como rodar, decisões que você tomou
- [ ] Commit final e push
- [ ] Gravar 2 minutos explicando o projeto (só para você ouvir)
- [ ] Marcar "Projeto 1" na trilha

## Desafio extra (depois de terminar)

- Validar o dígito verificador do CNPJ e separar as linhas inválidas num arquivo `saida/rejeitadas.csv`.
- Refazer o projeto do zero, **sem olhar o seu código**, em menos de 1 hora.
