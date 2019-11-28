__version__ = '0.1'
__date__ = '28-11-2019'
__author__ = 'Shervin Azadi'

node = hou.pwd()
geo = node.geometry()
import networkx as nx

#initiate the graph
G = nx.Graph()

#iterate over the points and add them as nodes of the graph
for point in geo.points():
    #retrieve the point number
    id = point.number()
    #add the node
    G.add_node(id)

#iterate over the prims and add them as edges of the graph
for prim in geo.prims():
    #retrieve the prim number
    id = prim.number()
    #getting the list of the points
    pnts = prim.points()
    #add the edge
    G.add_edge(pnts[0].number(),pnts[1].number())

#retrieve the start and end point number
start = hou.evalParm("start")
end = hou.evalParm("end")

#find the shortest path using A-star algorithm
path_nodeid = nx.astar_path(G, start, end)
#retrieve the point object given the point number
path_points = [geo.points()[id] for id in path_nodeid]
#group the points that are in the path
path_group = geo.createPointGroup('path')
path_group.add(path_points)