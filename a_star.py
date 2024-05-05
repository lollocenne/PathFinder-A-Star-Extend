from math import *

class Node:
    def __init__(self, x, y, state, neighbors, path):
        self.x: int = x
        self.y: int = y
        
        self.state: str = state
        
        self.neighbors: list = neighbors
        
        self.path: list = path

class Astar:
    def __init__(self):
        self.startNode: Node = None
        self.endNode: Node = None
        
        self.nodes: list[Node] = []
        self.activeNodes: list[Node] = []
    
    def addStartNode(self, x, y) -> None:
        self.startNode = Node(x, y, "start", [], [])
        
        for node in self.nodes:
            if node.state == "start":
                self.nodes.remove(node)
                break
        
        for node in self.nodes:
            if node.state != "start":
                for n in node.neighbors:
                    if n.state == "start":
                        node.neighbors.remove(n)
                        break
        
        for node in self.activeNodes:
            if node.state == "start":
                self.activeNodes.remove(node)
                break
        
        self.nodes.append(self.startNode)
        self.activeNodes.append(self.startNode)
    
    def addEndNode(self, x, y) -> None:
        self.endNode = Node(x, y, "target", [], None)
        
        for node in self.nodes:
            if node.state == "target":
                self.nodes.remove(node)
                break
        
        for node in self.nodes:
            if node.state != "target":
                for n in node.neighbors:
                    if n.state == "target":
                        node.neighbors.remove(n)
                        break
        
        self.nodes.append(self.endNode)
    
    def addNode(self, x, y) -> None:
        self.nodes.append(Node(x, y, None, [], None))
    
    @staticmethod
    def createConnection(node1: Node, node2: Node) -> None:
        if node1 in node2.neighbors:
            return
        
        node1.neighbors.append(node2)
        node2.neighbors.append(node1)
    
    def removeNode(self, node: Node) -> None:
        for n in node.neighbors:
                n.neighbors.remove(node)
        
        self.nodes.remove(node)
        
        if node in self.activeNodes:
            self.activeNodes.remove(node)
        
        if node.state == "start":
            self.startNode = None
            
        if node.state == "target":
            self.endNode = None
    
    @staticmethod
    def removeConnection(node1: Node, node2: Node) -> None:
        if not (node1 in node2.neighbors and node2 in node1.neighbors):
            return
        
        node1.neighbors.remove(node2)
        node2.neighbors.remove(node1)
    
    @staticmethod
    def g(node1: Node, node2: Node) -> float:
        return sqrt(pow(node1.x - node2.x, 2) + pow(node1.y - node2.y, 2))
    
    def h(self, node: Node) -> float:
        return sqrt(pow(node.x - self.endNode.x, 2) + pow(node.y - self.endNode.y, 2))
    
    def f(self, node1: Node, node2: Node) -> float:
        return self.g(node1, node2) + self.h(node2)
    
    @staticmethod
    def isUsed(node: Node) -> bool:
        for n in node.neighbors:
            if not n.state in ("used", "active", "start"):
                return False
        
        return True
    
    def updateActiveNodes(self) -> None:
        for node in self.activeNodes:
            if self.isUsed(node):
                node.state = "used"
                self.activeNodes.remove(node)
        
        for node in self.activeNodes:
            if not node.state in ("active", "start"):
                self.activeNodes.remove(node)
    
    def searchPath(self) -> None:
        if not self.complete():            
            possibleNode: Node = None
            possibleFValue: int = None
            Node1: Node = None
            
            for node in self.activeNodes:
                if len(node.neighbors) == 0:
                    continue
                
                for neighbor in node.neighbors:
                    if not neighbor.state in ("used", "active", "start", "target"):
                        if possibleNode == None:
                            possibleNode = neighbor
                            possibleFValue = self.f(node, neighbor)
                            Node1 = node
                        else:
                            if self.f(node, neighbor) < possibleFValue:
                                possibleNode = neighbor
                                possibleFValue = self.f(node, neighbor)
                                Node1 = node
            
            if possibleNode == None or possibleFValue == None or Node1 == None:
                return
            
            possibleNode.state = "active"
            possibleNode.path = Node1.path.copy()
            possibleNode.path.append(Node1)
            
            self.activeNodes.append(possibleNode)
            
            self.updateActiveNodes()
    
    def complete(self) -> bool:
        for neighbor in self.endNode.neighbors:
            if neighbor.state in ("active", "start", "path"):
                self.endNode.path = neighbor.path.copy()
                self.endNode.path.append(neighbor)
                self.endNode.state = "path"
                
                for node in self.endNode.path:
                    node.state = "path"
                
                self.updateActiveNodes()
                return True
        
        self.updateActiveNodes()
        return False
