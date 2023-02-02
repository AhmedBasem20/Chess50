import pygame
import sys
from const import *
from game import Game
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
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)

                #mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    #follow up
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        dragger.update_blit(screen)

                #release click
                elif event.type == pygame.MOUSEBUTTONUP:
                    #know the coordinates
                    #put the piece if valid
                    dragger.undrag_piece(piece)


                elif event.type == pygame.QUIT:
                    sys.exit()
        

            pygame.display.update()
if __name__ == "__main__":
    main = Main()
    main.mainloop()