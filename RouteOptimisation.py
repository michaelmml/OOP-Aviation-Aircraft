class Airport:

    def __init__(self, data, indexloc=None):
        self.data = data
        self.index = indexloc


class Flightpath:

    @classmethod
    def create_from_airports(self, airports):
        return Flightpath(len(airports), len(airports), airports)

    def __init__(self, row, col, airports=None):
        # set up adjacency matrix based on row and col input with sequence up to number of rows
        # instance attribute to create matrix
        # airports or nodes are attributes
        self.adj_mat = [[0] * col for _ in range(row)]
        self.airports = airports
        for i in range(len(self.airports)):
            self.airports[i].index = i

    # Connects from node1 to node2
    def flight_dir(self, airport1, airport2, weight=1):
        airport1, airport2 = self.get_index_from_airport(airport1), self.get_index_from_airport(airport2)
        self.adj_mat[airport1][airport2] = weight

    def flight(self, airport1, airport2, weight=1):
        self.flight_dir(airport1, airport2, weight)
        self.flight_dir(airport2, airport1, weight)

    # Get node row, map non-zero items to their node in the self.nodes array
    # Select any non-zero elements, leaving you with an array of nodes
    # which are connections_to (for a directed graph)
    # Return value: array of tuples (node, weight)
    def flight_from(self, airport):
        airport = self.get_index_from_airport(airport)
        return [(self.airports[col_num], self.adj_mat[airport][col_num]) for col_num in
                range(len(self.adj_mat[airport])) if self.adj_mat[airport][col_num] != 0]

    # Map matrix to column of node
    # Map any non-zero elements to the node at that row index
    # Select only non-zero elements
    # Note for a non-directed graph, you can use connections_to OR
    # connections_from
    # Return value: array of tuples (node, weight)
    def flight_to(self, airport):
        airport = self.get_index_from_airport(airport)
        column = [row[airport] for row in self.adj_mat]
        return [(self.airports[row_num], column[row_num]) for row_num in range(len(column)) if column[row_num] != 0]

    def print_adj_mat(self):
        for row in self.adj_mat:
            print(row)

    def airport(self, index):
        return self.airport[index]

    def remove_path(self, airport1, airport2):
        self.remove_path_dir(airport1, airport2)
        self.remove_path_dir(airport2, airport1)

    def remove_path_dir(self, airport1, airport2):
        node1, node2 = self.get_index_from_airport(airport1), self.get_index_from_node(airport2)
        self.adj_mat[airport1][airport2] = 0

    def can_traverse_dir(self, airport1, airport2):
        airport1, airport2 = self.get_index_from_airport(airport1), self.get_index_from_airport(airport2)
        return self.adj_mat[airport1][airport2] != 0

    def has_conn(self, airport1, airport2):
        return self.can_traverse_dir(airport1, airport2) or self.can_traverse_dir(airport2, airport1)

    def add_airport(self, airport):
        self.airport.append(airport)
        airport.index = len(self.airport) - 1
        for row in self.adj_mat:
            row.append(0)
        self.adj_mat.append([0] * (len(self.adj_mat) + 1))

    def get_weight(self, n1, n2):
        airport1, airport2 = self.get_index_from_airport(n1), self.get_index_from_airport(n2)
        return self.adj_mat[airport1][airport2]

    def get_index_from_airport(self, airport):
        if not isinstance(airport, Airport) and not isinstance(airport, int):
            raise ValueError("node must be an integer or a Node object")
        if isinstance(airport, int):
            return airport
        else:
            return airport.index

    def dijkstra(self, airport):
        # Get index of node (or maintain int passed in)
        airportnum = self.get_index_from_airport(airport)
        # Make an array keeping track of distance from node to any node
        # in self.nodes. Initialize to infinity for all nodes but the
        # starting node, keep track of "path" which relates to distance.
        # Index 0 = distance, index 1 = node hops
        dist = [None] * len(self.airports)
        for i in range(len(dist)):
            dist[i] = [float("inf")]
            dist[i].append([self.airports[airportnum]])

        dist[airportnum][0] = 0
        queue = [i for i in range(len(self.airports))]
        seen = set()
        while len(queue) > 0:
            # Get node in queue that has not yet been seen
            # that has smallest distance to starting node
            min_dist = float("inf")
            min_airport = None
            for n in queue:
                if dist[n][0] < min_dist and n not in seen:
                    min_dist = dist[n][0]
                    min_airport = n

                # Add min distance airport to seen, remove from queue
            queue.remove(min_airport)
            seen.add(min_airport)
            flights = self.flight_from(min_airport)
            # For each connection, update its path and total distance from
            # starting node if the total distance is less than the current distance
            # in dist array
            for (airport, weight) in flights:
                tot_dist = weight + min_dist
                if tot_dist < dist[airport.index][0]:
                    dist[airport.index][0] = tot_dist
                    dist[airport.index][1] = list(dist[min_airport][1])
                    dist[airport.index][1].append(airport)
        return dist


a = Airport("A")
b = Airport("B")
c = Airport("C")
d = Airport("D")
e = Airport("E")
f = Airport("F")

w_flightpath = Flightpath.create_from_airports([a, b, c, d, e, f])

w_flightpath.flight(a, b, 5)
w_flightpath.flight(a, c, 8)
w_flightpath.flight(a, e, 4)
w_flightpath.flight(b, c, 9)
w_flightpath.flight(b, d, 4)
w_flightpath.flight(c, d, 8)
w_flightpath.flight(c, f, 2)
w_flightpath.flight(d, e, 1)

print("Airports and Flight Paths:")
w_flightpath.print_adj_mat()
print([(weight, [n.data for n in airport]) for (weight, airport) in w_flightpath.dijkstra(a)])
