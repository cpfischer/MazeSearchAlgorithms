"""
Fringe is the base class if fringe subclasses.
    - put, get
    - membership (i.e., __contains__)
    - find and update (later for search such as UCS and heuristic)
    - size
    - __len__ (similar to size)
    - __iter__ (for iteration in a for-loop. This is already done for you.)

A complete Stack and Queue class is provided. However membership check (i.e.
__contains__) is very slow. Therefore we have the following classes:

FSStack and FSQueue

A FSStack object contains a stack and a set. They contain the same values.
The set is used for find membership fast (with O(1) runtime). This is also
the same for FSQueue.
"""

import collections


class Fringe(object):
    def __init__(self):
        object.__init__(self)
    def put(self, x):
        raise NotImplementedError
    def get(self, x):
        raise NotImplementedError
    def __contains__(self):
        raise NotImplementedError
    def size(self):
        raise NotImplementedError
    def __len__(self):
        return 0 # Must be overwritten
    def __contains__(self, x):
        raise NotImplementedError
    def __iter__(self):
        raise NotImplementedError
 
    
class Stack(Fringe):
    def __init__(self):
        Fringe.__init__(self)
        self.deque = collections.deque()
    def put(self, node):
        if node.state not in [n.state for n in self.deque]:
            self.deque.append(node)
    def get(self):
        return self.deque.pop()
    def __len__(self):
        return len(self.deque)
    def size(self):
        return len(self.deque)
    def __contains__(self, node):
        for n in self.deque:
            if node.state == n.state:
                return True
        return False
    def __str__(self):
        s = str(self.deque)[7:-2]
        return '<Stack [%s]>' % s
    def __iter__(self):
        return iter(self.deque)

    
class Queue(Fringe):
    def __init__(self):
        Fringe.__init__(self)
        self.deque = collections.deque()
    def put(self, x):
        self.deque.append(x)
    def get(self):
        return self.deque.popleft()
    def __len__(self):
        return len(self.deque)
    def size(self):
        return len(self.deque)
    def __contains__(self, node):
        for n in self.deque:
            if node.state == n.state:
                return True
        return False
    def __str__(self):
        s = str(self.deque)[7:-2]
        return '<Queue [%s]>' % s
    def __iter__(self):
        return iter(self.deque)


class FSStack(Stack):
    def __init__(self):
        Stack.__init__(self)
        self.set = set()
    def __contains__(self, node):
        return node in self.set
    def put(self, node):
        self.deque.append(node)
        self.set.add(node.state)
    def add(self, n):
        pass
    def get(self):
        node =  self.deque.pop()
        self.set.remove(node.state)
        return node
    def remove(self, x):
        self.set.remove(x)

    
class FSQueue(Queue):
    def __init__(self):
        Queue.__init__(self)
        self.set = set()
    def put(self, x):
        self.deque.append(x)
        self.set.add(x.state)
    def get(self):
        node =  self.deque.popleft()
        self.set.remove(node.state)
        return node
    def __contains__(self, node):
        return node in self.set
    def __str__(self):
        s = ''
        for n in self.deque:
            s += '<' + str(n.state) + '>'
        s = s[:-1]
        return '<FSQueue [%s]>' % s
    def remove(self, x):
        self.set.remove(x)

class UCSFringe(Fringe):
    """
    This implements a unique fringe as a priority queue. If a search node n is
    inserted into this fringe (using the put method), node.priority() is
    executed for the priority of the node (which should return the path_cost
    of the node. If node.state does not appear in the fringe, the node
    joins the fringe. If another node n1 has the same state as n, then
    1. If n.priority() >= n1.priority(), n is rejected.
    2. If n.priority() < n1.priority(), then n1 is overwritten by n and
    n1 is heapify-up.
    """
    def __init__(self):
        Fringe.__init__(self)
        self.deque = collections.deque()
        self.set = {} # dictionary of (state, index)
    
    def getParent(self, index):
        return ((index - 1) / 2)

    def heapify(self):
        for i in range(len(self.deque)):
            self.addNewNode(i, self.deque[i])
        

    def addNewNode(self, index, node):
        parentIndex = self.getParent(index)
        if parentIndex < 0: return
        parentNode = self.deque[parentIndex]
        if node.priority() < parentNode.priority():
            self.set[node.state] = self.set.pop(parentNode.state)
            self.set[parentNode.state] = index
            self.deque[index] = parentNode
            self.deque[parentIndex] = node
            self.addNewNode(parentIndex, node)

    def put(self, newNode):
        if newNode.state in self.set:
            indexOfNode = self.set[newNode.state]
            if (newNode.priority() < self.deque[indexOfNode].priority()):
                oldNode = self.deque[indexOfNode]
                self.deque[indexOfNode] = newNode
                self.addNewNode(indexOfNode, newNode)
        else:
            self.deque.append(newNode)
            self.set[newNode.state] = len(self.deque) - 1
            self.addNewNode((len(self.deque) - 1), newNode)
    
    def add(self, node):
        pass

    def get(self):
        popNode = self.deque[0]
        lastNode = self.deque[-1]
        nodeReturned = popNode
        if popNode.priority() != lastNode.priority():
            self.deque[0] = lastNode
            self.deque[-1] = popNode
            nodeReturned = self.deque.pop()
        else:
            nodeReturned = self.deque.popleft()
        self.heapify()
        del self.set[nodeReturned.state]
        return nodeReturned
        
    def __len__(self):
        return len(self.deque)

    def size(self):
        return len(self.deque)

    def __contains__(self, node):
        return node in self.set

    def __str__(self):
        s = ''
        for n in self.deque:
            s += '<' + str(n.state) + ' ' + str(n.priority()) + '>'
        s = s[:-1]
        return '<UCSFringe [%s]>' % s

    def __iter__(self):
        return iter(self.deque)

class IDDFS(FSStack):
    def __init__(self, max_depth = 0, initial_node = None, closed_list = None):
        FSStack.__init__(self)
        self.depth_limit = 0
        self.max_depth = max_depth
        self.initial_node = initial_node
        self.view0 = None

    def put(self, node):
        if node.parent != None:
            parent_cost = node.parent.path_cost
            node.path_cost = parent_cost + 1
            if (node.path_cost <= self.depth_limit):
                self.deque.append(node)
                self.set.add(node.state)
        else:
            self.deque.append(node)
            self.set.add(node.state)

    def reset(self):
        if self.depth_limit < self.max_depth:
            for state in self.closed_list.values():
                if state != self.initial_node.state:
                    self.view0['maze'].background[state] = (0,0,0) # remove color
            self.closed_list.clear()
            self.depth_limit += 1
            self.put(self.initial_node)

    def get(self):
        node =  self.deque.pop()
        self.set.remove(node.state)
        if len(self) == 0:
            self.reset()
        return node


if __name__ == '__main__':
    from SearchNode import SearchNode
    print "Testing stackfringe with search nodes from (0,0) -> (1,0) -> (1,1) by actions ['E', 'S']"
    fringe = Stack()
    state00 = (0, 0)
    node00 = SearchNode(state00)
    state01 = (0, 1)
    node01 = SearchNode(state01, node00, 'E', 1)
    state11 = (1, 1)
    node11 = SearchNode(state11, node01, 'S', 1)
    print(node00)
    print(node01)
    print(node11)

    print(fringe)
    fringe.put(node00)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)
    
    print(fringe)
    fringe.put(node01)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)

    print(fringe)
    fringe.put(node11)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)

    print(fringe)
    n = fringe.get()
    print(n)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)

    print(fringe)
    n = fringe.get()
    print(n)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)
    
    print(fringe)
    n = fringe.get()
    print(n)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)

    print(fringe)
    try:    
        n = fringe.get()
        print(n)
    except IndexError:
        print("stack fringe is empty ... cannot get()")
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)
    
