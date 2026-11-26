from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
import math
import recursos_rc

# OBS: Fazer a conferencia de altura util(CG) ----->> CHECK
# fazer mais uma camada de barras(3a camada) ---->>CHECK
# colocar um texto mostrando a altura ------>CHECK
# verificar armadura dupla (Bx>0.45)---->>>CHECK
# TALVEZ fazer o calculo nesse caso---->>CHECK
# Detlhar nesse caso tambem
# colocar botao que mostra os epac horiz e vertic e deixar o usuario escolher
class VIGASorganizadoIA(QMainWindow):
    def __init__(self):
        super().__init__()
        # achar o arquivo salvo
        uic.loadUi('VIGASorganizadoIA_v2.ui', self)
        #uic.loadUi('VIGASorganizadoIA.ui', self)
        # conectar o botão clique com o método escolher viga
        self.botaook.clicked.connect(self.escolherviga)
        # conectar o botão clique com o método  momento viga
        self.botaocalcular.clicked.connect(self.momento_viga)
        # desenhar seção transversal da viga
        self.desenhost.clicked.connect(self.acao_desenhar)
        self.desenhost.clicked.connect(self.vercg)
        self.desenhost.clicked.connect(self.acao_espacamentos_final)
        # calcular armadura long positiva
        self.armlong.clicked.connect(self.acao_calcarmlong)
        self.armlong.clicked.connect(self.achar_dominio)
        self.numero_barras.clicked.connect(self.acao_nunerobarras)
        # mostrar espaçamentos iniciais
        self.espacamentos.clicked.connect(self.acao_espacamentos_inicial)
        # arm dupla
        self.arm_dupla.clicked.connect(self.campos_arm_dupla)
        # numero barras arm dupla
        self.calcular_nbarrasdupla.clicked.connect(self.mostrar_numero_barras_dupla)
        self.configurar_estados()
        # teste
        self.comprimento.setText("7")
        self.bw.setText("20")
        self.cobrimento.setText("2")
        self.fck.setText("25")
        self.estribo.setText("5")
        self.inserirmomento.setText("15700")  # era 10000

    def configurar_estados(self):
        # Bloco 2: habilita só o que faz sentido para "Inserir" ou "Calcular"
        self.tipomomento.currentIndexChanged.connect(self.atualizar_bloco_momento)
        self.atualizar_bloco_momento()

        # Bloco 6: começa desabilitado; libere quando o bloco 3 indicar armadura dupla
        self.gb_dupla.setEnabled(False)

        # Mensagem de apoio na barra de status
        self.statusBar().showMessage("Siga os blocos de 1 a 6. Campos cinza são calculados.")

    def atualizar_bloco_momento(self):
        inserir = self.tipomomento.currentText() == "Inserir"
        self.inserirmomento.setEnabled(inserir)
        self.distribuida.setEnabled(not inserir)
        self.concentrada.setEnabled(not inserir)

    def liberar_armadura_dupla(self, precisa_dupla):
        # Armadura dupla: libera o bloco 6 e fecha o bloco 4 (que é só para armadura simples).
        # Armadura simples: o contrário.
        precisa_dupla = bool(precisa_dupla)
        self.gb_dupla.setEnabled(precisa_dupla)
        self.gb_barras.setEnabled(not precisa_dupla)
        self.gb_espacamentos.setEnabled(not precisa_dupla)

    def escolherviga(self):
        self.infos_basicasviga()
        # pegar tipo de viga
        tipo = self.tipoviga.currentText()
        # defino a variavel
        mostrar = self.nome_bonito(tipo)
        # faço o campo aparecer como a variavel
        self.tipodeviga.setText(str(mostrar))
        # arrumar o nome qdo escolher o tipo de viga

    def nome_bonito(self, tipo):
        if tipo == "BiApoiada":
            return "Viga bi apoiada"
        elif tipo == "Engastada":
            return "Viga em balanço"

    # apertar botao calcular e calc momento
    def momento_viga(self):
        # pegar o modo de calc do momento
        modo = self.tipomomento.currentText()
        if modo == "Inserir":
            # defino a variavel(valor do momento)
            momento = float(self.inserirmomento.text())
            # faço o campo aparecer como a variavel momento
            self.momentofletor.setText(str(momento))
        elif modo == "Calcular":
            # pego o tipo de viga
            tipo = self.tipoviga.currentText()
            # defino a variavel(valor do momento)
            momento = self.calcula_viga(tipo)
            # faço o campo aparecer como a variavel momento
            self.momentofletor.setText(str(momento))
        self.momento_max = momento

    # chama as funcoes de calculo
    def calcula_viga(self, tipo):
        if tipo == "BiApoiada":
            return self.calcula_biapoiada()
        elif tipo == "Engastada":
            return self.calcula_balanco()

    def calcula_biapoiada(self):
        vao = float(self.comprimento.text())
        carga = float(self.distribuida.text())
        maxmomento = (carga * (vao * vao)) / 8
        return maxmomento

    def calcula_balanco(self):
        vao = float(self.comprimento.text())
        carga = float(self.distribuida.text())
        maxmomento = (carga * (vao * vao)) / 2
        return maxmomento

    #desenhar cotas
    def cota(self, ax, x1, y1, x2, y2, texto, offset_texto=(0, 0)):
        ax.annotate('',xy=(x1, y1),xytext=(x2, y2),arrowprops=dict(arrowstyle='<->', lw=1))
        ax.text((x1 + x2) / 2 + offset_texto[0],(y1 + y2) / 2 + offset_texto[1],texto,ha='center',va='center')

    # desenhar a ST
    def desenhar_secao_positiva(self, largura, vao):
        import matplotlib.pyplot as plt
        self.infos_basicasviga()
        diametro = float(self.barra.currentText())
        altura = self.altura
        bwutil1 = self.cob + (self.diam_estribo / 10)
        bwutil2 = self.bwviga - self.cob - (self.diam_estribo / 10)
        altutil2 = self.altura - self.cob - (self.diam_estribo / 10)
        altutil1 = self.cob + (self.diam_estribo / 10)
        fig, ax = plt.subplots()  # Create a figure containing a single Axes.
        # secao bruta
        ax.plot([0, 0, largura, largura, 0], [0, altura, altura, 0, 0])
        #COTAS
        self.cota(ax,-3, 0,-3, altura,'h',(-0.8, 0)) #cota altura
        self.cota(ax,0, -3,largura, -3,r'$b_w$',(0, -0.8)) # cota bw
        self.cota(ax,0,altura - self.cob,bwutil1,altura - self.cob,'c',(0, 0.8)) # cota cobrimento
        # secao util do aço
        ax.plot([bwutil1, bwutil1, bwutil2, bwutil2, bwutil1], [altutil1, altutil2, altutil2, altutil1, altutil1])
        # criar funcoes p calcular armadura e colocar aq dps
        bwutil = 2 * (self.cob + (self.diam_estribo / 10))
        n = self.numerobarras()
        ah = (self.bwviga - (bwutil + (n * diametro / 10))) / (n - 1)
        # ahmin=self.espachorizontal()
        ahmin = float(self.es_horizontal.text())
        barra1 = plt.Circle(((bwutil1 + (diametro / 20)), (altutil1 + (diametro / 20))),
                            (diametro / 20))  # criar objeto circulo
        barra2 = plt.Circle(((bwutil2 - (diametro / 20)), (altutil1 + (diametro / 20))), (diametro / 20))
        novo1, _, _ = self.barraslinhas()
        i = 1
        _, novalinha, _ = self.barraslinhas()
        _, _, linha3 = self.barraslinhas()
        ahnovo = (self.bwviga - (bwutil + (novo1 * diametro / 10))) / (novo1 - 1)
        av = float(self.es_vertical.text())
        self.novoah = ahnovo
        if ah >= ahmin:
            self.ncg = 1
            # apenas para a primeira linha
            for cont in range(n - 2):
                barran = plt.Circle(
                    (((bwutil1 + (diametro / 20)) + (i * (ah + (diametro / 10)))), (altutil1 + (diametro / 20))),
                    (diametro / 20))
                i = i + 1
                ax.add_patch(barran)
            # para a primeira e segunda
        else:
            # COTA AV
            y1 = altutil1 + (diametro / 10)
            y2 = y1 + av
            x_cota = largura + 2
            self.cota(ax, x_cota, y1, x_cota, y2, r'$a_v$', (1, 0))
            self.ncg = 2

            # primeira linha:
            for cont in range(novo1 - 2):
                barranovo = plt.Circle(
                    (((bwutil1 + (diametro / 20)) + (i * (ahnovo + (diametro / 10)))), (altutil1 + (diametro / 20))),
                    (diametro / 20))
                i = i + 1
                ax.add_patch(barranovo)
            # fazer para a segunda linha :
            if novalinha == 1:
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil1 + (diametro / 20)) + av + (diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
            elif novalinha == 2:
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil1 + (diametro / 20)) + av + (diametro / 10)),
                    (diametro / 20))
                barranova2 = plt.Circle(
                    ((bwutil2 - (diametro / 20)), (altutil1 + (diametro / 20)) + av + (diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
                ax.add_patch(barranova2)
            elif novalinha >= 3:
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil1 + (diametro / 20)) + av + (diametro / 10)),
                    (diametro / 20))
                barranova2 = plt.Circle(
                    ((bwutil2 - (diametro / 20)), (altutil1 + (diametro / 20)) + av + (diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
                ax.add_patch(barranova2)
                for cont in range(1, novalinha - 1):
                    barrameio = plt.Circle((((bwutil1 + (diametro / 20)) + (cont * (ahnovo + (diametro / 10)))),
                                            (altutil1 + (diametro / 20)) + av + (diametro / 10)), (diametro / 20))
                    ax.add_patch(barrameio)
        ax.add_patch(barra1)  # aparecer na figura
        ax.add_patch(barra2)
        # desenhar a terceira linha
        if novo1 == novalinha:
            # COTA AV
            y1 = altutil1 + (diametro / 10)
            y2 = y1 + av
            x_cota = largura + 2
            self.cota(ax, x_cota, y1, x_cota, y2, r'$a_v$', (1, 0))

            #self.ncg = 3
            if linha3 == 1:
                self.ncg = 3
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil1 + (diametro / 20)) + av + av + (2 * diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
            elif linha3 == 2:
                self.ncg = 3
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil1 + (diametro / 20)) + av + av + (2 * diametro / 10)),
                    (diametro / 20))
                barranova2 = plt.Circle(
                    ((bwutil2 - (diametro / 20)), (altutil1 + (diametro / 20)) + av + av + (2 * diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
                ax.add_patch(barranova2)
            elif linha3 >= 3:
                self.ncg = 3
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil1 + (diametro / 20)) + av + av + (2 * diametro / 10)),
                    (diametro / 20))
                barranova2 = plt.Circle(
                    ((bwutil2 - (diametro / 20)), (altutil1 + (diametro / 20)) + av + av + (2 * diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
                ax.add_patch(barranova2)
                for cont in range(1, linha3 - 1):
                    barrameio = plt.Circle((((bwutil1 + (diametro / 20)) + (cont * (ahnovo + (diametro / 10)))),
                                            (altutil1 + (diametro / 20)) + av + av + (2 * diametro / 10)),
                                           (diametro / 20))
                    ax.add_patch(barrameio)
        else:
            pass
        # desenho de arm de pele:
        Aspele = self.arm_pele()
        if Aspele > 0:
            n_pele, Apele_diametro = self.num_arm_pele()
            if n_pele <= 1:
                return
            av = ((1 / 2) * self.altutil) / (
                        n_pele - 1)  # se quiser mudar a area de distrib da arm de pele, trocar aqui e:
            for cont in range(n_pele):
                y = altura - (altura / 4) - (Apele_diametro / 20) - (cont * av)  # mudar aqui tbm:
                barra_pele_esq = plt.Circle((bwutil1 + (Apele_diametro / 20), y), Apele_diametro / 20)
                barra_pele_dir = plt.Circle((bwutil2 - (Apele_diametro / 20), y), Apele_diametro / 20)

                ax.add_patch(barra_pele_esq)
                ax.add_patch(barra_pele_dir)
        #COTA AH
        x_barra1 = bwutil1 + (diametro / 20)
        x_barra2 = x_barra1 + ahnovo + (diametro / 10)
        y_cota = altutil1 - 2
        self.cota(ax,x_barra1,y_cota,x_barra2,y_cota,r'$a_h$',(0, -0.8))

        ax.set_aspect('equal')  # deixar tudo proporcional(importante!!-sem essa linha fica tudo esquisito)
        ax.set_xlim(-10, largura + 10)
        ax.set_ylim(-10, altura + 10)
        plt.show()  # Show the figure.

    def desenhar_secao_negativa(self, largura, vao):
        import matplotlib.pyplot as plt
        self.infos_basicasviga()
        diametro = float(self.barra.currentText())
        altura = self.altura
        bwutil1 = self.cob + (self.diam_estribo / 10)
        bwutil2 = self.bwviga - self.cob - (self.diam_estribo / 10)
        altutil2 = self.altura - self.cob - (self.diam_estribo / 10)
        altutil1 = self.cob + (self.diam_estribo / 10)
        fig, ax = plt.subplots()  # Create a figure containing a single Axes.
        # secao bruta
        ax.plot([0, 0, largura, largura, 0], [0, altura, altura, 0, 0])
        # secao util do aço
        ax.plot([bwutil1, bwutil1, bwutil2, bwutil2, bwutil1], [altutil1, altutil2, altutil2, altutil1, altutil1])
        # criar funcoes p calcular armadura e colocar aq dps
        bwutil = 2 * (self.cob + (self.diam_estribo / 10))
        n = self.numerobarras()
        ah = (self.bwviga - (bwutil + (n * diametro / 10))) / (n - 1)
        # ahmin = self.espachorizontal()
        ahmin = float(self.es_horizontal.text())
        barra1 = plt.Circle(((bwutil1 + (diametro / 20)), (altutil2 - (diametro / 20))),
                            (diametro / 20))  # criar objeto circulo
        barra2 = plt.Circle(((bwutil2 - (diametro / 20)), (altutil2 - (diametro / 20))), (diametro / 20))
        novo1, _, _ = self.barraslinhas()
        i = 1
        _, novalinha, _ = self.barraslinhas()
        _, _, linha3 = self.barraslinhas()
        ahnovo = (self.bwviga - (bwutil + (novo1 * diametro / 10))) / (novo1 - 1)
        av = float(self.es_vertical.text())
        self.novoah = ahnovo
        if ah >= ahmin:
            self.ncg = 1
            # apenas para a primeira linha
            for cont in range(n - 2):
                barran = plt.Circle(
                    (((bwutil1 + (diametro / 20)) + (i * (ah + (diametro / 10)))), (altutil2 - (diametro / 20))),
                    (diametro / 20))
                i = i + 1
                ax.add_patch(barran)
            # para a primeira e segunda
        else:
            self.ncg = 2
            # primeira linha:
            for cont in range(novo1 - 2):
                barranovo = plt.Circle(
                    (((bwutil1 + (diametro / 20)) + (i * (ahnovo + (diametro / 10)))), (altutil2 - (diametro / 20))),
                    (diametro / 20))
                i = i + 1
                ax.add_patch(barranovo)
            # fazer para a segunda linha :
            if novalinha == 1:
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil2 - (diametro / 20)) - av - (diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
            elif novalinha == 2:
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil2 - (diametro / 20)) - av - (diametro / 10)),
                    (diametro / 20))
                barranova2 = plt.Circle(
                    ((bwutil2 - (diametro / 20)), (altutil2 - (diametro / 20)) - av - (diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
                ax.add_patch(barranova2)
            elif novalinha >= 3:
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil2 - (diametro / 20)) - av - (diametro / 10)),
                    (diametro / 20))
                barranova2 = plt.Circle(
                    ((bwutil2 - (diametro / 20)), (altutil2 - (diametro / 20)) - av - (diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
                ax.add_patch(barranova2)
                for cont in range(1, novalinha - 1):
                    barrameio = plt.Circle((((bwutil1 + (diametro / 20)) + (cont * (ahnovo + (diametro / 10)))),
                                            (altutil2 - (diametro / 20)) - av - (diametro / 10)), (diametro / 20))
                    ax.add_patch(barrameio)
        ax.add_patch(barra1)  # aparecer na figura
        ax.add_patch(barra2)
        # desenhar a terceira linha
        if novo1 == novalinha:
            #self.ncg = 3
            if linha3 == 1:
                self.ncg = 3
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil2 - (diametro / 20)) - av - av - (2 * diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
            elif linha3 == 2:
                self.ncg = 3
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil2 - (diametro / 20)) - av - av - (2 * diametro / 10)),
                    (diametro / 20))
                barranova2 = plt.Circle(
                    ((bwutil2 - (diametro / 20)), (altutil2 - (diametro / 20)) - av - av - (2 * diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
                ax.add_patch(barranova2)
            elif linha3 >= 3:
                self.ncg = 3
                barranova1 = plt.Circle(
                    ((bwutil1 + (diametro / 20)), (altutil2 - (diametro / 20)) - av - av - (2 * diametro / 10)),
                    (diametro / 20))
                barranova2 = plt.Circle(
                    ((bwutil2 - (diametro / 20)), (altutil2 - (diametro / 20)) - av - av - (2 * diametro / 10)),
                    (diametro / 20))
                ax.add_patch(barranova1)
                ax.add_patch(barranova2)
                for cont in range(1, linha3 - 1):
                    barrameio = plt.Circle((((bwutil1 + (diametro / 20)) + (cont * (ahnovo + (diametro / 10)))),
                                            (altutil2 - (diametro / 20)) - av - av - (2 * diametro / 10)),
                                           (diametro / 20))
                    ax.add_patch(barrameio)
        else:
            pass

        # desenho de arm de pele:
        Aspele = self.arm_pele()
        if Aspele > 0:
            n_pele, Apele_diametro = self.num_arm_pele()
            if n_pele <= 1:
                return
            av = ((1 / 2) * self.altutil) / (
                        n_pele - 1)  # se quiser mudar a area de distrib da arm de pele, trocar aqui e:
            for cont in range(n_pele):
                y = altura - (altura / 4) - (Apele_diametro / 20) - (cont * av)  # mudar aqui tbm:
                barra_pele_esq = plt.Circle((bwutil1 + (Apele_diametro / 20), y), Apele_diametro / 20)
                barra_pele_dir = plt.Circle((bwutil2 - (Apele_diametro / 20), y), Apele_diametro / 20)

                ax.add_patch(barra_pele_esq)
                ax.add_patch(barra_pele_dir)

        ax.set_aspect('equal')  # deixar tudo proporcional(importante!!-sem essa linha fica tudo esquisito)
        plt.show()  # Show the figure.

        # descobrir qtas barras tem q ficar na primeira linha (novo) e na linha acima

    def barraslinhas(self):
        self.infos_basicasviga()
        diametro = float(self.barra.currentText())
        bwutil = 2 * (self.cob + (self.diam_estribo / 10))
        n = self.numerobarras()
        if self.es_horizontal.text():
            self.ahmin = float(self.es_horizontal.text())
        else:
            self.ahmin = self.espachorizontal()
        # self.ahmin = self.espachorizontal()   #trocar aqui se quiser aumentar o espaçamento minimo das barras
        # numero de barras na primeira linha
        barrasnovo = int((self.bwviga - bwutil + self.ahmin) / (self.ahmin + (diametro / 10)))
        # numero de barras que vai nas segunda linha
        numerobarras = n - barrasnovo
        # numero de barras que vai nas terceira linha
        numerobarras3 = numerobarras - barrasnovo
        if numerobarras >= barrasnovo:
            numerobarras = barrasnovo
        return barrasnovo, numerobarras, numerobarras3

    def barraslinhas_vertical(self):
        if self.es_vertical.text():
            self.av = float(self.es_vertical.text())
        else:
            self.av = self.espacvertical()
    # funcao para conectar com o botao de clique(só tem um parametro (self))
    def acao_desenhar(self):
        tipo = self.tipoviga.currentText()
        try:
            vao = float(self.comprimento.text())
            self.infos_basicasviga()
            largura = self.bwviga
        except:
            self.momentofletor.setText("Digite o comprimento do vão!!")
            return
        if tipo == "BiApoiada":
            self.desenhar_secao_positiva(largura, vao)
        elif tipo == "Engastada":
            self.desenhar_secao_negativa(largura, vao)

    # pegar as infos para calc armadura long
    def infos_basicasviga(self):

        # dados que talvez ainda nao existam
        try:
            self.bwviga = float(self.bw.text())
            self.cob = float(self.cobrimento.text())
            self.fckc = float(self.fck.text())
            self.diam_estribo = float(self.estribo.text())
        except:
            pass
        vao = float(self.comprimento.text())
        # ALTURA
        texto_altura = self.Altura.text()
        if texto_altura == "":
            self.altura = int(vao * 100 / 12) + 1
            self.Altura.blockSignals(True)
            self.Altura.setText(str(self.altura))
            self.Altura.blockSignals(False)
        else:
            self.altura = float(texto_altura)
        # ALTURA UTIL
        texto_altura_util = self.alturautil.text()
        if texto_altura_util == "":
            self.altutil = self.altura - 3
            self.alturautil.blockSignals(True)
            self.alturautil.setText(str(self.altutil))
            self.alturautil.blockSignals(False)
        else:
            self.altutil = float(texto_altura_util)

    # funcao para achar o dominio (2 ou 3)
    def achar_dominio(self):
        self.infos_basicasviga()
        kc = ((self.bwviga) * self.altutil * self.altutil) / (self.momento_max * 1.4)
        bx = self.achar_bx_por_kc(kc, self.fckc)

        if bx is None:
            self.dominio.setText("Dominio inválido - aumente a altura")
            self.Kc_mostrar.setText(str(f"{kc:.2f}"))
            self.Bx_mostrar.setText("X/D>0.45")
            return

        if 0.01 <= bx <= 0.26:
            self.dominio.setText(str("Domínio 2"))
        elif 0.27 <= bx <= 0.45:
            self.dominio.setText(str("Domínio 3"))
        self.Kc_mostrar.setText(str(f"{kc:.2f}"))
        self.Bx_mostrar.setText(str(f"{bx}"))

    # calcular armadura de pele
    def arm_pele(self):
        self.infos_basicasviga()
        if self.altura >= 50 and self.altura <= 60:
            Aspeleface = ((0.05) / 100) * self.bwviga * self.altura
            return Aspeleface
        if self.altura > 60:
            Aspeleface = ((0.10) / 100) * self.bwviga * self.altura
            return Aspeleface
        else:
            return 0

    # calcula o numero de barras
    def num_arm_pele(self):
        Aspeleface = self.arm_pele()
        numero_barras_pele1 = int(Aspeleface / 0.196) + 1
        numero_barras_pele2 = int(Aspeleface / 0.312) + 1
        if numero_barras_pele1 > 4:
            return numero_barras_pele2, 6.3
        else:
            return numero_barras_pele1, 5

    def av_pele(self):
        self.infos_basicasviga()
        n_pele, _ = self.num_arm_pele()
        if (self.num_arm_pele()) <= 1:
            return 0
        avpele = ((1 / 2) * self.altutil) / (n_pele - 1)
        return avpele

    # aqui eu considerei aço CA-50, pensar em criar opcao para CA-60 dps
    def calc_armlong(self):
        self.infos_basicasviga()
        # calcular armadura
        As = (self.achar_ks() * self.momento_max * 1.4) / self.altutil
        # armaddura minima
        pmin = self.pegar_pmin(int(self.fckc))
        Asmin = pmin * self.bwviga * self.altura
        if As > Asmin:
            return As
        else:
            return Asmin

        # funcao auxiliar para a de cima

    def pegar_pmin(self, fck):
        self.infos_basicasviga()
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

    # aparecer o resultado no campo
    def acao_calcarmlong(self):
        self.infos_basicasviga()
        kc = ((self.bwviga) * self.altutil * self.altutil) / (self.momento_max * 1.4)
        bx = self.achar_bx_por_kc(kc, self.fckc)
        if bx is None:
            self.longpositiva.setText(str(f"Armadura dupla necessaria"))
            self.liberar_armadura_dupla(True)
            return
        self.liberar_armadura_dupla(False)
        As = self.calc_armlong()
        self.longpositiva.setText(str(f"{As:.3f}"))

    def acao_nunerobarras(self):
        kc = ((self.bwviga) * self.altutil * self.altutil) / (self.momento_max * 1.4)
        bx = self.achar_bx_por_kc(kc, self.fckc)
        if bx is None:
            self.armadura.setText(str(f"!!Usar armadura dupla!!"))
            return
        n = self.numerobarras()
        self.armadura.setText(str(f"{n}"))
        self.infos_basicasviga()

    # qtidade de barras
    def numerobarras(self):
        numero = self.barra.currentText()
        As = self.calc_armlong()
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

    # espac minimo horizontal pela norma(notar que a letra c depende do diamentro max do agregado(1.9))
    def espachorizontal(self):
        diametro = float(self.barra.currentText())
        a = 2
        b = diametro / 10
        c = 1.2 * 1.9
        return max(a, b, c)
    # espac minimo vertical pela norma(mesma observacao da funcao acima)
    def espacvertical(self):
        diametro = float(self.barra.currentText())
        a = 2
        b = diametro / 10
        c = 0.5 * 1.9
        return max(a, b, c)

        # tabela para metodo ks

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

        # achar o valor de Bx:

    def achar_bx_por_kc(self, kc_calculado, fck):
        self.tabelaKc()
        self.infos_basicasviga()
        tabela = self.tabela_kc
        chave_fck = f"C{int(fck)}"

        # pega todos os kc da coluna escolhida
        valores_kc = [valores[chave_fck] for valores in tabela.values()]
        kc_max = max(valores_kc)
        kc_min = min(valores_kc)
        # fora da tabela
        if kc_calculado > kc_max or kc_calculado < kc_min:
            return None

        melhor_bx = None
        menor_erro = float("inf")
        for bx, valores in tabela.items():
            kc_tabela = valores[chave_fck]
            erro = abs(kc_calculado - kc_tabela)
            if erro < menor_erro:
                menor_erro = erro
                melhor_bx = bx
        return melhor_bx

        # achar valor de Ks:

    def achar_ks(self):
        self.infos_basicasviga()
        kc = ((self.bwviga) * self.altutil * self.altutil) / (self.momento_max * 1.4)
        bx = self.achar_bx_por_kc(kc, self.fckc)
        if 0.01 <= bx <= 0.05:
            return 0.023
        elif 0.06 <= bx <= 0.15:
            return 0.024
        elif 0.16 <= bx <= 0.24:
            return 0.025
        elif 0.25 <= bx <= 0.33:
            return 0.026
        elif 0.34 <= bx <= 0.40:
            return 0.027
        elif 0.40 <= bx <= 0.45:
            return 0.028

    def vercg(self):
        diametro = float(self.barra.currentText())
        alturautil = self.altutil
        #av = self.espacvertical()
        av = float(self.es_vertical.text())
        if self.ncg == 1:
            acg = self.cob + (self.diam_estribo / 10) + (diametro / 20)
            dutil = self.altura - acg
            if abs(alturautil - dutil) <= 1.5:
                self.verificar_cg.setText(f"Ok, altura util calculada: {dutil:.1f}")
            else:
                self.altutil = dutil
                self.verificar_cg.setText(f"!!Altura util recomendada!!: {dutil:.1f}")
        if self.ncg == 2:
            acg = self.cob + (self.diam_estribo / 10) + (diametro / 20) + av / 2 + diametro / 20
            dutil = self.altura - acg
            if abs(alturautil - dutil) <= 1.5:
                self.verificar_cg.setText(f"Ok, altura util calculada: {dutil:.1f}")
            else:
                self.altutil = dutil
                self.verificar_cg.setText(f"!!Altura util recomendada!!: {dutil:.1f}")
        if self.ncg == 3:
            acg = self.cob + (self.diam_estribo / 10) + (diametro / 20) + av + diametro / 10 + (av / 2) + (
                        diametro / 20)
            dutil = self.altura - acg
            if abs(alturautil - dutil) <= 1.5:
                self.verificar_cg.setText(f"Ok, altura util calculada: {dutil:.1f}")
            else:
                self.altutil = dutil
                self.verificar_cg.setText(f"!!Altura util recomendada!!: {dutil:.1f}")

    # Daqui para cima ta tudo certo, vou fazer para calcular a armadura dupla agora
    def achar_bx_por_kc_dupla(self, kc_calculado, fck):
        self.tabelaKc()
        self.infos_basicasviga()
        tabela = self.tabela_kc
        chave_fck = f"C{int(fck)}"
        melhor_bx = None
        menor_erro = float("inf")
        kc_encontrado = None
        for bx, valores in tabela.items():
            kc_tabela = valores[chave_fck]
            erro = abs(kc_calculado - kc_tabela)
            if erro < menor_erro:
                menor_erro = erro
                melhor_bx = bx
                kc_encontrado = kc_tabela
        return melhor_bx, kc_encontrado

    def momentos_dupla(self):
        self.infos_basicasviga()
        kc_calc = ((self.bwviga) * self.altutil * self.altutil) / (self.momento_max * 1.4)
        bx, self.kc_tabela = self.achar_bx_por_kc_dupla(kc_calc, self.fckc)
        self.M1d = self.bwviga * (self.altutil ** 2) / self.kc_tabela
        self.M2d = (self.momento_max * 1.4) - self.M1d

    def armadura_dupla(self):
        self.infos_basicasviga()
        d_linha = 3
        self.ks1 = self.achar_ks_dupla()
        self.ks2 = self.ks_As2_dupla(d_linha / self.altutil)
        self.As1_dupla = ((self.ks1 * self.M1d) / self.altutil) + (self.M2d / ((50 / 1.15) * (self.altutil - d_linha)))
        self.As2_dupla = self.ks2 * self.M2d / (self.altutil - d_linha)

    def achar_ks_dupla(self):
        return 0.028

    def ks_As2_dupla(self, d_d):
        tabela = {
            0.05: 0.023,
            0.10: 0.023,
            0.15: 0.023,
            0.20: 0.024,
            0.25: 0.031,
            0.30: 0.041
        }
        # acha o número mais próximo
        mais_proximo = min(tabela.keys(), key=lambda k: abs(k - d_d))
        return tabela[mais_proximo]

    def numerobarras_dupla(self, As, barra):
        self.armadura_dupla()
        numero = barra.currentText()
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

    def campos_arm_dupla(self):
        self.momentos_dupla()
        self.armadura_dupla()
        n1 = self.numerobarras_dupla(self.As1_dupla, self.barra_As)
        n2 = self.numerobarras_dupla(self.As2_dupla, self.barra_Aslinha)
        self.M1d_linha.setText(f"{self.M1d:.2f}")
        self.M2d_linha.setText(f"{self.M2d:.2f}")
        self.kslim.setText(f"{self.ks1:.3f}")
        self.kslinha.setText(f"{self.ks2:.3f}")
        self.kclim.setText(f"{self.kc_tabela:.1f}")
        self.As_dupla.setText(f"{self.As1_dupla:.2f}")
        self.As_dupla_linha.setText(f"{self.As2_dupla:.2f}")
        self.nAs.setText(f"{n1:.1f}")
        self.nAslinha.setText(f"{n2:.1f}")

    def mostrar_numero_barras_dupla(self):
        self.momentos_dupla()
        self.armadura_dupla()
        n1 = self.numerobarras_dupla(self.As1_dupla, self.barra_As)
        n2 = self.numerobarras_dupla(self.As2_dupla, self.barra_Aslinha)
        self.nAs.setText(f"{n1:.1f}")
        self.nAslinha.setText(f"{n2:.1f}")

    def acao_espacamentos_inicial(self):
        # força cálculo automático
        self.ahmin = self.espachorizontal()
        # mostra no campo
        self.es_horizontal.setText(f"{self.ahmin:.1f}")

        self.av=self.espacvertical()
        self.es_vertical.setText(f"{self.av:.1f}")
    def acao_espacamentos_final(self):
        av = float(self.es_vertical.text())
        self.es_horizontal_final.setText(f"{self.novoah:.1f}")
        self.es_vertical_final.setText(f"{av:.1f}")

# math.ceil() - usar dps (arredonda p cima)
if __name__ == '__main__':
    app = QApplication([])
    window = VIGASorganizadoIA()
    window.show()
    app.exec_()
