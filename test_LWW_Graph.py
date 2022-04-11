#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 22:02:26 2022

@author: serdarjan1995
"""

from unittest import TestCase
from .LWW_Graph import LWW_Graph
import copy


class LWWGraphTest(TestCase):

    def setUp(self):
        self.graph = LWW_Graph()
    
    def test_add_vertex(self):
        """ test if vertex was added to the graph """
        vertex = 'A'
        self.graph.put_vertex(vertex)
        self.assertTrue(self.graph.lookup_vertex(vertex))
        self.assertTrue(vertex in self.graph.add_set.keys())
    
    def test_vertex_lookup(self):
        """ test non existing vertex lookup """
        vertex = 'X'
        self.assertFalse(self.graph.lookup_vertex(vertex))
        self.assertTrue(vertex not in self.graph.add_set.keys())
        self.assertTrue(vertex not in self.graph.remove_set.keys())
    
    def test_vertex_add_and_delete(self):
        """ test add and delete vertex """
        vertex = 'B'
        self.graph.put_vertex(vertex)
        self.assertTrue(self.graph.lookup_vertex(vertex))
        self.assertTrue(vertex in self.graph.add_set.keys())
        
        self.graph.remove_vertex(vertex)
        self.assertFalse(self.graph.lookup_vertex(vertex))
        self.assertTrue(vertex in self.graph.remove_set.keys())
        
        self.assertLess(self.graph.add_set[vertex]['t'], self.graph.remove_set[vertex]['t'])
    
    def test_vertex_add_deleted_vertex(self):
        """ test add deleted vertex again"""
        self.test_vertex_add_and_delete()  # add and then delete vertex
        vertex = 'B'
        self.graph.put_vertex(vertex)
        self.assertTrue(self.graph.lookup_vertex(vertex))
        
        self.assertGreater(self.graph.add_set[vertex]['t'], self.graph.remove_set[vertex]['t'])
    
    def test_vertex_duplicate_add(self):
        """ test duplicate add """
        vertex = 'B'
        self.graph.put_vertex(vertex)
        self.graph.put_vertex(vertex)
        self.assertTrue(self.graph.lookup_vertex(vertex))
    
    def test_get_all_vertices(self):
        """ test get all vertices """
        self.graph.put_vertex('A')
        self.graph.put_vertex('B')
        self.graph.put_vertex('C')
        self.graph.put_vertex('D')
        self.assertEqual(sorted(self.graph.get_vertices()), sorted(['A', 'B', 'C', 'D']))
        self.graph.remove_vertex('C')
        self.assertEqual(sorted(self.graph.get_vertices()), sorted(['A', 'B', 'D']))
    
    def test_add_edges(self):
        """ test add edges """
        v1 = 'A'
        v2 = 'B'
        self.graph.put_vertex(v1)
        self.graph.put_vertex(v2)
        self.assertFalse(self.graph.lookup_edge(v1, v2))
        self.graph.put_edge(v1, v2)
        self.assertTrue(self.graph.lookup_edge(v1, v2))
    
    def test_delete_edges(self):
        """ test delete edges """
        self.test_add_edges()  # add edges
        self.graph.remove_edge('A', 'B')
        self.assertFalse(self.graph.lookup_edge('A', 'B'))
    
    def test_graph_multiple_edges(self):
        """ test multiple vertex connections """
        self.graph.put_vertex('A')
        self.graph.put_vertex('B')
        self.graph.put_vertex('C')
        self.graph.put_vertex('D')
        self.graph.put_vertex('E')
        self.graph.put_vertex('F')
        self.graph.put_vertex('G')
        self.graph.put_vertex('H')
        self.graph.put_vertex('I')
        
        self.graph.put_edge('A', 'B')
        self.graph.put_edge('A', 'G')
        self.graph.put_edge('B', 'C')
        self.graph.put_edge('B', 'D')
        self.graph.put_edge('B', 'F')
        self.graph.put_edge('G', 'E')
        self.graph.put_edge('G', 'H')
        self.graph.put_edge('D', 'E')
        self.graph.put_edge('F', 'E')
        self.graph.put_edge('G', 'E')
        self.graph.put_edge('E', 'H')
        
        self.assertTrue(sorted(self.graph.get_connected_vertices('A')) == sorted(['B', 'G']))
        self.assertTrue(sorted(self.graph.get_connected_vertices('B')) == sorted(['A', 'C', 'D', 'F']))
        self.assertTrue(sorted(self.graph.get_connected_vertices('C')) == sorted(['B']))
        self.assertTrue(sorted(self.graph.get_connected_vertices('D')) == sorted(['B', 'E']))
        self.assertTrue(sorted(self.graph.get_connected_vertices('E')) == sorted(['G', 'D', 'F', 'H']))
        self.assertTrue(sorted(self.graph.get_connected_vertices('F')) == sorted(['B', 'E']))
        self.assertTrue(sorted(self.graph.get_connected_vertices('G')) == sorted(['A', 'E', 'H']))
        self.assertTrue(sorted(self.graph.get_connected_vertices('H')) == sorted(['G', 'E']))
        self.assertTrue(sorted(self.graph.get_connected_vertices('I')) == [])
        
    def test_graph_find_paths(self):
        """ test graph find paths """
        self.test_graph_multiple_edges()  # put all test vertexes and edges
        correct_paths = [
            ['G', 'A', 'B'],
            ['G', 'E', 'D', 'B'],
            ['G', 'E', 'F', 'B'],
            ['G', 'H', 'E', 'D', 'B'],
            ['G', 'H', 'E', 'F', 'B']
        ]
        self.assertTrue(self.graph.find_paths('G', 'B') == correct_paths)
    
    def test_graph_merge(self):
        """ test graph find paths """
        self.test_graph_multiple_edges()  # put all test vertexes and edges
        
        # concurrent changes replica graph
        graph2 = copy.deepcopy(self.graph)
        graph2.put_vertex('K')
        graph2.put_edge('K', 'D')
        graph2.put_edge('K', 'A')
        graph2.remove_edge('F', 'B')
        
        # concurrent changes in self
        self.graph.put_vertex('M')
        self.graph.put_edge('M', 'A')
        self.graph.put_edge('M', 'B')
        self.graph.remove_edge('G', 'H')
        self.graph.remove_edge('E', 'F')

        # merge graphs
        graph_merged = self.graph + graph2
        
        self.assertTrue(sorted(graph_merged.get_connected_vertices('A')) == sorted(['M', 'K', 'G', 'B']))
        self.assertTrue(sorted(graph_merged.get_connected_vertices('B')) == sorted(['C', 'D', 'A', 'M']))
        self.assertTrue(sorted(graph_merged.get_connected_vertices('C')) == sorted(['B']))
        self.assertTrue(sorted(graph_merged.get_connected_vertices('D')) == sorted(['E', 'K', 'B']))
        self.assertTrue(sorted(graph_merged.get_connected_vertices('E')) == sorted(['H', 'G', 'D']))
        self.assertTrue(sorted(graph_merged.get_connected_vertices('F')) == [])
        self.assertTrue(sorted(graph_merged.get_connected_vertices('G')) == sorted(['E', 'A']))
        self.assertTrue(sorted(graph_merged.get_connected_vertices('H')) == ['E'])
        self.assertTrue(sorted(graph_merged.get_connected_vertices('I')) == [])
        self.assertTrue(sorted(graph_merged.get_connected_vertices('K')) == sorted(['D', 'A']))
        self.assertTrue(sorted(graph_merged.get_connected_vertices('M')) == sorted(['A', 'B']))
        
        # test paths
        correct_paths_self = [
            ['G', 'A', 'B'],
            ['G', 'A', 'M', 'B'],
            ['G', 'E', 'D', 'B']
        ]
        self.assertTrue(sorted(self.graph.find_paths('G', 'B')) == sorted(correct_paths_self))
        
        correct_paths_graph2 = [
            ['G', 'A', 'B'],
            ['G', 'A', 'K', 'D', 'B'],
            ['G', 'E', 'D', 'B'],
            ['G', 'E', 'D', 'K', 'A', 'B'],
            ['G', 'H', 'E', 'D', 'B'],
            ['G', 'H', 'E', 'D', 'K', 'A', 'B']
        ]
        self.assertTrue(sorted(graph2.find_paths('G', 'B')) == sorted(correct_paths_graph2))
        
        correct_paths_merged = [
            ['G', 'E', 'D', 'K', 'A', 'M', 'B'],
            ['G', 'E', 'D', 'K', 'A', 'B'],
            ['G', 'E', 'D', 'B'],
            ['G', 'A', 'M', 'B'],
            ['G', 'A', 'K', 'D', 'B'],
            ['G', 'A', 'B'],
        ]
        self.assertTrue(sorted(graph_merged.find_paths('G', 'B')) == sorted(correct_paths_merged))
