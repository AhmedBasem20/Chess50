import pygame
from const import *

class Game:

    def __init__(self):
        pass
    
    def show_background(self, surface):
        """Draw the chess background
        args: pygame surface"""
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (0, 0, 0)
                    
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)
    def show_pieces():
        pass