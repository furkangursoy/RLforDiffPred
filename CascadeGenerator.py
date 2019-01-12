## Lines 5-99 are taken from the referenced source and slightly modified. In this part, functions for generating cascades are defined.
## The application begins from Line 100. Please check readme section on github for replication steps for the method described in the paper:
## Gursoy, F., & Durahim, A. O. (2018). Predicting Diffusion Reach Probabilities via Representation Learning on Social Networks. Proceedings of the 5th International Management Information Systems Conference. doi:10.6084/m9.figshare.7565894

"""
Implement independent cascade model
"""
#!/usr/bin/env python
#    Copyright (C) 2004-2010 by
#    Hung-Hsuan Chen <hhchen@psu.edu>
#    All rights reserved.
#    BSD license.
#    NetworkX:http://networkx.lanl.gov/.
__author__ = """Hung-Hsuan Chen (hhchen@psu.edu)"""

import copy
import networkx as nx
import random

__all__ = ['independent_cascade']



def independent_cascade(DG, seeds):
  """Return the active nodes of each diffusion step by the independent cascade
  model
  Parameters
  -----------
  G : graph
    A NetworkX graph
  seeds : list of nodes
    The seed nodes for diffusion
  steps: integer
    The number of steps to diffuse.  If steps <= 0, the diffusion runs until
    no more nodes can be activated.  If steps > 0, the diffusion runs for at
    most "steps" rounds
  Returns
  -------
  layer_i_nodes : list of list of activated nodes
    layer_i_nodes[0]: the seeds
    layer_i_nodes[k]: the nodes activated at the kth diffusion step
  Notes
  -----
  When node v in G becomes active, it has a *single* chance of activating
  each currently inactive neighbor w with probability p_{vw}
  Examples
  --------
  >>> DG = nx.DiGraph()
  >>> DG.add_edges_from([(1,2), (1,3), (1,5), (2,1), (3,2), (4,2), (4,3), \
  >>>   (4,6), (5,3), (5,4), (5,6), (6,4), (6,5)], act_prob=0.2)
  >>> layers = networkx_addon.information_propagation.independent_cascade(DG, [6])
  References
  ----------
  [1] David Kempe, Jon Kleinberg, and Eva Tardos.
      Influential nodes in a diffusion model for social networks.
      In Automata, Languages and Programming, 2005.
  """

  # perform diffusion
  A = copy.deepcopy(seeds)  # prevent side effect
  return _diffuse_all(DG, A)


def _diffuse_all(G, A):
  tried_edges = set()
  layer_i_nodes = [ ]
  layer_i_nodes.append([i for i in A])  # prevent side effect
  while True:
    len_old = len(A)
    (A, activated_nodes_of_this_round, cur_tried_edges) = \
        _diffuse_one_round(G, A, tried_edges)
    layer_i_nodes.append(activated_nodes_of_this_round)
    tried_edges = tried_edges.union(cur_tried_edges)
    if len(A) == len_old:
      break
  return layer_i_nodes

def _diffuse_one_round(G, A, tried_edges):
  activated_nodes_of_this_round = set()
  cur_tried_edges = set()
  for s in A:
    for nb in G.successors(s):
      if nb in A or (s, nb) in tried_edges or (s, nb) in cur_tried_edges:
        continue
      if _prop_success(G, s, nb):
        activated_nodes_of_this_round.add(nb)
      cur_tried_edges.add((s, nb))
  activated_nodes_of_this_round = list(activated_nodes_of_this_round)
  A.extend(activated_nodes_of_this_round)
  return A, activated_nodes_of_this_round, cur_tried_edges

def _prop_success(G, src, dest):
  return random.random() <= G[src][dest]['act_prob']








"""
Created on Fri Dec 29 14:42:03 2017

@author: Furkan Gursoy (http://furkangursoy.github.io)
"""

# BEGIN APPLICATION
import datetime
import pickle

#inputs
r = 20 #number of cascades to be started from each node
edgelist = "email_edgeweight.txt" #the input graph file with edge weights
cascadefilename = 'cascades_email' #name of the file for storing output cascades

print("begin_app", datetime.datetime.now().time())
G=nx.read_edgelist(edgelist, data=(('act_prob',float),), encoding='utf-8', nodetype=int) #generate graph from edge lis
#G = max(nx.connected_component_subgraphs(G), key=len) #get the largest connected component
n = nx.number_of_nodes(G)

  # change to directed graph
if not G.is_directed():
   DG = G.to_directed()
else:
   DG = copy.deepcopy(G)
G=DG
#############################################
    
cascades = [] #an empty list for storing cascades

print("begin_IC", datetime.datetime.now().time()) 

for i in range(n): #generate r cascades for each node and append to the cascade list
    for j in range (r):
        cascades.append(independent_cascade(G, [i]))
        
print("end_IC", datetime.datetime.now().time())


with open(cascadefilename, 'wb') as fp: #save the cascades to a file. this file will be used by Prediction.py
    pickle.dump(cascades, fp)
    

