# Limpeza de Notas Fiscais com Python

Pipeline em Python que recebe um export de notas fiscais com dados inconsistentes, padroniza e valida as informações e gera um relatório de negócio.

## O problema
Recebi um CSV de notas fiscais com 341 linhas e dados sem padrão: datas em 3 formatos diferentes, CNPJs com e sem máscara (alguns sem os zeros à esquerda), valores com “R$”, vírgula ou ponto, além de linhas vazias e notas duplicadas. Do jeito que veio, não era possível somar valores nem agrupar por estado. A ideia foi carregar, limpar e padronizar esses dados para deixá-los prontos para análise.

## O que o pipeline faz

O CSV bruto contem 341 linhas → apos carregar ele remove vazias e duplicadas → padroniza textos e CNPJ → converte valores e datas → CSV limpo fica com 310 linhas + relatório

| Etapa | Função | O que resolve |
|---|---|---|
| Leitura | `ler_dados` | Lê tudo como texto para preservar zeros à esquerda do CNPJ |
| Limpeza | `remover_lixo` | Remove 6 linhas vazias e 15 notas duplicadas |
| Padronização | `padronizar_textos` | UF, razão social e situação padronizadas; CNPJ com 14 dígitos |
| Conversão | `converter_tipos` | Valores em 3 formatos viram número; datas em 3 formatos viram AAAA-MM-DD |
| Relatório | `gerar_relatorio` | Totais, valor por UF, canceladas e top 5 emitentes |

## Decisões técnicas
**Ler o CSV com `dtype=str`:** se o pandas lesse o CNPJ como número, ele apagaria os zeros à esquerda (`00071271000138` viraria `71271000138`), o mesmo problema que acontece no Excel. Lendo tudo como texto, nenhum dado se perde na leitura e a conversão de tipos é feita depois, de forma controlada.

 **Conversão de valores:** os valores chegavam em formatos diferentes (`R$ 1.234,56`, `1.234,56` e `1234.56`). A pista para identificar o formato brasileiro é a vírgula: quando ela existe, primeiro removo os pontos de milhar e depois troco a vírgula por ponto, chegando ao formato que o Python entende.



## Resultado

- 341 linhas brutas → **310 notas válidas**
- 13 verificações automáticas de qualidade passando (`verificar.py`), incluindo somas conferidas até o centavo
- Relatório com valor total de **R$ 3.924.451,44**, distribuído em 8 UFs

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python limpeza.py
python verificar.py
```

Os resultados ficam em `saida/notas_limpas.csv` e `saida/relatorio.txt`.

## Tecnologias

Python 3.11 · pandas · Git

## O que aprendi

**Pandas é SQL com outra sintaxe:** filtros viraram `WHERE`, `groupby` virou `GROUP BY` e `fillna` funcionou como `COALESCE` para unificar 3 formatos de data. Partir do que eu já sabia em SQL acelerou muito o aprendizado.
- **Explorar antes de limpar:** com `info()` e `value_counts()` descobri problemas que não estavam visíveis, como 32 escritas diferentes para 8 UFs e CNPJs com 5 tamanhos diferentes.
- **Validar com números, não com a aparência:** um resultado que "parecia certo" no `print` ainda era texto, não número. O verificador comparando as somas até o centavo foi o que garantiu que a conversão estava correta.