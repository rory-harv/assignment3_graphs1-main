
from __future__ import annotations

from typing import Any, Dict, List, Optional
from graph_interfaces import IEdge, IGraph, IVertex


# Implementation definitions
# You should implement the bodies of the methods required by the interface protocols.

class Graph(IGraph):

    def __init__(self) -> None:
        self._adj_list: dict[Vertex] = {}
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

    def add_edge(self, edge: IEdge, vertex_from_name: str, vertex_to_name: str, weight: float) -> None:
        vertex_from: Optional[Vertex] = None
        vertex_to: Optional[Vertex] = None
        weight: Optional[float] = weight

        if vertex_from not in self._vertices:
            self.add_vertex(vertex_from)
        if vertex_to not in self._vertices:
            self.add_vertex(vertex_to)
        
        for vertex in self._vertices:
            vertex = Vertex(vertex)
            if vertex.get_name() == vertex_from_name:
                vertex_from = vertex

            if vertex.get_name() == vertex_to_name:
                vertex_to = vertex

        if vertex_from is None or vertex_to is None:
            raise Exception("One or more of the vertices do not exist.")
        
        the_edge = Edge(edge, weight, vertex_to)
        vertex_from.add_edge(the_edge)

        second_edge = Edge(edge, weight, vertex_from)
        vertex_to.add_edge(second_edge)

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
        self._visited = visited

    def is_visited(self) -> bool:
        return self._visited
    
    def __str__(self) -> str:
        return self._name

class Edge(IEdge):

    def __init__(self, name: str, weight: float, destination: IVertex):
        self._name: str = name
        self._vertices: List[Vertex] = []
        self._weight: float = 0
        self._destination: IVertex = destination

    def get_name(self) -> str: 
        return self._name
    
    def set_name(self, name: str) -> None: 
        self._name = name

    def get_destination(self) -> IVertex: 
        return self._destination 

    def get_weight(self) -> float: 
        return self._weight
    
    def set_weight(self, weight: float) -> None: 
        self._weight = weight
