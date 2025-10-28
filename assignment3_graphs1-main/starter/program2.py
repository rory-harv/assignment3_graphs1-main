

import math
from queue import PriorityQueue
from typing import List, Optional
from graph_interfaces import IGraph, IVertex, IEdge
from graph_impl import Graph, Vertex, Edge
from math import atan2, cos, sin
from program import read_graph
import time

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

    edges = vertex_to.get_edges()

    for edge in edges:
        if edge.get_destination().get_name() == vertex_from.get_name():
            weight = edge.get_weight()
            break
    
    return weight


def reconstruct_path(parent: dict[IVertex], start: IVertex, goal: IVertex, vertices_explored: int, edges_explored: int, elapsed: float) -> None:
    '''Finds overall path from start to goal depending on graph traversal and end goal vertex.'''
    path: List[IVertex] = []
    total_dist: float = 0

    current = goal
    while current is not None:  # while there are vertices left to travel to
        if current == start:
            path.append(current)
            break
        path.append(current)
        current = parent[current]

    path = path[::-1]   # reverses path since the vertices are appended from last to first

    for i in range(len(path)-1):
        edges = path[i].get_edges()
        for edge in edges:
            if edge.get_destination().get_name() == path[i+1].get_name():
                total_dist += edge.get_weight()



    print(f'Path from {start.get_name()} to {goal.get_name()}: ')   # finalized print out
    for v in path:
        print(f'-> {v.get_name()}')
    print()
    print(f"Total Distance Travelled: {total_dist} miles")
    print(f'Total Vertices Explored: {vertices_explored}')
    print(f"Total Edges Explored: {edges_explored}")
    print(f'Execution Time: {elapsed} seconds')
    print()
    

# dijkstra's algorithm

def dijkstra(graph: IGraph, start: IVertex, goal: IVertex) -> None:
    '''Dijkstra's Algorithm using g(n) values to search graph.'''
    frontier = PriorityQueue()
    frontier.put((0, start))  # adds start vertex to the frontier
    explored: List[IVertex] = []
    parent: dict[IVertex] = {}
    cost_so_far: dict[IVertex, float] = {}
    vertices_explored: int = 0
    edges_explored: int = 0
    
    start_time = time.perf_counter()

    parent[start] = None
    cost_so_far[start] = 0

    while not frontier.empty(): # loops while frontier not empty
        first = frontier.get()
        current = first[1]    # pops vertex with lowest g(n)
        vertices_explored += 1
        if current == goal:
            end_time = time.perf_counter()
            elapsed = end_time - start_time
            reconstruct_path(parent, start, goal, vertices_explored, edges_explored, elapsed)   # return final path
            restart()   # initiates restart
            return ""   # ends while loop
        explored.append(current)
        edges = current.get_edges() # gets all neighbors of current
        neighbors = []
        for edge in edges:
            if edge.get_destination() not in neighbors:   # checks if already visited
                neighbors.append(edge.get_destination())
                edges_explored += 1
                cost_so_far[edge.get_destination()] = get_cost(graph, current, edge.get_destination())
        for neighbor in neighbors:
            tentative_g = cost_so_far[current] + get_cost(graph, current, neighbor) # updates g(n) for neighbor
            if neighbor not in explored:
                if neighbor not in frontier.queue or tentative_g < cost_so_far[neighbor]:  # checks whether to add to frontier
                    cost_so_far[neighbor] = tentative_g
                    parent[neighbor] = current  # sets parent
                    frontier.put((tentative_g, neighbor))   # adds neighbor to frontier
    
    print(f'Path from {start.get_name()} to {goal.get_name()} not found. ') # returns failure if no path found


# greedy best first search algorithm

def greedy_bfs(graph: IGraph, start: IVertex, goal: IVertex) -> None:
    '''Performs Greedy Best-First search for an inputted graph based on it's vertices coordinate graph.'''
    frontier = PriorityQueue()
    file_path = "starter\\vertices_v1.txt"  # file path containing data for coordinates
    h_val = get_heuristic(file_path, start, None)
    frontier.put((h_val, start))  # adds start vertex to the frontier
    explored: List[IVertex] = []
    parent: dict[IVertex] = {}
    vertices_explored: int = 0
    edges_explored: int = 0

    start_time = time.perf_counter()

    while not frontier.empty(): # loops while something in frontier
        first = frontier.get()
        current = first[1]    # pops vertex in frontier with the lowest h(n)
        vertices_explored += 1
        if current == goal:
            end_time = time.perf_counter()
            elapsed = end_time - start_time
            reconstruct_path(parent, start, goal, vertices_explored, edges_explored, elapsed) # return reconstructed path
            restart()   # initiates restart
            return ""
        explored.append(current)
        edges = current.get_edges() # evaluates neighbors for the vertex
        neighbors = []
        for edge in edges:
            if edge not in neighbors:   # checks if already visited
                neighbors.append(edge.get_destination())
                edges_explored += 1
        for neighbor in neighbors:
            if neighbor not in explored and neighbor not in frontier.queue: # not explored/evaluated yet
                parent[neighbor] = current
                h_val = get_heuristic(file_path, current, neighbor) # updates h(n)
                frontier.put((h_val, neighbor))
    
    print(f'Path from {start.get_name()} to {goal.get_name()} not found. ') # returns failure if no path found



# a* algorithm

def a_star(graph: IGraph, start: IVertex, goal: IVertex):
    '''A* Pathfinding Algorithm that searches using f(n) values.'''
    frontier = PriorityQueue()
    file_path = "starter\\vertices_v1.txt"  # file path containing data for coordinates
    h_val = get_heuristic(file_path, start, None)
    frontier.put((h_val, start))  # adds start vertex to the frontier
    explored: List[IVertex] = []
    cost_so_far: dict[IVertex, float] = {}
    f_scores: dict[IVertex, float] = {}
    parent: dict[IVertex] = {}
    vertices_explored: int = 0
    edges_explored: int = 0

    parent[start] = None
    cost_so_far[start] = 0

    start_time = time.perf_counter()

    while frontier:
        first = frontier.get()  # pops lowest f(n)
        current = first[1]
        vertices_explored += 1
        if current == goal:
            end_time = time.perf_counter()
            elapsed = end_time - start_time # marks overall execution time
            reconstruct_path(parent, start, goal, vertices_explored, edges_explored, elapsed)   # reconstructs final path
            restart()   # initiates restart
            return ""
        explored.append(current)
        edges = current.get_edges() # evaluates neighbors for the vertex
        neighbors = []
        for edge in edges:
            if edge not in neighbors:   # checks if already visited
                neighbors.append(edge.get_destination())
                edges_explored += 1
        for neighbor in neighbors:
            tentative_g = cost_so_far[current] + get_cost(graph, current, neighbor)    # calculates new g(n)
            if neighbor not in explored:    # checks if neighbor already evaluated
                if neighbor not in frontier.queue or tentative_g < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = tentative_g
                    h_val = get_heuristic(file_path, current, neighbor)
                    f_scores[neighbor] = cost_so_far[neighbor] + h_val  # updates f(n)
                    parent[neighbor] = current
                    frontier.put((f_scores[neighbor], neighbor))
    print(f'Path from {start.get_name()} to {goal.get_name()} not found. ') # returns failure if no path found


def restart():
    '''Initiates user response for retarting/ending the program.'''
    answer: str = input("Would you like to use Oregon Pathfinder again (y/n)?: ")
    if answer.lower() == "n":
        print("Thank you for using Oregon Pathfinder!")
    elif answer.lower() == "y":
        main()
    else:
        answer: str = input("Please reply with 'y' (Yes) or 'n' (No): ")


def main() -> None:
    graph: IGraph = read_graph("starter\\graph_v2.txt")

    print("Welcome to Oregon Pathfinder!")
    print()
    print("Select Pathfinding Algorithm:")
    print("1. Dijkstra's Algorithm")
    print("2. Greedy Best-First Search")
    print("3. A* Algorithm")
    choice: int = int(input("Enter Choice (1-3): "))

    if choice != 1 and choice !=2 and choice != 3:
        choice: int = int(input("Please Enter Valid Choice (1-3): "))


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
    
    if choice == 1:
        print(dijkstra(graph, start_vertex, goal_vertex))
    elif choice == 2:
        print(greedy_bfs(graph, start_vertex, goal_vertex))
    elif choice == 3:
        print(a_star(graph, start_vertex, goal_vertex))
    

if __name__ == '__main__':
    main()