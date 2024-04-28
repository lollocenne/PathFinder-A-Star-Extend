import pygame
from button import Button
from a_star import Astar

pygame.font.init()

WIDTH, HEIGHT = 820, 570

WINDOW: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PathFinder A*")

buttonsText = ("Start", "End", "Start Node", "End Node", "Node", "Road", "Grab", "Delete")
buttons: list[Button] = []

for i in range(len(buttonsText)):
    buttons.append(Button(WINDOW, i*WIDTH/8 + i, buttonsText[i]))

buttons[0].active = True

aStar: Astar = Astar()

def update():
    pass

def draw():
    WINDOW.fill((200, 200, 200))
    
    for b in buttons:
        b.draw()
    
    for node in aStar.nodes:
        if node["state"] == None:
            pygame.draw.circle(WINDOW, (0, 0, 0), (node["x"], node["y"]), 10)
    
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
