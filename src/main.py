import pygame
import sys
from const import *

class Main:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption("Chess50")
    
    def mainloop(slef):
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
        

            pygame.display.update()

main = Main()
main.mainloop()