#### Asynchronous execution problems

##### **PROBLEM: Node process starts before processing of all its neighbors.**

If the net is calculated in parallel, there is possibility, that some nodes will be pushed to exec() with empty input buffer.

As the consequence

1. The problem is semi-fixed a bit via shuffling the exec() order: There is still an average outstripping, but no nodes are prioritized
2. Looks like the problem can't be completely fixed due the essentially asynchronous way of execution
3. Can be fixed by splitting signalling and input processing and synchronizing it. This way is implemented in StageExecSync method (but needs some proper redesign), so to make nodes simultaneously receive, and then, simultaneously receive and process
4. [+] Another way of solution is tracking down how many times Node.exec() of the node is launched with an empty input buffer, and if too many, switch the note to 'idle' state, in which the node receives buffer but sends only zero signals (to wake up neighbor nodes from their possible 'idle' state,  which tells the node that at least one of its neighbors was already calculated)
  1. One can improve this algorithm. by broadcasting TransactionCalculated() or even sending a zero signals to all node's neighbors. When there would be enough of these signals (or the nonzero 'wealth transaction' signals), the node 'wakes up' and sends nonzero signal to the decided node and zero signals to all other 'not-preferred' nodes.
  2. [-] The problem is overloading the input stacks by broadcasting (this also requires additional input processing to count broadcasts)
  3. [-] Since the node is executed much more times than it's really ready to 'wake up', there is a lot of CPU time goes for doing nothing useful, but skipping ordinary exec()
  4. [-] There is some possibility of deadlock                    
        1. [+] Easy to solve by dropping all 'idle' states back to 'normal' at the end of traversing all nodes in its execution thread.
  5. ​	[+] But this indeed shall prevent nodes from premature-execution



Found the following solution. Far from being perfect, but still should work out:

1. Execution process is split into two phases:
	1. **Exec**. Income processing and exec()
		1. Collect all *set()* operations from outside of the node and update the inner database
		2. Collects all input signals from the input stack
		3. "The exec() itself" - operate on node's database and prepare all output signals into the output stack.
	2. **Return**. Send all set() operations done at the previous stage to the Host.
		* node-executing process (**NXProc**) requests all those set queries from each of it's nodes
		* NXProc sends those queries to the host-process (**HProc**) which holds the mirror database of all nodes. The latter exists to provide immediate get() operation for the processing stages (which runs separately and independently of NXProcs)
		* NXProc also sends the output signals.
2. At first, NXProc operates the Exec phase for each of it's node (in some order). At last, NXProc operates the Return phase.
3. If this two processes are synchronized for all NXProcs, meaning: at first all Exec of all processes are finished, at last all the Returns are finished, then it's the synchronous execution.
4. If this stages are not synced between processes, then, at least, it is possible to obtain "some level of synchronization" when the nodes gets signals from other NXPs with some delay (dependent on relation between execution speed and a mutual "phase shift")

**PROBLEM: Some colors are used much frequently the the others**

At the moment, the execution thread traverse nodes under its supervision and calls its *exec()* functions. Coloring of the network guarantees that all nodes of the same color can be executed in any order without affecting on each other (straightly). 

But, in practice, some colors are spread a lot whereas some of them is used only by a few nodes.

Applying asynchronous execution leads to 'overactivity' of such nodes of rare color (resources of the PC is divided approximately the same way for all threads).

1. The easiest way of solution is joining some colors together and passing to a common thread (but the nodes in it are executed in a specific sequence).
2. Another way is freezing overactivated threads.
	1. This requires collecting the calculation dynamics.
	2. But also this lets to balance PC's computation resources.
3. The simplest way is setting thread priority based on number of nodes in the thread. Can be done even before the launch, but will fail if the network is heterogenous.
4. Another way of regulation node's activity is bottlenecking the signal transmission mechanisms of such nodes.

#### **PROBLEM: Using queues**

According to https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue, Python starts a dedicated process for each queue to transmit data between synced processes. If to use four queues (as supposed at the first revision of RNSv2), this will raise at least five processes for each processing core (NXProc). Slowdown might be expected.

It is important not to cross input and output data, in other case, one have to overcomplicate data transmission code.

One can decrease the number of queues by unifying the input data queue with the input signal queue, and the output data queue with the output signal queue. This isn't changing things much since passing signals and data in the same direction (input nor output) is done at the same phase (simultaneously).

Unifying these two queues might be more problematic. The reason is that the A phase includes both reading data/signals from queues and execution the nodes. The latter leads to appending data to the output queues immediately. This can lead to crossing over the output data/signals with the old data/signals not yet read. 

From the other hand, data queries is not processed by the exec. Furthermore, it is fully processed right before the execution. This is why, at the A phase, when exec() starts the data queries is already extracted from the queue. So only the input signals can cross over with output signals.

To resolve this, one can demand to read all input signals right after the exec starts and put it to internal (local) buffer of the exec() function.

As the result, when any new data updates or signals will be passed to the queue, all previous input data updates and signals are already been read and extracted.

Since data transmission and signal transmission isn't done in parallel, there is no real need in splitting data and signal buses: it will be processed sequentially in a single thread. It might look that unification of the buses of different kind will overcomplicate dataflow process. But data updates can be encapsulated in the same form as signals: to specific signal classes and already comes in within a random order.

Since all process are connected only to it's host, one can use python's Pipe object instead of Queue. Using JoinableQueue might simplify syncing process, but since not all nodes are passed to each process (NXProc), the process can execute only it's own instructions and process only it's own nodes. This is why using Pipe as the data/signal bus and Event for syncing phases is more preferred.

Nodes aren't expected to read other node's states. The mirror database works one way and used by Stages launched by the master process. Mirror database can be changed by the Stages, but these changes remain at the mirror without affecting node's regular work. From the other hand, it's not complicated to add the ability to 're-mirror' changes from master database back to nodes.  Just for flexibility. This option is to be turned on manually (disabled by default), since it's idling will slow down master signal handling.

In short, the solution is as follows:

* Use Event object to sync phases of all processes.
* Use Pipe to transmit data and signals
* Use the same pipe for transmission signals from master process to hosts and vice versa.

