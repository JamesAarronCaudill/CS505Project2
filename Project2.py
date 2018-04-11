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
        myTempFile = myfile[i].split(' ')
        j = 1
        for z in range(len(myTempFile) - 1):
            DirectedEmailGraph.add_edge(myTempFile[0], myTempFile[j])
            j = j + 1
        i = i + 2
        print DirectedEmailGraph.edges()
        nx.draw(DirectedEmailGraph,with_labels=True)
        plt.show()
    return

GraphBuilderFunction()
