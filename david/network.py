"""Implementation of the Kademlia peer-to-peer (p2p) network protocol.

The Kademlia protocol consists of a Distributed Hash Table (DHT) which is used
to quick and efficiently located nodes that are "closest" to the current node.

A parameter called the replication factor (k) is used to determine the number
of nodes in the network. For example a network with a k value of 4 can have a
total of 2**k nodes, numbering from 0 to 2**k-1.

For example, see the binary tree below where k=2 and each edge of the tree
consists of a 0 or 1.

There is a total of 2**2 (8) nodes.


                     N1                ---> Root node

                0/        \1           ---> each edge has a value of 0 or 1

             N2             N3

          0/    \1       0/    \1

        L1        L2   L3        L4    ---> Leaf (peer) nodes

       (00)      (01) (10)      (11)   ---> put the edge values together


Each peer (i.e. node) of the p2p network is assigned a random node id or a key
shown in binary parenthesis above ranging from 0 to 2**k-1.

Each leaf node has a reference to at least one other leaf node in its subtree,
but at most k-1 nodes total if all the node ids are occupied.

The XOR bitwise operator is used to establish a "distance" between the peer
nodes. The closet nodes are returned on lookup. See example below of 3 XOR 5
which gives 6.

                    0011    (3 in binary)
                XOR 0101    (5 in binary)
                    ----
                    0110    (if the bits are different then a 1 else a 0)
"""

import socket

import socketserver
from socketserver import StreamRequestHandler


class DHTHandler(StreamRequestHandler):
    pass


if __name__ == "__main__":
    print("Hello World!")
