from typing import List
from graph_interfaces import IEdge, IGraph, IVertex
from __future__ import annotations

# Implementation definitions
# You should implement the bodies of the methods required by the interface protocols.

class Graph(IGraph):
    def __init__(self) -> None:
        self._vertices: List[Vertex] = []
        self._edges: List[Edge] = [] 

    def get_vertices(self) -> List[IVertex]:
        return self._vertices
    
    def get_edges(self) -> List[IEdge]: 
        return self._edges

    def add_vertex(self, vertex: IVertex) -> None: 
        self._vertices.append(vertex)

    def remove_vertex(self, vertex_name: str) -> None: 
        for vertex in self._vertices:
              if vertex.get_name() == vertex_name:
                  self._vertices.remove(vertex)
                  return

    def add_edge(self, edge: IEdge) -> None:
        self._edges.append(edge)

    def remove_edge(self, edge_name: str) -> None:
        for edge in self._edges:
              if edge.get_name() == edge_name:
                  self._edges.remove(edge)
                  return

class Vertex(IVertex):
    def __init__(self, name: str):
        self._name: str = name
        self._edges: List[Edge] = []
        self._visited: bool = False

    def get_name(self) -> str: 
        return self._name
    
    def set_name(self, name: str) -> None: 
        self._name = name

    def add_edge(self, edge: IEdge) -> None:
        self._edges.append(edge)

    def remove_edge(self, edge_name: str) -> None:
        for edge in self._edges:
              if edge.get_name() == edge_name:
                  self._edges.remove(edge)
                  return

    def get_edges(self) -> List[IEdge]:
        return self._edges

    def set_visited(self, visited: bool) -> None:
        self._visited = True

    def is_visited(self) -> bool:
        return self._visited

class Edge(IEdge):
    def __init__(self, name: str):
        self._name: str = name
        self._vertices: List[Vertex] = []
        self._weight: float = 0

    def get_name(self) -> str: 
        return self._name
    
    def set_name(self, name: str) -> None: 
        self._name = name

    def get_destination(self) -> IVertex: ...

    def get_weight(self) -> float: ...
    
    def set_weight(self, weight: float) -> None: ...
