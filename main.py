from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.gameimage import *
from PPlay.keyboard import *
from game import game
from skins import skins


janela = Window(900, 1000)
janela.set_title("Brick Breaker!")
background = GameImage("Game_images/Menu_background.png")
teclado = Keyboard()
cursor = Mouse()

def menu():
    skin_pad = 1
    skin_bola = 1
    while True:
        #desenha o background e os botões
        background.draw()
        janela.draw_text('Play', 320, 400, 100, (255, 255, 0), "Arial", True, True)
        janela.draw_text('Skins', 280, 550, 100, (255, 255, 0), "Arial", True, True)
        janela.draw_text('Exit', 320, 700, 100, (255, 255, 0), "Arial", True, True)

        if cursor.is_over_area((320,400), (550, 500)) and cursor.is_button_pressed(1):
            game(janela, teclado, menu, skin_pad, skin_bola)
        if cursor.is_over_area((280,550), (550, 650)) and cursor.is_button_pressed(1):
            skin_pad, skin_bola = skins(janela, teclado, cursor)
        if cursor.is_over_area((320, 700), (530, 800)) and cursor.is_button_pressed(1):
            janela.close()
        janela.update()

menu()