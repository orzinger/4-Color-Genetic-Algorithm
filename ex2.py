import numpy as np
import networkx as nx
import sys, getopt
import matplotlib.pyplot as plt


adj_mat = [(1,2),(1,6),(1,11),
(2,3),(2,7),(2,8),(2,9),(2,11),
(3,4),(3,5),(3,9),(3,11),
(4,5),(4,11),
(5,12),(5,11),(5,9),
(6,8),(6,10),(6,11),(6,12),(6,7),
(7,8),
(8,9),(8,10),
(9,12),(9,10),
(10,12),
(11,12)]


parameters = {
    "cv_%" : 0.5,
    "population" : 50,
    "mutation_probability" : 0.6
}

colormap = ["orange","blue","red","green"]

def fit(state):

    violations = 0

    for edges in adj_mat:

        if state[edges[0]-1] == state[edges[1]-1]:

            violations += 1
        
        # violations += len(np.intersect1d(np.array(np.where(adj_mat[i])), np.array(np.where(state==x))))

    return np.array(violations)



def selection(parents, population):

    parents = sorted(parents)

    norm_parents = parents / sum(parents)

    norm_parents = np.cumsum(norm_parents)

    r = np.random.rand()

    parent2 = parent1 = list(map(lambda x: x>r, norm_parents)).index(True)

    while parent2 == parent1:

        r = np.random.rand()

        parent2 = list(map(lambda x: x>r, norm_parents)).index(True)

    return population[parent1], population[parent2]



def crossover(parent1, parent2):

    cross_split_point = int(np.floor(len(parent1) * parameters["cv_%"]))

    offspring1 = np.concatenate([parent1[:cross_split_point], parent2[cross_split_point:]])

    offspring2 = np.concatenate([parent2[:cross_split_point], parent1[cross_split_point:]])

    return offspring1, offspring2



def mutation(offspring):

    for i in range(len(offspring)):
        
        m = np.random.rand()

        if m <= parameters["mutation_probability"]:

            old_color = set([offspring[i]])

            colors = set([1,2,3,4]) - old_color

            new_color = np.random.choice(list(colors))

            offspring[i] = new_color
    
    return offspring


if __name__ == "__main__":

    try:

      opts, args = getopt.getopt(sys.argv[1:],"hc:p:m:",["crossover=","population=","mutation="])

    except getopt.GetoptError:

      print("ex2.py -c <crossover> -p <population> -m <mutation>")
      print("ex2.py -h")
      print("-c <crossover> : crossover percentage (i.e. -c 20 = 20%)")
      print("-p <population> : population (i.e. -p 50)")
      print("-m <mutation> : mutation probability (i.e. -m 0.5)")
      sys.exit(2)

    for opt, arg in opts:

        if opt == '-h':
            
            print("ex2.py -c <crossover> -p <population> -m <mutation>")
            print("-c <crossover> : crossover percentage (i.e. -c 20 = 20%)")
            print("-p <population> : population (i.e. -p 50)")
            print("-m <mutation> : mutation probability (i.e. -m 0.5)")
            sys.exit()

        elif opt in ("-c", "--crossover"):

            parameters["cv_%"] = int(arg)

        elif opt in ("-p", "--population"):

            parameters["population"] = int(arg)

        elif opt in ("-m", "--mutation"):

            parameters["mutation_probability"] = float(arg)



    initial_population = np.random.randint(1,5,(parameters["population"],12))

    population = initial_population

    generation = 0

    while(True):

        generation += 1

        fit_of_parents = [fit(parent) for parent in population]

        if [0.] in fit_of_parents:

            solution = population[fit_of_parents.index(0.)]

            break

        new_population = list()

        while len(new_population) < parameters["population"]:

            parent1, parent2 = selection(fit_of_parents, population)

            offspring1, offspring2 = crossover(parent1, parent2)

            offspring1 = mutation(offspring1)

            offspring2 = mutation(offspring2)

            new_population.append(offspring1)

            new_population.append(offspring2)

        population = new_population

    color_solution = [colormap[i-1] for i in solution]

    G = nx.Graph()

    G.add_nodes_from([1,2,3,4,5,6,7,8,9,10,11,12])

    G.add_edges_from(adj_mat)

    nx.draw(G, node_color=color_solution, with_labels=True, font_weight='bold')

    plt.savefig("4-color mapping.png")

    print("Final solution: {}\nGenerations: {}".format(solution, generation))
