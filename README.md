# BiasedPageRank
# Language: Python
# Plugin Dependencies: Clusterize, PageRank
# Other Dependencies: pythonds, version 2.1 (https://pypi.python.org/pypi/pythonds/1.2.1)
# Input: Prefix (file prefix for network and cluster CSV files)
# Output: NOA (central nodes and centrality values) 
# Tested with: PluMA 1.0, Python 3.6

PluMA plugin that runs Edge-Weighted Personalized (EWP) PageRank (Xie et al, 2015).
This algorithm is a modification of Google's PageRank algorithm (Page, 1999).
In PageRank, a random walker is assigned a certain probability of moving
to a random neighbor (in the case of the Internet, this would be a hyperlink)
or teleporting somewhere random.  

With EWP PageRank, neighbors also can be biased (thus creating three or more probabilities).
This particular plugin expects both the network and a CSV file specifying clusters,
and in turn will give the random walker a higher probability of advancing to a neighbor in the 
same cluster compared to one that is not.  This is particularly useful for isolating leader
nodes in clusters, which should be hit the most.

The network file should be in CSV format with nodes as both rows and columns and entry
(i, j) indicating the weight of the edge from node i to node j.

The cluster CSV file should be in the following format (note this is also output by
some other PluMA plugins, i.e. AffinityPropagation):

"","x"
"1","Family.Lachnospiraceae.0001"
"2","Family.Ruminococcaceae.0003"
"3","Family.Lachnospiraceae.0029"
"4","Family.Lachnospiraceae.0043"
"5","Family.Ruminococcaceae.0019"
"6","Family.Lachnospiraceae.0095"
"","x"
"1","Family.Porphyromonadaceae.0005"
"2","Family.Porphyromonadaceae.0006"
"3","Family.Lachnospiraceae.0045"
"4","Order.Clostridiales.0007"
"","x"
"1","Kingdom.Bacteria.0001"
"2","Family.Porphyromonadaceae.0013"
"3","Phylum.Firmicutes.0004"

BiasedPageRank will then produce a NOde Attribute (NOA) file for Cytoscape containing
nodes and centrality values.  This file can subsequently be imported into Cytoscape, assigning
a centrality value to every node and enabling downstream analysis or visualization depending on this 
value.

Please see enclosed example.
 
