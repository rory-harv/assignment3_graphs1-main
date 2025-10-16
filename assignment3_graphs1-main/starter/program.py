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
        end_result.append(vertex)

    while stack:
        vertex: IVertex = stack.pop()
        if vertex.is_visited() == False:
            graph.add_vertex(vertex)
            visited: bool = True
            vertex.set_visited(visited)
            end_result.append(vertex.get_name())
            edges: List[IEdge] = start_vertex.get_edges()
            for edge in edges:
                destination: IVertex = edge.get_destination()
                if destination.is_visited() == False:
                    helper(destination)
                    stack.append(destination)
    
    print(end_result)



def print_bfs(graph: IGraph, start_vertex: IVertex) -> None: 
    """Print the BFS traversal of the graph starting from the start vertex"""
    queue: List[IVertex] = []
    nodes_visited: List[IVertex] = []
    visited: bool = False
    

            
    adj_list: dict[str, List[str]] = {}

    target = start_vertex.get_name()

    all_vertices = graph.get_vertices()
    all_edges = graph.get_edges()

    # for vertex in all_vertices:
    #     if vertex != None:
    #         print(vertex.get_name())
    
    target_vertex = start_vertex.get_name()
    target_index = all_vertices.index(start_vertex)

    for vertex in all_vertices[target_index:]:
        if vertex != None:
            destination_vertices: List[IVertex] = []
            for edge in vertex.get_edges():
                if vertex.is_visited() == False and vertex.get_name() == target_vertex:
                    destination_vertices.append(edge.get_destination().get_name())
                    visited: bool = True
                    vertex.set_visited(visited)
                    visited: bool = False
        adj_list[vertex] = destination_vertices
        print(adj_list[vertex])

        


    
    print(adj_list)


    # for vertex in adj_list:
    #     print(vertex)


    # visited: bool = True
    # start_vertex.set_visited(visited)   # sets starter vertex as visited
    
    # queue.append(start_vertex)
    # visited: bool = False

    # while queue:    # loops while queue exists
    #     start: IVertex = queue.pop(0)    # takes first element
    #     nodes_visited.append(start)  # appends to final results
    #     for key in adj_list:
    #         for destination in adj_list[key]:
    #             destination.is_visited()
    #             queue.append(key)
    #             visited: bool = True    
    #             key.set_visited(visited) # sets vertex as visited

    while queue:
        start: IVertex = queue.pop(0)
        nodes_visited.append(start)
        #print(adj_list[start])
                
    #for i in range(len(nodes_visited)):
    #    print(nodes_visited[i].get_name())
    #print(nodes_visited)    # returns end result

                
            


            






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