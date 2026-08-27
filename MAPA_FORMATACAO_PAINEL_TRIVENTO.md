# Mapa de formatacao do Painel Trivento

## Escopo

Este documento registra o padrao de cores e tipografia identificado no
relatorio Power BI `PAINEL TRIVENTO`.

O modelo possui a medida `Teste cor`, que retorna uma cor conforme a unidade
selecionada.

## Paleta por unidade

| Unidade | Cor | HEX |
| --- | --- | --- |
| Altamira | Verde escuro | `#004E37` |
| Lorena | Dourado | `#D5A62F` |
| Itabirito | Azul | `#1575BB` |
| Trivento, outros ou valor nao mapeado | Rosa | `#FF0078` |

### Regra dinamica existente

```DAX
SWITCH(
    SELECTEDVALUE('INI - Matriculados'[UNIDADE]),
    "Altamira", "#004E37",
    "Lorena", "#D5A62F",
    "Itabirito", "#1575BB",
    "#FF0078"
)
```

## Aplicacao por elemento

### Filtros

- Fundo: branco.
- Borda ou cabecalho: cor da unidade selecionada.
- Estado ativo: cor da unidade com maior contraste.
- Texto: cinza-escuro ou branco, conforme o contraste do fundo.
- Valores vazios: tratar como `Nao informado`, sem criar uma nova cor.

### Graficos

- Serie principal: cor da unidade selecionada.
- Comparacoes: variacoes de luminosidade da mesma cor.
- Metas: usar uma cor neutra ou secundaria, sem substituir a cor da unidade.
- Variacoes positivas e negativas: verde e vermelho sem alterar a identidade
  visual da unidade.
- Legenda: manter a mesma ordem das series e evitar cores sem significado.

### Tabelas

- Cabecalho: cor da unidade.
- Texto do cabecalho: branco quando houver contraste suficiente.
- Linhas: fundo branco com linhas alternadas em um tom claro da cor da unidade.
- Totais: peso semibold e destaque pela cor da unidade.
- Dados: texto em cinza-escuro para preservar a leitura.

### Indicadores e KPIs

- Numero principal: cor da unidade.
- Rotulo: cinza-escuro.
- Meta: cor neutra ou secundaria.
- Status: verde/vermelho somente para indicar resultado, alerta ou variacao.

## Hierarquia tipografica

| Elemento | Fonte | Tamanho | Peso |
| --- | --- | --- | --- |
| Titulo | Segoe UI | 20-24 px | Semibold ou bold |
| Subtitulo | Segoe UI | 14-16 px | Regular ou semibold |
| Legenda de grafico | Segoe UI | 10-12 px | Regular |
| Rotulo de dados | Segoe UI | 10-11 px | Regular |
| Cabecalho de tabela | Segoe UI | 11-12 px | Semibold |
| Dados da tabela | Segoe UI | 10-11 px | Regular |
| Rotulo de KPI | Segoe UI | 10-12 px | Regular |
| Valor de KPI | Segoe UI | 24-32 px | Semibold ou bold |

## Regras de consistencia

1. Usar uma unica familia tipografica em todos os visuais.
2. Reservar o maior tamanho para titulos e valores de KPI.
3. Nao usar a cor de uma unidade para representar outra unidade.
4. Manter contraste suficiente entre texto e fundo.
5. Usar a mesma cor quando a unidade aparecer em filtros, graficos e tabelas.
6. Nao criar uma cor adicional para registros vazios ou nao classificados.

## Observacao tecnica

A medida `Teste cor` referencia `INI - Matriculados[UNIDADE]`. Os dados do
modelo tambem possuem tabelas auxiliares de unidade em diferentes processos.
Para que a cor seja consistente em todos os visuais, os filtros e visuais
devem usar uma dimensao de unidade comum ou uma tabela com relacionamento
consistente.

## Medidas relacionadas

A tabela `Medidas Painel Trivento` contem medidas de matriculados, captacao,
evasao e rematricula, incluindo medidas especificas por unidade:

- `Evasao Captacao - Altamira`
- `Evasao Captacao - Itabirito`
- `Evasao Captacao - Lorena`
- `REA Captacao Bruta - Altamira`
- `REA Captacao Bruta - Itabirito`
- `REA Captacao Bruta - Lorena`
