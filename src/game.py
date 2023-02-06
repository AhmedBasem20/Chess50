import pygame
from board import *
from const import *
from dragger import *

class Game:

    def __init__(self):
        self.next_player = 'white'
        self.board = Board()
        self.dragger = Dragger()
    def show_background(self, surface):
        """Draw the chess background
        args: pygame surface"""
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (200, 200, 200)
                else:
                    color = (100, 50, 30)
                    
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) #tuple of: x, y, width, height
                pygame.draw.rect(surface, color, rect)
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    #all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                print(str(move.final.row)+" "+str(move.final.col))
                #color
                color = (255,0,0) if (move.final.row + move.final.col) % 2 == 0 else (0,255,0)
                #rect
                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                #draw
                pygame.draw.rect(surface, color, rect)
    
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        