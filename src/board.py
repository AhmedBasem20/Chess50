import os
from const import *
from move import *
class Square:

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
    
    def has_piece(self):
        return self.piece != None

    def isempty(self):
        return not self.has_piece()
    
    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color
    
    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def isempty_or_rival(self, color):
        return self.has_piece() == False or self.has_rival_piece(color)

    @staticmethod
    def in_board_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    
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
        


    def calc_moves(self, piece, row, col):
        """calculate all the valid moves of the selected piece"""
        
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                move_row = row + row_incr
                move_col = col + col_incr

                while True:
                    if Square.in_board_range(move_row, move_col):
                        #create initial and final move squares
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        #create new move
                        move = Move(initial, final)
                    
                        #empty
                        if self.squares[move_row][move_col].isempty():
                            piece.add_move(move)
                            
                        #has rival piece
                        if self.squares[move_row][move_col].has_rival_piece(piece.color):
                            #create new move
                            piece.add_move(move)
                            break
                        #has team piece
                        if self.squares[move_row][move_col].has_team_piece(piece.color):
                
                            break
                    else: break
                    #incremening moves
                    move_row += row_incr
                    move_col += col_incr       


        if piece.name == "pawn":
            
            #better approach
            steps = 1 if piece.moved else 2
            start = row + piece.dir
            end = row  + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_board_range(move_row):
                    if self.squares[move_row][col].isempty():
                        #create initial and final move squares
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        #create new move
                        move = Move(initial, final)
                        piece.add_move(move)
                    
                    else: break #blocked
                
                else: break #not in range
            
            #attack moves
            move_row = row + piece.dir
            move_cols = [col-1, col+1]
            for move_col in move_cols:
                if Square.in_board_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_rival_piece(piece.color):
                        #create initial and final move squares
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        #create new move
                        move = Move(initial, final)
                        piece.add_move(move)

        elif piece.name == "knight":
            #8 valid moves
            valid_moves = [
                (row-2,col+1),
                (row-2, col-1),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col+2),
                (row+1, col-2),
                (row-1, col+2),
                (row-1, col-2)
            ]
            for valid_move in valid_moves:
                valid_move_row, valid_move_col = valid_move
                
                if Square.in_board_range(valid_move_row, valid_move_col):
                    if self.squares[valid_move_row][valid_move_col].isempty_or_rival(piece.color):
                        #create new move squares
                        initial = Square(row, col)
                        final = Square(valid_move_row, valid_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)
            print(piece.moves[0])
            print(piece.moves[1])
        elif piece.name == "bishop":
            straightline_moves([
                (-1,1),
                (-1,-1),
                (1,-1),
                (1,1)
            ])
        
        elif piece.name == "rook":
            straightline_moves([
                (0,1),
                (0,-1),
                (1,0),
                (-1,0)
            ])
        
        elif piece.name == "queen":
            straightline_moves([
                (-1,1),
                (-1,-1),
                (1,-1),
                (1,1),
                (0,1),
                (0,-1),
                (1,0),
                (-1,0)
            ])
        
        elif piece.name == "king":
            pass
        
    



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
    def add_move(self, move):
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