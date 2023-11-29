from PPlay.window import *
from PPlay.sprite import *
from random import randint
from PPlay.keyboard import *
from PPlay.collision import *
import math
from lose import lose
from win import win

background = Sprite("Game_images/background.jpg")


def game(janela, teclado, menu):
    # temporizadores:
    tempo_total = 0  # tempo total decorrido
    big_time = 6  # tempo que o pad permanece grande
    big_starter = 0  # momento em que o pad fica grande

    # criação do pad
    pad = Sprite("Game_images/pad.png")
    pad.set_position(janela.width / 2 - pad.width / 2, 900)
    vel_pad = 400  # velocidade do pad
    pad_state = 0  # estado do pad(normal == 0 e grande == 1)

    # criação da bola(lá ele)
    ball = Ball(janela.width / 2, 700, 0, 1)
    balls = [ball]  # lista de bolas

    # criação dos tijolos
    bricks, alive_bricks = create_bricks()
    # bricks é a lista dos tijolos em si, já o alive vai indicar quais não foram destruídos e o tipo(de explosão, de
    # crescer o pad ou de adicionar bolinhas

    # game loop
    while True:
        background.draw()  # desenha o background
        mov_pad(janela, pad, vel_pad, teclado)  # movimentação do pad
        for bola in balls:
            if bola.sprite.y + 25 >= janela.height:#caso a bolinha acerte atrás do pad, será removida
                balls.remove(bola)
            bola.move(janela.delta_time())
            # atualiza a posição de cada bolinha
            bola.draw()  # desenha cada bola
            # a rebatida da bola na parede, fazendo a correção do escorregamento:
            if bola.y <= 0 or (bola.y + bola.height()) >= (janela.height):
                bola.y = 0 if bola.y <= 0 else (janela.height - bola.height())
                bola.direction_y *= -1.001
            if bola.x <= 0 or (bola.x + bola.width()) >= (janela.width):
                bola.x = 0 if bola.x <= 0 else (janela.width - bola.width())
                bola.direction_x *= -1.001
            # para cada tijolo, verificar a colisão com a bolinha, implementei uma otimização para que só verifique caso
            # a bolinha esteja próxima da altura da matriz dos tijolos
            if bola.x <= bricks[-1][0].x + bricks[-1][0].height + 5 or bola.x - bola.height() >= bricks[0][0].x - 5:
                for i in range(8):
                    for j in range(19):
                        if alive_bricks[i][j] != 0 and Collision.collided(bricks[i][j], bola.sprite):
                            # no caso de colisão, irá ser feita a verificação do tipo do tijolo, em seguida o acionamento dos poderes
                            if alive_bricks[i][j] == 2:
                                explosion(i, j, alive_bricks, pad, tempo_total, big_starter, pad_state, balls)
                            elif alive_bricks[i][j] == 3:
                                pad, pad_state, big_starter = bigger_pad(pad, tempo_total)
                                # após o crescimento do pad, seu estado passará a ser 1 e será inicializado o tempo dele
                            elif alive_bricks[i][j] == 4:
                                more_balls(balls, pad)
                                # adiciona duas bolinhas ao acertar esse tijolo
                            alive_bricks[i][j] = 0
                            #redirecionamento da bolinha ao acertar o tijolo
                            #caso da bolinha estar vindo de cima
                            if ball.sprite.y >= bricks[i][j].y + 40:
                                normalizedRelativeX = ((bricks[i][j].x + 45 / 2) - (
                                            bola.sprite.x + bola.sprite.height / 2)) / (45 / 2)
                                angle = (5 * math.pi / 12) * normalizedRelativeX
                                bola.direction_y = math.cos(-angle)
                                bola.direction_x = math.sin(-angle)

                            elif ball.sprite.y < bricks[i][j].y:
                                normalizedRelativeX = ((bricks[i][j].x + 45 / 2) - (
                                            bola.sprite.x + bola.sprite.height / 2)) / (45 / 2)
                                angle = (5 * math.pi / 12) * normalizedRelativeX
                                bola.direction_y = -math.cos(-angle)
                                bola.direction_x = -math.sin(-angle)
                            else:
                                bola.direction_x *= -1

            #redirecionada a colisão da bola com o pada
            if Collision.collided(pad, bola.sprite):
                normalizedRelativeX = ((pad.x + pad.width / 2) - (bola.sprite.x + bola.sprite.width / 2)) / (
                            pad.width / 2)
                angle = (5 * math.pi / 12) * normalizedRelativeX
                bola.direction_y = -math.cos(angle)
                bola.direction_x = -math.sin(angle)
         #se todas as bolinhas acabarem, o jogador perdeu
        if len(balls) == 0:
            lose(janela, menu)
        # ao terminar o tempo em que fica grande, volta ao normal
        if pad_state == 1 and tempo_total - big_starter > big_time:
            pad_state = 0
            x = pad.x
            y = pad.y
            pad = Sprite("Game_images/pad.png")
            pad.set_position(x, y)

        #apertando ESC o jogador volta ao menu
        if teclado.key_pressed('ESC'):
            menu()

        # desenha o pad e os tijolos
        pad.draw()
        draw_bricks(bricks, alive_bricks, janela, menu)

        # atualiza o tempo
        tempo_total += janela.delta_time()

        janela.update()


# desenha os tijolos
def draw_bricks(bricks, alive_bricks, janela, menu):
    win_condition = 0
    for i in range(len(bricks)):
        for j in range(len(bricks[0])):
            if alive_bricks[i][j] != 0:
                bricks[i][j].draw()
                win_condition = 1
    if win_condition == 0:
        win(janela, menu)


# cria os tijolos
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
                explosion_brick.set_position(4 + j * 47, 100 + i * 47)
                b_line.append(explosion_brick)
                a_line.append(2)

            elif a == 7 and i != 7:
                bigger_brick = Sprite("Game_images/bigger_brick.png")
                bigger_brick.set_position(4 + j * 47, 100 + i * 47)
                b_line.append(bigger_brick)
                a_line.append(3)

            elif a == 8 and i != 7:
                more_balls_brick = Sprite("Game_images/more_balls_brick.png")
                more_balls_brick.set_position(4 + j * 47, 100 + i * 47)
                b_line.append(more_balls_brick)
                a_line.append(4)
            else:
                default_brick = Sprite("Game_images/defaultbrick.png")
                default_brick.set_position(4 + j * 47, 100 + i * 47)
                b_line.append(default_brick)
                a_line.append(1)
        alive_bricks.append(a_line)
        bricks.append(b_line)
    return bricks, alive_bricks


# movimentação do pad
def mov_pad(janela, pad, vel_pad, teclado):
    if teclado.key_pressed("LEFT") and pad.x > 0:
        pad.move_x(-vel_pad * janela.delta_time())
    if teclado.key_pressed("RIGHT") and pad.x < (janela.width - pad.width):
        pad.move_x(vel_pad * janela.delta_time())


# explosão:
def explosion(i, j, alive_bricks, pad, tempo_total, big_starter, pad_state, balls):
    # o tijolo de explosão irá destruir todos os tijolos em volta, incluindo outros que possuam poderes
    for t in range(i - 1, i + 2):
        for q in range(j - 1, j + 2):
            if alive_bricks[t][q] == 2:
                alive_bricks[t][q] = 0
                explosion(t, q, alive_bricks, pad, tempo_total, big_starter, pad_state, balls)
            elif alive_bricks[t][q] == 3:
                pass
                #pad, pad_state, big_starter = bigger_pad(pad, tempo_total)
                #return pad, pad_state, big_starter
            elif alive_bricks[t][q] == 4:
                more_balls(balls, pad)
            alive_bricks[t][q] = 0


# poder que aumenta o pad
def bigger_pad(pad, tempo_total):
    x = pad.x
    y = pad.y
    pad = Sprite("Game_images/big_pad.png")
    pad.set_position(x, y)
    pad_state = 1
    big_starter = tempo_total
    return pad, pad_state, big_starter


# poder que adiciona mais bolas, incompleto
def more_balls(balls, pad):
    ball1 = Ball(pad.x + 30, pad.y - 30, -1, -1)
    balls.append(ball1)
    ball2 = Ball(pad.x + pad.width - 30 , pad.y - 30, 1, -1)
    balls.append(ball2)


# classe da bola
class Ball:

    def __init__(self, x, y, dir_x, dir_y):
        self.sprite = Sprite("Game_images/ball.png")
        self.x = x
        self.y = y
        self.sprite.set_position(self.x, self.y)
        self.direction_x = dir_x
        self.direction_y = dir_y

    def x(self):
        return self.sprite.x

    def y(self):
        return self.sprite.y

    def width(self):
        return self.sprite.width

    def height(self):
        return self.sprite.height

    def move(self, delta_time):
        self.sprite.move_x(350 * self.direction_x * delta_time)
        self.sprite.move_y(350 * self.direction_y * delta_time)
        self.x = self.sprite.x
        self.y = self.sprite.y

    def draw(self):
        self.sprite.draw()
