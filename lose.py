from PPlay.window import *
from PPlay.gameimage import *
from PPlay.keyboard import *
background = GameImage("Game_images/lose_background.png")
teclado = Keyboard()
def lose(janela, menu):
    while True:
        background.draw()
        if teclado.key_pressed("SPACE"):
            menu()
        janela.update()