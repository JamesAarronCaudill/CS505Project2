#This Project will be written in python

#NetworkX is going to be the API for our Graphs
#We will be using Directed Graphs
import networkx as nx
import urllib as url
import matplotlib.pyplot as plt

link = "http://www.cs.engr.uky.edu/~marek/dataset"

f = url.urlopen(link)
myfile = f.read()
myfile = myfile.split('\n')

DirectedEmailGraph = nx.DiGraph()

#This Function will build the Graph
#Because of the way the list is split
#This function will only be using the even numbers in my list
def GraphBuilderFunction():
    i = 0
    for x in range(len(myfile) - 1):
        #This is the iterator responsible for placing the list of items in the graph
        j = 1

        #This makes sure that we dont go outside of the range of the list
        if i <= (len(myfile) - 1):

            #Splits the string based on spaces, this allows us to have individual names
            myTempFile = myfile[i].split(' ')

            #This removes the last item in the list which happens to be an empty string caused by a space after the last name.
            myTempFile = myTempFile[:-1]

        #This runs through the size of the a list that is temp. which contains the split file.
        for z in range(len(myTempFile) - 1):

            #This uses iterator j to place everything in the graph as an edge from the first item.
            DirectedEmailGraph.add_edge(myTempFile[0], myTempFile[j])

            #j is increased by one to gain access to the next item
            j = j + 1

        #These are here for the purpose of debugging. Graph is to large to build on its own. Un comment these to see it run through
        #each like of the dataset.
        #nx.draw(DirectedEmailGraph, with_labels=True)
        #plt.show()

        #This increments i plus 2 because every other i is a new line character due to splitting on the new line characters.
        i = i + 2


    return


def FindCliquesAndButterflies():

    #This will compute a list of cliques.
    #Reciprocal = true make sure that only nodes that have both edges will be included for searching for cliques
    listOfCliques = list(nx.find_cliques(DirectedEmailGraph.to_undirected(reciprocal=True)))

    #This will find the maximum clique size.
    #Reciprocal = true make sure that only nodes that have both edges will be included for searching for cliques
    #Cliques = listOfCliques provides the list of cliques already computed
    maxCliqueSize = nx.graph_clique_number(DirectedEmailGraph.to_undirected(reciprocal=True), cliques=listOfCliques)

    #This list will hold the all of the cliques with the max size that matches maxCliqueSize
    listOfMaximumCliques = []

    #This will compute listOfMaximumCliques
    for i in range(len(listOfCliques) - 1):
        if len(listOfCliques[i]) == maxCliqueSize:
            listOfMaximumCliques.append(listOfCliques[i])

    #This will contain the nodes from the listOfMaximumCliques, a set is chosen because of no duplicate elements
    setOfNodes = set()

    #This will compute the setOfNodes
    for i in range(len(listOfMaximumCliques) - 1):
        for j in range(maxCliqueSize - 1):
            setOfNodes.add(listOfMaximumCliques[i][j])

    #This will hold a temporary list of butterflies. The reason behind this, is we have not verrified that these are only connected by one node and one node only.
    tempListOfButterflies = []
    maxSizeOfTempListOfButterflies = 0

    #Computes tempListOfButterflies
    for i in setOfNodes:
        tempList = nx.cliques_containing_node(DirectedEmailGraph.to_undirected(reciprocal=True), nodes=i, cliques=listOfMaximumCliques)
        if(len(tempList) >= 2):
            tempListOfButterflies.append(tempList)

            #This is going to be used to calculate butterflies
            if maxSizeOfTempListOfButterflies < len(tempList):
                maxSizeOfTempListOfButterflies = len(tempList)

    #This will hold a list of list of lists that contain {{{LeftWing}{RightWing}},{{LeftWing}{RightWing}}} and so on
    RealListOfButterflies = []

    #This Computes RealListOfButterflies
    for i in range(len(tempListOfButterflies) - 1):

        #We will create a temp list of the intersection of one of the possibilties for butterflies
        tempSet = set.intersection(*map(set,tempListOfButterflies[i]))

        #This will tell us if the list if larger than size 1, in the case that it is larger than size 1
        #Then we know that there are either 2 cliques with 2 nodes in common
        #or more than 2 cliques one or more with the possibility of more than one node in common.
        if len(tempListOfButterflies[i]) > 2:

            #If the cliques only have one node in common
            if len(tempSet) == 1:

                #If the list of cliques for butterflies has more than 2 cliques, this will calculate the butterflies
                for j in range(len(tempListOfButterflies[1]) - 2):
                    RealListOfButterflies.append(tempListOfButterflies[i][j][j+1])

            #If the cliques have more than one node in common
            if len(tempSet) >= 2:

                for j in range(len(tempListOfButterflies[i]) - 2):
                    for k in range(len(tempListOfButterflies[i] - 2)):
                        if k > j:
                            tempSetOne = set.intersection(*map(set,tempListOfButterflies[i][j][k + 1]))
                            if tempSetOne == 1:
                                RealListOfButterflies.append(tempListOfButterflies[i][j][k+1])

        #If there are only two cliques and only one node in common then we will add them to the list of butterflies
        if(len(tempListOfButterflies[i]) == 2):
            if len(tempSet) == 1:
                RealListOfButterflies.append(tempListOfButterflies[i])

    print RealListOfButterflies
    return

#Calls the GraphBuilderFunction
GraphBuilderFunction()
FindCliquesAndButterflies()
