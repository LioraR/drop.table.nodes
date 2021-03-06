# Helper functions for 'radio russia' algorithm


def provinces(INPUT_CSV):

    # open excel file
    with open(INPUT_CSV, newline='') as csvfile:

        lines = csvfile.readlines()

        list_provinces = []
        list_neighbors = []
        # loop through lines to get (neighboring) provinces
        for line in lines:
            # the csv file is splitted on ;
            split_list = line.split('; ')
            provinces = split_list[0]

            # to save provinces in a list
            list_provinces.append(provinces)
            province_neigbours = split_list[1].split(', ')
            province_neigbours[-1] = province_neigbours[-1].strip()
            list_neighbors.append(province_neigbours)

        return(list_provinces, list_neighbors)


def country_to_number(provinces, neighbours):
    """
        country_to_number: tranforms the country names to numbers.
    """

    # Makes dictionary with province and indexnumber.
    provinces_dic = {}
    index = 0
    for province in provinces:
        provinces_dic[province] = index
        index += 1
    neighbours_numbers = []
    # Matches province with neigbours in the made dictionary with indexnumber.
    for province in neighbours:
        neighbours_province = []

        for neighbour in province:
            if neighbour in provinces_dic:
                neighbours_province.append(provinces_dic[neighbour])
        neighbours_numbers.append(neighbours_province)
    return(neighbours_numbers)


"""
The Node class:
it can look for a suitable color for itself on its own.
It has a name, color (transmitter type), and a list of neighbors as unique features
"""


class Node(object):

    def __init__(self, name, transmitter_type, neighbors):
        self.name = name
        self.trans_type = transmitter_type
        self.neighbors = neighbors

    # Check for the color of neighbors and change accordingly.
    def changetype(self, transmitter_list, nodelist):
        a = 0
        type_found = False

        # Iterate through colors until a suitable color has been found.
        while (a < len(transmitter_list)) or not type_found:
            type_found = True
            check_type = transmitter_list[a]
            # Check if type is a suitable type.
            for node in self.neighbors:
                if nodelist[node].trans_type == check_type:
                    type_found = False
                    break
            if type_found:
                self.trans_type = check_type
                break
            a += 1

            if a == len(transmitter_list):
                return(False)

        return(True)


"""
generate a graph of type:
  0----0
/ | \/ |\
0-0-0-0-0-0-0
  \ | /
    0

It can make a graph from both the Node class or a neighbor number representation (A list of lists with the positions of the neighbors in the graph)
"""


def generate_triple(just_numbers=False):
    countrylist = []

    nodetop1 = Node(7, None, [0, 1, 2, 8])
    nodetop2 = Node(8, None, [2, 3, 4, 7])
    nodebottom = Node(9, None, [1, 2, 3])

    countrylist.append(Node(0, None, [1, nodetop1.name]))
    countrylist.append(Node(1, None, [0, 2, nodetop1.name, nodebottom.name]))
    countrylist.append(Node(2, None, [1, 3, nodetop1.name, nodebottom.name, nodetop2.name]))
    countrylist.append(Node(3, None, [2, 4, nodebottom.name, nodetop2.name]))
    countrylist.append(Node(4, None, [3, 5, nodetop2.name]))
    countrylist.append(Node(5, None, [4, 6]))
    countrylist.append(Node(6, None, [5]))

    countrylist.append(nodetop1)
    countrylist.append(nodetop2)
    countrylist.append(nodebottom)

    if just_numbers:
        new_countrylist = []
        for i in countrylist:
            new_countrylist.append(i.neighbors)
        countrylist = new_countrylist

    return(countrylist)


def numbers_to_nodes(neighborlist):
    nodelist = []
    for i in range(0, len(neighborlist)):
        nodelist.append(Node(i, None, neighborlist[i]))
    return(nodelist)


"""
This greedy algorithm takes 4 arguments: The list of countries, the list of available transmitters,
The starting country (or node), and an argument to find the most neighbored countries.
The program will first find the highest number of neighbors any node has in the list, and then add the nodes with that many minus the last argument to a list.
This to test if there is an optimum to be found for prefilling the most neighbored countries.
The program will then run over the list from left to right (and back to 0 if at the end of the list), changing the type of the nodes accordingly.
If no suitable type has been found, it simply returns False.
There are 2 versions of the algorithm: a 'node' version, that uses the Node class
And a regular version, that uses a list of neighbors, below this version
"""


def greedy_nodes(countrylist, transmitter_list, starting_node, find_most_neighbors):
    # From helpers import Node.
    neighborcount = 0
    most_neighbored_countries = []
    countrytranslist = []

    for node in countrylist:
        if len(node.neighbors) > neighborcount:
            neighborcount = len(node.neighbors)

    for node in countrylist:
        if len(node.neighbors) >= neighborcount - find_most_neighbors:
            most_neighbored_countries.append(node.name)

    # Country with most neighbors gets the least used color.
    for node in most_neighbored_countries:
        countrylist[node].changetype(transmitter_list[::-1], countrylist)

    # Change transmitter of country accordingly.
    for i in range(starting_node, starting_node + len(countrylist)):
        if countrylist[i % len(countrylist)].trans_type is None:
            if not countrylist[i % len(countrylist)].changetype(transmitter_list, countrylist):
                return(False)

    for node in most_neighbored_countries:
        countrylist[node].changetype(transmitter_list, countrylist)

    for node in countrylist:
        countrytranslist.append(node.trans_type)

    return(countrytranslist)


def check_neighbors(neighbors_of_node, transmitter_type, countrylist):
    for neighbor in neighbors_of_node:
        if countrylist[neighbor] == transmitter_type:
            return False
    return True


def changetype_greedy_regular(countrylist, neighborlist, transmitter_list, node):
    for type in transmitter_list:
        if check_neighbors(neighborlist[node], type, countrylist):
            return type
    return None


def greedy_regular(neighborlist, transmitter_list, starting_node, find_most_neighbors=0):
    neighborcount = 0
    most_neighbored_countries = []

    # Find node with the most connections.
    for node in neighborlist:
        if len(node) > neighborcount:
            neighborcount = len(node)
    # Add most neighbored countries to list.
    for node in neighborlist:
        if len(node) >= neighborcount - find_most_neighbors:
            most_neighbored_countries.append(neighborlist.index(node))

    country_transmitter_list = [None for i in range(len(neighborlist))]
    for node in most_neighbored_countries:
        country_transmitter_list[node] = changetype_greedy_regular(country_transmitter_list, neighborlist, transmitter_list[::-1], node)

    for node in range(len(neighborlist)):
        if country_transmitter_list[node] is None:
            country_transmitter_list[node] = changetype_greedy_regular(country_transmitter_list, neighborlist, transmitter_list, node)

    for node in most_neighbored_countries:
        country_transmitter_list[node] = changetype_greedy_regular(country_transmitter_list, neighborlist, transmitter_list, node)

    if None in country_transmitter_list:
        print("No suitable options found")
        return(False)

    return(country_transmitter_list)


"""
A function to calculate the cost of a given transmitter configuration
"""


def cost(countrylist, transmitter_cost, transmitter_list):
    cost = 0
    for country in countrylist:
        cost = cost + transmitter_cost[transmitter_list.index(country)]
    return cost


"""
A function to calculate the cost of the transmitters.
It takes a list of the total number of transmitters in the country per type
e.g. [4, 3, 2, 1, 1, 0]
It then returns the cost of this list based on the transmitter cost given.
"""


def calculate_cost(number_of_transmitters, transmitter_cost_list):
    cost = 0
    for i in range(len(number_of_transmitters)):
        cost += transmitter_cost_list[i] * number_of_transmitters[i]
    return(cost)


"""
A function to rewrite the transmitter list to number of transmitters per type
To be used in the calculate_cost function
"""


def countrylist_to_transmitter_amount(countrylist, transmitter_list):
    count_list = []
    for type in transmitter_list:
        count_list.append(countrylist.count(type))
    return(count_list)


"""
A function to count the number of neighbors with the same transmitter
"""


def check_for_matching_neighbors(countrylist, neighborlist):
    matching = 0
    for country in range(len(countrylist)):
        for neighbor in neighborlist[country]:
            if countrylist[neighbor] is None:
                pass

            elif neighbor > country:
                if countrylist[country] == countrylist[neighbor]:
                    matching += 1
    return(matching)


"""
make comment
"""


def generate_random_country(neighborlist, transmitter_list):
    import random
    import copy
    transmitter_list = copy.deepcopy(transmitter_list)
    countrylist = [None]
    while None in countrylist:
        countrylist = [None for i in range(len(neighborlist))]
        countryshuffle = list(range(len(countrylist)))
        random.shuffle(countryshuffle)
        
        for country in countryshuffle:
            random.shuffle(transmitter_list)
            for transmitter_type in transmitter_list:
                if check_neighbors(neighborlist[country], transmitter_type, countrylist):
                    countrylist[country] = transmitter_type
    return countrylist


def visualise_graph(countrylist, neighborlist, transmitter_list, transmitter_colors):
    import networkx as nx
    import matplotlib.pyplot as plt
    gr = []
    country_colors = []
    for node in range(len(countrylist)):
        for neighbor in neighborlist[node]:
            gr.append((node, neighbor))
    graph = nx.Graph(gr)

    for node in graph.nodes():
        country_colors.append(transmitter_colors[transmitter_list.index(countrylist[node])])

    nx.draw_kamada_kawai(graph, node_color=country_colors, with_labels=True)
    plt.show()
