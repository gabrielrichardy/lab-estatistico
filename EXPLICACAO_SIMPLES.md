# Explicação simples do projeto (pra explicar pra qualquer pessoa)

Uma versão "sem código e sem fórmulas" do Laboratório Estatístico — como contar pra quem
não é da área (e pro dia da gravação do vídeo).

---

## As 3 palavras que você precisa saber

- **Estatística** = a arte de resumir um milhão de números usando poucos números que importam.
- **Dado** = a informação de uma pessoa. Uma linha da planilha = uma pessoa.
- **Programa** = uma *receita* passo a passo que o computador segue.

## A ideia (contada simples)

É um **microscópio de números**: você coloca dados dentro e ele responde perguntas
("qual é o valor típico?", "os valores são parecidos ou muito diferentes?", "dado a altura,
dá pra chutar o peso?").

Os dados são de **13.393 pessoas** que fizeram avaliação física (altura, peso, gordura,
pressão, abdominais, salto...). É um "enquete gigante da educação física".

A parte legal (e que o professor pede): normalmente um app usa calculadora pronta de
estatística. Aqui **a calculadora foi construída do zero** — como aprender a fazer pão em vez
de comprar pronto. No final, a gente compara nosso pão com o da padaria famosa (NumPy) e
mostra que ficou igual.

---

## O núcleo: as "medidas" (Módulo 1)

Imagina a fila de 13.393 pessoas ordenadas por altura:

- **Média** — somar tudo e dividir. É o "equilíbrio" da fila.
- **Mediana** — a pessoa do meio da fila. Um gigante puxa a média, mas quase não mexe na mediana.
- **Moda** — o valor que mais se repete.
- **Amplitude** — do mais baixo ao mais alto.
- **Desvio padrão / Variância** — o quanto a fila está espalhada ou concentrada.
- **Quartis** — cortar a fila em 4 partes: Q1 (25%), Q2 (mediana), Q3 (75%).
- **Outlier** — gente fora do padrão; a regra do IQR diz quem é.
- **Correlação de Pearson** — "essas duas coisas andam juntas?" (perto de 1 = juntas,
  perto de 0 = sem relação).

## Módulo 2 — Descritiva: "contar o que tem"

Descreve os dados com números E desenhos: tabela de frequências (agrupa em faixas, com a
regra de Sturges), histograma (retrato da distribuição), boxplot (onde está o meio e quem
é outlier) e interpretação automática escrita em português.

## Módulo 3 — Simulação: "experimentos que cabem no computador"

- **Lei dos Grandes Números**: jogue uma moeda 10x e podem sair 7 caras (70%!). Jogue
  100.000x e a proporção se aproxima de 50%. Probabilidade só "funciona" com MUITOS
  experimentos — o app desenha essa convergência.
- **Teorema Central do Limite**: pegue grupos de pessoas e tire a média de cada grupo.
  Essas médias formam uma **curva de sino** (Normal) mesmo que os dados originais sejam
  estranhos, e o desvio dela obedece **σ/√n** (quanto maior o grupo, mais fininha a curva).

## Módulo 4 — Distribuições teóricas: "achar o molde certo"

Coloca-se uma curva teórica (Normal, Exponencial...) por cima do histograma para ver qual
"molde" mais parece. Os parâmetros (média, desvio) são **estimados dos próprios dados**.

## Módulo 5 — Regressão: "a régua que adivinha"

Dispersão (cada pessoa é um pontinho) + reta de regressão que melhor passa no meio dos
pontos (**mínimos quadrados**). O **R²** diz quanto a reta explica (0,54 = altura explica
54% do peso). Campo de predição: digita X → o app prevê Ŷ. E o aviso de ouro:
correlação ≠ causalidade.

---

## Como o projeto é montado (2 frases)

A cozinha tem dois cômodos separados: a **cozinha da matemática** (`nucleo`) onde as contas
são feitas pela receita da gente, e o **salão** (`app`) que é a parte bonita onde você clica
nos botões — ele só pede as contas pra cozinha, não calcula nada. E tem o **controle de
qualidade** (`testes`): 44 testes comparando nossa conta com o NumPy até a 10ª casa decimal.

## O resumo de 1 frase

> "É um laboratório online de estatística: eu construí as fórmulas do zero, validei contra
> as bibliotecas famosas, e criei uma interface onde você analisa dados reais de desempenho
> físico — com gráficos, simulações e até uma reta que prevê coisas."