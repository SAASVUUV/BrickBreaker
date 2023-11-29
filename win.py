from PPlay.window import *
from PPlay.gameimage import *
from PPlay.keyboard import *
background = GameImage("Game_images/win_background.png")
teclado = Keyboard()
def win(janela, menu):
    while True:
        background.draw()
        if teclado.key_pressed("SPACE"):
            menu()
        janela.update()