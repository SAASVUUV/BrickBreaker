from PPlay.window import *
from PPlay.sprite import *
from random import randint
janela = Window(900, 1000)
janela.set_title("Brick Breaker!")
background = Sprite("background.jpg")
pad = Sprite("pad.png")
pad.set_position(janela.width/2-pad.width/2, 950)
teclado = janela.get_keyboard()
ball = Sprite("ball.png")
ball.set_position(janela.width/2 - ball.width/2, 750)
def create_bricks():
    bricks = []
    for i in range(8):
        b_line = []
        for j in range(19):
            a = randint(1, 15)
            if a == 6 and i != 7:
                special_brick = Sprite("special_brick.png")
                special_brick.set_position(5 +j*47, 100 + i*47)
                b_line.append(special_brick)
            else:
                default_brick = Sprite("defaultbrick.png")
                default_brick.set_position(5+j*47, 100 + i*47)
                b_line.append(default_brick)
        bricks.append(b_line)
    return bricks
def draw_bricks(bricks):
    for i in range(len(bricks)):
        for j in range(len(bricks[0])):
            bricks[i][j].draw()

bricks = create_bricks()
while True:
    background.draw()
    if (teclado.key_pressed("left")) and (pad.x > 0):
        pad.move_x(janela.delta_time()*400*-1)
    if (teclado.key_pressed("right")) and (pad.x + pad.width < janela.width):
        pad.move_x(janela.delta_time()*400)
    draw_bricks(bricks)
    ball.draw()
    pad.draw()
    janela.update()