import numpy
import math
import random
import sys
import networkx as nx

from Clusterize.ClusterizePlugin import *
from PageRank.PageRankPlugin import *


def biasedpagerank(G,clusters,alpha1=0.5,alpha2=0.35,max_iter=100,tol=1.0e-8,nstart=None):

    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise Exception("pagerank() not defined for graphs with multiedges.")

    if not G.is_directed():
        D=G.to_directed()
    else:
        D=G

    # create a copy in (right) stochastic form        
    W=nx.stochastic_graph(D)

    # choose fixed starting vector if not given
    if nstart is None:
        x=dict.fromkeys(W,1.0/W.number_of_nodes())
    else:
        x=nstart
        # normalize starting vector to 1                
        s=1.0/sum(x.values())
        for k in x: x[k]*=s

    nnodes=W.number_of_nodes()
    # "dangling" nodes, no links out from them
    out_degree=W.out_degree()
    dangle=[n for n in W if out_degree[n]==0.0]
    i=0
    while True: # power iteration: make up to max_iter iterations
        xlast=x
        x=dict.fromkeys(xlast.keys(),0)
        danglesum=((alpha1+alpha2)/nnodes)*sum(xlast[n] for n in dangle)
        teleportsum=(1.0-alpha1-alpha2)/nnodes*sum(xlast.values())
        for n in x:
            # this matrix multiply looks odd because it is
            # doing a left multiply x^T=xlast^T*W
            for nbr in W[n]:
               if (inSameCluster(n, nbr, clusters)):
                x[nbr]+=alpha1*xlast[n]*W[n][nbr]['weight']
               else:
                x[nbr]+=alpha2*xlast[n]*W[n][nbr]['weight']
            x[n]+=danglesum+teleportsum
        # normalize vector to 1                
        s=1.0/sum(x.values())
        for n in x: x[n]*=s
        # check convergence, l1 norm            
        err=sum([abs(x[n]-xlast[n]) for n in x])
        print err, tol
        if err < tol:
            break
        if i>max_iter:
            raise NetworkXError(\
        "pagerank: power iteration failed to converge in %d iterations."%(i+1))
        i+=1
    return x



############################################################
####################################################################################################

class BiasedPageRankPlugin(PageRankPlugin):
   def input(self, filename):
      PageRankPlugin.input(self,filename+".csv")
      self.clusters = readClusterFile(filename+".clusters.csv")      
   def run(self):
      self.U = biasedpagerank(self.graph, self.clusters, alpha1=0.5, alpha2=0.35, max_iter=100)


