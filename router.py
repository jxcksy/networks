import pandas as pd

class Router:


   def __init__(self, name, graph_connection) -> None:

      '''This function initialises the graph instance with a name and connection.'''

      self.name = name
      self.graph_connection = graph_connection


   def get_path(self, end) -> str:

      '''This function visits every node (except for itself) and keeps track of the 
      weight of each path. Then, using Dijkstra's algorithm, an algorithm for 
      finding the shortest paths between nodes in a graph, the lowest cost from 
      the router given to all other remaining nodes is then recorded, as well 
      as the path taken. The start (router given to the function), end 
      (each other node respectively), path (the shorest path taken) and cost 
      (weight of the path) are then printed.'''

      nodes = ["a", "b", "c", "d", "e", "f"]
      unvisited = {n: float("inf") for n in nodes}

      unvisited[self.name] = 0 # SET START TO 0
      visited = {}  # DICT OF VISITED NODES
      predecessors = {}  # DICT OF PREDECESSORS

      while unvisited:
         minimum = min(unvisited, key=unvisited.get) # GET SMALLEST DISTANCE

         for neighbour, _ in Graph.graph.get(minimum, {}).items():
            if neighbour in visited:
               continue

            new_cost = unvisited[minimum] + Graph.graph[minimum].get(neighbour, float("inf"))

            if new_cost < unvisited[neighbour]:
               unvisited[neighbour] = new_cost
               predecessors[neighbour] = minimum

         visited[minimum] = unvisited[minimum]
         unvisited.pop(minimum)

         if minimum == end:
            break

      path = [end]
      while True:

         key = predecessors[path[0]]
         path.insert(0, key)

         if key == self.name:
            break

      return("Start: %s \nEnd: %s \nPath: %s \nCost: %.2d" % (self.name, end, "->".join(path), visited[end]))

   # DUPLICATE GET_PATH FUNCTION THAT RETURNS VALUES INSTEAD OF PRINTING THEM
   # USED IN THE PRINT_ROUTING_TABLE AND REMOVE_ROUTER FUNCTIONS

   def find_path(self, end, nodes = ["a", "b", "c", "d", "e", "f"]) -> tuple:

      '''This function, similarly to the get_path function, 
      visits every node (except for itself) and keeps track of the weight 
      of each path. Then, using Dijkstra's algorithm, 
      an algorithm for finding the shortest paths between nodes in a graph, 
      the lowest cost from the router given to all other remaining nodes is then recorded, 
      as well as the path taken. The start (router given to the function), 
      end (each other node respectively), path (the shorest path taken) 
      and cost (weight of the path) values are then returned instead of printed. 
      This means that the values recorded through the use of this fucntion can then be 
      used without printing them every time.'''

      #nodes = ["a", "b", "c", "d", "e", "f"]
      unvisited = {n: float("inf") for n in nodes}
      unvisited[self.name] = 0  # SET START TO 0
      visited = {}  # DICT OF VISITED NODES
      predecessors = {}  # DICT OF PREDECESSORS
      while unvisited:
         minimum = min(unvisited, key=unvisited.get)  # GET SMALLEST DISTANCE
         for neighbour, _ in Graph.graph.get(minimum, {}).items():
            if neighbour in visited:
               continue
            new_cost = unvisited[minimum] + Graph.graph[minimum].get(neighbour, float("inf"))
            try:
               if new_cost < unvisited[neighbour]:
                  unvisited[neighbour] = new_cost
                  predecessors[neighbour] = minimum
            except KeyError:
               pass
         visited[minimum] = unvisited[minimum]
         unvisited.pop(minimum)
         if minimum == end:
            break
      path = [end]
      while True:
         key = predecessors[path[0]]
         path.insert(0, key)
         if key == self.name:
            break
      
      return(predecessors, visited, path, self.name, end)

   #FUNCTION TO PRINT ROUTING TABLE

   def print_routing_table(self, nodes = ["a", "b", "c", "d", "e", "f"]) -> None:

      '''This function makes use of the find_path function to retrieve the start, end, cost and path values without having to print them (as the get_path function was intended to), these values, once returned, are then recorded and added to a table as a pandas dataframe. Once this is done, print is then called on the table which is then outputted.'''

      paths = [] #LIST OF PATHS FOR EACH NODE
      costs = [] #LIST OF COSTS FOR EACH PATH
      for node in nodes:
         if self.name != node: #NO NEED TO PATH TO ITSELF AS ITS ALWAYS 0
            key, value, path, start, end = self.find_path(node)
            paths.append("->".join(path))
            costs.append(value[end])

      for node in nodes:
         if self.name == node:
            nodes.remove(self.name)

      # INITIALIZE PANDAS DATAFRAME

      cols = ['from', 'to', 'cost', 'path']
      df = pd.DataFrame(columns=cols)

      for i in range(len(nodes)):
         df = df.append({'from': start, 'to': nodes[i], 'cost': costs[i], 'path': paths[i]}, ignore_index=True)

      print('\n{}\n'.format(df))

   # SIMILAR TO PRINT_ROUTING_TABLE FUNCTION EXCEPT THIS FUNCTION:
   # REMOVES THE NODE SPECIFIED
   # THEN CALCULATES PATHS AND COSTS FOR EACH PATH

   def remove_router(self, router_name) -> None:

      '''This function first takes in a router name to be deleted, 
      checks if the router exists in the list of nodes, if it exists, 
      it is then deleted. The updated list of nodes is then passed to 
      the find_path function, as paths and the cost of paths that had 
      originally used the now removed node will also have to be updated. 
      Once this is done, a new routing table is printed with the updated information.'''

      nodes = ["a", "b", "c", "d", "e", "f"]
      paths = [] #LIST OF PATHS FOR EACH NODE
      costs = [] #LIST OF COSTS FOR EACH PATH

      for node in nodes:

         if router_name == node:
            nodes.remove(router_name)

      for node in nodes:

         if self.name != node:

            key, value, path, start, end = self.find_path(node, nodes)
            paths.append("->".join(path))
            costs.append(value[end])

      cols = ['from', 'to', 'cost', 'path']
      df = pd.DataFrame(columns=cols)

      for i in range((len(nodes) - 1)):
         df = df.append({'from': start, 'to': nodes[i+1], 'cost': costs[i], 'path': paths[i]}, ignore_index=True)

      #print(df)
      #print(paths)
      #print(costs)
      #print(nodes)


class Graph:

   graph = {} #INITIALIZE GRAPH

   def add_edge(self, node_one, node_two, weight) -> None:

      '''This function adds an edge to a graph by taking in a 
      node as a start position, another node as an end position 
      and the weight of the path from the first to the second node.'''

      if node_one in Graph.graph:
         Graph.graph[node_one][node_two] = int(weight)

      else:
         Graph.graph[node_one] = {}

      Graph.graph[node_one][node_two] = int(weight)


def main():

   # TESTING GRAPH

   graph = Graph()

   graph.add_edge("a", "b", 7)
   graph.add_edge("a", "c", 9)
   graph.add_edge("a", "f", 14)
   graph.add_edge("b", "c", 10)
   graph.add_edge("b", "d", 15)
   graph.add_edge("c", "d", 11)
   graph.add_edge("c", "f", 2)
   graph.add_edge("d", "e", 6)
   graph.add_edge("e", "f", 9)
   graph.add_edge("f", "a", 14)
   graph.add_edge("f", "e", 9)

   router = Router("a", graph)
   router_two = Router("c", graph)

   # TESTING FUNCTIONS

   print(router.get_path("e"))
   router.print_routing_table()
   router.remove_router("c")
   router_two.print_routing_table()

   # PYDOC

   #print(Router.get_path.__doc__)
   #print(Router.find_path.__doc__)
   #print(Router.print_routing_table.__doc__)
   #print(Router.remove_router.__doc__)


if __name__ == '__main__':
   main()
