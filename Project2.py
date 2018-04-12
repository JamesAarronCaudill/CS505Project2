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


def FindCliques():
    print find_cliques(DirectedEmailGraph.to_undirected(reciprocal=False))
    return

#Calls the GraphBuilderFunction
GraphBuilderFunction()
FindCliques()
