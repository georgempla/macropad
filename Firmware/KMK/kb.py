import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner

class Keyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.matrix = KeysScanner(
            pins=[
                board.D3,  
                board.D4,  
                board.D1,  
                board.D0,  
                board.D5,  
                board.D6,  
            ],
            value_when_pressed=False,
        )

        self.coord_mapping = [0, 1, 2, 3, 4, 5]
