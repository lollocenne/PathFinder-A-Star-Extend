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

buttons[2].active = True

aStar: Astar = Astar()

start = False

def selectButton(x, y) -> None:
    for button in buttons:
        if button.active == True:
            button.active = False
        
        button.active = button.press()

def addStartNode(x, y) -> None:
    aStar.startNode = {"x": x, "y": y, "state": "start", "neighbors": [], "path": []}
    
    for node in aStar.nodes:
        if node["state"] != "start":
            for n in node["neighbors"]:
                if n["state"] == "start":
                    node["neighbors"].remove(n)
                    break
    
    for node in aStar.nodes:
        if node["state"] == "start":
            aStar.nodes.remove(node)
            break
            
    for node in aStar.activeNodes:
        if node["state"] == "start":
            aStar.activeNodes.remove(node)
            break
    
    aStar.nodes.append(aStar.startNode)
    aStar.activeNodes.append(aStar.startNode)

def addEndNode(x, y) -> None:
    aStar.endNode = {"x": x, "y": y, "state": "target", "neighbors": [], "path": None}
    
    for node in aStar.nodes:
        if node["state"] != "target":
            for n in node["neighbors"]:
                if n["state"] == "target":
                    node["neighbors"].remove(n)
                    break
    
    for node in aStar.nodes:
        if node["state"] == "target":
            aStar.nodes.remove(node)
            break
    
    aStar.nodes.append(aStar.endNode)

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

roadNode = []
def addRoad(x, y) -> None:
    if len(aStar.nodes) <= 1:
        return None
    
    for node in aStar.nodes:
        if sqrt(pow(node["x"] - x, 2) + pow(node["y"] - y, 2)) <= 10:
            if len(roadNode) == 0:
                roadNode.append(node)
            else:
                if roadNode[0] != node and not node in roadNode[0]["neighbors"]:
                    roadNode[0]["neighbors"].append(node)
                    node["neighbors"].append(roadNode[0])
                
                del roadNode[0]

grabbedNode = []
def grab():
    if pygame.mouse.get_pressed()[0]:
        xMouse, yMouse = pygame.mouse.get_pos()
        
        if len(grabbedNode) == 0:
            for node in aStar.nodes:
                if sqrt(pow(node["x"] - xMouse, 2) + pow(node["y"] - yMouse, 2)) <= 10:
                    grabbedNode.append(node)
        
        if len(grabbedNode) == 1:
            grabbedNode[0]["x"] = xMouse
            grabbedNode[0]["y"] = yMouse
    elif len(grabbedNode) == 1:
        del grabbedNode[0]

def delete(x, y) -> None:
    for node in aStar.nodes:
        if sqrt(pow(x - node["x"],2) + pow(y - node["y"], 2)) <= 10:
            for n in node["neighbors"]:
                n["neighbors"].remove(node)
                
            aStar.nodes.remove(node)
            return
    
    #distance point-rect: abs(a*x + b*y + c)/sqrt(pow(a, 2) + pow(b, 2))
    for node in aStar.nodes:
        for n in node["neighbors"]:
            a = (node["y"] - n["y"])/(node["x"] - n["x"])
            c = node["y"] - a * node["x"]
            
            if abs(a*x - y + c)/sqrt(pow(a, 2) + 1) <= 10:
                node["neighbors"].remove(n)
                n["neighbors"].remove(node)
                
                return

def update():
    start = buttons[0].active
    
    if start:
        aStar.searchPath()
    
    if buttons[6].active:
        grab()

def draw():
    WINDOW.fill((200, 200, 200))
    
    for b in buttons:
        b.draw()
    
    if len(roadNode) == 1:
        pygame.draw.line(WINDOW, (0, 0, 0), (roadNode[0]["x"], roadNode[0]["y"]), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), 5)
    
    for node in aStar.nodes:
        for n in node["neighbors"]:
            if node["state"] == "active":
                if n["state"] in {"start", "active", "target"}:
                    pygame.draw.line(WINDOW, (255, 255, 0), (node["x"], node["y"]), (n["x"], n["y"]), 5)
            elif node["state"] == n["state"] == "path":
                pygame.draw.line(WINDOW, (0, 100, 0), (node["x"], node["y"]), (n["x"], n["y"]), 5)
            else:
                pygame.draw.line(WINDOW, (0, 0, 0), (node["x"], node["y"]), (n["x"], n["y"]), 5)
    
    for node in aStar.nodes:
        if node["state"] == None:
            pygame.draw.circle(WINDOW, (0, 255, 255), (node["x"], node["y"]), 10)
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
                    if buttons[5].active:
                        addRoad(event.pos[0], event.pos[1])
                    elif buttons[7].active:
                        delete(event.pos[0], event.pos[1])
                    else:
                        addNodes(event.pos[0], event.pos[1])
                else:
                    selectButton(event.pos[0], event.pos[1])
        
        update()
        draw()
    
    pygame.quit()

if __name__ == "__main__":
    main()
