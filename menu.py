import pygame  
import sys  

class Btn () :
    def __init__(self, texto, action, color):
        self.font = pygame.font.SysFont("Arial Black", 40)
        self.conteudo_texto = texto
        self.texto = self.font.render(texto, True, color)
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
            return self.acao()

class Menu():
    def __init__(self, btns, cx, cy, darkc, lightc):
        self.botoes = btns
        self.running = False
        self.coord_x = cx
        self.coord_y = cy
        self.color_dark = darkc
        self.color_light = lightc

    def end(self):
        self.running = False

    def draw_buttons(self):
        for i in range(len(self.botoes)):
                    self.botoes[i].draw((self.coord_x, self.coord_y + i * 100), self.color_dark)
                    
                    x_btn, btn_largura = self.botoes[i].x, self.botoes[i].largura
                    y_btn, btn_altura = self.botoes[i].y, self.botoes[i].altura

                    if  x_btn + btn_largura >= self.mouse[0] >= x_btn and y_btn + btn_altura >= self.mouse[1] >= y_btn:
                        self.botoes[i].draw((self.coord_x, self.coord_y + i * 100), self.color_light)  

    def check_clicks(self):
        for ev in pygame.event.get():  
            if ev.type == pygame.QUIT:  
                self.running = False  
                
            if ev.type == pygame.MOUSEBUTTONDOWN:  
                for btn in self.botoes:
                    btn.click()

    def start(self):
        self.running = True

        while self.running:
            screen.fill((60,25,60))  
      
            self.mouse = pygame.mouse.get_pos()

            self.draw_buttons()
            self.check_clicks()

            pygame.display.flip() 
    
if __name__ == "__main__":
    pygame.init()

    WIDTH = 720
    HEIGHT = 720
    res = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(res)

    start_button = Btn("Start", )

    menu = Menu(btns=(Btn("Start", "comecar",(46,52,64)), Btn("Exit", "sair",(46,52,64)), Btn("Loja", "comprar",(46,52,64))),
                cx=WIDTH/2-53.5, cy=HEIGHT/2-28.5,
                darkc=(100,100,100), lightc=(170,170,170))

    menu.start()
