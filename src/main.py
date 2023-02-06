import pygame
import sys
from const import *
from game import Game
from board import *
class Main:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption("Chess50")
        self.game = Game()
    
    def mainloop(self):
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger
        while True:

            game.show_background(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #store current position
                    #if the square had piece, move it
                    dragger.update_mouse(event.pos)
                    print(event.pos)

                    clicked_row = dragger.mouseY // SQUARE_SIZE
                    clicked_col = dragger.mouseX // SQUARE_SIZE
                    
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        
                        if piece.color == game.next_player: #check valid turn

                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            game.show_moves(screen)
                          

                #mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    #follow up
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #game.show_background(screen)
                        #game.show_pieces(screen)
                        dragger.update_blit(screen)

                #release click
                elif event.type == pygame.MOUSEBUTTONUP:
                    #know the coordinates
                    #put the piece if valid
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQUARE_SIZE
                        released_col = dragger.mouseX // SQUARE_SIZE

                        #create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_moves(dragger.piece, move):
                            board.move(dragger.piece, move)
                            
                            game.show_background(screen)
                            game.show_pieces(screen)
                            game.next_turn()

                    dragger.undrag_piece(piece)


                elif event.type == pygame.QUIT:
                    sys.exit()
        

            pygame.display.update()
if __name__ == "__main__":
    main = Main()
    main.mainloop()