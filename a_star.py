from math import *


#node = {"x": x, "y": y, "state": None, "neighbors": list[node], "path": list[node]}
class Astar:
    def __init__(self):
        self.startNode: dict = None
        self.endNode: dict = None
        
        self.nodes: list[dict] = []
        self.activeNodes: list[dict] = []
    
    @staticmethod
    def g(node1: list[dict], node2: list[dict]) -> float:
        return sqrt(pow(node1["x"] - node2["x"], 2) + pow(node1["y"] - node2["y"], 2))
    
    def h(self, node) -> float:
        return sqrt(pow(node["x"] - self.endNode["x"], 2) + pow(node["y"] - self.endNode["y"], 2))
    
    def f(self, node1, node2) -> float:
        return self.g(node1, node2) + self.h(node2)
    
    def updateActiveNodes(self) -> None:
        for node in self.activeNodes:
            numActiveNode = 0
            for n in node["neighbors"]:
                if n["state"] in {"active", "start"}:
                    numActiveNode += 1
            
            if numActiveNode == len(node["neighbors"]):
                node["state"] == "used"
                self.activeNodes.remove(node)
            
            if not node["state"] in {"active", "start"}:
                self.activeNodes.remove(node)
    
    def searchPath(self) -> None:
        if not self.complete():
            self.updateActiveNodes()
            
            possibleNode: dict = None
            possibleFValue: int = None
            Node1: dict = None
            
            for node in self.activeNodes:
                if len(node["neighbors"]) == 0:
                    continue
                
                for neighbor in node["neighbors"]:
                    if not neighbor["state"] in {"active", "start", "target"}:
                        if possibleNode == None:
                            possibleNode = neighbor
                            possibleFValue = self.f(node, neighbor)
                            Node1 = node
                        else:
                            if self.f(node, neighbor) < possibleFValue:
                                possibleNode = neighbor
                                possibleFValue = self.f(node, neighbor)
                                Node1 = node
            
            if possibleNode == None or possibleFValue == None or Node1 == Node1:
                return
            
            possibleNode["state"] = "active"
            possibleNode["path"] = Node1["path"].copy()
            possibleNode["path"].append(Node1)
            
            self.activeNodes.append(possibleNode)
    
    def complete(self) -> bool:
        for neighbor in self.endNode["neighbors"]:
            if neighbor["state"] in {"active", "start", "path"}:
                self.endNode["path"] = neighbor["path"].copy()
                self.endNode["path"].append(neighbor)
                self.endNode["state"] = "path"
                
                for node in self.endNode["path"]:
                    node["state"] = "path"
                
                return True
        
        return False
