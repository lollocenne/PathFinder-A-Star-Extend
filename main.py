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

buttons[2].active = True

aStar: Astar = Astar()

def addStartNode(x, y) -> None:
    aStar.startNode["x"] = x
    aStar.startNode["y"] = y

def addEndNode(x, y) -> None:
    aStar.endNode["x"] = x
    aStar.endNode["y"] = y

def addNode(x, y) -> None:
    aStar.nodes.append({"x": x, "y": y, "state": None, "neighbors": [], "path": None})

def addNodes(x, y) -> None:
    for button in buttons:
        if button.active == True:
            if button.txt == "Start Node":
                addStartNode(x, y)
            elif button.txt == "End Node":
                addEndNode(x, y)
            elif button.txt == "Node":
                addNode(x, y)

def update():
    pass

def draw():
    WINDOW.fill((200, 200, 200))
    
    for b in buttons:
        b.draw()
    
    for node in aStar.nodes:
        if node["state"] == None:
            pygame.draw.circle(WINDOW, (0, 0, 0), (node["x"], node["y"]), 10)
        elif node["state"] == "active":
            pygame.draw.circle(WINDOW, (255, 255, 0), (node["x"], node["y"]), 10)
        elif node["state"] == "used":
            pygame.draw.circle(WINDOW, (255, 0, 255), (node["x"], node["y"]), 10)
        elif node["state"] == "path":
            pygame.draw.circle(WINDOW, (0, 100, 0), (node["x"], node["y"]), 10)
        elif node["state"] == "start":
            if node["x"] != None and node["y"] != None:
                pygame.draw.circle(WINDOW, (0, 0, 255), (node["x"], node["y"]), 10)
        elif node["state"] == "target":
            if node["x"] != None and node["y"] != None:
                pygame.draw.circle(WINDOW, (255, 0, 0), (node["x"], node["y"]), 10)
    
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] > buttons[0].y + buttons[0].height + 10:
                    addNodes(event.pos[0], event.pos[1])
                else:
                    pass
        
        update()
        draw()
    
    pygame.quit()

if __name__ == "__main__":
    main()
