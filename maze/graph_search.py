import random
from SearchNode import SearchNode
from State import MazeState

#==============================================================================
# GRAPH_SEARCH
#
# The fringe and closed list must be drawn while the thinking takes place.
# - Draw the closed list blue (255, 0, 0).
# - Draw the fringe in green (0, 255, 0).
#
# There must be NO console printing in this python file. Make sure you remove
# them or comment them out when you are done.
#==============================================================================
def graph_search(problem=None,
                 Node=None,
                 fringe=None,
                 closed_list=None,
                 view0=None,
                 ):
    maze = problem.maze

    #==========================================================================
    # TODO: The code here creates a *random* solution starting at state (0,0).
    # Replace with the correct late version of graph search algorithm.
    #==========================================================================
    solution = []
    while 1:
        while len(fringe) > 0:
            #print fringe
            #stop = raw_input("Enter to continue")
            for state in fringe:
                if state.state != Node.state and not(problem.is_dangerous(state.state)):
                    view0['maze'].background[state.state] = (0,0,255) # color it blue
            for state in closed_list.values():
                if state != Node.state and not(problem.is_dangerous(state)):
                    view0['maze'].background[state] = (255,0,0) # color it red 
            for state in problem.dangerous_rooms:
                if state != Node.state:
                    view0['maze'].background[state] = (255,255,0) # color it yellow 
            view0.run()

            s = fringe.get()
            view0['maze'].background[s.state] = (0,255,0) # color it green 
            view0.run()
            
            if problem.goal_test(s.state):
                view0['maze'].background[s.state] = (0,255,0) # color it green
                view0.run()
                while s.parent != None:
                    solution.append(s.parent_action)
                    s = s.parent
                solution.reverse()
                return solution
            else:
                closed_list.add(s.state)
                dirs = maze.get_directions(s.state)
                if dirs != []:
                    for d in dirs:
                        (r, c) = maze.get_adj_tuple(s.state, d)
                        s0 = (r, c)
                        if not(s0 in fringe) and not(s0 in closed_list):
                            fringe.put(SearchNode(s0, s, d, problem.get_cost(s0, s))) #send state and parent node
                        
            


        #======================================================================
        # TODO: The following randomly colors the maze cells with red and blue.
        # Replace with the following:
        # - Iterate through the fringe and color the states of the search
        #   nodes with blue
        # - Iterate through the closed list and color the states with red
	    # - Color the initial state green
        #======================================================================
             # Draw everything
        
    return None # None is used to indicate no solution
