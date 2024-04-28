from math import *


#node = {"x": x, "y": y, "state": None, "neighbors": list[node], "path": list[node]}
class Astar:
    def __init__(self):
        self.startNode: dict = {"x": None, "y": None, "state": "start", "neighbors": None}
        self.endNode: dict = {"x": None, "y": None, "state": "target", "neighbors": None}
        
        self.nodes: list[dict] = [self.startNode, self.endNode]
        self.activeNodes: list[dict] = [self.startNode]
    
    @staticmethod
    def g(node1: list[dict], node2: list[dict]) -> float:
        return sqrt(pow(node1["x"] - node2["x"], 2) + pow(node1["y"] - node2["y"], 2))
    
    def h(self, node) -> float:
        return sqrt(pow(node["x"] - self.endNode["x"], 2) + pow(node["y"] - self.endNode["y"], 2))
    
    def f(self, node1, node2) -> float:
        return self.g(node1, node2) + self.h(node2)
    
    def searchPath() -> None:
        pass
