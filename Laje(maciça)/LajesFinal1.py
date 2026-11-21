from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
import math
import recursos_rc

class LajesUI(QMainWindow):
    def __init__(self):
        super().__init__()
        #achar o arquivo salvo
        uic.loadUi('Lajes.ui', self)
        #conectar o botão clique com o método lambdaEarmacao
        self.armacao_tipo.clicked.connect(self.lambdaEarmacao)
        #conectar o botao(igual o de cima) ao metodo fazer_tabela
        self.armacao_tipo.clicked.connect(self.fazer_tabela)
        #conectar o botao ao metodo fazer_tabela2
        self.botao_calcular.clicked.connect(self.fazer_tabela2)
        #conectar o botao ao metodo fazer_tabela3
        self.botao_calcular.clicked.connect(self.fazer_tabela3)
        #conectar o botao planta_apoio com o metodo desenho_reacao_apoio
        self.planta_apoio.clicked.connect(self.desenho_reacao_apoio)
        #conectar o botao planta_momento com o metodo desenho_momento
        self.planta_momento.clicked.connect(self.desenho_momento)
        # conectar o botao detalhar com o metodo desenhar_detalhamento_positivo
        self.detalhar.clicked.connect(self.desenhar_detalhamento_positivo)
        self.detalhar_neg.clicked.connect(self.desenhar_detalhamento_negativo)
            #teste automatico do programa
        # self.lxvalor.setText("586")
        # self.lyvalor.setText("656")
        # self.carga_p.setText("6.58")
        #teste laje unidirecional
        self.lxvalor.setText("200")
        self.lyvalor.setText("600")
        self.carga_p.setText("6.58")
        self.Llajes()

    #pegar as infos iniciais(geometria e carga p(kN.m²)
    def Llajes(self):
        self.lx = float(self.lxvalor.text())
        self.ly = float(self.lyvalor.text())
        self.λ = self.ly / self.lx
        self.p=float(self.carga_p.text())
        self.tipolaje= self.tiposdelaje.currentText()
        if self.lx<0.7*self.ly:
            self.l1=self.lx/100
        else:
            self.l1=self.ly*0.7/100

    #calcular lambada e aparecer nna tela o tipo de armacao e o tipo de laje
    def lambdaEarmacao(self):
        self.Llajes()
        if self.λ>=2:
            self.tipodearmacao.setText(str(f"Armada em uma direção,tipo {self.tipolaje}"))
        else:
            self.tipodearmacao.setText(str(f"Armada em duas direções,tipo {self.tipolaje}"))

    #pegar o valor de n(numeros de bordas engastadas) de acordo com o tipo selecionado
    def valor_n(self):
        self.Llajes()
        apoiosengaste = {
            "1": 0,
            "2A": 1,
            "2B": 1,
            "3": 2,
            "4A": 2,
            "4B": 2,
            "5A": 3,
            "5B": 3,
            "6": 4,
            "7": 0,
            "8": 2,
            "9": 1,
            "10": 3,
         }
        n = apoiosengaste.get(self.tipolaje)
        return n
        # if n is not None:
        #     self.resultado.setText(str(n))

    #pre calculo altura h e altura util d
    def pre_altura(self):
        self.Llajes()
        self.d=(2.5-(0.1*(self.valor_n())))*self.l1
        self.hi=self.d+2.5
        #isso aqui aproxima para o inteiro mais proximo e aproxima pra cima valor com 0.5
        self.h = math.floor(self.hi + 0.5)

    #fazer a tabela das infos basicas
    def fazer_tabela(self):
        self.Llajes()
        self.pre_altura()
        self.tabela.setColumnWidth(2, 80)
        dados = [self.lx,self.ly,f"{self.λ:.2f}",self.valor_n(),f"{self.d:.2f}",self.h ]
        for col, valor in enumerate(dados):
            self.tabela.setItem(0, col, QTableWidgetItem(str(valor)))

    #tabelas que retornam os valores dos coef para calculo do momento fletor
    def tabela_momentofletor(self):
        self.tabela_A8 = {
            "1": {
                1.00: (4.23, 4.23),
                1.05: (4.62, 4.25),
                1.10: (5.00, 4.27),
                1.15: (5.38, 4.25),
                1.20: (5.75, 4.22),
                1.25: (6.10, 4.17),
                1.30: (6.44, 4.12),
                1.35: (6.77, 4.06),
                1.40: (7.10, 4.00),
                1.45: (7.41, 3.95),
                1.50: (7.72, 3.89),
                1.55: (7.99, 3.82),
                1.60: (8.26, 3.74),
                1.65: (8.50, 3.66),
                1.70: (8.74, 3.58),
                1.75: (8.95, 3.53),
                1.80: (9.16, 3.47),
                1.85: (9.35, 3.38),
                1.90: (9.54, 3.29),
                1.95: (9.73, 3.23),
                2.00: (9.91, 3.16),
            },

            "2A": {
                1.00: (2.91, 3.54, 8.40),
                1.05: (3.26, 3.64, 8.79),
                1.10: (3.61, 3.74, 9.18),
                1.15: (3.98, 3.80, 9.53),
                1.20: (4.35, 3.86, 9.88),
                1.25: (4.72, 3.89, 10.16),
                1.30: (5.09, 3.92, 10.41),
                1.35: (5.44, 3.93, 10.64),
                1.40: (5.79, 3.94, 10.86),
                1.45: (6.12, 3.91, 11.05),
                1.50: (6.45, 3.88, 11.23),
                1.55: (6.76, 3.85, 11.39),
                1.60: (7.07, 3.81, 11.55),
                1.65: (7.28, 3.78, 11.67),
                1.70: (7.49, 3.74, 11.79),
                1.75: (7.53, 3.69, 11.88),
                1.80: (7.56, 3.63, 11.96),
                1.85: (8.10, 3.58, 12.05),
                1.90: (8.63, 3.53, 12.14),
                1.95: (8.86, 3.45, 12.17),
                2.00: (9.08, 3.36, 12.20),
            },

            "2B": {
                1.00: (3.54, 8.40, 2.91),
                1.05: (3.77, 8.79, 2.84),
                1.10: (3.99, 9.17, 2.76),
                1.15: (4.19, 9.49, 2.68),
                1.20: (4.38, 9.80, 2.59),
                1.25: (4.55, 10.06, 2.51),
                1.30: (4.71, 10.32, 2.42),
                1.35: (4.86, 10.54, 2.34),
                1.40: (5.00, 10.75, 2.25),
                1.45: (5.12, 10.92, 2.19),
                1.50: (5.24, 11.09, 2.12),
                1.55: (5.34, 11.23, 2.04),
                1.60: (5.44, 11.36, 1.95),
                1.65: (5.53, 11.48, 1.87),
                1.70: (5.61, 11.60, 1.79),
                1.75: (5.68, 11.72, 1.74),
                1.80: (5.75, 11.84, 1.68),
                1.85: (5.81, 11.94, 1.67),
                1.90: (5.86, 12.03, 1.59),
                1.95: (5.90, 12.08, 1.54),
                2.00: (5.94, 12.13, 1.48),
            },
            "3": {
                1.00: (2.69, 6.99, 2.69, 6.99),
                1.05: (2.94, 7.43, 2.68, 7.18),
                1.10: (3.19, 7.87, 2.67, 7.36),
                1.15: (3.42, 8.28, 2.65, 7.50),
                1.20: (3.65, 8.69, 2.62, 7.63),
                1.25: (3.86, 9.03, 2.56, 7.72),
                1.30: (4.06, 9.37, 2.50, 7.81),
                1.35: (4.24, 9.65, 2.45, 7.88),
                1.40: (4.42, 9.93, 2.39, 7.94),
                1.45: (4.58, 10.17, 2.32, 8.00),
                1.50: (4.73, 10.41, 2.25, 8.06),
                1.55: (4.86, 10.62, 2.16, 8.09),
                1.60: (4.99, 10.82, 2.07, 8.12),
                1.65: (5.10, 10.99, 1.99, 8.14),
                1.70: (5.21, 11.16, 1.91, 8.15),
                1.75: (5.31, 11.30, 1.85, 8.16),
                1.80: (5.40, 11.43, 1.78, 8.17),
                1.85: (5.48, 11.55, 1.72, 8.17),
                1.90: (5.56, 11.67, 1.66, 8.18),
                1.95: (5.63, 11.78, 1.63, 8.19),
                2.00: (5.70, 11.89, 1.60, 8.20),
            },

            "4A": {
                1.00: (2.01, 3.09, 6.99),
                1.05: (2.32, 3.23, 7.43),
                1.10: (2.63, 3.36, 7.87),
                1.15: (2.93, 3.46, 8.26),
                1.20: (3.22, 3.56, 8.65),
                1.25: (3.63, 3.64, 9.03),
                1.30: (3.99, 3.72, 9.33),
                1.35: (4.34, 3.77, 9.69),
                1.40: (4.69, 3.82, 10.00),
                1.45: (5.03, 3.86, 10.25),
                1.50: (5.37, 3.90, 10.49),
                1.55: (5.70, 3.90, 10.70),
                1.60: (6.03, 3.89, 10.91),
                1.65: (6.35, 3.85, 11.08),
                1.70: (6.67, 3.81, 11.24),
                1.75: (6.97, 3.79, 11.39),
                1.80: (7.27, 3.76, 11.53),
                1.85: (7.55, 3.72, 11.65),
                1.90: (7.82, 3.67, 11.77),
                1.95: (8.09, 3.60, 11.83),
                2.00: (8.35, 3.52, 11.88),
            },

            "4B": {
                1.00: (3.09, 6.99, 2.01),
                1.05: (3.22, 7.20, 1.92),
                1.10: (3.35, 7.41, 1.83),
                1.15: (3.46, 7.56, 1.73),
                1.20: (3.57, 7.70, 1.63),
                1.25: (3.66, 7.82, 1.56),
                1.30: (3.74, 7.93, 1.49),
                1.35: (3.80, 8.02, 1.41),
                1.40: (3.86, 8.11, 1.33),
                1.45: (3.91, 8.13, 1.26),
                1.50: (3.96, 8.15, 1.19),
                1.55: (4.00, 8.20, 1.14),
                1.60: (4.04, 8.25, 1.08),
                1.65: (4.07, 8.28, 1.03),
                1.70: (4.10, 8.30, 0.98),
                1.75: (4.12, 8.31, 0.95),
                1.80: (4.14, 8.32, 0.91),
                1.85: (4.15, 8.33, 0.87),
                1.90: (4.16, 8.33, 0.83),
                1.95: (4.16, 8.33, 0.80),
                2.00: (4.17, 8.33, 0.76),
            },
            "5A": {
                1.00: (2.02, 5.46, 2.52, 6.17),
                1.05: (2.27, 5.98, 2.56, 6.46),
                1.10: (2.52, 6.50, 2.60, 6.75),
                1.15: (2.76, 7.11, 2.63, 6.97),
                1.20: (3.00, 7.72, 2.65, 7.19),
                1.25: (3.23, 8.81, 2.64, 7.36),
                1.30: (3.45, 8.59, 2.61, 7.51),
                1.35: (3.66, 8.74, 2.57, 7.63),
                1.40: (3.86, 8.88, 2.53, 7.74),
                1.45: (4.05, 9.16, 2.48, 7.83),
                1.50: (4.23, 9.44, 2.43, 7.91),
                1.55: (4.39, 9.68, 2.39, 7.98),
                1.60: (4.55, 9.91, 2.34, 8.02),
                1.65: (4.70, 10.13, 2.28, 8.03),
                1.70: (4.84, 10.34, 2.22, 8.10),
                1.75: (4.97, 10.53, 2.15, 8.13),
                1.80: (5.10, 10.71, 2.08, 8.17),
                1.85: (5.20, 10.88, 2.02, 8.16),
                1.90: (5.30, 11.04, 1.96, 8.14),
                1.95: (5.40, 11.20, 1.88, 8.13),
                2.00: (5.50, 11.35, 1.80, 8.12),
            },

            "5B": {
                1.00: (2.52, 6.17, 2.02, 5.46),
                1.05: (2.70, 6.47, 1.97, 5.56),
                1.10: (2.87, 6.76, 1.91, 5.65),
                1.15: (3.02, 6.99, 1.84, 5.70),
                1.20: (3.16, 7.22, 1.77, 5.75),
                1.25: (3.28, 7.40, 1.70, 5.75),
                1.30: (3.40, 7.57, 1.62, 5.76),
                1.35: (3.50, 7.70, 1.55, 5.75),
                1.40: (3.59, 7.82, 1.47, 5.74),
                1.45: (3.67, 7.91, 1.41, 5.73),
                1.50: (3.74, 8.00, 1.35, 5.72),
                1.55: (3.80, 8.07, 1.29, 5.69),
                1.60: (3.86, 8.14, 1.23, 5.66),
                1.65: (3.91, 8.20, 1.18, 5.62),
                1.70: (3.95, 8.25, 1.13, 5.58),
                1.75: (3.99, 8.30, 1.07, 5.56),
                1.80: (4.02, 8.34, 1.00, 5.54),
                1.85: (4.05, 8.38, 0.97, 5.55),
                1.90: (4.08, 8.42, 0.94, 5.56),
                1.95: (4.10, 8.45, 0.91, 5.60),
                2.00: (4.12, 8.47, 0.88, 5.64),
            },

            "6": {
                1.00: (2.02, 5.15, 2.02, 5.15),
                1.05: (2.22, 5.50, 2.00, 5.29),
                1.10: (2.42, 5.85, 1.98, 5.43),
                1.15: (2.65, 6.14, 1.94, 5.51),
                1.20: (2.87, 6.43, 1.89, 5.59),
                1.25: (2.97, 6.67, 1.83, 5.64),
                1.30: (3.06, 6.90, 1.77, 5.68),
                1.35: (3.19, 7.09, 1.71, 5.69),
                1.40: (3.32, 7.28, 1.65, 5.70),
                1.45: (3.43, 7.43, 1.57, 5.71),
                1.50: (3.53, 7.57, 1.49, 5.72),
                1.55: (3.61, 7.68, 1.43, 5.72),
                1.60: (3.69, 7.79, 1.36, 5.72),
                1.65: (3.76, 7.88, 1.29, 5.72),
                1.70: (3.83, 7.97, 1.21, 5.72),
                1.75: (3.88, 8.05, 1.17, 5.72),
                1.80: (3.92, 8.12, 1.13, 5.72),
                1.85: (3.96, 8.18, 1.07, 5.72),
                1.90: (3.99, 8.24, 1.01, 5.72),
                1.95: (4.02, 8.29, 0.99, 5.72),
                2.00: (4.05, 8.33, 0.96, 5.72),
            },
            "7": {
                0.30: (11.33, 15.89, 28.44),
                0.35: (10.63, 15.60, 27.19),
                0.40: (9.94, 15.31, 25.94),
                0.45: (9.13, 14.48, 24.47),
                0.50: (8.32, 13.64, 23.00),
                0.55: (7.58, 12.95, 21.56),
                0.60: (6.83, 12.25, 20.11),
                0.65: (6.21, 11.59, 18.71),
                0.70: (5.59, 10.92, 17.31),
                0.75: (5.09, 10.24, 15.86),
                0.80: (4.59, 9.55, 14.41),
                0.85: (4.16, 9.09, 13.61),
                0.90: (3.73, 8.63, 12.80),
                0.95: (3.39, 8.14, 11.94),
                1.00: (3.05, 7.64, 11.08),
                1.05: (3.05, 7.94, 11.31),
                1.10: (3.06, 8.24, 11.55),
                1.15: (3.06, 8.53, 11.78),
                1.20: (3.07, 8.83, 12.01),
                1.25: (3.03, 9.01, 12.12),
                1.30: (3.00, 9.19, 12.22),
                1.35: (2.97, 9.38, 12.33),
                1.40: (2.94, 9.56, 12.43),
                1.45: (2.91, 9.74, 12.54),
                1.50: (2.88, 9.92, 12.64),
            },
            "8": {
                0.30: (10.44, 14.22, 25.55, 41.89, 77.00),
                0.35: (8.85, 12.82, 23.37, 36.69, 62.94),
                0.40: (7.25, 11.50, 19.29, 29.50, 48.88),
                0.45: (6.22, 10.39, 16.82, 23.89, 41.36),
                0.50: (5.20, 9.28, 14.44, 22.28, 33.84),
                0.55: (4.57, 8.35, 12.82, 19.64, 28.76),
                0.60: (3.94, 7.42, 11.19, 17.00, 23.67),
                0.65: (3.46, 6.76, 9.94, 15.26, 20.55),
                0.70: (2.98, 6.10, 8.69, 13.51, 17.43),
                0.75: (2.61, 5.54, 7.77, 12.28, 15.38),
                0.80: (2.23, 4.98, 6.84, 11.05, 13.33),
                0.85: (1.96, 4.65, 6.15, 10.12, 11.91),
                0.90: (1.68, 4.31, 5.46, 9.19, 10.49),
                0.95: (1.47, 3.97, 4.96, 8.45, 9.49),
                1.00: (1.26, 3.62, 4.45, 7.71, 8.48),
            },
            "9": {
                0.30: (-12.50, 5.00, 0.78, 6.22),
                0.35: (-7.33, 4.38, 0.78, 6.22),
                0.40: (-3.17, 3.98, 1.89, 7.89),
                0.45: (-3.00, 3.87, 3.00, 9.56),
                0.50: (-0.56, 3.09, 4.24, 11.52),
                0.55: (0.25, 2.80, 4.62, 11.82),
                0.60: (1.06, 2.51, 5.00, 12.11),
                0.65: (1.47, 2.29, 5.25, 12.11),
                0.70: (1.88, 2.06, 5.49, 12.12),
                0.75: (2.06, 1.84, 5.61, 11.81),
                0.80: (2.23, 1.70, 5.72, 11.50),
                0.85: (2.26, 1.59, 5.66, 11.05),
                0.90: (2.28, 1.46, 5.60, 10.59),
                0.95: (2.25, 1.29, 5.48, 10.07),
                1.00: (2.21, 1.18, 5.36, 9.55),
            },
            "10": {
                0.30: (-12.50, 5.00, 2.11, 8.67, 14.56, 37.00),
                0.35: (-2.57, 3.08, 3.18, 9.74, 14.84, 35.53),
                0.40: (-0.25, 2.83, 4.25, 10.81, 15.13, 34.06),
                0.45: (0.54, 2.39, 4.53, 10.77, 14.26, 31.21),
                0.50: (1.32, 2.04, 4.80, 10.72, 13.40, 28.36),
                0.55: (1.62, 1.70, 4.86, 9.99, 12.48, 25.26),
                0.60: (1.92, 1.46, 4.92, 9.25, 11.56, 22.17),
                0.65: (1.91, 1.29, 4.68, 8.55, 10.81, 19.63),
                0.70: (1.90, 1.06, 4.43, 7.84, 10.06, 17.08),
                0.75: (1.82, 0.96, 4.14, 7.15, 9.42, 15.17),
                0.80: (1.73, 0.86, 3.86, 6.45, 8.77, 13.25),
                0.85: (1.64, 0.78, 3.59, 5.86, 8.19, 11.87),
                0.90: (1.54, 0.71, 3.33, 5.26, 7.60, 10.49),
                0.95: (1.40, 0.62, 3.11, 4.81, 7.12, 9.50),
                1.00: (1.25, 0.59, 2.88, 4.35, 6.64, 8.51),
            }
        }
    # pegar os coef
    def pegar_coeficientes(self):
        self.tabela_momentofletor()
        self.Llajes()  # já garante que λ está atualizado
        tipo = self.tipolaje
        lamb = self.λ
        tabela = self.tabela_A8.get(tipo)
        if tabela is None:
            return None
        # acha λ mais próximo
        lamb_proximo = min(tabela.keys(), key=lambda x: abs(x - lamb))
        coef = tabela[lamb_proximo]
        return coef

    #organizar os coef
    def organizar_coeficientes(self):
        coef = self.pegar_coeficientes()
        tipo = self.tipolaje
        if coef is None:
            return None
        if tipo == "1":
            mux, muy = coef
            return {"mux": mux, "muy": muy}
        elif tipo == "2A":
            mux, muy, muy_linha = coef
            return {"mux": mux, "muy": muy, "muy_linha": muy_linha}
        elif tipo == "2B":
            mux, mux_linha, muy = coef
            return {"mux": mux, "muy": muy, "mux_linha": mux_linha}
        elif tipo == "3":
            mux, mux_linha, muy, muy_linha = coef
            return {
                "mux": mux,
                "muy": muy,
                "mux_linha": mux_linha,
                "muy_linha": muy_linha
            }
        elif tipo == "4A":
            mux, muy, muy_linha = coef
            return {
                "mux": mux,
                "muy": muy,
                "muy_linha": muy_linha
            }
        elif tipo == "4B":
            mux, mux_linha, muy = coef
            return {
                "mux": mux,
                "muy": muy,
                "mux_linha": mux_linha
            }
        elif tipo == "5A":
            mux, mux_linha, muy, muy_linha = coef
            return {
                "mux": mux,
                "muy": muy,
                "mux_linha": mux_linha,
                "muy_linha": muy_linha
            }
        elif tipo == "5B":
            mux, mux_linha, muy, muy_linha = coef
            return {
                "mux": mux,
                "muy": muy,
                "mux_linha": mux_linha,
                "muy_linha": muy_linha
            }
        elif tipo == "6":
            mux, mux_linha, muy, muy_linha = coef
            return {
                "mux": mux,
                "muy": muy,
                "mux_linha": mux_linha,
                "muy_linha": muy_linha
            }
        elif tipo == "7":
            mux, muy, muyb = coef
            return {"mux": mux, "muy": muy, "muyb": muyb}
        elif tipo == "8":
            mux, muy, muyb, muy_linha, muyb_linha = coef
            return {
                "mux": mux,
                "muy": muy,
                "muyb": muyb,
                "muy_linha": muy_linha,
                "muyb_linha": muyb_linha
            }
        elif tipo == "9":
            mux, mux_linha, muy, muyb = coef
            return {
                "mux": mux,
                "mux_linha": mux_linha,
                "muy": muy,
                "muyb": muyb
            }
        elif tipo == "10":
            mux, mux_linha, muy, muyb, muy_linha, muyb_linha = coef
            return {
                "mux": mux,
                "mux_linha": mux_linha,
                "muy": muy,
                "muyb": muyb,
                "muy_linha": muy_linha,
                "muyb_linha": muyb_linha
            }

    def calcular_momentos(self):
        self.Llajes()
        coef=self.organizar_coeficientes()
        lx=self.lx/100
        self.mux=coef["mux"]
        self.muy=coef["muy"]
        self.mux_linha = coef.get("mux_linha", 0)
        self.muy_linha = coef.get("muy_linha", 0)
        self.Mx= self.mux*self.p*lx*lx/100
        self.My = self.muy * self.p * lx * lx / 100
        self.Mx_linha = self.mux_linha * self.p * lx * lx / 100
        self.My_linha = self.muy_linha * self.p * lx * lx / 100

        #tabela momentos fletores
    def fazer_tabela2(self):
        self.Llajes()
        #self.calcular_momentos()
        self.escolher_calcular_momentos()
        self.tabela_momento.setColumnWidth(0, 70)
        dados = [self.p, self.mux, self.mux_linha, self.muy, self.muy_linha, f"{self.Mx:.2f}", f"{self.Mx_linha:.2f}", f"{self.My:.2f}", f"{self.My_linha:.2f}"]
        for col, valor in enumerate(dados):
            self.tabela_momento.setItem(0, col, QTableWidgetItem(str(valor)))

    def tabela_reacoes_apoio(self):
        self.tabela_nu = {

            "1": {
                1.00: (2.50, 2.50),
                1.05: (2.62, 2.50),
                1.10: (2.73, 2.50),
                1.15: (2.83, 2.50),
                1.20: (2.92, 2.50),
                1.25: (3.00, 2.50),
                1.30: (3.08, 2.50),
                1.35: (3.15, 2.50),
                1.40: (3.21, 2.50),
                1.45: (3.28, 2.50),
                1.50: (3.33, 2.50),
                1.55: (3.39, 2.50),
                1.60: (3.44, 2.50),
                1.65: (3.48, 2.50),
                1.70: (3.53, 2.50),
                1.75: (3.57, 2.50),
                1.80: (3.61, 2.50),
                1.85: (3.65, 2.50),
                1.90: (3.68, 2.50),
                1.95: (3.72, 2.50),
                2.00: (3.75, 2.50),
            },

            "2A": {
                1.00: (1.83, 2.75, 4.02),
                1.05: (1.92, 2.80, 4.10),
                1.10: (2.01, 2.85, 4.17),
                1.15: (2.10, 2.88, 4.22),
                1.20: (2.20, 2.91, 4.27),
                1.25: (2.29, 2.94, 4.30),
                1.30: (2.38, 2.95, 4.32),
                1.35: (2.47, 2.96, 4.33),
                1.40: (2.56, 2.96, 4.33),
                1.45: (2.64, 2.96, 4.33),
                1.50: (2.72, 2.96, 4.33),
                1.55: (2.80, 2.96, 4.33),
                1.60: (2.87, 2.96, 4.33),
                1.65: (2.93, 2.96, 4.33),
                1.70: (2.99, 2.96, 4.33),
                1.75: (3.05, 2.96, 4.33),
                1.80: (3.10, 2.96, 4.33),
                1.85: (3.15, 2.96, 4.33),
                1.90: (3.20, 2.96, 4.33),
                1.95: (3.25, 2.96, 4.33),
                2.00: (3.29, 2.96, 4.33),
            },

            "2B": {
                1.00: (2.75, 4.02, 1.83),
                1.05: (2.82, 4.13, 1.83),
                1.10: (2.89, 4.23, 1.83),
                1.15: (2.95, 4.32, 1.83),
                1.20: (3.01, 4.41, 1.83),
                1.25: (3.06, 4.48, 1.83),
                1.30: (3.11, 4.55, 1.83),
                1.35: (3.16, 4.62, 1.83),
                1.40: (3.20, 4.68, 1.83),
                1.45: (3.24, 4.74, 1.83),
                1.50: (3.27, 4.79, 1.83),
                1.55: (3.31, 4.84, 1.83),
                1.60: (3.34, 4.89, 1.83),
                1.65: (3.37, 4.93, 1.83),
                1.70: (3.40, 4.97, 1.83),
                1.75: (3.42, 5.01, 1.83),
                1.80: (3.45, 5.05, 1.83),
                1.85: (3.47, 5.09, 1.83),
                1.90: (3.50, 5.12, 1.83),
                1.95: (3.52, 5.15, 1.83),
                2.00: (3.54, 5.18, 1.83),
            },

            "3": {
                1.00: (2.17, 3.17, 2.17, 3.17),
                1.05: (2.27, 3.32, 2.17, 3.17),
                1.10: (2.36, 3.46, 2.17, 3.17),
                1.15: (2.45, 3.58, 2.17, 3.17),
                1.20: (2.53, 3.70, 2.17, 3.17),
                1.25: (2.60, 3.80, 2.17, 3.17),
                1.30: (2.63, 3.90, 2.17, 3.17),
                1.35: (2.73, 3.99, 2.17, 3.17),
                1.40: (2.78, 4.08, 2.17, 3.17),
                1.45: (2.84, 4.15, 2.17, 3.17),
                1.50: (2.89, 4.23, 2.17, 3.17),
                1.55: (2.93, 4.29, 2.17, 3.17),
                1.60: (2.98, 4.36, 2.17, 3.17),
                1.65: (3.02, 4.42, 2.17, 3.17),
                1.70: (3.06, 4.48, 2.17, 3.17),
                1.75: (3.09, 4.53, 2.17, 3.17),
                1.80: (3.13, 4.58, 2.17, 3.17),
                1.85: (3.16, 4.63, 2.17, 3.17),
                1.90: (3.19, 4.67, 2.17, 3.17),
                1.95: (3.22, 4.71, 2.17, 3.17),
                2.00: (3.25, 4.75, 2.17, 3.17),
            },
            "4A": {
                1.00: (1.44, 3.56),
                1.05: (1.52, 3.66),
                1.10: (1.59, 3.75),
                1.15: (1.66, 3.84),
                1.20: (1.73, 3.92),
                1.25: (1.80, 3.99),
                1.30: (1.88, 4.06),
                1.35: (1.95, 4.12),
                1.40: (2.02, 4.17),
                1.45: (2.09, 4.22),
                1.50: (2.17, 4.25),
                1.55: (2.24, 4.28),
                1.60: (2.31, 4.30),
                1.65: (2.38, 4.32),
                1.70: (2.45, 4.33),
                1.75: (2.53, 4.33),
                1.80: (2.59, 4.33),
                1.85: (2.63, 4.33),
                1.90: (2.72, 4.33),
                1.95: (2.78, 4.33),
                2.00: (2.83, 4.33),
            },
            "4B": {
                1.00: (3.56, 1.44),
                1.05: (3.63, 1.44),
                1.10: (3.69, 1.44),
                1.15: (3.74, 1.44),
                1.20: (3.80, 1.44),
                1.25: (3.85, 1.44),
                1.30: (3.89, 1.44),
                1.35: (3.93, 1.44),
                1.40: (3.97, 1.44),
                1.45: (4.00, 1.44),
                1.50: (4.04, 1.44),
                1.55: (4.07, 1.44),
                1.60: (4.10, 1.44),
                1.65: (4.13, 1.44),
                1.70: (4.15, 1.44),
                1.75: (4.18, 1.44),
                1.80: (4.20, 1.44),
                1.85: (4.22, 1.44),
                1.90: (4.24, 1.44),
                1.95: (4.26, 1.44),
                2.00: (4.28, 1.44),
            },
            "5A": {
                1.00: (1.71, 2.50, 3.03),
                1.05: (1.79, 2.63, 3.08),
                1.10: (1.88, 2.75, 3.11),
                1.15: (1.96, 2.88, 3.14),
                1.20: (2.05, 3.00, 3.16),
                1.25: (2.13, 3.13, 3.17),
                1.30: (2.22, 3.25, 3.17),
                1.35: (2.30, 3.36, 3.17),
                1.40: (2.37, 3.47, 3.17),
                1.45: (2.44, 3.57, 3.17),
                1.50: (2.50, 3.66, 3.17),
                1.55: (2.56, 3.75, 3.17),
                1.60: (2.61, 3.83, 3.17),
                1.65: (2.67, 3.90, 3.17),
                1.70: (2.72, 3.98, 3.17),
                1.75: (2.76, 4.04, 3.17),
                1.80: (2.80, 4.11, 3.17),
                1.85: (2.85, 4.17, 3.17),
                1.90: (2.89, 4.22, 3.17),
                1.95: (2.92, 4.28, 3.17),
                2.00: (2.96, 4.33, 3.17),
            },
            "5B": {
                1.00: (3.03, 1.71, 2.50),
                1.05: (3.12, 1.71, 2.50),
                1.10: (3.21, 1.71, 2.50),
                1.15: (3.29, 1.71, 2.50),
                1.20: (3.36, 1.71, 2.50),
                1.25: (3.42, 1.71, 2.50),
                1.30: (3.48, 1.71, 2.50),
                1.35: (3.54, 1.71, 2.50),
                1.40: (3.59, 1.71, 2.50),
                1.45: (3.64, 1.71, 2.50),
                1.50: (3.69, 1.71, 2.50),
                1.55: (3.73, 1.71, 2.50),
                1.60: (3.77, 1.71, 2.50),
                1.65: (3.81, 1.71, 2.50),
                1.70: (3.84, 1.71, 2.50),
                1.75: (3.87, 1.71, 2.50),
                1.80: (3.90, 1.71, 2.50),
                1.85: (3.93, 1.71, 2.50),
                1.90: (3.96, 1.71, 2.50),
                1.95: (3.99, 1.71, 2.50),
                2.00: (4.01, 1.71, 2.50),
            },
            "6": {
                1.00: (2.50, 2.50),
                1.05: (2.62, 2.50),
                1.10: (2.73, 2.50),
                1.15: (2.83, 2.50),
                1.20: (2.92, 2.50),
                1.25: (3.00, 2.50),
                1.30: (3.08, 2.50),
                1.35: (3.15, 2.50),
                1.40: (3.21, 2.50),
                1.45: (3.28, 2.50),
                1.50: (3.33, 2.50),
                1.55: (3.39, 2.50),
                1.60: (3.44, 2.50),
                1.65: (3.48, 2.50),
                1.70: (3.53, 2.50),
                1.75: (3.57, 2.50),
                1.80: (3.61, 2.50),
                1.85: (3.65, 2.50),
                1.90: (3.68, 2.50),
                1.95: (3.72, 2.50),
                2.00: (3.75, 2.50),
            }
        }


    def pegar_nu(self):
        self.tabela_reacoes_apoio()
        if not hasattr(self, "tabela_nu"):
            self.tabela_reacoes()
        self.Llajes()
        tipo = self.tipolaje
        lamb = self.λ
        tabela = self.tabela_nu.get(tipo)
        if tabela is None:
            return None
        lamb_proximo = min(tabela.keys(), key=lambda x: abs(x - lamb))
        return tabela[lamb_proximo]

    def organizar_nu(self):
        coef = self.pegar_nu()
        tipo = self.tipolaje
        if coef is None:
            return None
        if tipo == "1":
            vx, vy = coef
            return {"vx": vx, "vy": vy}
        elif tipo == "2A":
            vx, vy, vy_linha = coef
            return {"vx": vx, "vy": vy, "vy_linha": vy_linha}
        elif tipo == "2B":
            vx, vx_linha, vy = coef
            return {"vx": vx, "vx_linha": vx_linha, "vy": vy}
        elif tipo == "3":
            vx, vx_linha, vy, vy_linha = coef
            return {
                "vx": vx,
                "vx_linha": vx_linha,
                "vy": vy,
                "vy_linha": vy_linha
            }
        elif tipo == "4A":
            vx, vy_linha = coef
            return {
                "vx": vx,
                "vy_linha": vy_linha
            }
        elif tipo == "4B":
            vx_linha, vy = coef
            return {
                "vx_linha": vx_linha,
                "vy": vy
            }
        elif tipo == "5A":
            vx, vx_linha, vy = coef
            return {
                "vx": vx,
                "vx_linha": vx_linha,
                "vy": vy
            }
        elif tipo == "5B":
            vx_linha, vy, vy_linha = coef
            return {
                "vx_linha": vx_linha,
                "vy": vy,
                "vy_linha": vy_linha
            }
        elif tipo == "6":
            vx_linha,vy_linha = coef
            return {
                "vx_linha": vx_linha,
                "vy_linha": vy_linha
            }

    def calcular_apoio(self):
        self.Llajes()
        coef = self.organizar_nu()
        lx = self.lx / 100
        self.vx = coef.get("vx", 0)
        self.vy = coef.get("vy", 0)
        self.vx_linha = coef.get("vx_linha", 0)
        self.vy_linha = coef.get("vy_linha", 0)
        self.Vx = self.vx * self.p * lx / 10
        self.Vy = self.vy * self.p * lx / 10
        self.Vx_linha = self.vx_linha * self.p * lx / 10
        self.Vy_linha = self.vy_linha * self.p * lx / 10

    #tabela reacoes de apoio
    def fazer_tabela3(self):
        self.Llajes()
        #self.calcular_apoio()
        self.escolher_calcular_apoio()
        self.tabela_Rapoio.setColumnWidth(0, 70)
        dados = [self.p, self.vx, self.vx_linha, self.vy, self.vy_linha, f"{self.Vx:.2f}", f"{self.Vx_linha:.2f}", f"{self.Vy:.2f}", f"{self.Vy_linha:.2f}"]
        for col, valor in enumerate(dados):
            self.tabela_Rapoio.setItem(0, col, QTableWidgetItem(str(valor)))

            #fazer o desenho(planta reações de apoio)

    def desenho_reacao_apoio(self):
        import matplotlib.pyplot as plt
        self.Llajes()
        self.escolher_calcular_apoio()

        fig, ax = plt.subplots()
        ax.plot([0, 0, self.lx, self.lx, 0],[0, self.ly, self.ly, 0, 0])

        ax.plot([self.lx / 2, (self.lx / 2) + self.lx / 10, self.lx / 2, (self.lx / 2) - self.lx / 10],
            [self.ly / 2, self.ly / 2,
             self.ly / 2, self.ly / 2]
        )

        ax.text(self.lx / 2,(self.ly / 2) + 10,"X", ha='center',va='center')
        mapa_reacoes = {
            "1": [self.Vx, self.Vy, self.Vx, self.Vy],
            "2A": [self.Vx, self.Vy, self.Vx, self.Vy_linha],
            "2B": [self.Vx, self.Vy, self.Vx_linha, self.Vy],
            "3": [self.Vx, self.Vy_linha, self.Vx_linha, self.Vy],
            "4A": [self.Vx, self.Vy_linha, self.Vx, self.Vy_linha],
            "4B": [self.Vx_linha, self.Vy, self.Vx_linha, self.Vy],
            "5A": [self.Vx, self.Vy_linha, self.Vx_linha, self.Vy_linha],
            "5B": [self.Vx_linha, self.Vy_linha, self.Vx_linha, self.Vy],
            "6": [self.Vx_linha, self.Vy_linha, self.Vx_linha, self.Vy_linha],
            "9": [self.Vx_linha, self.Vy_linha, self.Vx, self.Vy_linha],
            "10": [self.Vx_linha, self.Vy_linha, self.Vx, self.Vy_linha],
        }

        esq, baixo, dir, cima = mapa_reacoes[self.tipolaje]

        ax.text(30, self.ly / 2, f"{esq:.2f}",ha='center', va='center')
        ax.text(self.lx / 2, 15, f"{baixo:.2f}",ha='center', va='center')
        ax.text(self.lx - 40, self.ly / 2, f"{dir:.2f}",ha='center', va='center')
        ax.text(self.lx / 2, self.ly - 30, f"{cima:.2f}",ha='center', va='center')
        ax.set_aspect('equal')
        plt.show()

    def desenho_momento(self):
        import matplotlib.pyplot as plt
        self.Llajes()
        #self.calcular_apoio()
        self.escolher_calcular_momentos()
        self.calc_As()
        fig, ax = plt.subplots()
        #plotar o quadrado
        ax.plot([0, 0, self.lx, self.lx, 0], [0, self.ly, self.ly, 0, 0])
        #plotar as retas no meio e o x
        ax.plot([self.lx / 2, self.lx / 2, (self.lx / 2) + self.lx / 10],[(self.ly / 2) + self.ly / 10, self.ly / 2, self.ly / 2])
        ax.text((self.lx / 2)+self.lx/8, (self.ly / 2), "X", ha='center', va='center',fontsize=6)
        #plotar os momentos POSITIVOS e armaduras nas retas
        ax.text((self.lx / 2) - self.lx / 40, self.ly / 1.95,int(self.My*100), ha='center', va='center', fontsize=7, rotation=90)#mom
        ax.text((self.lx / 2) - self.lx / 40, (self.ly / 2)+self.ly/10, f"({self.Asy:.2f})", ha='center', va='center', fontsize=7,rotation=90)#as
        ax.text((self.lx / 2) + self.lx / 20, (self.ly / 2) + self.ly / 70, int(self.Mx*100), ha='center', va='center', fontsize=7)#mom
        ax.text((self.lx / 2) + self.lx / 20, (self.ly / 2) + (self.ly / 70)-self.ly/20, f"({self.Asx:.2f})", ha='center',va='center', fontsize=7)#as
        #fazer os retangulos
        w = 0.18 * self.lx
        h = 0.08 * self.ly
        x0 = (self.lx - w) / 2
        y0 = 0
        ax.plot([x0, x0 + w, x0 + w, x0, x0], [y0, y0, y0 + h, y0 + h, y0])
        x0 = (self.lx - w) / 2
        y0 = self.ly - h
        ax.plot([x0, x0 + w, x0 + w, x0, x0], [y0, y0, y0 + h, y0 + h, y0])
        wl = h
        hl = w
        xe = 0
        ye = (self.ly - hl) / 2
        ax.plot([xe, xe + wl, xe + wl, xe, xe], [ye, ye, ye + hl, ye + hl, ye])
        xd = self.lx - wl
        yd = (self.ly - hl) / 2
        ax.plot([xd, xd + wl, xd + wl, xd, xd], [yd, yd, yd + hl, yd + hl, yd])
        ax.set_xlim(-50, self.lx + 50)
        ax.set_ylim(-50, self.ly + 50)
        #plotar os numeros no retangulo
        offset = 10
        # fazer um if para cada tipo devido aos momentos NEGATIVOS(_linha)- olhar figura da interface.obs:letras minusculas=mom e maiusculas=As
        if self.tipolaje=="2A"or self.tipolaje=="5B":
            ax.text(self.lx / 2, h / 2, int(self.My_linha * 100), ha='center', va='center')  # baixo
            ax.text(x0 - offset, h / 2, f"{self.Asy_linha:.2f}", ha='right', va='center')  # BASE
            ax.text(self.lx / 2, self.ly - h / 2, 0, ha='center', va='center')  # cima
            ax.text(h / 2, self.ly / 2, int(self.Mx_linha * 100), rotation=90, ha='center', va='center')  # esquerda
            ax.text(xe + wl / 2, ye + hl + offset, f"{self.Asx_linha:.2f}", rotation=90, ha='center',va='bottom')  # ESQUERDA
            ax.text(self.lx - h / 2, self.ly / 2, int(self.Mx_linha * 100), rotation=90, ha='center',va='center')  # direita
            ax.text(xd + wl / 2, yd + hl + offset, f"{self.Asx_linha:.2f}", rotation=90, ha='center',va='bottom')  # DIREITA
        if self.tipolaje == "2B" or self.tipolaje=="5A":
            ax.text(self.lx / 2, h / 2, int(self.My_linha * 100), ha='center', va='center')  # baixo
            ax.text(x0 - offset, h / 2, f"{self.Asy_linha:.2f}", ha='right', va='center')  # BASE
            ax.text(self.lx / 2, self.ly - h / 2, int(self.My_linha * 100), ha='center', va='center')  # cima
            ax.text(x0 - offset, self.ly - h / 2, f"{self.Asy_linha:.2f}", ha='right', va='center')  # TOPO
            ax.text(h / 2, self.ly / 2, 0, rotation=90, ha='center', va='center')  # esquerda
            ax.text(self.lx - h / 2, self.ly / 2, int(self.Mx_linha * 100), rotation=90, ha='center',va='center')  # direita
            ax.text(xd + wl / 2, yd + hl + offset, f"{self.Asx_linha:.2f}", rotation=90, ha='center', va='bottom')  # DIREITA
        if self.tipolaje=="3":
            ax.text(self.lx / 2, h / 2, int(self.My_linha*100), ha='center', va='center') #baixo
            ax.text(x0 - offset, h / 2, f"{self.Asy_linha:.2f}", ha='right', va='center')  # BASE
            ax.text(self.lx / 2, self.ly - h / 2, 0, ha='center', va='center')#cima
            ax.text(h / 2, self.ly / 2, 0, rotation=90, ha='center', va='center')#esquerda
            ax.text(self.lx - h / 2, self.ly / 2, int(self.Mx_linha*100), rotation=90, ha='center', va='center')#direita
            ax.text(xd + wl / 2, yd + hl + offset, f"{self.Asx_linha:.2f}", rotation=90, ha='center', va='bottom')  # DIREITA
        if self.tipolaje=="1" or self.tipolaje=="4A" or self.tipolaje=="4b" or self.tipolaje=="6":
            ax.text(self.lx / 2, h / 2, int(self.My_linha*100), ha='center', va='center')  # baixo
            ax.text(x0 - offset, h / 2, f"{self.Asy_linha:.2f}", ha='right', va='center')  # BASE
            ax.text(self.lx / 2, self.ly - h / 2,int(self.My_linha*100), ha='center', va='center')  # cima
            ax.text(x0 - offset, self.ly - h / 2, f"{self.Asy_linha:.2f}", ha='right', va='center')  # TOPO
            ax.text(h / 2, self.ly / 2,  int(self.Mx_linha*100), rotation=90, ha='center', va='center')  # esquerda
            ax.text(xe + wl / 2, ye + hl + offset, f"{self.Asx_linha:.2f}", rotation=90, ha='center',va='bottom')  # ESQUERDA
            ax.text(self.lx - h / 2, self.ly / 2,  int(self.Mx_linha*100), rotation=90, ha='center', va='center')  # direita
            ax.text(xd + wl / 2, yd + hl + offset, f"{self.Asx_linha:.2f}", rotation=90, ha='center',va='bottom')  # DIREITA

        ax.set_aspect('equal')
        plt.show()

#Sessao para calcular a armadura
    #armadura minima
    def arm_minima(self,h):
        pmin = self.pegar_pmin(int(self.fck_conc.currentText()))
        Asmin=pmin*h*100
        return Asmin
    #auxilia a de cima
    def pegar_pmin(self, fck):
        tabela = {
            20: 0.0015,
            25: 0.0015,
            30: 0.0015,
            35: 0.00164,
            40: 0.00179,
            45: 0.00194,
            50: 0.00208
        }
        return tabela.get(fck)

    def tabelaKc(self):
        self.tabela_kc = {
        0.01: {"C20": 103.4, "C25": 82.7, "C30": 68.9, "C35": 59.1, "C40": 51.7, "C45": 47.8, "C50": 44.5},
        0.02: {"C20": 51.9, "C25": 41.5, "C30": 34.6, "C35": 29.6, "C40": 25.9, "C45": 24.0, "C50": 22.4},
        0.03: {"C20": 34.7, "C25": 27.8, "C30": 23.2, "C35": 19.8, "C40": 17.4, "C45": 16.1, "C50": 15.0},
        0.04: {"C20": 26.2, "C25": 20.9, "C30": 17.4, "C35": 14.9, "C40": 13.1, "C45": 12.1, "C50": 11.3},
        0.05: {"C20": 21.0, "C25": 16.8, "C30": 14.0, "C35": 12.0, "C40": 10.5, "C45": 9.7, "C50": 9.1},
        0.06: {"C20": 17.6, "C25": 14.1, "C30": 11.7, "C35": 10.0, "C40": 8.8, "C45": 8.1, "C50": 7.6},
        0.07: {"C20": 15.1, "C25": 12.1, "C30": 10.1, "C35": 8.6, "C40": 7.6, "C45": 7.0, "C50": 6.5},
        0.08: {"C20": 13.3, "C25": 10.6, "C30": 8.9, "C35": 7.6, "C40": 6.6, "C45": 6.1, "C50": 5.7},
        0.09: {"C20": 11.9, "C25": 9.5, "C30": 7.9, "C35": 6.8, "C40": 5.9, "C45": 5.5, "C50": 5.1},
        0.10: {"C20": 10.7, "C25": 8.6, "C30": 7.1, "C35": 6.1, "C40": 5.4, "C45": 5.0, "C50": 4.6},
        0.11: {"C20": 9.8, "C25": 7.8, "C30": 6.5, "C35": 5.6, "C40": 4.9, "C45": 4.5, "C50": 4.2},
        0.12: {"C20": 9.0, "C25": 7.2, "C30": 6.0, "C35": 5.1, "C40": 4.5, "C45": 4.2, "C50": 3.9},
        0.13: {"C20": 8.4, "C25": 6.7, "C30": 5.6, "C35": 4.8, "C40": 4.2, "C45": 3.9, "C50": 3.6},
        0.14: {"C20": 7.8, "C25": 6.2, "C30": 5.2, "C35": 4.5, "C40": 3.9, "C45": 3.6, "C50": 3.4},
        0.15: {"C20": 7.3, "C25": 5.8, "C30": 4.9, "C35": 4.2, "C40": 3.7, "C45": 3.4, "C50": 3.1},
        0.16: {"C20": 6.9, "C25": 5.5, "C30": 4.6, "C35": 3.9, "C40": 3.4, "C45": 3.2, "C50": 3.0},
        0.17: {"C20": 6.5, "C25": 5.2, "C30": 4.3, "C35": 3.7, "C40": 3.2, "C45": 3.0, "C50": 2.8},
        0.18: {"C20": 6.2, "C25": 4.9, "C30": 4.1, "C35": 3.5, "C40": 3.1, "C45": 2.8, "C50": 2.7},
        0.19: {"C20": 5.9, "C25": 4.7, "C30": 3.9, "C35": 3.4, "C40": 2.9, "C45": 2.7, "C50": 2.5},
        0.20: {"C20": 5.6, "C25": 4.5, "C30": 3.7, "C35": 3.2, "C40": 2.8, "C45": 2.6, "C50": 2.4},
        0.21: {"C20": 5.4, "C25": 4.3, "C30": 3.6, "C35": 3.1, "C40": 2.7, "C45": 2.5, "C50": 2.3},
        0.22: {"C20": 5.1, "C25": 4.1, "C30": 3.4, "C35": 2.9, "C40": 2.6, "C45": 2.4, "C50": 2.2},
        0.23: {"C20": 4.9, "C25": 3.9, "C30": 3.3, "C35": 2.8, "C40": 2.5, "C45": 2.3, "C50": 2.1},
        0.24: {"C20": 4.7, "C25": 3.8, "C30": 3.2, "C35": 2.7, "C40": 2.4, "C45": 2.2, "C50": 2.1},
        0.25: {"C20": 4.6, "C25": 3.7, "C30": 3.1, "C35": 2.6, "C40": 2.3, "C45": 2.1, "C50": 2.0},
        0.26: {"C20": 4.4, "C25": 3.5, "C30": 2.9, "C35": 2.5, "C40": 2.2, "C45": 2.0, "C50": 1.9},
        0.27: {"C20": 4.3, "C25": 3.4, "C30": 2.8, "C35": 2.4, "C40": 2.1, "C45": 2.0, "C50": 1.8},
        0.28: {"C20": 4.1, "C25": 3.3, "C30": 2.7, "C35": 2.3, "C40": 2.0, "C45": 1.9, "C50": 1.8},
        0.29: {"C20": 4.0, "C25": 3.2, "C30": 2.7, "C35": 2.3, "C40": 2.0, "C45": 1.9, "C50": 1.7},
        0.30: {"C20": 3.9, "C25": 3.1, "C30": 2.6, "C35": 2.2, "C40": 1.9, "C45": 1.8, "C50": 1.7},
        0.31: {"C20": 3.8, "C25": 3.0, "C30": 2.5, "C35": 2.2, "C40": 1.9, "C45": 1.8, "C50": 1.6},
        0.32: {"C20": 3.7, "C25": 3.0, "C30": 2.5, "C35": 2.1, "C40": 1.8, "C45": 1.7, "C50": 1.6},
        0.33: {"C20": 3.6, "C25": 2.9, "C30": 2.4, "C35": 2.1, "C40": 1.8, "C45": 1.7, "C50": 1.5},
        0.34: {"C20": 3.5, "C25": 2.8, "C30": 2.3, "C35": 2.0, "C40": 1.8, "C45": 1.6, "C50": 1.5},
        0.35: {"C20": 3.4, "C25": 2.7, "C30": 2.3, "C35": 2.0, "C40": 1.7, "C45": 1.6, "C50": 1.5},
        0.36: {"C20": 3.3, "C25": 2.7, "C30": 2.2, "C35": 1.9, "C40": 1.7, "C45": 1.5, "C50": 1.4},
        0.37: {"C20": 3.3, "C25": 2.6, "C30": 2.2, "C35": 1.9, "C40": 1.6, "C45": 1.5, "C50": 1.4},
        0.38: {"C20": 3.2, "C25": 2.6, "C30": 2.1, "C35": 1.8, "C40": 1.6, "C45": 1.5, "C50": 1.4},
        0.39: {"C20": 3.1, "C25": 2.5, "C30": 2.0, "C35": 1.8, "C40": 1.5, "C45": 1.4, "C50": 1.3},
        0.40: {"C20": 3.1, "C25": 2.5, "C30": 2.0, "C35": 1.8, "C40": 1.5, "C45": 1.4, "C50": 1.3},
        0.41: {"C20": 2.9, "C25": 2.4, "C30": 2.0, "C35": 1.7, "C40": 1.5, "C45": 1.4, "C50": 1.3},
        0.42: {"C20": 2.9, "C25": 2.4, "C30": 2.0, "C35": 1.7, "C40": 1.5, "C45": 1.4, "C50": 1.3},
        0.43: {"C20": 2.8, "C25": 2.3, "C30": 1.9, "C35": 1.6, "C40": 1.4, "C45": 1.3, "C50": 1.2},
        0.44: {"C20": 2.8, "C25": 2.3, "C30": 1.9, "C35": 1.6, "C40": 1.4, "C45": 1.3, "C50": 1.2},
        0.45: {"C20": 2.8, "C25": 2.2, "C30": 1.9, "C35": 1.6, "C40": 1.4, "C45": 1.3, "C50": 1.2},
    }

        #achar o valor de Bx:
    def achar_bx_por_kc(self, kc_calculado, fck):
        tabela = self.tabela_kc
        chave_fck = f"C{int(fck)}"
        melhor_bx = None
        menor_erro = float("inf")
        for bx, valores in tabela.items():
            kc_tabela = valores[chave_fck]
            erro = abs(kc_calculado - kc_tabela)
            if erro < menor_erro:
                menor_erro = erro
                melhor_bx = bx
        return melhor_bx

        #achar valor de Ks:
    def achar_ks(self,d,momento):
        self.tabelaKc()
        if momento == 0:
            return 0
        kc = ((100) * d* d) / (momento*100* 1.4) #d=self.h-2,5 para Mpositivos e h-2 para Mnegativso
        bx = self.achar_bx_por_kc(kc, float(self.fck_conc.currentText()))
        if 0.01<= bx<=0.05:
            return 0.023
        elif 0.06<= bx<=0.15:
            return 0.024
        elif 0.16<=bx<=0.24:
            return 0.025
        elif 0.25<=bx<=0.33:
            return 0.026
        elif 0.34<=bx<=0.40:
            return 0.027
        elif 0.40<=bx<=0.45:
            return 0.028

    def geralAs(self,ks,momento,d):#colocar o coef extra de laje em balanço
        As=(ks*1.4*momento*100/d)
        return As
    def calc_As(self):
        # d para positivo e negativo
        d_pos = self.h - 2.5
        d_neg = self.h - 2.0
        # Ks
        ks_Mx = self.achar_ks(d_pos, self.Mx)
        ks_My = self.achar_ks(d_pos, self.My)
        ks_Mx_linha = self.achar_ks(d_neg, self.Mx_linha)
        ks_My_linha = self.achar_ks(d_neg, self.My_linha)
        # As
        self.Asx = self.geralAs(ks_Mx, self.Mx, d_pos)
        self.Asy = self.geralAs(ks_My, self.My, d_pos)
        self.Asx_linha = self.geralAs(ks_Mx_linha, self.Mx_linha, d_neg)
        self.Asy_linha = self.geralAs(ks_My_linha, self.My_linha, d_neg)
        #defininfo armadura minima e pegando a maior valor
        As_p_min=self.arm_minima(0.67*self.h)
        As_n_min=self.arm_minima(self.h)
        if self.ly/self.lx >=2:
            As_p_min=self.arm_minima(self.h)
        self.Asx = max(self.Asx, As_p_min)
        self.Asy = max(self.Asy, As_p_min)
        self.Asx_linha = max(self.Asx_linha, As_n_min)
        self.Asy_linha = max(self.Asy_linha, As_n_min)
#detalhamento
    def tabela_armadura(self):
        self.tabela_As = {
            7.0: {4.2: 1.98, 5.0: 2.86, 6.3: 4.50, 8.0: 7.14, 10.0: 11.43, 12.5: 17.86},
            7.5: {4.2: 1.85, 5.0: 2.67, 6.3: 4.20, 8.0: 6.67, 10.0: 10.67, 12.5: 16.67},
            8.0: {4.2: 1.73, 5.0: 2.50, 6.3: 3.94, 8.0: 6.25, 10.0: 10.00, 12.5: 15.63},
            8.5: {4.2: 1.63, 5.0: 2.35, 6.3: 3.71, 8.0: 5.88, 10.0: 9.41, 12.5: 14.71},
            9.0: {4.2: 1.54, 5.0: 2.22, 6.3: 3.50, 8.0: 5.56, 10.0: 8.89, 12.5: 13.89},
            9.5: {4.2: 1.46, 5.0: 2.11, 6.3: 3.32, 8.0: 5.26, 10.0: 8.42, 12.5: 13.16},
            10.0: {4.2: 1.39, 5.0: 2.00, 6.3: 3.15, 8.0: 5.00, 10.0: 8.00, 12.5: 12.50},
            11.0: {4.2: 1.26, 5.0: 1.82, 6.3: 2.86, 8.0: 4.55, 10.0: 7.27, 12.5: 11.36},
            12.0: {4.2: 1.15, 5.0: 1.67, 6.3: 2.62, 8.0: 4.17, 10.0: 6.67, 12.5: 10.42},
            12.5: {4.2: 1.11, 5.0: 1.60, 6.3: 2.52, 8.0: 4.00, 10.0: 6.40, 12.5: 10.00},
            13.0: {4.2: 1.07, 5.0: 1.54, 6.3: 2.42, 8.0: 3.85, 10.0: 6.15, 12.5: 9.62},
            14.0: {4.2: 0.99, 5.0: 1.43, 6.3: 2.25, 8.0: 3.57, 10.0: 5.71, 12.5: 8.93},
            15.0: {4.2: 0.92, 5.0: 1.33, 6.3: 2.10, 8.0: 3.33, 10.0: 5.33, 12.5: 8.33},
            16.0: {4.2: 0.87, 5.0: 1.25, 6.3: 1.97, 8.0: 3.13, 10.0: 5.00, 12.5: 7.81},
            17.0: {4.2: 0.81, 5.0: 1.18, 6.3: 1.85, 8.0: 2.94, 10.0: 4.71, 12.5: 7.35},
            17.5: {4.2: 0.79, 5.0: 1.14, 6.3: 1.80, 8.0: 2.86, 10.0: 4.57, 12.5: 7.14},
            18.0: {4.2: 0.77, 5.0: 1.11, 6.3: 1.75, 8.0: 2.78, 10.0: 4.44, 12.5: 6.94},
            19.0: {4.2: 0.73, 5.0: 1.05, 6.3: 1.66, 8.0: 2.63, 10.0: 4.21, 12.5: 6.58},
            20.0: {4.2: 0.69, 5.0: 1.00, 6.3: 1.58, 8.0: 2.50, 10.0: 4.00, 12.5: 6.25},
        }

    def achar_espacamento(self, As_calc, diametro):
        if not hasattr(self, "tabela_As"):
            self.tabela_armadura()
        melhor_espacamento = None
        menor_As_valido = float("inf")
        for espacamento, valores in self.tabela_As.items():
            As_tabela = valores.get(diametro)
            if As_tabela is None:
                continue
            # queremos o menor valor >= As_calc
            if As_tabela >= As_calc and As_tabela < menor_As_valido:
                menor_As_valido = As_tabela
                melhor_espacamento = espacamento
        return melhor_espacamento

    def dados_desenhar_detalhamento_positivo(self):
        self.Llajes()
        #self.calcular_apoio()
        self.escolher_calcular_momentos()
        self.calc_As()
        self.esAsx = self.achar_espacamento(self.Asx, float(self.d_armadura.currentText()))
        self.esAsy = self.achar_espacamento(self.Asy, float(self.d_armadura.currentText()))
        # 🚨 PROTEÇÃO
        if self.esAsx is None or self.esAsy is None:
            self.detalhar.setText("Erro: diâmetro pequeno")
            return False  # interrompe tudo
        # se passou, volta texto normal
        self.detalhar.setText("Detalhamento As positiva")
        self.n_barras_Asy=int(self.lx/self.esAsy)
        self.n_barras_Asx = int(self.ly / self.esAsx)
        return True

    def dados_desenhar_detalhamento_negativo(self):
        self.Llajes()
        #self.calcular_apoio()
        self.escolher_calcular_momentos()
        self.calc_As()
        self.esAsx_linha = self.achar_espacamento(self.Asx_linha, float(self.d_armadura.currentText()))
        self.esAsy_linha = self.achar_espacamento(self.Asy_linha, float(self.d_armadura.currentText()))
        if self.esAsx_linha is None or self.esAsy_linha is None:
            self.detalhar_neg.setText("Erro: diâmetro pequeno")
            return False  # interrompe tudo
            # se passou, volta texto normal
        self.detalhar_neg.setText("Detalhamento As negativa")
        self.n_barras_Asy_linha = int(self.lx / self.esAsy_linha)
        self.n_barras_Asx_linha = int(self.ly / self.esAsx_linha)
        return True


    def desenhar_detalhamento_positivo(self):
        import matplotlib.pyplot as plt
        ok = self.dados_desenhar_detalhamento_positivo()
        if not ok:
            return
        fig, ax = plt.subplots()
        lx = self.lx
        ly = self.ly
        # ===== RETÂNGULO =====
        ax.plot([0, 0, lx, lx, 0], [0, ly, ly, 0, 0])
        # FUNÇÕES
        def cota_horizontal():
            y_cota_top = ly * 0.85
            ax.annotate('',xy=(lx * 0.001, y_cota_top),xytext=(lx * 0.999, y_cota_top),arrowprops=dict(arrowstyle='<->'))
            ax.text(lx / 2,y_cota_top + 10,f"N Ø {self.d_armadura.currentText()} - {self.n_barras_Asy} c/{self.esAsy}",ha='center',va='bottom')
        def cota_vertical():
            x_cota_left = lx * 0.15
            ax.annotate('',xy=(x_cota_left, ly * 0.001),xytext=(x_cota_left, ly * 0.999),arrowprops=dict(arrowstyle='<->'))
            ax.text(x_cota_left - 10,ly / 2,f"N Ø {self.d_armadura.currentText()} - {self.n_barras_Asx} c/{self.esAsx}",rotation=90,ha='right',va='center')
        def barra_horizontal():
            offset = 50
            comp = lx
            x_ini = (lx - comp) / 2
            x_fim = x_ini + comp
            y_barra1 = ly + offset
            y_barra2 = ly + offset + 1
            ax.plot([x_ini, x_fim],[y_barra1, y_barra1],linewidth=3,color='black')
            ax.plot([x_ini, x_fim],[y_barra2, y_barra2],linewidth=3,color='black')
            ax.text(lx / 2,y_barra1 - 10,f"N - {self.n_barras_Asx} Ø {self.d_armadura.currentText()} C=",ha='center',va='top')
        def barra_vertical():
            offset = 50
            comp = ly
            y_ini = (ly - comp) / 2
            y_fim = y_ini + comp
            x_barra1 = lx + offset
            x_barra2 = lx + offset + 1
            ax.plot([x_barra1, x_barra1],[y_ini, y_fim],linewidth=3,color='black')
            ax.plot([x_barra2, x_barra2],[y_ini, y_fim],linewidth=3,color='black')
            ax.text(x_barra1 + (offset / 2),ly / 2,f"N - {self.n_barras_Asy} Ø {self.d_armadura.currentText()} C=",rotation=90,ha='center',va='center')
        # MAPA
        mapa = self.escolher_calcular_desenho_positivo()
        # EXECUÇÃO
        elementos = mapa.get(self.tipolaje, [])
        if "CH" in elementos:
            cota_horizontal()
        if "CV" in elementos:
            cota_vertical()
        if "BH" in elementos:
            barra_horizontal()
        if "BV" in elementos:
            barra_vertical()
        # VISUAL
        ax.set_xlim(-50, lx + 50)
        ax.set_ylim(-50, ly + 50)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.show()

    def desenhar_detalhamento_negativo(self):
        import matplotlib.pyplot as plt
        ok = self.dados_desenhar_detalhamento_negativo()
        if not ok:
            return  # 🚨 NÃO DESENHA se deu erro
        self.dados_desenhar_detalhamento_negativo()
        fig, ax = plt.subplots()
        lx = self.lx
        ly = self.ly
        # quadrado
        ax.plot([0, 0, lx, lx, 0], [0, ly, ly, 0, 0])
        offset = 70
        offset2 = offset * 2
        desloc = 170
        lw = 3
        gancho = 8
        comprimento = 150
        lw1 = 0.3
        # ===== BARRA COM GANCHO =====
        def barra_com_gancho(xs, ys):
            ax.plot(xs, ys, color='black', linewidth=lw)
            if max(xs) - min(xs) > max(ys) - min(ys):  # horizontal
                x_ini = min(xs)
                x_fim = max(xs)
                y_ref = ys[0]
                ax.plot([x_ini, x_ini], [y_ref, y_ref - gancho], color='black', linewidth=lw)
                ax.plot([x_fim, x_fim], [y_ref, y_ref - gancho], color='black', linewidth=lw)
            else:  # vertical
                y_ini = min(ys)
                y_fim = max(ys)
                x_ref = xs[0]
                ax.plot([x_ref, x_ref + gancho], [y_ini, y_ini], color='black', linewidth=lw)
                ax.plot([x_ref, x_ref + gancho], [y_fim, y_fim], color='black', linewidth=lw)
        # ===== FUNÇÃO DE CANTO =====
        def desenhar_canto(canto):
            if canto == "SE":  # superior esquerdo
                barra_com_gancho([0, desloc, 0, -desloc / 2], [ly + offset] * 4)
                barra_com_gancho([0, desloc / 2, 0, -desloc], [ly + offset2] * 4)
                ax.plot([0, 0], [ly, ly + comprimento], color='black', linewidth=lw1)
                ax.text(0, ly + offset - 10, f"N - {self.n_barras_Asx_linha} Ø {self.d_armadura.currentText()} C=", ha='center', va='top',fontsize=9)
                ax.text(0, ly + offset2 + 10, "123", ha='center', va='bottom')
                x_cota_left = lx * 0.15
                ax.annotate('', xy=(x_cota_left, ly * 0.001), xytext=(x_cota_left, ly * 0.999),arrowprops=dict(arrowstyle='<->'))
                ax.text(x_cota_left - 10, ly / 2,f"N Ø {self.d_armadura.currentText()} - {self.n_barras_Asx_linha} c/{self.esAsx_linha}", rotation=90,ha='right', va='center')
            elif canto == "SD":  # superior direito
                barra_com_gancho([lx + offset] * 4, [ly, desloc + ly, ly, ly - desloc / 2])
                barra_com_gancho([lx + offset2] * 4, [ly, ly + desloc / 2, ly, ly - desloc])
                ax.plot([lx, lx + comprimento], [ly, ly], color='black', linewidth=lw1)
                ax.text(lx + offset - 10, ly, "123", rotation=90, ha='right', va='center')
                ax.text(lx + offset2 + 50, ly, f"N - {self.n_barras_Asy_linha} Ø {self.d_armadura.currentText()} C=", rotation=90, ha='right', va='center',fontsize=9)
                y_cota_top = ly * 0.85
                ax.annotate('', xy=(lx * 0.001, y_cota_top), xytext=(lx * 0.999, y_cota_top),arrowprops=dict(arrowstyle='<->'))
                ax.text(lx / 2, y_cota_top + 10,f"N Ø {self.d_armadura.currentText()} - {self.n_barras_Asy_linha} c/{self.esAsy_linha}", ha='center',va='bottom')
            elif canto == "IE":  # inferior esquerdo
                barra_com_gancho([-offset] * 4, [0, desloc, 0, -desloc / 2])
                barra_com_gancho([-offset2] * 4, [0, desloc / 2, 0, -desloc])
                ax.plot([0, -comprimento], [0, 0], color='black', linewidth=lw1)
                ax.text(-offset2 - 10, 0, "123", rotation=90, ha='right', va='center')
                ax.text(-offset + 10, 0, f"N - {self.n_barras_Asy_linha} Ø {self.d_armadura.currentText()} C=", rotation=90, ha='left', va='center',fontsize=9)
                y_cota_top = ly * 0.85
                ax.annotate('', xy=(lx * 0.001, y_cota_top), xytext=(lx * 0.999, y_cota_top),arrowprops=dict(arrowstyle='<->'))
                ax.text(lx / 2, y_cota_top + 10,f"N Ø {self.d_armadura.currentText()} - {self.n_barras_Asy_linha} c/{self.esAsy_linha}", ha='center',va='bottom')
            elif canto == "ID":  # inferior direito
                barra_com_gancho([lx, lx - desloc, lx, lx + desloc / 2], [-offset] * 4)
                barra_com_gancho([lx, lx - desloc / 2, lx, lx + desloc], [-offset2] * 4)
                ax.plot([lx, lx], [0, -comprimento], color='black', linewidth=lw1)
                ax.text(lx, -offset + 15, "123", ha='center', va='bottom')
                ax.text(lx, -offset2 - 15, f"N - {self.n_barras_Asx_linha} Ø {self.d_armadura.currentText()} C=", ha='center', va='top',fontsize=9)
                x_cota_left = lx * 0.15
                ax.annotate('', xy=(x_cota_left, ly * 0.001), xytext=(x_cota_left, ly * 0.999),arrowprops=dict(arrowstyle='<->'))
                ax.text(x_cota_left - 10, ly / 2,f"N Ø {self.d_armadura.currentText()} - {self.n_barras_Asx_linha} c/{self.esAsx_linha}", rotation=90,ha='right', va='center')
        # ===== MAPA DE LAJES =====
        # mapa_lajes = {
        #     "6": ["SE", "SD", "IE", "ID"],
        #     "2A": ["IE"],
        #     "2B": ["ID"],
        #     "3": ["IE", "ID"],
        #     "4A": ["SD", "IE"],
        #     "4B": ["ID", "SE"],
        #     "5A": ["SD", "ID", "IE"],
        #     "5B": ["ID", "IE", "SE"],
        # }
        mapa_lajes = self.escolher_calcular_desenho_negativo()
        # ===== EXECUÇÃO =====
        for canto in mapa_lajes.get(self.tipolaje, []):
            desenhar_canto(canto)
        # ===== VISUAL =====
        ax.set_xlim(-200, lx + 200)
        ax.set_ylim(-200, ly + 200)
        ax.set_aspect('equal')
        ax.axis('off')

        plt.show()

#Sessao para escolher o calculo( se laje unidirecional ou bidirecional) e suas funções auxiliares
    def escolher_calcular_apoio(self):
        if (self.ly/self.lx) >= 2:
            return self.calcular_apoio_uni()
        else:
            return self.calcular_apoio() #essa funcao foi feita em cima

    def calcular_apoio_uni(self):
        self.Llajes()
        lx=self.lx/100
        self.vx = 0
        self.vy = 0
        self.vx_linha = 0
        self.vy_linha = 0
        self.Vy = 0
        self.Vy_linha = 0
        tipo = self.tiposdelaje.currentText()
        if tipo in ["1", "2A", "4A"]:  # biapoiada
            self.Vx = self.p * lx / 2
            self.Vx_linha = self.p * lx / 2
        elif tipo in ["2B", "3", "5A"]:  # engastada e apoiada
            self.Vx = (3 / 8) * self.p * lx
            self.Vx_linha = (5 / 8) * self.p * lx
        elif tipo in ["4B", "5B", "6"]:  # biengastada
            self.Vx = self.p * lx / 2
            self.Vx_linha = self.p * lx / 2
        elif tipo in ["9","10"]:
            self.Vx=0
            self.Vx_linha=self.p*lx #colocar coef extra de balanço tab4

    def escolher_calcular_momentos(self):
        if self.ly / self.lx >= 2:
            return self.calcular_momentos_uni()
        else:
            return self.calcular_momentos() #essa funcao aqui esta la em cima no codigo

    def calcular_momentos_uni(self):
        self.Llajes()
        lx = self.lx / 100
        tipo=self.tiposdelaje.currentText()
        self.mux = 0
        self.muy = 0
        self.mux_linha = 0
        self.muy_linha = 0
        self.My = 0
        self.My_linha = 0
        self.Mx = 1
        self.Mx_linha = 1
        if tipo == "1" or tipo== "2A" or tipo=="4A":  # biapoiada
            self.Mx=self.p*lx*lx/8
            self.Mx_linha=0
        if tipo == "2B" or tipo== "3" or tipo== "5A":  # engastada e apoiada
            self.Mx = self.p*lx*lx/14.22
            self.Mx_linha = self.p*lx*lx/8
        if tipo == "4B" or tipo=="5B" or tipo=="6":  # biengastada
            self.Mx = self.p*lx*lx/24
            self.Mx_linha = self.p*lx*lx/12
        if tipo == "9" or tipo == "10":  # engastada e livre
            self.Mx_linha = self.p*lx*lx/2 * self.coef_momento_uni() # coef extra de balanço

    def escolher_calcular_desenho_negativo(self):
        if self.ly / self.lx >= 2:
            return self.desenho_negativo_uni()
        else:
            return self.desenho_negativo_bi()

    def desenho_negativo_uni(self):
        mapa_lajes = {
            "6": ["SE", "ID"],
            "2A": [],
            "2B": ["ID"],
            "3": ["ID"],
            "4A": [],
            "4B": ["ID", "SE"],
            "5A": ["ID"],
            "5B": ["ID", "SE"],
            "9": ["SE"],
            "10": ["SE"],
        }
        return mapa_lajes

    def desenho_negativo_bi(self):
        mapa_lajes = {
            "6": ["SE", "SD", "IE", "ID"],
            "2A": ["IE"],
            "2B": ["ID"],
            "3": ["IE", "ID"],
            "4A": ["SD", "IE"],
            "4B": ["ID", "SE"],
            "5A": ["SD", "ID", "IE"],
            "5B": ["ID", "IE", "SE"],
        }
        return mapa_lajes


    def escolher_calcular_desenho_positivo(self):
        if self.ly / self.lx >= 2:
            return self.desenho_positivo_uni()
        else:
            return self.desenho_positivo_bi()

    def desenho_positivo_bi(self):
        mapa = {
            "1": ["CH", "CV", "BH", "BV"],
            "2A": ["CH", "CV", "BH", "BV"],
            "2B": ["CH", "CV", "BH", "BV"],
            "3": ["CH", "CV", "BH", "BV"],
            "4A": ["CH", "CV", "BH", "BV"],
            "4B": ["CH", "CV", "BH", "BV"],
            "5A": ["CH", "CV", "BH", "BV"],
            "5B": ["CH", "CV", "BH", "BV"],
            "6": ["CH", "CV", "BH", "BV"],
        }
        return mapa

    def desenho_positivo_uni(self):
        mapa = {
            "1": ["CV", "BH"],
            "2A": ["CV", "BH"],
            "2B": ["CV", "BH"],
            "3": ["CV", "BH"],
            "4A": ["CV", "BH"],
            "4B": ["CV", "BH"],
            "5A": ["CV", "BH"],
            "5B": ["CV", "BH"],
            "6": ["CV", "BH"],
        }
        return mapa

    def coef_momento_uni(self):
        yn=1.95-(0.05*self.h)
        return yn



if __name__ == '__main__':
    app = QApplication([])
    window = LajesUI()
    window.show()
    app.exec_()

