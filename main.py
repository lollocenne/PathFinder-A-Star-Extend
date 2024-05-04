import pygame
from button import Button
from a_star import Astar
from math import *

pygame.font.init()

WIDTH, HEIGHT = 820, 570

WINDOW: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PathFinder A*")

buttonsText = ("Start", "End", "Start Node", "End Node", "Node", "Road", "Grab", "Delete")
buttons: list[Button] = []

for i in range(len(buttonsText)):
    buttons.append(Button(WINDOW, i*WIDTH/8 + i, buttonsText[i]))

buttons: tuple[Button] = tuple(buttons)

buttons[2].active = True

NODE_SIZE: int = 10
LINE_SIZE: int = 5

aStar: Astar = Astar()

def selectButton() -> None:
    for button in buttons:
        if button.active:
            button.active = False
        
        button.active = button.press()

def addNodes(x, y) -> None:
    for button in buttons:
        if button.active:
            if button.txt == "Start Node":
                aStar.addStartNode(x, y)
            elif button.txt == "End Node":
                aStar.addEndNode(x, y)
            elif button.txt == "Node":
                aStar.addNode(x, y)

roadNode = []
def addRoad(x, y) -> None:
    if len(aStar.nodes) <= 1:
        return None
    
    for node in aStar.nodes:
        if sqrt(pow(node["x"] - x, 2) + pow(node["y"] - y, 2)) <= 10:
            if len(roadNode) == 0:
                roadNode.append(node)
            else:
                if roadNode[0] != node:
                    aStar.createConnection(node, roadNode[0])
                
                del roadNode[0]

grabbedNode = []
def grab():
    if pygame.mouse.get_pressed()[0]:
        xMouse, yMouse = pygame.mouse.get_pos()
        
        if len(grabbedNode) == 0:
            for node in aStar.nodes:
                if sqrt(pow(node["x"] - xMouse, 2) + pow(node["y"] - yMouse, 2)) <= NODE_SIZE:
                    grabbedNode.append(node)
        
        if len(grabbedNode) == 1:
            grabbedNode[0]["x"] = xMouse
            grabbedNode[0]["y"] = yMouse
    elif len(grabbedNode) == 1:
        del grabbedNode[0]

def delete(x, y) -> None:
    for node in aStar.nodes:
        if sqrt(pow(x - node["x"],2) + pow(y - node["y"], 2)) <= NODE_SIZE:
            aStar.removeNode(node)
            return
    
    #distance point-line: abs(a*x + b*y + c)/sqrt(pow(a, 2) + pow(b, 2))
    for node in aStar.nodes:
        for n in node["neighbors"]:
            if (node["x"] - n["x"]) != 0:
                a = (node["y"] - n["y"])/(node["x"] - n["x"])
            else:
                a = (node["y"] - n["y"])/((node["x"] + 0.0001) - n["x"]) #approssimate the line to a vertical line
            
            c = node["y"] - a * node["x"]
            
            if (n["x"] <= x and node["x"] >= x) or (node["x"] <= x and n["x"] >= x):
                if (n["y"] <= y and node["y"] >= y) or (node["y"] <= y and n["y"] >= y):
                    if abs(a*x - y + c)/sqrt(pow(a, 2) + 1) <= LINE_SIZE + 5:
                        aStar.removeConnection(node, n)
                        return

def endSearch() -> None:
    for node in aStar.nodes:
        node["state"] = None
        node["path"] = None
    
    aStar.activeNodes = []
    
    if aStar.startNode != None:
        aStar.startNode["state"] = "start"
        aStar.startNode["path"] = []
        
        aStar.activeNodes.append(aStar.startNode)
    
    if aStar.endNode != None:
        aStar.endNode["state"] = "target"

def update():    
    if aStar.startNode != None and aStar.endNode != None:
        start = buttons[0].active
    else:
        start = False
    
    if start:
        aStar.searchPath()
    
    if buttons[6].active:
        grab()
    
    if buttons[1].active:
        endSearch()
        buttons[1].active = False

def draw():
    WINDOW.fill((200, 200, 200))
    
    for b in buttons:
        b.draw()
    
    if len(roadNode) == 1:
        pygame.draw.line(WINDOW, (0, 0, 0), (roadNode[0]["x"], roadNode[0]["y"]), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), LINE_SIZE)
    for node in aStar.nodes:
        for n in node["neighbors"]:
            if node["state"] == "active":
                if n["state"] in ("start", "active", "target"):
                    pygame.draw.line(WINDOW, (255, 255, 0), (node["x"], node["y"]), (n["x"], n["y"]), LINE_SIZE)
            elif node["state"] == n["state"] == "path":
                pygame.draw.line(WINDOW, (0, 100, 0), (node["x"], node["y"]), (n["x"], n["y"]), LINE_SIZE)
            else:
                pygame.draw.line(WINDOW, (0, 0, 0), (node["x"], node["y"]), (n["x"], n["y"]), LINE_SIZE)
    
    if aStar.startNode != None:
        pygame.draw.circle(WINDOW, (0, 0, 255), (aStar.startNode["x"], aStar.startNode["y"]), NODE_SIZE + 3)
    
    if aStar.endNode != None:
        pygame.draw.circle(WINDOW, (255, 0, 0), (aStar.endNode["x"], aStar.endNode["y"]), NODE_SIZE + 3)
    
    for node in aStar.nodes:
        if node["state"] == None:
            pygame.draw.circle(WINDOW, (0, 255, 255), (node["x"], node["y"]), NODE_SIZE)
        elif node["state"] == "active":
            pygame.draw.circle(WINDOW, (255, 255, 0), (node["x"], node["y"]), NODE_SIZE)
        elif node["state"] == "used":
            pygame.draw.circle(WINDOW, (255, 0, 255), (node["x"], node["y"]), NODE_SIZE)
        elif node["state"] == "path":
            pygame.draw.circle(WINDOW, (0, 100, 0), (node["x"], node["y"]), NODE_SIZE)
    
    pygame.display.update()

def main():
    run = True
    
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(10)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] > buttons[0].y + buttons[0].height + 10:
                    if buttons[5].active:
                        addRoad(event.pos[0], event.pos[1])
                    elif buttons[7].active:
                        delete(event.pos[0], event.pos[1])
                    else:
                        addNodes(event.pos[0], event.pos[1])
                else:
                    selectButton()
        
        update()
        draw()
    
    pygame.quit()

if __name__ == "__main__":
    main()