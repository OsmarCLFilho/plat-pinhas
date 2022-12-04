import math
import pygame, sys
from pygame.locals import *


def escrever_texto(texto, superficie, x, y, fonte, color = (255, 255, 255)):
        """Escreve um texto na tela

        Args:
            texto (str): Texto que será escrito na superficie
            fonte (pygame.font.Font): Fonte do texto
            color (tuple): Tupla contendo 3 numeros de 0 a 255, infornando as cores em RGB
            superficie (pygame.Surface): Janela em que o texto sera escrito
            x (int): Coordenada x para escrita do texto (origem no topo à esquerda, crescimento da esquerda para direita)
            y (int): Coordenada y para escrita do texto (origem no topo à esquerda, crescimento de cima para baixo)
        """
        textobj = fonte.render(texto, True, color)
        superficie.blit(textobj, (x, y))

def escrever_centralizado(texto, fonte, color, superficie, x, y):
        """Escreve um texto na tela centralizado horizontalmente

        Args:
            texto (str): Texto que será escrito na superficie
            fonte (pygame.font.Font): Fonte do texto
            color (tuple): Tupla contendo 3 numeros de 0 a 255, infornando as cores em RGB
            superficie (pygame.Surface): Janela em que o texto sera escrito
            x (int): Coordenada x para escrita do texto, sendo a referencia para a
                     centrealização   (origem no topo à esquerda,  crescimento  da 
                     esquerda para direita)
            y (int): Coordenada y para escrita do texto (origem no topo à esquerda,
                     crescimento de cima para baixo)
        """
        textobj = fonte.render(texto, True, color)
        x_novo = x - textobj.get_width()/2          # Texto centralizado
        superficie.blit(textobj, (x_novo, y))



class Botao () :
    def __init__(self, texto,  tela, coordenada, cor_botao_1 = (25, 25, 25), cor_botao_2 = (80, 80, 80), cor_fonte = (255, 255, 255),imagem = None, imagem_2 = None):
        """Cria um botão para uma tela com pygame

        Args:
            texto (str): Texto do botão
            tela (pygame.Surface):  Janela do botão
            coordenada (tuple):     Tupla contendo 2 inteiros 
                                    representandos as coordenadas do mouse
            cor_botao_1 (tuple):    Tupla contendo 3 numeros de 0 a 255,
                                    informando as cores em RGB do botão
            cor_botao_2 (tuple):    Tupla contendo 3 numeros de 0 a 255,
                                    informando as cores em RGB do botão        
            cor_fonte (tuple):      Tupla contendo 3 numeros de 0 a 255, 
                                    informando as cores em RGB da fonte
            imagem (pygame.Surface):    Imagem do pygame, fundo do botão
            imagem_2 (pygame.Surface):  Imagem do pygame, fundo do botão
                                        quando o mouse passa por cima
        """
        self.__conteudo_texto = texto
        self.__cor_botao_1 = cor_botao_1
        self.__cor_botao_2 = cor_botao_2
        self.__cor_fonte = cor_fonte
        self.__tela = tela
        self.__coordenada = coordenada
        self.__imagem = imagem
        if imagem_2 != None:
            self.__imagem_2 = imagem_2
        else:
            self.__imagem_2 = imagem
        
        self.__font = pygame.font.SysFont("arialblack", 30) 
        self.__tamanho_botao = 1
        self.__largura = 50 
        self.__altura = self.texto.get_height()
       
    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, altura):
        self.__altura = altura/3 * self.tamanho_botao

    @property
    def borda_cor(self):
        return (0, 0, 0)

    @property
    def borda_tamanho(self):
        return 4

    @property
    def conteudo_texto(self):
        return self.__conteudo_texto 

    @property
    def coordenada(self):
        return self.__coordenada 

    @property
    def cor_botao_1(self):
        return self.__cor_botao_1

    @property
    def cor_botao_2(self):
        return self.__cor_botao_2

    @property
    def cor_botao(self):
        cores = [self.cor_botao_1, self.cor_botao_2]
        return cores

    @property
    def cor_fonte(self):
        return self.__cor_fonte

    @property
    def esta_botao(self):
        esta_botao = False
        pos_mou = pygame.mouse.get_pos()
        esta_botao = self.rect.collidepoint(pos_mou)

        self.__esta_botao = esta_botao
        return self.__esta_botao

    @property
    def esta_botao_imagem(self):
        esta_botao = False
        pos_mou = pygame.mouse.get_pos()
        esta_botao = self.rect_imagem.collidepoint(pos_mou)

        self.__esta_botao_imagem = esta_botao
        return self.__esta_botao_imagem

    @property
    def font(self):
        return self.__font

    @font.setter
    def font(self, font):
        self.__font = font 

    @property
    def imagem(self):
        return self.__imagem
    
    @property
    def imagem_2(self):
        return self.__imagem_2

    @property
    def imagens(self):
        imagens = [self.imagem, self.imagem_2]
        return imagens

    @property
    def largura(self):
        self.__largura = self.__largura * self.tamanho_botao
        return self.__largura

    @largura.setter
    def largura(self, largura):
        self.__largura = largura/4 * self.tamanho_botao

    @property
    def rect(self):
        tam = self.tamanho_botao

        largura = self.largura
        altura = self.altura

        x = self.coordenada[0] - tam * largura
        y = self.coordenada[1] 

        largura += 3*(tam * largura)

        return pygame.Rect(x, y, largura, altura)

    @property
    def rect_borda(self):
        tam = self.tamanho_botao
        bor = self.borda_tamanho

        largura = self.largura
        altura = self.altura

        x = self.coordenada[0] - tam * largura
        y = self.coordenada[1] 

        largura += 3*(tam * largura)

        return pygame.Rect(x-bor, y-bor, largura+2*bor, altura+2*bor)

    @property
    def rect_imagem(self):

        imagem = self.imagem
        rect = imagem.get_rect()
        
        x = self.rect.centerx - imagem.get_width()/2
        y = self.rect.centery - imagem.get_height()/2
        alt = rect.height
        lar = rect.width
        return pygame.Rect(x, y, lar, alt)

    @property
    def tamanho_botao(self):
        return self.__tamanho_botao

    @tamanho_botao.setter
    def tamanho_botao(self, tamanho):
        self.__tamanho_botao = tamanho 

    @property
    def tela(self):
        return self.__tela

    @property
    def texto(self):
        return self.font.render(self.conteudo_texto, True, self.cor_fonte)

    def draw(self):
        cor = self.cor_botao[self.esta_botao]

        pygame.draw.rect(self.tela, self.borda_cor, self.rect_borda)
        pygame.draw.rect(self.tela, cor, self.rect)

        x = self.rect.centerx
        y = self.coordenada[1]
        
    def escrever(self, x_varia = 0, y_varia = 0):
        x = self.rect.centerx + x_varia
        y = self.coordenada[1] + y_varia

        escrever_centralizado(self.conteudo_texto, self.font, self.cor_fonte, self.tela, x, y)

    def draw_image(self):
        imagem = self.imagens[self.esta_botao_imagem]

        x = self.rect.centerx - imagem.get_width()/2
        y = self.rect.centery - imagem.get_height()/2

        self.tela.blit(imagem,(x, y))


class Personagem:
    def __init__(self, nome, atributos = ["9999", "Não existe", False, "imagens/error_char.png"], selecionado = False):
        """Inicialização da classe

        Args:
            nome (str):         Nome do personagem
            atributos (list):   Lista com os atributo do personagem: preco(str),
                                descricao(str), comprado(bool), imagem (Surface)
            selecionado (bool): Se o personagem selecionado ou não
        """
        self.__nome = nome
        self.__preco = atributos[0]
        self.__descricao = atributos[1]
        self.__comprado = atributos[2]
        self.__imagem = atributos[3]
        self.__selecionado = selecionado

    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def preco(self):
        return self.__preco
        
    @property
    def descricao(self):
        return self.__descricao

    @property
    def imagem(self):
        return pygame.image.load(self.__imagem)

    @property
    def imagem_endereco(self):
        return self.__imagem

    @property
    def comprado(self):
        return self.__comprado

    @comprado.setter
    def comprado(self, comprado):
        self.__comprado = comprado

    @property
    def selecionado(self):
        return self.__selecionado

    @selecionado.setter
    def selecionado(self, selecionado):
        self.__selecionado = selecionado

    def __str__(self):
        return self.nome

class Loja:

    def __init__(self, personagens):
        """Inicialização da classes

        Args:
            personagens (lista): Lista contendo objetos do tipo Personagem
        """
        self.__personsgens = personagens
        self.screen = pygame.display.set_mode((900, 700))

    @property
    def personagens(self):
        return self.__personsgens

    @property
    def tela(self):
        return self.screen

    def __len__(self):
        return len(self.personagens)

    def selecionado(self):
        for personagem in self.personagens:
            if personagem.selecionado:
                break
        return personagem

    
    def exibir_loja(self):
        """Exibe a loja

        """

        def exibir_personagem(tela, personagem, x, y):
            """Exibe um persoagem na loja

            Args:
                personagem (Personagem): Personagem a ser exibido
                x (int): Posição a ser exibido em relação ao eixo x
                y (int): Posição a ser exibido em relação ao eixo y
            """

            #font = pygame.font.SysFont("arialblack", 40)
            font = pygame.font.Font('fonte/AGENTORANGE.TTF', 40)
            font_3 = pygame.font.SysFont("arialblack", 20)
            font_2 = pygame.font.Font('fonte/AGENTORANGE.TTF', 20)
            preto = (230,230,230)#(255, 255, 255)
            cinza = (200, 200, 200)
            cinza_2 = (40, 40, 40)
            branco = (0,0,0) # Eu sei que tá trocado

            # Escreve o nome do personagem
            nome = personagem.nome
            y_nome = y - 200
            escrever_centralizado(nome, font, preto, tela, x, y_nome)

            # Moldura
            moldura = pygame.image.load("imagens/nuvem_moldura.png")       
            x_mold = x - moldura.get_width()/2
            y_mold = y - moldura.get_height()/2  
            tela.blit(moldura, (x_mold, y_mold))

            # Exibe a imagem do personagem
            imagem = personagem.imagem  
            x_imagem = x - imagem.get_width()/2
            y_imagem = y - imagem.get_height()/2   
            tela.blit(imagem, (x_imagem, y_imagem))

            # Escreve a descrição do personagem
            descricao = personagem.descricao
            y_descricao = y + 150
            escrever_centralizado(descricao, font_3, preto, tela, x, y_descricao)


            # Escreve o preço do personagem
            preco = personagem.preco
            y_preco = y + 200
            # Moldura 2
            moldura_2 = pygame.image.load("imagens/cloud_4.png")
            x_mold_2 = x - moldura_2.get_width()/2
            tela.blit(moldura_2, (x_mold_2, y_preco-15))

            if not personagem.comprado:
                escrever_centralizado(preco, font, cinza_2, tela, x, y_preco)
            else:
                escrever_centralizado(preco, font, branco, tela, x, y_preco)


        #----------------------------------------------------------------------------
        
        clock = pygame.time.Clock()
        rodando = True
    
        index_per = 0
        tamanho_loja = len(self)
        slide = 0
        ativar_slide = 0

        x = self.tela.get_width()/2     
        y = self.tela.get_height()/2 -50

        ceu = pygame.image.load("imagens/ceu.png")
        esquerda = pygame.image.load("imagens/esquerda.png")
        esquerda_2 = pygame.image.load("imagens/esquerda_2.png")
        direita = pygame.image.load("imagens/direita.png")
        direita_2 = pygame.image.load("imagens/direita_2.png")
        sair = pygame.image.load("imagens/sair.png")
        sair_2 = pygame.image.load("imagens/sair_2.png")
        confirmar = pygame.image.load("imagens/V.png")
        cancelar = pygame.image.load("imagens/X.png")
        nuvem = pygame.image.load("imagens/cloud_3.png")
        nuvem_2 = pygame.image.load("imagens/cloud_5.png")

        rect_nuvem = nuvem.get_rect()

        font_2 = pygame.font.Font('fonte/AGENTORANGE.TTF', 30)

        preto = (255, 255, 255)
        cinza = (10, 10, 10)
        cinza_2 = (40, 40, 40)

        b_esquerda = Botao("Esquerda", self.screen, (75, 620), imagem = esquerda, imagem_2 =  esquerda_2)
        b_esquerda.largura = 0
        b_esquerda.altura = 0

        b_direita = Botao("Direita", self.screen, (x*2-70, 620), imagem = direita, imagem_2 = direita_2)
        b_direita.largura = 0
        b_direita.altura = 0

        b_confirmar = Botao("Confirmar", self.screen, (285, 610), cinza, cinza_2, preto, confirmar)
        b_confirmar.largura = 60
        b_confirmar.altura = 160

        b_cancelar = Botao("Cancelar", self.screen, (x*2-315, 610), cinza, cinza_2, preto, cancelar)
        b_cancelar.largura = 60
        b_cancelar.altura = 160

        b_sair = Botao("Sair", self.screen, (2*x-100, 20), imagem = sair, imagem_2 = sair_2)

        b_comprar = Botao("Comprar", self.screen, (x-75, 600))
        b_comprar.largura = 275
        compra = False

        b_selecionar = Botao("Selecionar", self.screen, (x-75, 600))
        b_selecionar.largura = 275

        b_selecionado = Botao("Selecionado", self.screen, (x-75, 600))
        b_selecionado.largura = 275

        while rodando:

            self.screen.blit(ceu, (0,0))

            # Reiniciando variaveis
            click = False
            click_esquerda = False
            click_direita = False

            #self.screen.fill((11,59,70))    # Preenche a tela com um tom de azul

            self.screen.blit(nuvem, (0,0))
            escrever_centralizado("Loja", font_2, cinza, self.tela, rect_nuvem.centerx, rect_nuvem.centery-20)

            self.screen.blit(nuvem_2, (2*x-90,0))
            b_sair.draw_image()

            # Exibe um personagem no meio da tela
            personagem = self.personagens[index_per]
            exibir_personagem(self.tela, personagem, x + slide, y)

            if index_per > 0: # Exibe um personagem a direita da tela
                exibir_personagem(self.tela, self.personagens[index_per - 1], 0 + slide, y)
            if index_per > 1: # Exibe um personagem a direita fora da tela para sua visubilidade no slide
                exibir_personagem(self.tela, self.personagens[index_per - 2], -x + slide, y)

            if index_per < tamanho_loja - 1: # Exibe um personagem a esquerda da tela
                exibir_personagem(self.tela, self.personagens[index_per + 1], x*2 + slide, y)
            if index_per < tamanho_loja - 2: # Exibe um personagem a esquerda fora da tela para sua visubilidade no slide
                exibir_personagem(self.tela, self.personagens[index_per + 2], x*3 + slide, y)


            b_esquerda.draw_image() # Exibe o botão para ir para esquerda
            b_direita.draw_image()  # Exibe o botão para ir para direita

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        rodando = False
                    # Seta para esquerda
                    elif event.key == pygame.K_LEFT:
                        click_esquerda = True
                    # Seta para direita
                    elif event.key == pygame.K_RIGHT:
                        click_direita = True
            
            
            # Ativa o slide ou o deslizar da tela
            if ativar_slide != 0:
                slide -= 25 * ativar_slide
                if math.fabs(slide) > x:
                    slide = 0
                    index_per += 1 * ativar_slide
                    ativar_slide = 0
                compra = False
            # Os botões relacionados a compra serão exibidos apenas quando o slide não estiver acontecendo
            elif not personagem.comprado:       # Opções de compra
                if not compra:
                    b_comprar.draw()            # Exibe o botão de compra
                    b_comprar.escrever()
                    if b_comprar.esta_botao and click:
                        compra = True
                else:
                    b_confirmar.draw()
                    b_confirmar.draw_image()    # Exibe o botão de confirmação da compra 
                    b_cancelar.draw()       
                    b_cancelar.draw_image()     # Exibe o botão de cancelamento da compra
                    if b_cancelar.esta_botao and click:
                        compra = False 
                    elif b_confirmar.esta_botao and click:
                        personagem.comprado = True
            else:                               # Opções de seleção
                if not personagem.selecionado:
                    b_selecionar.draw()
                    b_selecionar.escrever()
                    if b_selecionar.esta_botao and click:
                        for pers in self.personagens:
                            pers.selecionado = False
                        personagem.selecionado = True 
                else:
                    b_selecionado.draw()
                    b_selecionado.escrever()

            # Verfica se o botão ou se a seta para esquerda foram pressionados
            if (b_esquerda.esta_botao_imagem and click) or click_esquerda:
                if index_per > 0 and ativar_slide == 0:
                    ativar_slide = -1
            # Verfica se o botão ou se a seta para direita foram pressionados
            elif (b_direita.esta_botao_imagem and click) or click_direita:
                if index_per < tamanho_loja - 1 and ativar_slide == 0:
                    ativar_slide = 1  

            if b_sair.esta_botao_imagem and click:
                rodando = False
                        
            pygame.display.update()
            clock.tick(60)

class Menu:
    def __init__(self):
        self.galinha = "imagens/galinha.png"
        self.elefante = "imagens/Lfant.png"
        self.elefante_gold = "imagens/Lfantgold.png"
        self.personagem = {"Gala Galinha": ["50", "Consegue dar pulos duplos", True, self.galinha], "Emaperson": ["100", "Pulos longos", False, self.elefante], "Gala Gali": ["500", "Consegue mais pontos", False, self.galinha], "Emapon": ["5000", "É shine", False, self.elefante_gold]}

        self.lista_pers = []
        for nome, atributo in self.personagem.items():
            self.lista_pers.append(Personagem(nome,atributo))

        self.lista_pers[0].selecionado = True

        self.loja = Loja(self.lista_pers)

    def menu_principal(self):
        largura, altura = 900, 700
        screen = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Jogo")
        clock = pygame.time.Clock()

        #fonte = pygame.font.SysFont("arialblack", 80)
        font = pygame.font.Font('fonte/AGENTORANGE.TTF', 80)
        font_2 = pygame.font.Font('fonte/AGENTORANGE.TTF', 30)

        ceu = pygame.image.load("imagens/ceu.png")
        nuvem = pygame.image.load("imagens/cloud.png")
        nuvem_chuva = pygame.image.load("imagens/cloud_rain.png")
        nuvem_2 = pygame.image.load("imagens/cloud_2.png")

        preto = (0, 0, 0)
        cinza = (35, 35, 35)
        cinza_2 = (70, 70, 70)

        bt1 = Botao("Jogar", screen, (largura-205, 100), cor_fonte = preto, imagem = nuvem, imagem_2 = nuvem_chuva)
        bt1.font = font_2
        bt2 = Botao("Loja", screen, (largura-205, 315), cor_fonte = cinza, imagem = nuvem, imagem_2 = nuvem_chuva)
        bt2.font = font_2
        bt3 = Botao("Sair", screen, (largura-205, 530), cor_fonte = cinza_2, imagem = nuvem, imagem_2 = nuvem_chuva)
        bt3.font = font_2

        x_centro_nuvem = nuvem_2.get_rect().centerx
        y_centro_nuvem = nuvem_2.get_rect().centery

        while True:

            click = False

            screen.fill((20,20,20))
            screen.blit(ceu, (0,0))

            screen.blit(nuvem_2, (25,25))
            escrever_centralizado("Plat", font, cinza_2, screen, x_centro_nuvem+25, y_centro_nuvem - 70)
            escrever_centralizado("Pinhas", font, cinza, screen, x_centro_nuvem+25, y_centro_nuvem + 30)

            # Exibe botão "Jogar"
            bt1.draw_image()
            bt1.escrever(y_varia = 10)

            # Exibe botão "Loja"
            bt2.draw_image()
            bt2.escrever(y_varia = 10)

            # Exibe botão "Sair"
            bt3.draw_image()
            bt3.escrever(y_varia = 10)

            pos_mou = pygame.mouse.get_pos()

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = True  

                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            exit()

            if bt1.esta_botao_imagem and click:
                self.jogo(screen)

            if bt2.esta_botao_imagem and click:
                self.loja.exibir_loja()

            if bt3.esta_botao_imagem and click:
                pygame.quit()
                exit()

            pygame.display.update()
            clock.tick(60)

    def jogo(self, screen):
        import pygame as pg
        import numpy as np
        import dev_game as gs #game src
        import menu as mn

        PLAYER_SPEED = 10
        CAMERA_DISTANCE = 15
        GRAVITY = 40
        SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
        MOUSE_SENSITIVITY = 0.1

        pers_selecionado = self.loja.selecionado()

        game = gs.Game(surface=screen, player_speed=PLAYER_SPEED, camera_distance=CAMERA_DISTANCE,
                       gravity=GRAVITY, mouse_sensitivity=MOUSE_SENSITIVITY, character=pers_selecionado)
        game.start_game()
