from PPlay.window import *
from PPlay.sprite import *
from random import randint
from PPlay.keyboard import *
from PPlay.collision import *
from math import sqrt



background = Sprite("Game_images/background.jpg")


def game(janela, teclado):
    #temporizadores:
    tempo_total = 0#tempo total decorrido
    big_time = 4#tempo que o pad permanece grande
    big_starter = 0#momento em que o pad fica grande

    #criação do pad
    pad = Sprite("Game_images/pad.png")
    pad.set_position(janela.width/2 - pad.width/2, 900)
    vel_pad = 300#velocidade do pad
    pad_state = 0#estado do pad(normal == 0 e grande == 1)

    #criação da bola(lá ele)
    ball = Ball(janela.width/2, 700)
    balls = [ball]#lista de bolas
    vel_bola = 300#velocidade das bolas
    direction_x = 1
    direction_y = 1

    #criação dos tijolos
    bricks, alive_bricks = create_bricks()
    #bricks é a lista dos tijolos em si, já o alive vai indicar quais não foram destruídos e o tipo(de explosão, de
    #crescer o pad ou de adicionar bolinhas

    #game loop
    while True:
        background.draw()#desenha o background
        mov_pad(janela, pad, vel_pad, teclado)#movimentação do pad
        for bola in balls:
            bola.set_position(bola.x + (vel_bola * janela.delta_time() * direction_x), bola.y - (vel_bola*janela.delta_time()*direction_y))
            #atualiza a posição de cada bolinha
            bola.draw()#desenha cada bola
            # a rebatida da bola na parede, fazendo a correção do escorregamento:
            if bola.y <= 0 or (bola.y + bola.height()) >= (janela.height):
                bola.y = 0 if bola.y <= 0 else (janela.height - bola.height())
                direction_y *= -1
            if bola.x <= 0 or (bola.x + bola.width()) >= (janela.width):
                bola.x = 0 if bola.x <= 0 else (janela.width - bola.width())
                direction_x *= -1
            #para cada tijolo, verificar a colisão com a bolinha, implementei uma otimização para que só verifique caso
            #a bolinha esteja próxima da altura da matriz dos tijolos
            if bola.x <= bricks[-1][0].x + bricks[-1][0].height + 5 or bola.x - bola.height() >= bricks[0][0].x - 5:
                for i in range(8):
                    for j in range(19):
                        if alive_bricks[i][j] != 0 and Collision.collided(bricks[i][j], bola.sprite):
                            #no caso de colisão, irá ser feita a verificação do tipo do tijolo, em seguida o acionamento dos poderes
                            if alive_bricks[i][j] == 2:
                                explosion(i, j, alive_bricks, pad)
                            elif alive_bricks[i][j] == 3:
                                pad = bigger_pad(pad)
                                #após o crescimento do pad, seu estado passará a ser 1 e será inicializado o tempo dele
                                pad_state = 1
                                big_starter = tempo_total

                            elif alive_bricks[i][j] == 4:
                                pass
                                #tentei implementar esse poder, mas não deu certo
                                #more_balls(balls, pad)
                            #após isso, a direção é alterada e o tijolo passa a ser do tipo 0(morto)
                            alive_bricks[i][j] = 0
                            direction_y *= -1

            if Collision.collided(pad, bola.sprite):
                direction_y *= -1
                #aspecto a melhorar, pois seria melhor que tanto o angulo, quanto o ponto onde a bola bate influenciassem
                #na rebatida da bola no pad

        #ao terminar o tempo em que fica grande, volta ao normal
        if pad_state == 1 and tempo_total - big_starter > big_time:
            pad_state = 0
            x = pad.x
            y = pad.y
            pad = Sprite("Game_images/pad.png")
            pad.set_position(x, y)

        #desenha o pad e os tijolos
        pad.draw()
        draw_bricks(bricks, alive_bricks)

        #atualiza o tempo
        tempo_total += janela.delta_time()

        janela.update()





#desenha os tijolos
def draw_bricks(bricks, alive_bricks):
    for i in range(len(bricks)):
        for j in range(len(bricks[0])):
            if alive_bricks[i][j] != 0:
                bricks[i][j].draw()

#cria os tijolos
def create_bricks():
    bricks = []
    alive_bricks = []
    for i in range(8):
        b_line = []
        a_line = []
        for j in range(19):
            a = randint(1, 15)
            if a == 6 and i != 7 and j != 0 and j != 18:
                explosion_brick = Sprite("Game_images/special_brick.png")
                explosion_brick.set_position(5 +j*47, 100 + i*47)
                b_line.append(explosion_brick)
                a_line.append(2)

            elif a == 7 and i != 7:
                bigger_brick = Sprite("Game_images/bigger_brick.png")
                bigger_brick.set_position(5 + j*47, 100 + i*47)
                b_line.append(bigger_brick)
                a_line.append(3)

            elif a == 8 and i != 7:
                more_balls_brick = Sprite("Game_images/more_balls_brick.png")
                more_balls_brick.set_position(5 + j*47, 100 + i*47)
                b_line.append(more_balls_brick)
                a_line.append(4)
            else:
                default_brick = Sprite("Game_images/defaultbrick.png")
                default_brick.set_position(5+j*47, 100 + i*47)
                b_line.append(default_brick)
                a_line.append(1)
        alive_bricks.append(a_line)
        bricks.append(b_line)
    return bricks, alive_bricks

#movimentação do pad
def mov_pad(janela, pad, vel_pad, teclado):
    if teclado.key_pressed("LEFT") and pad.x > 0:
        pad.move_x(-vel_pad * janela.delta_time())
    if teclado.key_pressed("RIGHT") and pad.x < (janela.width - pad.width):
        pad.move_x(vel_pad * janela.delta_time())


#explosão:
def explosion(i, j, alive_bricks, pad):
    #o tijolo de explosão irá destruir todos os tijolos em volta, incluindo outros que possuam poderes
    for t in range(i - 1, i + 2):
        for q in range(j - 1, j + 2):
            if alive_bricks[t][q] == 2:
                alive_bricks[t][q] = 0
                explosion(t, q, alive_bricks, pad)
            elif alive_bricks[t][q] == 3:
                bigger_pad(pad)
            elif alive_bricks[t][q] == 4:
                pass
            alive_bricks[t][q] = 0

#poder que aumenta o pad
def bigger_pad(pad):
    x = pad.x
    y = pad.y
    pad = Sprite("Game_images/big_pad.png")
    pad.set_position(x, y)
    return pad

#poder que adiciona mais bolas, incompleto
def more_balls(balls, pad):
    ball1 = Ball(pad.x, pad.y + 25)
    balls.append(ball1)
    ball2 = Ball(pad.x + pad.width, pad.y + 25)
    balls.append(ball2)


#classe da bola
class Ball:

    def __init__(self, x, y):
        self.sprite = Sprite("Game_images/ball.png")
        self.x = x
        self.y = y
        self.sprite.set_position(self.x, self.y)

    def x(self):
        return self.x

    def y(self):
        return self.y

    def width(self):
        return self.sprite.width

    def height(self):
        return self.sprite.height
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.sprite.set_position(x, y)

    def draw(self):
        self.sprite.draw()
