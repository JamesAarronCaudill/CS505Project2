#This Project will be written in python

#Authors: James Aarron Caudill & Kristina Gessel
#University of Kentucky CS505G Project 2
#If this is used please give credit where credit is due, also please use within the terms of NetworkX, urllib and matplotlib

#NetworkX is going to be the API for our Graphs
#We will be using networkX's implementation of Cliques, as their source provided
#is identical to how it would need to be implemented.
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


#Here we will be using NetworkX's implementation of cliques to find the cliques
#The source they provided on their website was very similar to other information and
#psuedo code that we located for cliques. For simplification we decided to use their implementation
#as it is ambiguious to reinvent the wheel.
def FindCliquesAndButterflies():

    #This will compute a list of cliques.
    #We are using NetworkX's Implementation of Cliques
    #Reciprocal = true make sure that only nodes that have both edges will be included for searching for cliques
    listOfCliques = list(nx.find_cliques(DirectedEmailGraph.to_undirected(reciprocal=True)))

    #This will find the maximum clique size.
    #Reciprocal = true make sure that only nodes that have both edges will be included for searching for cliques
    #Cliques = listOfCliques provides the list of cliques already computed
    maxCliqueSize = nx.graph_clique_number(DirectedEmailGraph.to_undirected(reciprocal=True), cliques=listOfCliques)

    #This list will hold the all of the cliques with the max size that matches maxCliqueSize
    listOfMaximumCliques = []

    #This will compute listOfMaximumCliques
    for i in range(len(listOfCliques)):
        if len(listOfCliques[i]) == maxCliqueSize:
            listOfMaximumCliques.append(listOfCliques[i])

    #This will contain the nodes from the listOfMaximumCliques, a set is chosen because of no duplicate elements
    setOfNodes = set()

    #This will compute the setOfNodes
    for i in range(len(listOfMaximumCliques)):
        for j in range(maxCliqueSize):
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
    for i in range(len(tempListOfButterflies)):

        #This will tell us if the list if larger than size 1, in the case that it is larger than size 1
        #Then we know that there are either 2 cliques with 2 nodes in common
        #or more than 2 cliques one or more with the possibility of more than one node in common.
        if len(tempListOfButterflies[i]) > 2:
            for j in range(len(tempListOfButterflies[i])):
                for k in range(len(tempListOfButterflies[i])):
                    if k > j:
                        tempSet = set.intersection(*map(set,(tempListOfButterflies[i][j],tempListOfButterflies[i][k])))
                        if len(tempSet) == 1:
                            RealListOfButterflies.append((tempListOfButterflies[i][j], tempListOfButterflies[i][k]))

        #If there are only two cliques and only one node in common then we will add them to the list of butterflies
        if(len(tempListOfButterflies[i]) == 2):
            tempSet = set.intersection(*map(set,tempListOfButterflies[i]))
            if len(tempSet) == 1:
                RealListOfButterflies.append(tempListOfButterflies[i])



    #Here we will start listing cliques of largest size.
    print "##########################################################"
    print "The largest size clique in the graph was: ", maxCliqueSize
    print "##########################################################"
    print "List of Butterflies: \n"

    for i in range(len(RealListOfButterflies)):
        print RealListOfButterflies[i]
    return

#This function will find all of the people that have emailed woods.
#These are the people that could of secretly let him know that they have documents
#It could be as simple as "Hey meet me tomorrow"
#However we know that in order to signal woods that the person had to emailed him.
#This will compile a list of everyone that has emailed woods.
def FindWoodsSource ():

    #Setting up a list to hold all of the users that have emailed WOODS
    listOfSuspects = []

    #This will iterate over the graph and see if an edge exsits between
    #A different user and WOODS, this checks only to see people that have emailed him
    for i in DirectedEmailGraph:
        if DirectedEmailGraph.has_edge(i, 'WOODS'):
            listOfSuspects.append(i)

    #Function providing data that was calculated to help find suspects
    print "\n##########################################################"
    print "The list of suspects that could have provided user woods"
    print "with trade secrets of HN."
    print "##########################################################"

    for i in range(len(listOfSuspects)):
        print listOfSuspects[i]
    return

#These are calling all of our functions in order of how they need to be called.
GraphBuilderFunction()
FindCliquesAndButterflies()
FindWoodsSource()
