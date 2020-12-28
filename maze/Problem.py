"""
MazeProblem is a subclass of Problem.The following methods of MazeProblem must tbe implemented:
- goal_test(self, state)
- actions(self, state)
- result(self, state, action)
- successors(self, state)
    
"""
import math

class Problem(object):

    def __init__(self,
                 initial_state):
        self.initial_state = initial_state
    
    def get_initial_state(self):
        return self.initial_state

    def goal_test(self, state):
        raise NotImplementedError
                 
    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def successors(self, state):
	raise NotImplementedError
    
    def cost(self, state, action):
        return 1


class MazeProblem(Problem):

    def __init__(self,
                 maze=None,
                 initial_state=None,
                 goal_states=None,
                 search=None,
                 dangerous_rooms={}):
        Problem.__init__(self, initial_state)
        self.maze = maze
        self.goal_states = goal_states
        self.dangerous_rooms = dangerous_rooms
        self.search = search
    def goal_test(self, state):
        #print "Goal test: state: " + str(state) + " Goal: " + str(self.goal_states)
        return state in self.goal_states

    def is_dangerous(self, state):
        return state in self.dangerous_rooms
    
    #Note: 1 is base cost to move from one node to another
    def get_cost(self, state, parent_node):
        if self.search == 'gbfs':
            dx = abs(state[0] - self.goal_states[0][0])
            dy = abs(state[1] - self.goal_states[0][1])
            if self.is_dangerous(state):
                danger_cost = 0
                if self.is_dangerous(state):
                    danger_cost = self.dangerous_rooms[state] 
                return float(danger_cost) + (1 * (math.sqrt(dx * dx + dy * dy)))
            else: 
                1 * (math.sqrt(dx * dx + dy * dy))
        elif self.search == 'A*':
            dx = abs(state[0] - self.goal_states[0][0])
            dy = abs(state[1] - self.goal_states[0][1])
            parent_cost = 0
            if parent_node != None:
                parent_cost = parent_node.path_cost
            danger_cost = 0
            if self.is_dangerous(state):
                    danger_cost = self.dangerous_rooms[state] 
            return float(danger_cost) + parent_cost + (1 * (math.sqrt(dx * dx + dy * dy)))
        else:
            return self.dangerous_rooms[state] if self.is_dangerous(state) else 0

    def actions(self, state):
        return self.maze.get_directions(state)

    def result(self, state, action):
        return self.maze.get_adj_tuple(state, action)

    def successors(self, state):
        dirs = self.actions(state)
        return [(d, self.result(state, d)) for d in dirs]

