## The path to the synchronous parallel RNS

### Node

* set and append methods of the node also invokes Host.push_set() and Host.push_append respectively, which pushes changes to into the host bus if any.



### Host

Previous version of Host was interacting with nodes (altering, adding, exec)  via node index. In multi-process app each host contains its own nodes, which are the parts of the whole network held by the RNS. This is why, from now one can't traverse nodes like

```python
for node_index in range(self.size):
    ...
```

From the other hand, rewiring network builders and local stages will take a bunch of time. 

* We definitely need the global indexing. 

Because in that case there is no need to re-index nodes in the host after splitting it so parallel hosts, and no need to re-index nodes at the master process when sending signals from one host to another. I see two ways of implementing this:

* Still index nodes, but Host._nodes is now a dict, not the list.

This requires some changes in traversing nodes, basically, not using range(self.size) and similar approaches.

* Set and get



##### Problem with apply() and check_connectivity()

There is several functions which is applied to the whole network (so can run beyond a single host process):

* copy
* get_node[s]
* add_node[s]
* connect
* check_connectivity
* filter
* hist_values

First of all, the nodes itself doesn't interact with the host except sending signals and mirroring its own data. It isn't expected for nodes to reconnect. It's also not expected for network to change its structure during the parallel execution. This is why, add_node(), connect(), check_connectivity() and other methods are expected to be used before splitting the host into parallel hosts. Which doesn't mean that we wouldn't want to implement such features.

But apply(), filter() and hist_values() are still needed features (for instance, to monitor metrics). How shall it work?

Well, first one need to mention, that process hosts (unlike the master host) aren't expected to run Stages. [From the other hand, I see probability of such a horizontal relations between nodes, this is why I would like to implement 'p2p hosts' in later versions]. This is why, there is no need to implement these functions at process hosts [at least, for now]. 

* Processing hosts doesn't run Stages, do it don't need consistent apply() and etc
* There is no problem to extend the architecture up to MapReduce. Distribute inputs section of the Processing Host can not only split input signals to data alteration and signal stacking, but can also divert some packages and process it somehow (due to equity between all modules all this functions are always accessible for all processing hosts instances)

Well, apply, filter and hist_values() interacts with Node._data only, which is mirrored. This is why, re-implementation will include rewriting these parts.

* The 'mirror database' can look right the same as the usual nodes, but with using the Node class. The Node can be a little bit modified to hold it's own full functionality (included reverse-mirroring)
* NodeDoll (NodeGhost) will have an empty exec() and can't send messages, but getters and setters works similar way: it passes written data to the master bus. Mirroring doll nodes sends #set, #set_last and #append messages with the same alias as the real nodes (#terminate, for instance). So if reverse-mirroring is enabled, these nodes sends the instructions to corresponding real node as it would be themselves.

Attention: to hold database consistency, if reverse-mirroring is enabled, one have to launch Stages not simultaneously with Processing Hosts, but after it.





Solution?

* Master host
* Process host
* 

### Master

