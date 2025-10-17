from typing import List, Optional
from graph_interfaces import IGraph, IVertex, IEdge
from graph_impl import Graph, Vertex, Edge

def read_graph(file_path: str) -> IGraph:  
    """Read the graph from the file and return the graph object"""

    try: 
        with open(file_path, 'r') as f:
            next(f)
            new_path = Graph()
            for line in f:
                source, destination, highway, distance = line.strip().split(',')
                source = Vertex(source)
                destination = Vertex(destination)

                in_list: bool = False
                for vertex in new_path.get_vertices():
                    if vertex.get_name() == source.get_name():
                        in_list = True
                        source = vertex
                        break
                if in_list == False:
                    new_path.add_vertex(source)

                in_list: bool = False
                for vertex in new_path.get_vertices():
                    if vertex.get_name() == destination.get_name():
                        in_list = True
                        destination = vertex
                        break
                if in_list == False:
                    new_path.add_vertex(destination)

                highway = Edge(highway, distance, destination)
                source.add_edge(highway)
    
            return new_path
    except:
        raise FileNotFoundError(f'{file_path} not found in directory.')


def print_dfs(graph: IGraph, start_vertex: IVertex) -> None: 
    """Print the DFS traversal of the graph starting from the start vertex"""
    stack: List[IVertex] = []
    end_result: List[IVertex] = []
    stack.append(start_vertex)

    def helper(vertex: IVertex) -> None:
        '''Accepts a vertex, marks it as visited and appends to end result array.'''
        visited: bool = True
        vertex.set_visited(visited)
        if vertex not in end_result:
            end_result.append(vertex)

    while stack:
        vertex: IVertex = stack.pop()
        if vertex.is_visited() == False:
            graph.add_vertex(vertex)
            visited: bool = True
            vertex.set_visited(visited)
            end_result.append(vertex)
            edges: List[IEdge] = vertex.get_edges()
            for edge in edges:
                destination: IVertex = edge.get_destination()
                if destination.is_visited() == False:
                    helper(destination)
                    stack.append(destination)
    
    for result in end_result:
        print(result.get_name())



def print_bfs(graph: IGraph, start_vertex: IVertex) -> None: 
    """Print the BFS traversal of the graph starting from the start vertex"""
    queue: List[IVertex] = []
    nodes_visited: List[IVertex] = []
    visited: bool = False

    all_vertices = graph.get_vertices()

    for vertex in all_vertices:
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
                if vertex not in nodes_visited:
                    nodes_visited.append(vertex)

    for node in nodes_visited:    # returns end result
        print(node.get_name())



def main() -> None:
    graph: IGraph = read_graph("graph.txt")
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