import pygame  
import sys  
  
  
pygame.init()  
res = (720,720)  
screen = pygame.display.set_mode(res)  
color = (46,52,64)  
color_light = (170,170,170)  
color_dark = (100,100,100)  
width = screen.get_width()  
height = screen.get_height()   
smallfont = pygame.font.SysFont("Arial Black", 40)  
text = smallfont.render('start' , True , color)  
text2 = smallfont.render('sair' , True , color)  

run = True

class Btn () :
    def __init__(self, texto, action):
        self.conteudo_texto = texto
        self.texto = smallfont.render(texto, True, color)
        self.ret_text = self.texto.get_rect()
        self.acao = action

    def draw(self ,coordenada, cor):
        self.x = coordenada[0] - 10
        self.y = coordenada[1] - 10
        self.largura = self.ret_text.width + 20
        self.altura = self.ret_text.height + 20
        pygame.draw.rect(screen, cor, [self.x, self.y, self.largura, self.altura])
        screen.blit(self.texto, coordenada)

    def click(self, coordenada):
        if self.x + self.largura >= coordenada[0] >= self.x and self.y + self.altura >= coordenada[1] >= self.y:
            print("clickou" + self.conteudo_texto)
            if self.acao == "sair":  
                global run
                run = False 

while run:  
    screen.fill((60,25,60))  
      
    mouse = pygame.mouse.get_pos()  

    lista_botoes = []

    btn_start = Btn("Start", "comecar")
    btn_exit = Btn("Exit", "sair")
    btn_loja = Btn("Loja", "comprar")

    lista_botoes.append(btn_start)
    lista_botoes.append(btn_exit)
    lista_botoes.append(btn_loja)

    coord_x, coord_y = width/2-53.5, height/2-28.5

    for i in range(len(lista_botoes)):
        lista_botoes[i].draw((coord_x, coord_y + i * 100), color_dark)
        
        x_btn, btn_largura = lista_botoes[i].x, lista_botoes[i].largura
        y_btn, btn_altura = lista_botoes[i].y, lista_botoes[i].altura

        if  x_btn + btn_largura >= mouse[0] >= x_btn and y_btn + btn_altura >= mouse[1] >= y_btn:
            lista_botoes[i].draw((coord_x, coord_y + i * 100), color_light)  
            

    for ev in pygame.event.get():  
        if ev.type == pygame.QUIT:  
            run = False  
            
        if ev.type == pygame.MOUSEBUTTONDOWN:  
            for btn in lista_botoes:
                btn.click(mouse)

    pygame.display.update() 