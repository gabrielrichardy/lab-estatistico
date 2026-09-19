# 🧮 Laboratório Estatístico Interativo

Equipe para a Sistematização de **Matemática e Estatística para Computação** (Prof. Romes Heriberto).

## Componentes

| Nome completo | Matrícula |
|---|---|
| *(substituir)* | *(substituir)* |
| *(substituir)* | *(substituir)* |
| *(substituir)* | *(substituir)* |
| *(substituir)* | *(substituir)* |
| *(substituir)* | *(substituir)* |

## Descrição do projeto

Aplicação computacional que carrega um **dataset real** (Body Performance Data) e permite explorar
estatística descritiva, distribuições de probabilidade, simulação de Monte Carlo e regressão linear.
O diferencial: **o núcleo matemático é implementado do zero** na biblioteca própria
[`nucleo/minhastats.py`](nucleo/minhastats.py) e validado contra NumPy/SciPy por uma suíte de testes
(44 testes, tolerância `rtol=1e-10`).

### Estrutura do repositório

```
lab-estatistico/
├── nucleo/            # biblioteca estatística própria (sem funções prontas de estatística)
│   ├── minhastats.py  # média, mediana, moda, amplitude, var/dp (amostral/pop), quartis/percentis, CV, covariância, Pearson
│   ├── distribuicoes.py# PDFs: Normal, Exponencial, Uniforme, Poisson, Binomial
│   ├── simulacao.py   # Lei dos Grandes Números e Teorema Central do Limite (Monte Carlo)
│   └── regressao.py   # mínimos quadrados, equação da reta, R², predição
├── app/               # interface (separada do núcleo)
│   ├── app.py         # Streamlit (5 abas)
│   └── views/         # descritiva, probabilidade, distribuicoes, regressao
├── testes/            # pytest: cada função própria vs NumPy/SciPy
├── scripts/           # baixar dados
└── data/              # bodyPerformance.csv (13.393 registros)
```

### Módulos implementados

| Módulo | O que faz |
|---|---|
| **0 — Dados** | Body Performance Data: 13.393 registros, 10 variáveis numéricas, 2 categóricas (`gender`, `class`) |
| **1 — Núcleo** | 11+ medidas implementadas manualmente e validadas contra NumPy/SciPy (`pytest`) |
| **2 — Descritiva** | tabela de frequências (classes via Sturges), medidas, histograma/boxplot/barras, outliers (IQR) e interpretação automática |
| **3 — Simulação** | LGN (dado/moeda) e TCL com sliders de repetições e tamanho de amostra |
| **4 — Distribuições** | curvas Normal/Exponencial/Uniforme sobrepostas ao histograma, com parâmetros estimados dos dados |
| **5 — Regressão** | OLS implementado à mão, dispersão + reta, equação, R², predição interativa e alerta "correlação ≠ causalidade" |

## Dataset

- **Fonte original**: [Body Performance Data — Kaggle](https://www.kaggle.com/datasets/kukuroo3/body-performance-data)
- **Tamanho**: 13.393 registros (≥ 1.000 exigido), 12 variáveis.
- **Critérios atendidos**: 10 variáveis numéricas (≥ 4) e 2 categóricas (`gender`, `class`; ≥ 2).
- O arquivo já vem neste repositório em `data/bodyPerformance.csv`. Para rebaixá-lo do zero:

```bash
python -m scripts.baixar_dados
```

## Como instalar e executar

Requer Python 3.10+.

```bash
# 1. clonar
git clone https://github.com/SEU_TIME/lab-estatistico.git
cd lab-estatistico

# 2. ambiente virtual
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # Linux / macOS

# 3. dependências
pip install -r requirements.txt

# 4. (se data/bodyPerformance.csv estiver ausente)
python -m scripts.baixar_dados

# 5. rodar a aplicação
streamlit run app/app.py

# 6. validar o núcleo estatístico
pytest testes/ -v
```

A aplicação abre em `http://localhost:8501`.

## Capturas de tela

Figuras geradas pela própria aplicação (`scripts/gerar_graficos.py` reproduz cada
aba e exporta as imagens):

![Módulo 2 — histograma](assets/m2_histograma_altura.png)
![Módulo 2 — boxplot](assets/m2_boxplot_peso.png)
![Módulo 2 — categórica](assets/m2_categorica_barras.png)
![Módulo 3 — Lei dos Grandes Números](assets/m3_lgn.png)
![Módulo 3 — TCL](assets/m3_tcl.png)
![Módulo 4 — distribuições teóricas](assets/m4_distribuicoes.png)
![Módulo 5 — regressão linear](assets/m5_regressao.png)

## Reproduzindo a validação do núcleo

```bash
pytest testes/ -v
```

Tolerância documentada: `np.allclose(resultado_proprio, referencia, rtol=1e-10, atol=1e-12)`.
Detalhes das fórmulas no [RELATORIO.md](RELATORIO.md).

---

*Entrega: PDF `SISTEMATIZACAO_MEC_NomeDoGrupo.pdf` no padrão pedido pelo Prof. Romes.*