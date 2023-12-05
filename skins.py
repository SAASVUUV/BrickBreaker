from PPlay.window import*
from PPlay.sprite import*
from PPlay.gameimage import*
from PPlay.keyboard import *

background = GameImage('Game_images/skinsmenu.png')

#defini cada um dos sprites
default_pad = Sprite('Game_images/pad.png')
pad2 = Sprite('Game_images/pad2.png')
pad3 = Sprite('Game_images/pad3.png')
pad4 = Sprite('Game_images/pad4.png')
pad5 = Sprite('Game_images/pad5.png')
#essa será a borda que ficará em volta do pad escolhido
borda1 = Sprite('Game_images/borda.png')
borda1.set_position(900, 1000)#coloquei nessa posição para que não apareça a pincípio
default_ball = Sprite('Game_images/ball.png')
ball2 = Sprite('Game_images/ball2.png')
ball3 = Sprite('Game_images/ball3.png')
ball4 = Sprite('Game_images/ball4.png')
ball5 = Sprite('Game_images/ball5.png')
#borda que ficará em volta da bola escolhida
borda2 = Sprite('Game_images/borda2.png')
borda2.set_position(900, 1000)
def skins(janela, teclado, cursor):
    skin_pad = 1
    skin_ball = 1
    default_pad.set_position(janela.width/2 - default_pad.width/2, janela.height/10)
    pad2.set_position(janela.width / 2 - default_pad.width*3/2, janela.height* 2/ 10)
    pad3.set_position(janela.width / 2 - default_pad.width*3/2, janela.height *4/ 10)
    pad4.set_position(janela.width / 2 + default_pad.width / 2, janela.height *2/ 10)
    pad5.set_position(janela.width / 2 + default_pad.width / 2, janela.height *4/ 10)




    default_ball.set_position(janela.width / 2 - default_ball.width / 2, janela.height*6 / 10)
    ball2.set_position(janela.width*3/10, janela.height * 7 / 10)
    ball3.set_position(janela.width*3/10, janela.height * 8 / 10)
    ball4.set_position(janela.width*7/10, janela.height * 7 / 10)
    ball5.set_position(janela.width*7/10, janela.height * 8 / 10)
    while True:
        background.draw()
        if cursor.is_over_object(default_pad) and cursor.is_button_pressed(1):
            borda1.set_position(default_pad.x - 3, default_pad.y - 3)
            skin_pad = 1
        elif cursor.is_over_object(pad2) and cursor.is_button_pressed(1):
            borda1.set_position(pad2.x - 3, pad2.y - 3)
            skin_pad = 2
        elif cursor.is_over_object(pad3) and cursor.is_button_pressed(1):
            borda1.set_position(pad3.x - 3, pad3.y - 3)
            skin_pad = 3
        elif cursor.is_over_object(pad4) and cursor.is_button_pressed(1):
            borda1.set_position(pad4.x - 3, pad4.y - 3)
            skin_pad = 4
        elif cursor.is_over_object(pad5) and cursor.is_button_pressed(1):
            borda1.set_position(pad5.x - 3, pad5.y - 3)
            skin_pad = 5


        if cursor.is_over_object(default_ball) and cursor.is_button_pressed(1):
            borda2.set_position(default_ball.x - 4, default_ball.y - 4)
            skin_ball = 1
        elif cursor.is_over_object(ball2) and cursor.is_button_pressed(1):
            borda2.set_position(ball2.x - 4, ball2.y - 4)
            skin_ball = 2
        elif cursor.is_over_object(ball3) and cursor.is_button_pressed(1):
            borda2.set_position(ball3.x - 4, ball3.y - 4)
            skin_ball = 3
        elif cursor.is_over_object(ball4) and cursor.is_button_pressed(1):
            borda2.set_position(ball4.x - 4, ball4.y - 4)
            skin_ball = 4
        elif cursor.is_over_object(ball5) and cursor.is_button_pressed(1):
            borda2.set_position(ball5.x - 4, ball5.y - 4)
            skin_ball = 5
        default_pad.draw()
        pad2.draw()
        pad3.draw()
        pad4.draw()
        pad5.draw()
        borda1.draw()
        default_ball.draw()
        ball2.draw()
        ball3.draw()
        ball4.draw()
        ball5.draw()
        borda2.draw()
        if teclado.key_pressed('ESC'):
            return skin_pad, skin_ball
        janela.update()
