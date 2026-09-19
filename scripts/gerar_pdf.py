"""Gera o PDF de entrega SISTEMATIZACAO_MEC_NomeDoGrupo.pdf (draft).

Propósito: atender ao padrão pedido na disciplina (identificação, link dos
dados, link da solução, link do vídeo e resumo executivo de 1 página).

Antes de entregar, preencha os (SUBSTITUIR) e teste os links em janela
anônima. Uso:  python -m scripts.gerar_pdf
"""

from __future__ import annotations

import os
import sys

from fpdf import FPDF

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from nucleo import minhastats as ms
from nucleo import regressao as rg
import pandas as pd

FONTES = {
    "": "C:/Windows/Fonts/arial.ttf",
    "B": "C:/Windows/Fonts/arialbd.ttf",
    "I": "C:/Windows/Fonts/ariali.ttf",
}
ASSETS = os.path.join(RAIZ, "assets")
SAIDA = os.path.join(RAIZ, "SISTEMATIZACAO_MEC_NomeDoGrupo.pdf")


def dados():
    df = pd.read_csv(os.path.join(RAIZ, "data", "bodyPerformance.csv"))
    y = df["height_cm"].astype(float)
    x = df["weight_kg"].astype(float)
    r0 = ms.resumo_completo(x)
    r1 = ms.resumo_completo(y)
    rg_res = rg.regressao_linear(y.tolist(), x.tolist())
    return r0, r1, rg_res


class Pdf(FPDF):
    def cabecalho_secao(self, texto: str):
        self.set_font("Arial", "B", 13)
        self.set_text_color(178, 0, 0)
        self.cell(0, 8, texto, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(178, 0, 0)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def criar(self):
        r0, r1, rg_res = dados()
        self.set_auto_page_break(auto=True, margin=12)
        self.add_font("Arial", "", FONTES[""])
        self.add_font("Arial", "B", FONTES["B"])
        self.add_font("Arial", "I", FONTES["I"])
        self.set_author("Equipe - Semestre")
        self.add_page()

        # ------------------------------------------------------------------
        self.set_font("Arial", "B", 18)
        self.cell(0, 10, "SISTEMATIZACAO_MEC_NomeDoGrupo", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "", 11)
        self.cell(0, 6, "Matematica e Estatistica para Computacao - Prof. Romes Heriberto", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 6, "Laboratorio Estatistico Interativo - versao principal (versao com codigo)", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

        # 1. Identificacao ---------------------------------------------------
        self.cabecalho_secao("1. Identificacao")
        self.set_font("Arial", "B", 11)
        self.cell(0, 7, "Nome do grupo: trabalho individual - Gabriel Richardy",
                  new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "", 10)
        self.set_font("Arial", "B", 10)
        self.cell(10, 7, "N", border=1, align="C")
        self.cell(110, 7, "Nome completo", border=1)
        self.cell(0, 7, "Matricula", border=1, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "", 10)
        self.cell(10, 7, "1", border=1, align="C")
        self.cell(110, 7, "Gabriel Richardy", border=1)
        self.cell(0, 7, "(SUBSTITUIR matricula)", border=1, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

        # 2. Link dos dados crus ----------------------------------------------
        self.cabecalho_secao("2. Link dos dados crus")
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, "Dataset: Body Performance Data (Kaggle) - 13.393 registros, "
                             "10 variaveis numericas e 2 categoricas (gender, class).")
        self.set_font("Arial", "I", 10)
        self.set_text_color(0, 0, 200)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, "https://www.kaggle.com/datasets/kukuroo3/body-performance-data")
        self.set_text_color(0, 0, 0)

        # 3. Link da solucao ----------------------------------------------------
        self.cabecalho_secao("3. Link da solucao (repositorio publico)")
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6,
            "Repositorio GitHub com: nucleo estatistico proprio (nucleo/), interface "
            "Streamlit (app/), testes pytest vs NumPy/SciPy (testes/), README.md e "
            "RELATORIO.md (formulas, validacao, 3 descobertas) e graficos em assets/.")
        self.set_font("Arial", "I", 10)
        self.set_text_color(0, 0, 200)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, "https://github.com/gabrielrichardy/lab-estatistico")
        self.set_text_color(0, 0, 0)

        # 4. Link do video -------------------------------------------------------
        self.cabecalho_secao("4. Link do video de demonstracao (3-5 min)")
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, "Video nao listado no YouTube (ou Drive com acesso liberado): "
                             "dataset (30 s) - cada modulo rodando - explicacao de um trecho "
                             "do nucleo - melhor achado.")
        self.set_font("Arial", "I", 10)
        self.set_text_color(0, 0, 200)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, "https://youtu.be/COLE_AQUI_O_LINK_DO_VIDEO")
        self.set_text_color(0, 0, 0)

        # 5. Resumo executivo ------------------------------------------------------
        self.cabecalho_secao("5. Resumo executivo")
        self.set_font("Arial", "B", 10)
        self.cell(0, 6, "5.1. Dataset", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5.8,
            "Body Performance Data reune 13.393 avaliacoes de desempenho fisico "
            "(altura, peso, percentual de gordura, pressao, forca, flexibilidade, "
            "abdominais, salto; genero e classe A-D). Atende aos criterios: mais de "
            "1.000 registros, 10 variaveis numericas e 2 categoricas.")
        self.set_font("Arial", "B", 10)
        self.cell(0, 6, "5.2. Modulos implementados", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5.8,
            "Circulos 1-2: nucleo estatistico proprio (media, mediana, moda, amplitude, "
            "variancia/dp amostral e populacional, quartis/percentis type 7, coeficiente "
            "de variacao, covariancia e Pearson) validado em 44 testes contra "
            "NumPy/SciPy (rtol 1e-10) + estatistica descritiva interativa com tabelas de "
            "frequencia, histograma/boxplot, outliers (IQR) e interpretacao automatica. "
            "Circulos 3-4: simulacao de Monte Carlo (Lei dos Grandes Numeros e Teorema "
            "Central do Limite) com parametros controlaveis e ajuste de distribuicoes "
            "teoricas (Normal e Exponencial/Uniforme) com parametros estimados dos dados. "
            "Circulos 5-6: regressao linear por minimos quadrados implementada na mao "
            "(equacao, R2, predicao interativa) e 3 descobertas documentadas no relatorio.")
        self.set_font("Arial", "B", 10)
        self.cell(0, 6, "5.3. As 3 principais descobertas", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5.8,
            "1) A altura e a variavel mais homogenea: CV = 5,00% (media 168,6 cm; dp 8,4), "
            "contra CV de 37,0% na idade e 35,9% nos abdominais - a amostra varia muito "
            "mais em condicionamento do que em estatura. "
            "2) Peso e percentual de gordura nao caminham juntos: r = -0,08, enquanto "
            "altura x peso dao r = 0,73 e abdominais x salto r = 0,75 - mais peso nao "
            "implica mais gordura relativa, pois massa muscular pesa mais. "
            "3) O dataset mistura formas: idade e assimetrica a direita (media 36,8 > "
            "mediana 32,0; cauda de idosos) enquanto salto e abdominais sao assimetricos "
            "a esquerda - nao existe 'a curva dos dados', cada variavel pede modelo proprio.")
        r2 = rg_res["r2"]
        self.set_font("Arial", "", 9)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.4,
            f"Suporte de regressao: height_cm x weight_kg ajustam y = {rg_res['beta']:.2f}*x "
            f"{rg_res['alpha']:+.2f} com r = {rg_res['r']:.4f} e R2 = {r2:.4f} "
            f"({r2*100:.1f}% da variacao do peso explicada linearmente pela altura).")

        # Imagens de apoio no resumo ---------------------------------------------
        self.ln(2)
        y0 = self.get_y()
        self.image(os.path.join(ASSETS, "m2_histograma_altura.png"), x=10, y=y0, w=93)
        self.image(os.path.join(ASSETS, "m5_regressao.png"), x=105, y=y0, w=95)
        self.set_y(y0 + 55)
        self.image(os.path.join(ASSETS, "m3_tcl.png"), x=10, w=95)
        self.set_font("Arial", "I", 9)
        self.set_xy(108, y0 + 55)
        self.multi_cell(90, 5,
            "Figuras geradas pela propria aplicacao (scripts/gerar_graficos.py): "
            "histograma de altura, regressao altura x peso e distribuicao das medias "
            "amostrais (TCL, n=30).")

        # observacoes finais ------------------------------------------------------
        self.cabecalho_secao("Observacoes antes de enviar")
        self.set_font("Arial", "", 9.5)
        self.multi_cell(0, 5.4,
            "* Preencha (SUBSTITUIR) em identificacao, repositorio e video. "
            "* Teste os 3 links em uma janela anonima do navegador antes de enviar. "
            "* Envie o PDF no ambiente virtual da disciplina (Adicionar envio > "
            "anexar > Salvar mudancas), dentro do prazo.")
        self.output(SAIDA)
        print("PDF gerado:", SAIDA)


if __name__ == "__main__":
    Pdf(orientation="P", unit="mm", format="A4").criar()