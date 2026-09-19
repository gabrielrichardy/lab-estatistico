# Roteiro do vídeo — Laboratório Estatístico Interativo (3–5 min)

**Formato:** tela + narração (pode gravar com OBS ou a gravação de tela de qualquer ferramenta).
**Objetivo do professor:** demonstrar a aplicação **em funcionamento** e explicar **um trecho do
código** do núcleo estatístico.

> Dica geral: fale pausado. Toda frase com número a seguir foi gerada pela biblioteca própria e
> confere com o NumPy. Se travar em algo, respira e repete a ideia com suas palavras — o domínio
> aparece mais na naturalidade do que na decorebra.

---

## [0:00 – 0:35] Abertura — o dataset

>O que fazer na tela: mostrar o arquivo `bodyPerformance.csv` (ou o notebook de exploração).

**Narração:**

"Oi, esse aqui é o meu Laboratório Estatístico Interativo, da Sistematização de Matemática e
Estatística para Computação. O projeto carrega um dataset real e permite explorar estatística,
probabilidade e regressão — com a diferença de que o núcleo matemático foi implementado por mim,
sem usar funções prontas de estatística."

"Nós carregamos o Body Performance Data, do Kaggle: são 13 mil 393 avaliações de desempenho
físico — altura, peso, percentual de gordura, pressão, força de preensão, abdominais e salto.
São 10 variáveis numéricas e 2 categóricas, gênero e a classe de aptidão física, que vai de A até D.
O arquivo tem mais de mil registros, então atende o critério da atividade."

---

## [0:35 – 1:40] Módulo 2 — Estatística Descritiva

>O que fazer na tela: aba "2 — Estatística Descritiva", selecionar `height_cm`.

**Narração:**

"Aqui na aba de descritiva, eu escolho uma variável — vou de altura. O painel de medidas vem
todo da minha biblioteca própria, a `minhastats`. A média é 168 e 56 centésimos de centímetro, a
mediana 169 e 2. Repara que média e mediana quase se encontram: isso indica uma distribuição
aproximadamente simétrica, sem uma cauda puxando pra um lado."

"O desvio padrão amostral é 8,4 centímetros. E aqui o coeficiente de variação de 5 por cento.
O coeficiente de variação é o desvio dividido pela média, vezes 100 — ele é interessante porque
permite comparar variáveis de escalas diferentes. A altura tem CV de 5%, enquanto a idade tem
37% e os abdominais quase 36%: ou seja, essa amostra é muito mais parecida em estatura do que
em condicionamento físico."

"A tabela de frequências agrupa em classes. O número de classes vem da regra de Sturges:
k igual a logaritmo de base 2 de n, mais 1, arredondado pra cima. E o boxplot marca os outliers:
a regra do IQR diz que é outlier quem tiver valor abaixo de Q1 menos 1,5 vezes a amplitude inter
quartil, ou acima de Q3 mais 1,5 vezes o IQR. Aqui temos dez outliers na altura, todos acima do
limite de 193,4 centímetros."

---

## [1:40 – 2:50] Módulo 3 — Probabilidade e Simulação

>O que fazer na tela: aba "3 — Probabilidade e Simulação", experimento da Lei dos Grandes Números (10.000–100.000 lançamentos), depois TCL com `systolic`, n=30.

**Narração:**

"Aqui eu demonstro a Lei dos Grandes Números com uma simulação de Monte Carlo. Fiz 100 mil
lançamentos de um dado honesto e plotei a frequência relativa acumulada do 'sair 6'. A
probabilidade teórica é 1 sobre 6, aproximadamente 0,1667, que está desenhada em vermelho.
Depois de 100 mil lançamentos, a frequência observada ficou em 0,1664. O ponto importante é a
convergência: com poucos lançamentos o valor oscila bastante, e só no limite ele estabiliza na
probabilidade teórica."

"Agora o Teorema Central do Limite. Eu sortei 5 mil amostras de tamanho 30 da pressão sistólica
e calculei a média de cada amostra. A distribuição dessas médias amostrais se aproxima de uma
Normal, mesmo que a variável original não seja Normal. E olha como o teorema é preciso na
prática: a média das médias deu 130,19, contra 130,24 da população. E o desvio padrão dessas
médias, que se chama erro padrão, deu 2,72, contra o valor teórico sigma sobre raiz de 30, que é
2,69. Esse sigma sobre raiz de n é a assinatura do TCL: quanto maior a amostra, mais estreita
fica a distribuição das médias."

---

## [2:50 – 3:40] Módulo 4 — Distribuições Teóricas

>O que fazer na tela: aba "4 — Distribuições Teóricas", escolher `weight_kg`, com Normal + Exponencial.

**Narração:**

"No módulo de distribuições, eu sobreponho a curva teórica ao histograma em densidade. Para o
peso, a candidata Normal foi estimada com a média e o desvio dos próprios dados — 67,45 de média,
11,95 de desvio. A curva vermelha acompanha bem o pico das barras. A segunda candidata é a
Exponencial: aqui o parâmetro lambda é estimado como 1 dividido pela média dos dados, porque o
estimador de máxima verossimilhança da exponencial é exatamente o inverso da média amostral."

"A exponencial não acompanha tão bem: ela parte do zero com a densidade máxima e decai sempre,
mas a distribuição do peso sobe até o pico e só depois cai. Isso é uma inspeção visual do ajuste
— e essa comparação entre candidatas mostra por que a escolha da distribuição depende da forma
dos dados."

---

## [3:40 – 4:40] Módulo 5 — Regressão Linear + Código do núcleo (o ponto que o professor pede)

>O que fazer na tela: aba "5 — Correlação e Regressão", `height_cm × weight_kg`. Depois abrir
>`nucleo/minhastats.py` ou `nucleo/regressao.py` e mostrar o cálculo.

**Narração:**

"Por fim, a regressão linear. Eu escolho altura no eixo X e peso no eixo Y. O coeficiente de
Pearson deu 0,73, uma correlação forte e positiva. A reta foi ajustada pelo método dos mínimos
quadrados, implementado por mim." [**abre o código aqui**]

"Vou explicar o coração do código. O coeficiente angular beta é a covariância de x e y dividida
pela variância de x. E o intercepto, o alpha, é a média de y menos beta vezes a média de x — ou
seja, a reta passa pelo ponto médio do conjunto. Vocês podem conferir aqui no `regressao.py`.
Todas essas medidas internas, covariância e variância, vêm da minha biblioteca, e cada função tem
um teste comparando com o NumPy, com tolerância de 10 elevado a menos 10."

"De volta aos números: a equação fica peso igual a menos 108,22 mais 1,04 vezes a altura. A
interpretação é concreta: a cada centímetro a mais de altura, o peso aumenta em média 1,04
quilograma. O R quadrado é 0,54 — cerca de 54 por cento da variação do peso é explicada
linearmente pela altura. E aqui o campo de predição: eu digito a altura 175 e o modelo prevê o
peso. Mas atenção: correlação não implica causalidade. Altura explica parte do peso, mas não
'causa' peso — pessoas mais altas tendem a pesar mais em média, e ponto final."

---

## [4:40 – 5:00] Encerramento — o melhor achado

>O que fazer na tela: voltar pro Módulo 2 em `weight_kg` e `body fat_%` (ou mostrar a correlação
>peso × gordura na aba 5).

**Narração:**

"Pra fechar, o achado mais contraintuitivo do laboratório: o peso tem correlação praticamente
nula com o percentual de gordura — Pearson de menos 0,08. Enquanto isso, altura e peso dão 0,73,
e abdominais com salto, 0,75. Ou seja: neste dataset quem pesa mais não é necessariamente quem
tem mais gordura relativa — o que faz sentido, porque massa muscular também pesa. É um exemplo
de que os números, quando você constrói a estatística do zero, contam histórias que a intuição
não contava."

"Resumindo: núcleo estatístico próprio, validado contra o NumPy em 44 testes, interface
interativa com simulação e regressão — e três descobertas no relatório. Obrigado!"

---

## Checklist de domínio (repare o narrador)

- [ ] Fez o gesto de explicar "o que é CV e por que ele compara escalas"
- [ ] Falou "erro padrão = σ/√n" (assinatura do TCL) sem ler
- [ ] Explicou o estimador de máxima verossimilhança da exponencial (λ = 1/média)
- [ ] Explicou no código que β = cov(x,y)/var(x) e que a reta passa pela média
- [ ] Falou a frase "correlação não implica causalidade" por conta própria
- [ ] Números na ponta da língua: 0,7349 · R²=0,54 · CV altura 5% vs idade 37% · 130,19 vs σ/√30=2,69