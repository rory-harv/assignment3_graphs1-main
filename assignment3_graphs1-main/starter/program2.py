

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
                lat1: float = lats[index1]  # converts variables to floats
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


def get_cost(graph: IGraph, vertex_to: IVertex, vertex_from: IVertex) -> float:
    '''Gets cost between two given points.'''
    weight: float = 0
    all_vertices = graph.get_vertices()

    for vertex in all_vertices:
        if vertex.get_name() == vertex_to.get_name():
            index: int = all_vertices.index(vertex)
            break
    start_vertex = all_vertices[index]
    edges = start_vertex.get_edges()

    for edge in edges:
        if edge.get_destination() == vertex_from.get_name():
            weight = edge.get_weight()
            break
    
    return weight


def reconstruct_path(parent: dict[IVertex], start: IVertex, goal: IVertex) -> None:
    '''Finds overall path from start to goal depending on graph traversal and end goal vertex.'''
    path: List[IVertex] = []
    current = goal
    while current is not None:  # while there are vertices left to travel to 
        path.append(current)
        current = parent[current]
    path = path[::-1]   # reverses path since the vertices are appended from last to first

    print(f'Path from {start.get_name()} to {goal.get_name()}: ')
    for v in path:
        print(f'-> {v.get_name()}')
    

# dijkstra's algorithm

def dijkstra(graph: IGraph, start: IVertex, goal: IVertex) -> None:
    frontier = PriorityQueue()
    frontier.put(start, 0)  # adds start vertex to the frontier
    explored: List[IVertex] = []
    g_scores: dict[IVertex, int] = {start: 0}
    parent: dict[IVertex] = {}

    while frontier: # loops while frontier not empty
        current = frontier.get()    # pops vertex with lowest g(n)
        if current == goal:
            reconstruct_path(parent, start, goal)   # return final path
        explored.append(current)
        edges = current.get_edges() # gets all neighbors of current
        neighbors = []
        for edge in edges:
            if edge not in neighbors:   # checks if already visited
                neighbors.append(edge.get_destination())
        for neighbor in neighbors:
            index = neighbors.index(neighbor)
            tentative_g = g_scores[current] + get_cost(graph, current, neighbors[index])    # calculates new g(n)
            if neighbor not in explored:
                if neighbor not in frontier.queue or tentative_g < g_scores[neighbor]:  # checks whether to add to frontier
                    g_scores[neighbor] = tentative_g
                    parent[neighbor] = current
                    frontier.put(neighbor, tentative_g)
    print(f'Path from {start.get_name()} to {goal.get_name()} not found. ') # returns failure if no path found


# greedy best first search algorithm

def greedy_bfs(graph: IGraph, start: IVertex, goal: IVertex) -> None:
    '''Performs Greedy Best-First search for an inputted graph based on it's vertices coordinate graph.'''
    frontier = PriorityQueue()
    file_path = "starter\\vertices_v1.txt"  # file path containing data for coordinates
    h_val = get_heuristic(file_path, start, None)
    frontier.put(start, h_val)  # adds start vertex to the frontier
    explored: List[IVertex] = []
    parent: dict[IVertex] = {}

    while frontier: # loops while something in frontier
        current = frontier.get()    # pops vertex in frontier with the lowest h(n)
        if current == goal:
            reconstruct_path(parent, start, goal) # return reconstructed path
        explored.append(current)
        edges = current.get_edges() # evaluates neighbors for the vertex
        neighbors = []
        for edge in edges:
            if edge not in neighbors:   # checks if already visited
                neighbors.append(edge.get_destination())
        for neighbor in neighbors:
            if neighbor not in explored and neighbor not in frontier.queue: # not explored/evaluated yet
                parent[neighbor] = current
                h_val = get_heuristic(file_path, current, neighbor)
                frontier.put(neighbor, h_val)
    print(f'Path from {start.get_name()} to {goal.get_name()} not found. ') # returns failure if no path found



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
    
    print(dijkstra(graph, start_vertex, goal_vertex))

if __name__ == '__main__':
    main()