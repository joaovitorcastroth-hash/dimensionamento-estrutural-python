from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from sympy import symbols, Eq, solve
from PyQt5.QtWidgets import QTableWidgetItem
from PilaresV1 import PilarCA
import math
import sys

def excecao_customizada(tipo, valor, traceback_obj):
    import traceback
    traceback.print_exception(tipo, valor, traceback_obj)

sys.excepthook = excecao_customizada
class JanelaSecundaria(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("PilaresCAv2.ui", self)
        self.calcular_momento_total.clicked.connect(self.escrever_momento)
    def pegar_dados(self):
        self.L_inferior=float(self.l_inferior.text())
        self.L_superior = float(self.l_superior.text())
        self.momentoviga=float(self.momento_viga.text())
    def calcular_momento(self):
        self.pegar_dados()
        self.momento_propagado_inferior=(self.momentoviga*(1/self.L_inferior))/((1/self.L_inferior)+(1/self.L_superior))
        self.momento_propagado_superior=(self.momentoviga*(1/self.L_superior))/((1/self.L_inferior)+(1/self.L_superior))
        momento_maior=max(self.momento_propagado_inferior,self.momento_propagado_superior)
        momento_t= self.momentoviga+momento_maior
        return momento_t
    def escrever_momento(self):
        momento=self.calcular_momento()
        if self.momento_propagado_superior>self.momento_propagado_inferior:
            self.momento_total.setText(str(f"Mk,topo={momento:.1f}"))
        if self.momento_propagado_superior < self.momento_propagado_inferior:
            self.momento_total.setText(str(f"Mk,base={momento:.1f}"))
        else:
            self.momento_total.setText(str(f"Mk,base=Mk,topo={momento:.1f}"))

class PilaresCACopia_reorganizadoUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('PilaresCACopia_reorganizado.ui', self)
        self.pilar_tipo.currentTextChanged.connect(self.bloquear_campos)
        self.bloquear_campos()
        self.calcular_prop.clicked.connect(self.grande_pequeno_e)
        self.calcular_prop.clicked.connect(self.preencher_dados)
        self.calcular_pre_lados.clicked.connect(self.pre_dimens_lados)
        self.numero_barras_botao.clicked.connect(self.cal_numero_barras)
        self.momento_mkx.setText("0")
        self.momento_mky.setText("0")
        self.lado_lx.setText("0")
        self.lado_ly.setText("0")

        self.momento_mkx.setText("2041")
        self.momento_mky.setText("1360.5")
        self.altura_lexy.setText("350")
        self.lado_lx.setText("18")
        self.lado_ly.setText("50")
        self.normal_nk.setText("850")
        self.valor_d_linha.setText("5")
        self.pegar_dados()
        self.calcular_momento_janela.clicked.connect(self.abrir_janela)
    def abrir_janela(self):
        self.PilaresCAv2 = JanelaSecundaria()
        self.PilaresCAv2.show()


    def bloquear_campos(self):
        opcao = self.pilar_tipo.currentText()
        if opcao == "Intermediário":
            self.momento_mkx.setEnabled(False)
            self.momento_mky.setEnabled(False)
        else:
            self.momento_mkx.setEnabled(True)
            self.momento_mky.setEnabled(True)
        self.distribuicao_obliqua.setEnabled(opcao == "Canto")
        self.label_17.setEnabled(opcao == "Canto")
        #pre dimensionamento

    def pre_dimens_lados(self):
        self.pegar_dados()
        self.combobox()
        nd = self.nk * 1.4 * 1.25
        ac = nd / ((0.5 * (self.fck / 10)) + 0.4)
        if ac < 360:
            ac = 360
        lx = 14
        ly = int(ac / lx)
        self.lado_lx.setText(str(lx))
        self.lado_ly.setText(str(ly))

    def pegar_dados(self):
        self.d_linha = float(self.valor_d_linha.text())
        self.nk = float(self.normal_nk.text())
        self.mkx_grau1 = float(self.momento_mkx.text())
        self.mky_grau1 = float(self.momento_mky.text())
        self.lx = float(self.lado_lx.text())
        self.ly = float(self.lado_ly.text())
        self.lexy=float(self.altura_lexy.text())
        self.dx = self.lx - self.d_linha
        self.dy = self.ly - self.d_linha
        # self.ey = self.mdy / self.nd
    def preparar_dados(self):
        self.pegar_dados()
        self.valores_calculo()
        self.esbeltez_limite()
        self.momentos_totais()
    def combobox(self):
        self.fck = float(self.fck_conc.currentText())

    def valores_calculo(self): #ver tabela 6
        self.pegar_dados()
        self.nd = self.nk * 1.4 * self.ajudar_valores_calculo()
        self.mdx_grau1 = self.mkx_grau1 * 1.4 * self.ajudar_valores_calculo()
        self.mdy_grau1 = self.mky_grau1 * 1.4 * self.ajudar_valores_calculo()
        self.e1x = self.mdx_grau1 / self.nd
        self.e1y = self.mdy_grau1 / self.nd
        print("Mdx =", self.mdx_grau1)
        print("Mdy =", self.mdy_grau1)
    def ajudar_valores_calculo(self):
        gamma_n=(1.95-0.05*min(self.lx,self.ly))
        if min(self.lx,self.ly)>=19:
            gamma_n=1
        return gamma_n
#fazer aql calcula da norma)
    def momentos_totais(self):
        self.pegar_dados()
        self.valores_calculo()
        opcao = self.pilar_tipo.currentText()
        mdx_grau2,mdy_grau2=self.usar_momento_segunda_ordem()
        momento_min_x = self.momento_minimo(self.lx)
        momento_min_y = self.momento_minimo(self.ly)
        if opcao == "Intermediário":
            self.mdx_total = momento_min_x+mdx_grau2 #aql calculo da norma(só mom de 2grau)
            print(f"Momentos em x:{momento_min_x}(minimo) e {mdx_grau2}(maximo). Total={self.mdx_total}")
            self.mdy_total = momento_min_y+mdy_grau2 #msm coisa da de cima
            print(f"Momentos em y:{momento_min_y}(minimo) e {mdy_grau2}(maximo). Ttotal={self.mdy_total}")
        elif opcao == "Extremidade":
            maiorx=max(self.mdx_grau1,momento_min_x)
            maiory=max(self.mdy_grau1,momento_min_y)
            self.mdx_total=maiorx+mdx_grau2
            self.mdy_total=maiory+mdy_grau2
        elif opcao == "Canto":
            maiorx=max(self.mdx_grau1,momento_min_x)
            maiory=max(self.mdy_grau1,momento_min_y)
            self.mdx_total=maiorx+mdx_grau2
            self.mdy_total=maiory+mdy_grau2

    def excentricidades(self):
        self.ex = self.mdx_total / self.nd
        self.ey = self.mdy_total / self.nd
        return max(self.ex, self.ey)

    def indice_esbeltez(self, lexy, l1):
        return 3.46*lexy/l1

    def momento_minimo(self, h):
        mom_min = self.nd*(1.5+0.03*h)
        return mom_min

    def esbeltez_limite(self):
        opcao = self.pilar_tipo.currentText()
        if opcao == "Intermediário":
            self.lamb1x = 35
            self.lamb1y = 35
        if opcao == "Extremidade" or opcao == "Canto":
            if self.mdx_grau1<self.momento_minimo(self.lx):
                self.lamb1x=35
            if self.mdy_grau1<self.momento_minimo(self.ly):
                self.lamb1y=35

            if self.mdx_grau1>self.momento_minimo(self.lx):
                ab=0.6+(0.4*(-self.mdx_grau1/self.mdx_grau1))
                if ab >=0.4:
                    ab= 0.6+(0.4*(-self.mdx_grau1/self.mdx_grau1))
                else:
                    ab=0.4
                self.lamb1x = (25+(12.5*self.e1x/self.lx))/ab
                if self.lamb1x<=35:
                    self.lamb1x=35
                else:
                    self.lamb1x = (25 + (12.5 * self.e1x / self.lx)) / ab
            if self.mdy_grau1 > self.momento_minimo(self.ly):
                ab = 0.6 + (0.4 * (-self.mdy_grau1 / self.mdy_grau1))
                if ab >= 0.4:
                    ab = 0.6 + (0.4 * (-self.mdy_grau1 / self.mdy_grau1))
                else:
                    ab = 0.4
                self.lamb1y = (25 + (12.5 * self.e1y / self.ly)) / ab
                if self.lamb1y<=35:
                    self.lamb1y=35
                else:
                    self.lamb1y = (25 + (12.5 * self.e1y / self.ly)) / ab



    #compara lambda com lambda limite para ver necessidade de calcular mom de 2grau
    def usar_momento_segunda_ordem(self):
        lamb_x = self.indice_esbeltez(self.lexy,self.lx)
        lamb_y = self.indice_esbeltez(self.lexy,self.ly)
        momento_x = 0
        momento_y = 0
        if lamb_x > self.lamb1x:
            momento_x = self.calc_momento_seg_ordem(self.lx,self.ly)
        if lamb_y > self.lamb1y:
            momento_y = self.calc_momento_seg_ordem(self.ly,self.lx)
        return momento_x, momento_y

    def calc_momento_seg_ordem(self,h1,h2):
        self.combobox()
        v=self.nd/(h1*h2*(self.fck/14))
        #print(v)
        r=0.005/(h1*(v+0.5))
        #print(r)
        e2=self.lexy*self.lexy*r/10
        #print(e2)
        m2d=self.nd*e2
        return m2d

    def grande_pequeno_e(self):
        self.as_sim_x.setText(str(""))
        self.as_sim_x2.setText(str(""))
        self.as_sim_y.setText(str(""))
        self.as_sim_y2.setText(str(""))
        self.pegar_dados()
        self.valores_calculo()
        self.esbeltez_limite()
        self.momentos_totais()
        e = self.excentricidades()
        opcao = self.pilar_tipo.currentText()
        self.armadura_grande_final=0
        if opcao == "Intermediário":
            if self.ex>= self.lx/6:
                self.excentricidade_x.setText(str(f"Grande excentricidade,e={self.ex:.1f}"))
                if e == self.ex:
                    self.iteracao(self.dx, self.lx, self.ly, self.mdx_total)
                    self.as_sim_x.setText(str(f"{self.armadura_grande_final:.1f} cm²"))
                    self.as_sim_x2.setText(str(f"{self.armadura_grande_final:.1f} cm²"))
            if self.ey >= self.ly / 6:
                self.excentricidade_y.setText(str(f"Grande excentricidade,e={self.ey:.1f}"))
                if e == self.ey:
                    self.iteracao(self.dy, self.ly, self.lx, self.mdy_total)
                    self.as_sim_y.setText(str(f"{self.armadura_grande_final:.1f} cm²"))
                    self.as_sim_y2.setText(str(f"{self.armadura_grande_final:.1f} cm²"))
            if self.ex< self.lx/6:
                self.excentricidade_x.setText(str(f"Pequena excentricidade,e={self.ex:.1f}"))
                if e == self.ex:
                    self.eslim(self.lx,self.ly,self.ex)
            if self.ey < self.ly / 6:
                self.excentricidade_y.setText(str(f"Pequena excentricidade,e={self.ey:.1f}"))
                if e == self.ey:
                    self.eslim(self.ly,self.lx,self.ey)
        self.arm_minima()
        if opcao == "Extremidade":
            if self.ex >= self.lx / 6:
                self.excentricidade_x.setText(str(f"Grande excentricidade,e={self.ex:.1f}"))
                if e == self.ex:
                    self.iteracao(self.dx, self.lx, self.ly, self.mdx_total)
                    self.as_sim_x.setText(str(f"{self.armadura_grande_final:.1f} cm²"))
                    self.as_sim_x2.setText(str(f"{self.armadura_grande_final:.1f} cm²"))
            if self.ey >= self.ly / 6:
                self.excentricidade_y.setText(str(f"Grande excentricidade,e={self.ey:.1f}"))
                if e == self.ey:
                    self.iteracao(self.dy, self.ly, self.lx, self.mdy_total)
                    self.as_sim_y.setText(str(f"{self.armadura_grande_final:.1f} cm²"))
                    self.as_sim_y2.setText(str(f"{self.armadura_grande_final:.1f} cm²"))
            if self.ex < self.lx / 6:
                self.excentricidade_x.setText(str(f"Pequena excentricidade,e={self.ex:.1f}"))
                if e == self.ex:
                    self.eslim(self.lx,self.ly,self.ex)
            if self.ey < self.ly / 6:
                self.excentricidade_y.setText(str(f"Pequena excentricidade,e={self.ey:.1f}"))
                if e == self.ey:
                    self.eslim(self.ly, self.lx, self.ey)
        self.arm_minima()

        if opcao=="Canto":
            print("entrou")
            resultado=self.flexao_obliqua()
            print("entrou 2")
            self.armadura_grande_final=resultado['As_sim']
            self.info_1.setText(str(f"As_sim  = {resultado['As_sim']:.2f} cm²; Erro= {resultado['erro']:.2f}%"))
            self.info_2.setText(str((f"  Mdx_calc= {resultado['Mdx_calc']:.1f}  (alvo {self.mdy_total})")))
            self.info_3.setText(str((f"  Mdy_calc= {resultado['Mdy_calc']:.1f}  (alvo {self.mdx_total})")))
            self.info_4.setText(str((f"x = {resultado['x']:.3f} cm, θ = {resultado['theta']}°")))
            bitola,area_bitola,area_n=self.escolher_bitola(self.armadura_grande_final,self.n_barras)
            self.info_5.setText(str((f"Bitola de {bitola} mm({area_bitola} cm²) para uma área de {area_n} cm²")))
        self.arm_minima()
#para flexao obliqua
    def flexao_obliqua(self): #ao chamar buscar solucao, mdx e mdy devem ser chamados INVERTIDOS, primeiro mdy dps mdx
        self.distribuicao_armadura()
        pilar = PilarCA()
        fyd=43.5
        self.obliqua = pilar.buscar_solucao(self.lx,self.ly,self.nd,self.mdy_total,self.mdx_total,self.fck/14,fyd,self.distribuicao,tolerancia=2)
        return self.obliqua
    def distribuicao_armadura(self):
        tipo = int(self.distribuicao_obliqua.currentText())
        if tipo==1:
            self.distribuicao=self.arranjo_1(self.lx,self.ly,self.d_linha,area_barra=1.0, n_por_lado=8)
            self.n_barras = len(self.distribuicao)
        if tipo==2:
            self.distribuicao = self.arranjo_2(self.lx, self.ly, self.d_linha, area_barra=1.0, n_por_lado=4)
            self.n_barras = len(self.distribuicao)
        if tipo==3:
            self.distribuicao=self.arranjo_3(self.lx,self.ly,self.d_linha,area_barra=1.0)
            self.n_barras = len(self.distribuicao)
        if tipo==4:
            self.distribuicao=self.arranjo_4(self.lx,self.ly,self.d_linha,area_barra=1.0)
            self.n_barras = len(self.distribuicao)
        if tipo==5:
            self.distribuicao=self.arranjo_5(self.lx,self.ly,self.d_linha,area_barra=1.0)
            self.n_barras = len(self.distribuicao)
        if tipo==6:
            self.distribuicao=self.arranjo_6(self.lx,self.ly,self.d_linha,area_barra=1.0)
            self.n_barras = len(self.distribuicao)


    def arranjo_1(self,lx, ly, cobrimento, area_barra=1.0, n_por_lado=8):
        """
        Arranjo 1 — muitas barras, só nas faces ESQUERDA/DIREITA
        (faces de comprimento ly). Sem barras no topo/base.
        """
        xi = lx / 2 - cobrimento
        yi = ly / 2 - cobrimento

        barras = []
        for k in range(n_por_lado):
            y = yi - k * (2 * yi / (n_por_lado - 1))
            barras.append((xi, y, area_barra))
            barras.append((-xi, y, area_barra))
        return barras

    def arranjo_2(self,lx, ly, cobrimento, area_barra=1.0, n_por_lado=4):
        """
        Arranjo 2 — igual ao 1, mas com menos barras por lado.
        """
        xi = lx / 2 - cobrimento
        yi = ly / 2 - cobrimento

        barras = []
        for k in range(n_por_lado):
            y = yi - k * (2 * yi / (n_por_lado - 1))
            barras.append((xi, y, area_barra))
            barras.append((-xi, y, area_barra))
        return barras

    def arranjo_3(self,lx, ly, cobrimento, area_barra=1.0):
        """
        Arranjo 3 — 4 cantos + 1 barra no meio de cada face
        ESQUERDA/DIREITA (sem barras no topo/base).
        6 barras no total.
        """
        xi = lx / 2 - cobrimento
        yi = ly / 2 - cobrimento

        barras = [
            (-xi, -yi, area_barra), (xi, -yi, area_barra),
            (xi, yi, area_barra), (-xi, yi, area_barra),
            (xi, 0, area_barra), (-xi, 0, area_barra),
        ]
        return barras

    def arranjo_4(self,lx, ly, cobrimento, area_barra=1.0):
        """
        Arranjo 4 — só os 4 cantos. 4 barras no total.
        Indicado só para pilares pequenos/quadrados.
        """
        xi = lx / 2 - cobrimento
        yi = ly / 2 - cobrimento

        barras = [
            (-xi, -yi, area_barra), (xi, -yi, area_barra),
            (xi, yi, area_barra), (-xi, yi, area_barra),
        ]
        return barras

    def arranjo_6(self,lx, ly, cobrimento, area_barra=1.0):
        """
        Arranjo 5 — 4 cantos + 1 barra no meio de CADA uma das 4 faces
        (esquerda, direita, topo, base). 8 barras no total.

        (Esse é exatamente o molde que você já usa.)
        """
        xi = lx / 2 - cobrimento
        yi = ly / 2 - cobrimento

        barras = [
            (-xi, -yi, area_barra), (xi, -yi, area_barra),
            (xi, yi, area_barra), (-xi, yi, area_barra),
            (0, -yi, area_barra), (xi, 0, area_barra),
            (0, yi, area_barra), (-xi, 0, area_barra),
        ]
        return barras

    def arranjo_5(self,lx, ly, cobrimento, area_barra=1.0):
        """
        Arranjo 6 — 4 cantos + 1 no meio de cada face ESQUERDA/DIREITA
        + 2 distribuídas no topo/base (mais barras nas faces curtas
        do que no arranjo 5). 10 barras no total.
        """
        xi = lx / 2 - cobrimento
        yi = ly / 2 - cobrimento
        xm = xi / 3  # posições intermediárias no topo/base

        barras = [
            (-xi, -yi, area_barra), (xi, -yi, area_barra),
            (xi, yi, area_barra), (-xi, yi, area_barra),
            (xi, 0, area_barra), (-xi, 0, area_barra),
            (-xm, yi, area_barra), (xm, yi, area_barra),
            (-xm, -yi, area_barra), (xm, -yi, area_barra),
        ]
        return barras


#para pequena excentricidade
    def eslim(self,l1,l2,e):
        excentricidade = self.excentricidades()
        es_linha_lilimte=(0.85*(self.fck/14)*l1*l2*((l1/2)-4))/self.nd
        es_linha=(l1/2)-e-(self.d_linha)
        if es_linha_lilimte > es_linha:
            if excentricidade == self.ex:
                self.x_menor_h(self.lx,self.ly,self.mdx_total)
                self.armadura_grande_final=self.as_sol1
                self.as_sim_x.setText(str(f"{self.as_sol1:.1f} cm²"))
                self.as_sim_x2.setText(str(f" 0 cm²"))

            if excentricidade == self.ey:
                self.x_menor_h(self.ly,self.lx,self.mdy_total)
                self.armadura_grande_final = self.as_sol1
                self.as_sim_y.setText(str(f"{self.as_sol1:.1f} cm²"))
                self.as_sim_y2.setText(str(f" 0 cm²"))
        if es_linha_lilimte < es_linha:
            if excentricidade == self.ex:
                self. x_maior_h_As_nao_0(self.lx,self.ly,self.mdx_total)
                self.armadura_grande_final = max(self.as_x_maior,self.as_linha_x_maior)
                self.as_sim_x.setText(str(f"{self.as_x_maior:.1f} cm²"))
                self.as_sim_x2.setText(str(f"{self.as_linha_x_maior:.1f} cm²"))
            if excentricidade == self.ey:
                self.x_maior_h_As_nao_0(self.ly,self.lx,self.mdy_total)
                self.armadura_grande_final = max(self.as_x_maior, self.as_linha_x_maior)
                self.as_sim_y.setText(str(f"{self.as_x_maior:.1f} cm²"))
                self.as_sim_y2.setText(str(f"{self.as_linha_x_maior:.1f} cm²"))
    def x_menor_h(self,l1,l2,mdtotal):
        self.info_1.setText(str(""))
        self.info_2.setText(str(""))
        self.info_3.setText(str(""))
        self.info_4.setText(str(""))
        sigma_sd_linha=43.5
        # nd = 0.68 * self.ly* x * (self.fck/14) + As_linha * sigma_sd_linha
        # md = (0.68 * self.ly * x * (self.fck/14) * ((self.lx / 2) - 0.4 * x)+ As_linha * sigma_sd_linha * ((self.lx / 2) - self.d_linha))
        x, As_linha = symbols('x As_linha')
        eq1 = Eq(self.nd,0.68 * l2 * x * (self.fck/14) + As_linha * sigma_sd_linha)
        eq2 = Eq(mdtotal,0.68 * l2 * x * (self.fck/14) * ((l1 / 2) - 0.4 * x)+ ((As_linha * sigma_sd_linha) * ((l1 / 2) - self.d_linha)))
        solucoes = solve((eq1, eq2), (x, As_linha))
        print(solucoes)
        solucoes_validas = []
        for sol in solucoes:
            x_sol = float(sol[0])
            As_sol = float(sol[1])
            if x_sol<=0:
                self.info_1.setText(str("Hipótese : 0.8x<h"))
                print("Hpótese descartada")
                self.info_2.setText(str("Hpótese descartada"))
                print("Utilizar armadura minima")
                self.info_3.setText(str("Utilizar armadura minima"))
                self.as_sol1 = 0
                return
            if 0.8*x_sol < l1 and As_sol > 0:
                self.info_1.setText(str("0.8x<h"))
                print(f"Hipótese válida, x = {x_sol:.2f} cm")
                self.info_2.setText(str("Hpótese válida"))
                self.info_3.setText(str(f"x = {x_sol:.2f} cm"))
                print(f"As' = {As_sol:.2f} cm²")
                self.as_sol1=As_sol
                if x_sol>=l1:
                    print("Domínio 5")
                    E_linha_s=(2*(x_sol-self.d_linha))/(x_sol-((3/7)*l1))
                    print(f"{E_linha_s:.2f}‰ > 2.07‰")
                    print(f"Tensão fyd=43.5 correta")
                return x_sol, As_sol
        self.as_sol1 = 0
        print("Solução não válida")
        self.info_1.setText(str("Solução não válida"))

    def x_maior_h_As_nao_0(self,l1,l2,mdtotal):
        self.info_1.setText(str(""))
        self.info_2.setText(str(""))
        self.info_3.setText(str(""))
        self.info_4.setText(str(""))
        sigma_sd_linha = 42
        sigma_sd = 42
        # self.nd=0.85*self.ly*self.lx*(self.fck/14)+As*sigma_sd+As_linha*sigma_sd_linha
        # self.mdx=(As_linha*sigma_sd_linha-As*sigma_sd)*((lx/2)-self.d_linha)
        As, As_linha = symbols('As As_linha')
        eq1 = Eq(self.nd,0.85*l2*l1*(self.fck/14)+As*sigma_sd+As_linha*sigma_sd_linha)
        eq2 = Eq(mdtotal,(As_linha*sigma_sd_linha-As*sigma_sd)*((l1/2)-self.d_linha))
        solucoes = solve((eq1, eq2), (As, As_linha))
        self.as_x_maior = float(solucoes[As])
        self.as_linha_x_maior = float(solucoes[As_linha])
        print(f"Pequena excentricidade, x>0.8h, As={self.as_x_maior} e As'={self.as_linha_x_maior}")
        self.info_1.setText(str("Hipótese: x>0.8h"))
        self.info_2.setText(str("Hipótese: Solução na reta B"))
        self.info_3.setText(str("c = ’s = s = 2,0 ‰"))
        self.info_4.setText(str("σsd = ,σ’sd = 42,0 kN/cm2"))

    def procurar_solucao(self, x_inicial, x_final, d, l1, l2, md_total):
        fyd_linha = 43.5
        tolerancia_fyd = 0.5
        while True:
            melhor_erro = float("inf")
            melhor_x = None
            melhor_As = None
            melhor_es = None
            x = x_inicial

            while x <= x_final:
                e_s = (3.5 * (d - x)) / x
                fyd = (e_s / 1000) * 21000
                fyd = max(min(fyd, 43.5), -43.5)
                As_sim = (
                                 self.nd
                                 - 0.68 * l2 * x * (self.fck / 14)
                         ) / (fyd_linha - fyd)

                md = (
                        0.68 * l2 * x * (self.fck / 14)
                        * ((l1 / 2) - 0.4 * x)
                        + As_sim * (fyd + fyd_linha)
                        * ((l1 / 2) - self.d_linha)
                )

                erro = 100 * abs(md - md_total) / md_total
                if erro < melhor_erro:
                    melhor_erro = erro
                    melhor_x = x
                    melhor_As = As_sim
                    melhor_es = 3.5 * (x - self.d_linha) / x
                x += 0.01
            # armadura comprimida escoou
            if melhor_es >= 2.07:
                break
            novo_fyd_linha = 21000 * (melhor_es / 1000)
            print(f"fyd_linha antigo = {fyd_linha:.3f}")
            print(f"fyd_linha novo   = {novo_fyd_linha:.3f}")
            if abs(novo_fyd_linha - fyd_linha) < tolerancia_fyd:
                fyd_linha = novo_fyd_linha
                break
            fyd_linha = novo_fyd_linha
        if melhor_x is not None and melhor_erro < 2:
            self.x_final = melhor_x
            self.erro_final = melhor_erro
            self.armadura_grande_final = melhor_As
            print("Solução encontrada")
            print(f"x = {melhor_x:.2f}")
            print(f"As = {melhor_As:.2f}")
            print(f"erro = {melhor_erro:.2f}%")
            self.info_1.setText("Solução encontrada")
            self.info_3.setText(f"x = {melhor_x:.2f}")
            self.info_4.setText(f"erro = {melhor_erro:.2f}%")

            if melhor_es >= 2.07:
                self.info_5.setText(f"{melhor_es:.2f}‰ >= 2.07‰ ok!")
            else:
                self.info_5.setText(f"{melhor_es:.2f}‰ < 2.07‰")

            return True

        self.melhor_x = melhor_x
        self.melhor_erro = melhor_erro
        self.melhor_As = melhor_As

        return False

    def iteracao(self, d, l1, l2, md_total):
        self.armadura_grande_final = 0
        self.x_final = 0
        self.erro_final = 0
        self.info_2.setText(str("Domínio 4a"))
        if self.procurar_solucao(
            math.ceil(d),
            l1,
            d,
            l1,
            l2,
            md_total
        ):
            return
        print("Tentando domínio 4")
        self.info_2.setText(str("Domínio 4"))
        if self.procurar_solucao(
            math.ceil(0.63*d),
            d, #colocar 1.15d(assim o x vai ficar levemente superior a d e vai achar solucao-dominio 4a)
            d,
            l1,
            l2,
            md_total
        ):
            return
        print("Tentando domínio 3")
        self.info_2.setText(str("Domínio 3"))
        if self.procurar_solucao(
            math.ceil(0.26*d),
            0.63*d,
            d,
            l1,
            l2,
            md_total
        ):
            return
        print("Tentando domínio 2b")
        self.info_2.setText(str("Domínio 2b"))
        if self.procurar_solucao(
            math.ceil(self.d_linha),
            0.26*d,
            d,
            l1,
            l2,
            md_total
        ):
            return
        print("Nenhum domínio convergiu")
        self.info_1.setText(str("Nenhum domínio convergiu"))
        self.info_2.setText(str("Nenhum domínio convergiu"))

        #tentar remover esses 3 prints p ver se para de crashar
        # print(f"Melhor x = {self.melhor_x:.2f}")
        # print(f"Melhor As = {self.melhor_As:.2f}")
        # print(f"Melhor erro = {self.melhor_erro:.2f}%")


    def preencher_dados(self):
        self.pegar_dados()
        self.esbeltez_limite()
        self.momentos_totais()
        lamb_x = self.indice_esbeltez(self.lexy,self.lx)
        lamb_y = self.indice_esbeltez(self.lexy,self.ly)
        if self.lamb1x < lamb_x:
            self.esbeltez_x.setText(str(f"λx={lamb_x:.1f} >{self.lamb1x:.1f}(λlimite)- Considerar momento de 2°grau"))
        if self.lamb1x > lamb_x:
            self.esbeltez_x.setText(str(f"λx={lamb_x:.1f} <{self.lamb1x:.1f}(λlimite)- Não considerar momento de 2°grau"))
        if self.lamb1y <lamb_y:
            self.esbeltez_y.setText(str(f"λy={lamb_y:.1f} >{self.lamb1y:.1f}(λlimite)- Considerar momento de 2°grau"))
        if self.lamb1y > lamb_y:
            self.esbeltez_y.setText(str(f"λx={lamb_y:.1f} <{self.lamb1y:.1f}(λlimite)- Não considerar momento de 2°grau"))
        momento_min_x = self.momento_minimo(self.lx)
        momento_min_y = self.momento_minimo(self.ly)
        self.mx_minimo.setText(str(f"{momento_min_x:.1f}"))
        self.my_minimo.setText(str(f"{momento_min_y:.1f}"))
        mdx_grau2, mdy_grau2 = self.usar_momento_segunda_ordem()
        self.mx_segundo_grau.setText(str(f"{mdx_grau2:.1f}"))
        self.my_segundo_grau.setText(str(f"{mdy_grau2:.1f}"))
        self.momento_mx_total.setText(f"{self.mdx_total:.1f}")
        self.momento_my_total.setText(f"{self.mdy_total:.1f}")

    def numerobarras(self,As):
        numero = self.barra.currentText()
        if numero == "6.3":
            n = int((As / 0.3112)) + 1
            return n
        if numero == "8":
            n = int((As / 0.503)) + 1
            return n
        if numero == "10":
            n = int((As / 0.785)) + 1
            return n
        if numero == "12.5":
            n = int((As / 1.227)) + 1
            return n
        if numero == "16":
            n = int((As / 2.011)) + 1
            return n
        if numero == "20":
            n = int((As / 3.142)) + 1
            return n

    def cal_numero_barras(self):
        n=self.numerobarras(self.armadura_grande_final)
        self.numero_barras.setText(str(f"{n:.1f} barras"))
        opcao = self.pilar_tipo.currentText()

    def arm_minima(self):
        am1=0.15*(self.nd/43.5)
        am2=0.004*self.ly*self.lx
        am=(max(am1,am2))/2
        if am>=self.armadura_grande_final:
            self.armadura_grande_final=am
            self.info_6.setText(str(f"Armadura minima usada: {self.armadura_grande_final:.1f} cm²"))
        else:
            self.info_6.setText(str(f"Armadura minima não usada: {am:.1f} cm²"))


    def escolher_bitola(self,As_total, n_barras):
        BITOLAS = {
            "6.3": 0.3112,
            "8": 0.503,
            "10": 0.785,
            "12.5": 1.227,
            "16": 2.011,
            "20": 3.142,
        }
        """
        Divide a armadura total pelo número de barras para achar a área
        necessária por barra, e escolhe a menor bitola da tabela cuja
        área seja imediatamente SUPERIOR (ou igual) a essa necessidade.

        Parâmetros:
            As_total  : área total de armadura (cm²)
            n_barras  : número de barras

        Retorna:
            (bitola, area_bitola, area_necessaria) — ou (None, None, area_necessaria)
            se nenhuma bitola da tabela for suficiente.
        """
        area_necessaria = As_total / n_barras

        # ordena as bitolas pela área, da menor para a maior
        bitolas_ordenadas = sorted(BITOLAS.items(), key=lambda item: item[1])

        for bitola, area in bitolas_ordenadas:
            if area >= area_necessaria:
                return bitola, area, area_necessaria

        # nenhuma bitola da tabela é suficiente
        return None, None, area_necessaria
if __name__ == '__main__':
    app = QApplication([])
    window = PilaresCACopia_reorganizadoUI()
    window.show()
    app.exec_()
