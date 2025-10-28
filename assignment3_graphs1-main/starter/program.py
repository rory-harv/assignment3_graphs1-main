from typing import List, Optional
from graph_interfaces import IGraph, IVertex, IEdge
from graph_impl import Graph, Vertex, Edge

def read_graph(file_path: str) -> IGraph:  
    """Read the graph from the file and return the graph object"""

    try: 
        with open(file_path, 'r') as f:
            next(f)
            new_path = Graph()  # creates new graph instance
            for line in f:
                source, destination, highway, distance = line.strip().split(',')    # gets info for new vertices/edges
                source = Vertex(source) # turns string to vertex type
                destination = Vertex(destination)

                in_list: bool = False   # base variable to determine if vertex already exists
                for vertex in new_path.get_vertices():
                    if vertex.get_name() == source.get_name():
                        in_list = True
                        source = vertex
                        break
                if in_list == False:
                    new_path.add_vertex(source) # adds vertex to all graph vertices

                in_list: bool = False
                for vertex in new_path.get_vertices():
                    if vertex.get_name() == destination.get_name():
                        in_list = True
                        destination = vertex
                        break
                if in_list == False:
                    new_path.add_vertex(destination)    # adds vertex to all graph vertices

                highway = Edge(highway, float(distance), destination)  # creates new edge
                source.add_edge(highway)    # connects new vertices w/ new edge
    
            return new_path
    except Exception as m:
        raise FileNotFoundError(f'{file_path} not found in directory. {str(m)}')


def print_dfs(graph: IGraph, start_vertex: IVertex) -> None: 
    """Print the DFS traversal of the graph starting from the start vertex"""
    stack: List[IVertex] = []
    end_result: List[IVertex] = []
    visited: bool = False

    all_vertices = graph.get_vertices() # gets all vertices for graph

    for vertex in all_vertices: # defaults all vertices to be not visited
        vertex.set_visited(visited)

    visited: bool = True
    start_vertex.set_visited(visited)   # sets starter vertex as visited

    stack.append(start_vertex)
    visited: bool = False

    adj_list: dict[IVertex, List[IVertex]] = {}

    def helper(vertex: IVertex) -> None:
        '''Accepts a vertex, marks it as visited and appends to end result array.'''
        visited: bool = True
        vertex.set_visited(visited)
        if vertex not in end_result:    # adds to end result if not visited yet
            end_result.append(vertex)

    while stack:
        start: IVertex = stack.pop()    # takes last element
        if start not in end_result:
            end_result.append(start)  # appends to final results
        adj_list[start] = []

        for edge in start.get_edges():  # create adj list for focused vertex
            destination = edge.get_destination()
            adj_list[start].append(destination)

        for vertex in adj_list[start]:  # loops through adj list for focused vertex
            if vertex.is_visited() == False:
                helper(vertex)  # invokes helper function
                stack.append(vertex)
    
    print(('-'*10) + 'Depth First Search' + ('-'*10))
    for result in end_result:   # returns end result
        print(result.get_name())
    print()



def print_bfs(graph: IGraph, start_vertex: IVertex) -> None: 
    """Print the BFS traversal of the graph starting from the start vertex"""
    queue: List[IVertex] = []
    nodes_visited: List[IVertex] = []
    visited: bool = False

    all_vertices = graph.get_vertices() # gets all graph vertices

    for vertex in all_vertices: # sets all vertices to not visited
        vertex.set_visited(visited)

    visited: bool = True
    start_vertex.set_visited(visited)   # sets starter vertex as visited

    queue.append(start_vertex)
    visited: bool = False

    adj_list: dict[IVertex, List[IVertex]] = {}

    while queue:    # loops while queue exists
        start: IVertex = queue.pop(0)    # takes first element
        if start not in nodes_visited:
            nodes_visited.append(start)  # appends to final results
        adj_list[start] = []

        for edge in start.get_edges():  # create adj list for focused vertex
            destination = edge.get_destination()
            adj_list[start].append(destination)
        
        for vertex in adj_list[start]:  # loops through adjacency list for focused vertex
            if vertex.is_visited() == False:
                visited: bool = True    
                vertex.set_visited(visited) # sets vertex as visited
                queue.append(vertex)
                if vertex not in nodes_visited: # checks if vertex already visited
                    nodes_visited.append(vertex)

    print(('-'*10) + 'Breadth First Search' + ('-'*10))
    for node in nodes_visited:    # returns end result
        print(node.get_name())
    print()



def main() -> None:
    graph: IGraph = read_graph("starter\\graph.txt")
    start_vertex_name: str  = input("Enter the start vertex name: ")

    # Find the start vertex object
    start_vertex: Optional[IVertex]= next((v for v in graph.get_vertices() if v.get_name() == start_vertex_name), None)

    if start_vertex is None:
        print("Start vertex not found")
        return
    
    print_dfs(graph, start_vertex)
    print_bfs(graph, start_vertex)


if __name__ == "__main__":
    main()