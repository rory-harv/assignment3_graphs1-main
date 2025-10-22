

import math
from queue import PriorityQueue
from typing import List, Optional
from graph_interfaces import IGraph, IVertex, IEdge
from graph_impl import Graph, Vertex, Edge
from math import atan2, cos, sin
from program import read_graph

def get_heuristic(file_path: str, vertex_to: IVertex, vertex_from: IVertex) -> float:
    '''Computes heuristic value b/w two given points on a graph.'''
    RAD_EARTH = 3963   # radius of earth (in miles)
    try: 
        with open(file_path, 'r') as f: # reads vertices file
            next(f) # skips intro line
            vertices: List[IVertex] = []
            lats: List[float] = []
            longs: List[float] = []
            heuristic: float = 0

            for line in f:
                vertex, lat, long = line.strip().split(',') # assigns variable names to data
                vertex = Vertex(vertex) # type casts variables from str to actual
                lat = float(lat)
                long = float(long)
                vertices.append(vertex)
                lats.append(lat)
                longs.append(long)

            v1_present: bool = False
            v2_present: bool = False
            
            if vertex_to != None and vertex_from != None:
                for vertex in vertices: # searches for index of instance of vertex_to
                    if vertex_to.get_name() == vertex.get_name():
                        index1 = vertices.index(vertex)
                        v1_present = True
                        break
                for vertex in vertices: # searches for index of instance of vertex_from
                    if vertex_from.get_name() == vertex.get_name():
                        index2 = vertices.index(vertex)
                        v2_present = True
                        break
            

            if v1_present == True and v2_present == True:   # checks if both vertices exist
                lat1: float = lats[index1]
                lat2: float = lats[index2]
                long1: float = longs[index1]
                long2: float = longs[index2]

                lat1_rad = lat1 * float(math.pi) / 180  # converts lat and long to radians
                lat2_rad = lat2 * float(math.pi) / 180
                long1_rad = long1 * float(math.pi) / 180
                long2_rad = long2 * float(math.pi) / 180

                diff_lat = lat2_rad - lat1_rad  # calculates distance b/w lat and long
                diff_long = long2_rad - long1_rad

                a = sin(diff_lat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(diff_long / 2)**2
                central_angle = 2 * atan2(math.sqrt(a), math.sqrt(1-a))
                heuristic = RAD_EARTH * central_angle   # calculates distance (miles) b/w two given vertices

        return heuristic    # returns heuristic 

    except: 
        raise FileNotFoundError(f'{file_path} not found in directory.')
    

# dijkstra's algorithm

def dijkstra():
    pass


# greedy best first search algorithm

def greedy_bfs(graph: IGraph, start: IVertex, goal: IVertex):
    frontier = PriorityQueue()
    file_path = "starter\\vertices_v1.txt"  # file path containing data for coordinates
    h_val = get_heuristic(file_path, start, None)
    frontier.put(start, h_val)
    explored: List[IVertex] = []
    parent: dict[IVertex] = {}

    while frontier:
        current = frontier.get()
        if current == goal:
            return # return path
        explored.append(current)
        edges = current.get_edges()
        neighbors = []
        for edge in edges:
            if edge not in neighbors:
                neighbors.append(edge.get_destination())
        for neighbor in neighbors:
            if neighbor not in explored and neighbor not in frontier.queue:
                parent[neighbor] = current
                h_val = get_heuristic(file_path, current, neighbor)
                frontier.put(neighbor, h_val)
    




# a* algorithm

def a_star():
    pass


def main() -> None:
    graph: IGraph = read_graph("starter\\graph_v2.txt")
    start_vertex_name: str  = input("Enter the start vertex name: ")
    goal_vertex_name: str = input("Enter the goal vertex name: ")

    # Find the start vertex object
    start_vertex: Optional[IVertex]= next((v for v in graph.get_vertices() if v.get_name() == start_vertex_name), None)

    # Find the start vertex object
    goal_vertex: Optional[IVertex]= next((v for v in graph.get_vertices() if v.get_name() == goal_vertex_name), None)

    if start_vertex is None:
        print("Start vertex not found")
        return
    
    if goal_vertex is None:
        print("Goal vertex not found")
        return
    
    print(greedy_bfs(graph, start_vertex, goal_vertex))

if __name__ == '__main__':
    main()