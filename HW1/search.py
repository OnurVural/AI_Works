# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    lifo = Stack()
    visitedNodes = []
    
    # We are already in the goal state, no path required
    if problem.isGoalState(problem.getStartState()):    
        return []

    # First, add the initial state in the fringe structure with an empty path value
    lifo.push((problem.getStartState(), []))

    # While our fringe has item(s), proceed in adding the successor nodes of the first reachable item
    while not lifo.isEmpty():
        visitedNode, path = lifo.pop()
        # select the first item and mark it as visited
        if visitedNode not in visitedNodes:
            visitedNodes.append(visitedNode)

            # if the item corresponds to desired state we return
            if problem.isGoalState(visitedNode):
                return path
            
            # obtain the successor states of our node
            successors = problem.getSuccessors(visitedNode)

            # for each successor, calculate the path and add into fringe structure
            for connectedNodes, alternativePath, cost in successors:
                # get the previous path
                newPath = path.copy()
                # add the new path value
                newPath.append(alternativePath)
                # add the node to the fringe
                lifo.push((connectedNodes, newPath))
    util.raiseNotDefined()
    
def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    fifo = Queue()
    visitedNodes = []
    
    # We are already in the goal state, no path required
    if problem.isGoalState(problem.getStartState()):    
        return []
    # First, add the initial state in the fringe structure with an empty path value
    fifo.push((problem.getStartState(), []))

    # While our fringe has item(s), proceed in adding the successor nodes of the first reachable item
    while not fifo.isEmpty():
        visitedNode, path = fifo.pop()
        # select the first item and mark it as visited
        if visitedNode not in visitedNodes:
            visitedNodes.append(visitedNode)
            # if the item corresponds to desired state we return
            if problem.isGoalState(visitedNode):
                return path
            
            # obtain the successor states of our node
            successors = problem.getSuccessors(visitedNode)

            # for each successor, calculate the path and add into fringe structure
            for connectedNodes, alternativePath, cost in successors:
                # get the previous path
                newPath = path.copy()
                # add the new path value
                newPath.append(alternativePath)
                # add the node to the fringe
                fifo.push((connectedNodes, newPath))
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # This time we need to use a priority queue
    from util import PriorityQueue
    pq = PriorityQueue()
    visitedNodes = []
    
    # We are already in the goal state, no path required
    if problem.isGoalState(problem.getStartState()):    
        return []

    # First, add the initial state in the fringe structure with an empty path value, 0 priority value
    # Priority is needed in triple structure since priority queue itself does not allow us to learn the priority cost val of a specific item
    pq.push((problem.getStartState(), [], 0), 0)

    # While our fringe has item(s), proceed in adding the successor nodes of the lowest cost item
    while not pq.isEmpty():
        # select the first item and mark it as visited
        visitedNode, path, formerCost = pq.pop()
        if visitedNode not in visitedNodes:
            visitedNodes.append(visitedNode)
            # if the item corresponds to desired state we return
            if problem.isGoalState(visitedNode):
                return path
            # for each successor, calculate the path, cost and add into fringe structure
            for connectedNodes, alternativePath, cost in problem.getSuccessors(visitedNode):
                # get the previous path
                newPath = path.copy()
                # add the new path value
                newPath.append(alternativePath)
                # compute the cummulative cost for the current node to be added to the fringe
                cumulativeCost = formerCost + cost
                # add the structure to the fringe
                pq.push((connectedNodes, newPath, cumulativeCost), cumulativeCost)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # We need to use a priority queue
    from util import PriorityQueue
    pq = PriorityQueue()
    visitedNodes = []
    
    # We are already in the goal state, no path required
    if problem.isGoalState(problem.getStartState()):    
        return []

    # First, add the initial state in the fringe structure with an empty path value, 0 priority value
    # Priority is needed in triple structure since priority queue itself does not allow us to learn the priority cost val of a specific item
    pq.push((problem.getStartState(), [], 0), 0)

    # While our fringe has item(s), proceed in adding the successor nodes of the lowest cost item
    while not pq.isEmpty():
        # select the first item and mark it as visited
        visitedNode, path, formerCost = pq.pop()
        if visitedNode not in visitedNodes:
            visitedNodes.append(visitedNode)
            # if the item corresponds to desired state we return
            if problem.isGoalState(visitedNode):
                return path
            # for each successor, calculate the path, cost and add into fringe structure
            for connectedNodes, alternativePath, cost in problem.getSuccessors(visitedNode):
                # get the previous path
                newPath = path.copy()
                # add the new path value
                newPath.append(alternativePath)
                # compute the cummulative cost for the current node to be added to the fringe
                cumulativeCost = formerCost + cost 
                # this time we need to consider the heuristic value as well, but for specific node, not as a cumulative property
                pq.push((connectedNodes, newPath, cumulativeCost), cumulativeCost + heuristic(connectedNodes, problem))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
