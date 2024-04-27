import pygame
from button import Button


WIDTH, HEIGHT = 820, 570

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PathFinder A*")


def update():
    pass

def draw():
    pass
    
    pygame.display.update()

def main():
    run = True
    
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
        update()
        draw()
    
    pygame.quit()

if __name__ == "__main__":
    main()
