import os
from const import *

class Square:

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
    
    def has_piece(self):
        return self.piece != None

class Board:
    
    def __init__(self):
        self.squares = [[0,0,0,0, 0,0,0,0] for col in range(COLS)] #console board
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def _create(self):

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
   
    def _add_pieces(self,color):
        if color == 'white':
            row_pawn, row_other = (6,7) #last two rows
        else:
            row_pawn, row_other = (1,0) #first two rows

        #pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        #knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        #bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        #rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        #king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        
class Piece:

    def __init__(self, name, color, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        self.texture = texture
        self.moves = []
        self.moved = False
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f"assets/images/imgs-{size}px/{self.color}_{self.name}.png"
        )
    def add_moves(self, move):
        self.moves.append(move)
class Pawn(Piece):

    def __init__(self, color):
        if color == 'white':
            self.dir = -1
        else:
            self.dir = 1
        
        super().__init__('pawn', color)

class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color)

class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color)

class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color)

class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color)

class King(Piece):

    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color)