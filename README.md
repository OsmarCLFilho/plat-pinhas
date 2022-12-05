# plat-pinhas
## Objetivo do Jogo
O objetivo deste jogo é sobreviver o maior tempo possível, pulando da plataforma atual para a plataforma seguinte, caso o tempo acabe ou o personagem caia o jogo termina.
## Controles
- **A**: O personagem move para a esquerda.
- **D**: O personagem move para a direita.
- **W**: O personagem move para frente.
- **S**: O personagem move para a trás.
- **Espaço**: O personagem pula.

Observação: É possível saltar no ar quando o personagem estiver empurrando um dos lados da plataforma.
- **Esc**: Sair do jogo.

## Progressão
A medida que você vai jogando seus pontos vão acumulando, com esses pontos é possível comprar novos personagens com diferentes atributos, que vão te dar diferentes vantagens para sobreviver por mais tempo.

## Mecânicas do Jogo
Ao decorrer do jogo um dos seguinte três tipos de plataformas serão geradas aleatoriamente em frente ao jogador:
### Plataformas
- **Normal**: Plataforma fixa, a qual o jogador conseguirá soltar normalmente.
- **Alta**: Plataforma fixa, com a altura maior do que a normal. Caso seu pulo seja muito fraco, será necessário encostar nela para conseguir escalá-la.
- **Móvel**: Plataforma de altura normal que ficará se movimentando da direita para esquerda. Os octaedros delimitam seu movimento.
### Personagens
- **Gala Galinha**: Personagem padrão, com pulos fracos e baixa velocidade. Ela não conseguirá ir mais rápido que as plataformas, portanto não é possível ir muito longe com ela.
- **Emaperson**: Personagem disponível na loja por 100 pontos, pulo bem mais alto e velocidade maior, mas ainda mais lenta que as plataformas. 
- **Gala Gali**: Personagem disponível na loja por 500 pontos, pulo fraco e velocidade bem maior, que irá permitir ir mais rápido que as plataformas.
- **Emapon**: Personagem disponível na loja por 2.000 pontos, pulo bem mais alto e velocidade bem maior.

## Código
- **render.py**: Calcula os triângulos das mesh dentro do espaço, projeta elas na tela e define a ordem em que são renderizadas.
- **game.py**: Contém a lógica do jogo, que se encarrega de de calcular coisas como colisões com o jogador e as posições de cada objeto dentro do espaço, usando as classes do render.py.
- **loja.py**: Se encarrega de desenhar na tela os diferentes menu e da navegação entre eles e o jogo em si.
- **jogo.py**: Se encarrega de iniciar o jogo, chamando o menu principal.
