# CRDT-Element-Graph  
#### _Python implementation_  

Conflict-Free Replicated Data Types (CRDTs) are data structures that power real-time collaborative applications in distributed systems. CRDTs can be replicated across systems, they can be updated independently and concurrently without coordination between the replicas, and it is always mathematically possible to resolve inconsistencies that might result.  


#### Implemented LWW-Element-Graph functionalities:  
● add a vertex/edge,  
● remove a vertex/edge,  
● check if a vertex is in the graph,  
● query for all vertices connected to a vertex,  
● find any path between two vertices  
● merge with concurrent changes from other graph/replica.  


Conflict Free Replicated Data Types (CRDTs) are data structures that power real time collaborative applications in
distributed systems. CRDTs can be replicated across systems, they can be updated independently and concurrently without
coordination between the replicas, and it is always mathematically possible to resolve inconsistencies which might result.




Ref:  
[CRDT Wiki](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type)  
[Reading materials github repo](https://github.com/pfrazee/crdt_notes)  
[Tech report](https://hal.inria.fr/inria-00555588/PDF/techreport.pdf)  


 
## Install

```
pip install -r requirements.txt
```

## Usage

- Create a new LWW_Graph instance  
```
graph = LWW_Graph()
```

- Add a new vertex  
```
graph.put_vertex('A')
```

- Remove vertex  
```
graph.remove_vertex('A')
```

- Get all vertices in Graph  
```
all_vertices = graph.get_vertices()
```

- Lookup vertex in Graph  
```
exists = graph.lookup_vertex('A')
```

- Get connected verices for a vertex  
```
connected_vertices = graph.get_connected_vertices('A')
```

- Add a new edge  
```
graph.put_vertex('A')
graph.put_vertex('B')
graph.put_edge('A', 'B')
```

- Remove edge  
```
graph.remove_edge('A', 'B')
```

- Lookup edge in Graph  
```
graph.lookup_edge('A', 'B')
```

- Find all paths between vertices  
```
all_paths = graph.find_paths('A', 'B')
```


## Test
After install run in terminal:  
```
pytest
```

or

```
python -m unittest discover
```


----

# Issues
- CRDT violation that causes data loss:  
    - Edges data are erased when the same vertex is added for the second time (after adding edges) in the same replica, and also when added to another replica before merge.
