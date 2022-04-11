#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 02:22:39 2022

@author: serdarjan1995

Graph data structure python implementation

dictionary containing keys will be vertex and value will contain edges
connected to that vertex

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C'],
    'E': []
}

LWW requires timestamp to be attached, ideally now keys will contain
data structure like
VERTEX: {
      't': 'timestamp_of_VERTEX'
      'edges': {
          'VERTEX_X': 'timestamp_of_edge_VERTEX_X',
          'VERTEX_Y': 'timestamp_of_edge_VERTEX_Y'
      }
}

"""
import time


class LWW_Graph:
    def __init__(self, name: str = None):
        self.name = name or 'LWW-Element-Graph'
        self.add_set: dict = dict()
        self.remove_set: dict = dict()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
    
    def lookup_vertex(self, v_name: str):
        """ returns true if vertex is in the graph """
        if v_name not in self.add_set.keys():
            # vertex not in the graph
            return False
        
        if v_name not in self.remove_set.keys():
            # vertex is in the graph and not in remove set
            return True
        else:
            t_add = self.add_set[v_name]['t']
            t_remove = self.remove_set[v_name]['t']
            return t_add > t_remove
    
    def _check_edge_exists(self, v_name_1: str, v_name_2: str):
        """ returns true if edge is not in the remove_set or timestamp in remove_set
        less than timestamp in add_set
        """
        # check v_name_2 is connected to v_name_1
        if v_name_2 not in self.add_set[v_name_1]['edges'].keys():
            return False
        
        if v_name_1 in self.remove_set and v_name_2 in self.remove_set[v_name_1]['edges'].keys():
            t_add = self.remove_set[v_name_1]['edges'][v_name_2]
            t_remove = self.remove_set[v_name_1]['edges'][v_name_2]
            return t_add > t_remove
        
        # not in remove set
        return True
    
    def lookup_edge(self, v_name_1: str, v_name_2: str):
        """ returns true if edge is in the graph"""
        if not self.lookup_vertex(v_name_1):
            # vertex v_name_1 is deleted
            return False
        
        if not self.lookup_vertex(v_name_2):
            # vertex v_name_2 is deleted
            return False
        
        # check edge is not in remove_set
        return self._check_edge_exists(v_name_1, v_name_2) and self._check_edge_exists(v_name_2, v_name_1)
    
    def put_vertex(self, v_name: str):
        """ adds a new vertex into the graph """
        timestamp = time.time_ns()
        vertex = {
            v_name: {
                "t": timestamp,
                "edges": dict()
            }
        }
        self.add_set.update(vertex)
    
    def remove_vertex(self, v_name: str):
        """ removes a vertex from the graph """
        if not self.lookup_vertex(v_name):
            # vertex v_name is already deleted
            return False
            
        vertex = {
            v_name: {
                **self.add_set[v_name],
                "t": time.time_ns(),
            }
        }
        self.remove_set.update(vertex)
    
    def get_vertices(self):
        """ returns all vertices that are in Graph """
        return [v for v in self.add_set.keys() if self.lookup_vertex(v)]

    def put_edge(self, v_name_1: str, v_name_2: str):
        """ adds an edge to the graph """
        assert self.lookup_vertex(v_name_1), f"There is no vertex {v_name_1}"
        assert self.lookup_vertex(v_name_2), f"There is no vertex {v_name_2}"
        
        timestamp = time.time_ns()
        self.add_set[v_name_1]['edges'].update({
            v_name_2: timestamp
        })
        
        self.add_set[v_name_2]['edges'].update({
            v_name_1: timestamp
        })
    
    def remove_edge(self, v_name_1: str, v_name_2: str):
        """ removes an edge from the graph """
        if not self.lookup_edge(v_name_1, v_name_2):
            # edge is already deleted
            return False
        
        timestamp = time.time_ns()
        if v_name_1 not in self.remove_set.keys():
            self.remove_set[v_name_1] = {
                't': -1,
                'edges': dict()
            }
        
        self.remove_set[v_name_1]['edges'].update({
            v_name_2: timestamp
        })
        
        if v_name_2 not in self.remove_set.keys():
            self.remove_set[v_name_2] = {
                't': -1,
                'edges': dict()
            }
        
        self.remove_set[v_name_2]['edges'].update({
            v_name_1: timestamp
        })
    
    def get_connected_vertices(self, v_name: str):
        """ returns all connected vertices for v_name """
        assert self.lookup_vertex(v_name), f"There is no vertex {v_name}"
        
        return [v for v in self.add_set[v_name]['edges'].keys() 
                if self.lookup_edge(v_name, v)]
    
    def find_paths(self, v_name_1: str, v_name_2: str, current_path=[]):
        """ returns all path available from v_name_1 to v_name_2 """
        assert self.lookup_vertex(v_name_1), f"There is no vertex {v_name_1}"
        assert self.lookup_vertex(v_name_2), f"There is no vertex {v_name_2}"
        
        current_path = current_path + [v_name_1]   # use __add__ not __iadd__ 
        if v_name_1 == v_name_2:
            # final path
            return [current_path]
        
        all_paths = []
        for node in self.get_connected_vertices(v_name_1):
            if node not in current_path:
                new_paths = self.find_paths(node, v_name_2, current_path)
                for path in new_paths:
                    all_paths.append(path)
        return all_paths

    def _merge_edges(self, edges1, edges2):
        """ returns merged edges for given two sets """
        merged = {}
        for e in set(list(edges1.keys()) + list(edges2.keys())):
            if e in edges1 and e in edges2:
                merged.update({
                    e: edges1[e] if edges1[e] >= edges2[e] else edges2[e]
                })
            elif e in edges1:
                merged.update({
                    e: edges1[e]
                })
            else:
                merged.update({
                    e: edges2[e]
                })
        return merged
    
    def _merge_vertices(self, set1, set2, v):
        """ returns merged vertices with the merged edges belong to vertex """
        new_set = {}
        if v in set1 and v in set2:
            if set1[v]['t'] > set2[v]['t']:
                # deep copy vertex from set1
                new_set.update({
                    v: set1[v]
                })
            elif set1[v]['t'] < set2[v]['t']:
                # deep copy vertex from set2
                new_set.update({
                    v: set2[v]
                })
            else:
                # compare edges and merge if timestamps are equal
                new_set.update({
                    v: {
                        't': set1[v]['t'],
                        'edges': self._merge_edges(set1[v]['edges'],
                                                   set2[v]['edges'])
                    }
                })
                            
        elif v in set1:
            new_set.update({
                v: set1[v]
            })
        elif v in set2:
            new_set.update({
                v: set2[v]
            })
        return new_set
            
    def __add__(self, other):
        """ LWW_Graph merge func.
        This is python's magic func makes ease of use LWW_Graph + LWW_Graph
        """
        new_graph = LWW_Graph()
        self_add_vertices = list(self.add_set.keys())
        other_add_vertices = list(other.add_set.keys())
        for v in set(self_add_vertices + other_add_vertices):
            new_graph.add_set.update(self._merge_vertices(self.add_set, other.add_set, v))
            new_graph.remove_set.update(self._merge_vertices(self.remove_set, other.remove_set, v))
        return new_graph



def fibb(n):
    if n <=1 :
        return 1
    else:
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a+b

print(list(fibb(7)))


def fib(n):
    if n <=1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
    

print(fib(7))
    
    