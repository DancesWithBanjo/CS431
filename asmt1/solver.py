import heapq
from pprint import pprint
import math

def solve(puzzle):
    """
    This function takes in a 2D-list representing a sliding puzzle
    and finds a solution with the fewest number of moves

    @params puzzle: the puzzle to solve
    """
    open_list = []
    closed_list = set()
    moves = []
    start = State(puzzle, None, None)
    dist_to_goal = start.heuristic()
    # Check if puzzle is solvable
    if not solvable(start.puz): return None
    # Add the given puzzle to the search list
    heapq.heappush(open_list, start)
    a=0
    # while (dist_to_goal != 0) and (a != 10):
    while (dist_to_goal != 0):
        a+=1
        active = heapq.heappop(open_list)
        dist_to_goal = active.heuristic()
        # if active state has already been checked, restart loop
        if active in closed_list: continue
        # check if active is the goal state
        if active.is_goal():
            # Build the end list
            while active.previous is not None:
                moves.insert(0, active.move)
                active = active.previous
            return moves
        # Find next possible moves
        for x in active.make_adj_states():
            if x not in closed_list:
                heapq.heappush(open_list, x)
        closed_list.add(active)
    return moves

def solvable(puzzle):
    """
    Checks if a puzzle is solvable

    @params puzzle: the 2D puzzle to check for solvability
    """
    gap = find_gap(puzzle)
    zrow = gap[0]
    width = len(puzzle)+1
    gap_sub_len = len(puzzle[0]) - zrow
    flatlist = flatten(puzzle)
    flatlist.remove(0)
    inv_count = InversionsCount(flatlist)
    inv_and_gap = gap_sub_len + inv_count
    if width % 2 != 0 and inv_count % 2 == 0:
        return True
    elif width % 2 == 0 and inv_and_gap % 2 == 0:
        return True
    else:
        return False

def InversionsCount(flatPuz):
    """
    Finds the number of inversions for a given list of numbers

    @params flatPuz: a flattened representation of a 2D puzzle
    """
    inv_count = 0
    for i in range(len(flatPuz)):
        for j in range(i, len(flatPuz)):
            if flatPuz[i] > flatPuz[j]:
                inv_count = inv_count + 1
    return inv_count

def find_gap(puzzle):
    """
    Looks inside a 2D-list to find the gap (0)

    @params puzzle: The puzzle in which to find a gap
    """
    for i, x in enumerate(puzzle):
        if 0 in x:
            return (i, x.index(0))

def flatten(list_2d):
    """
    Takes a 2D-list and flattens it to a 1D-list

    @params list_2d: the 2D-list to flatten
    """
    flattened_list = [y for x in list_2d for y in x]
    return flattened_list


class State(object):
    """
    A class designed to represent the state of a given puzzle
    """
    def __init__(self, puz, previous, move, dist_to_here = 0):
        if type(puz) == tuple: self.puz = puz
        else: self.puz = tuple([tuple(x) for x in puz])
        self.previous = previous
        self.dist_to_here = dist_to_here
        self.move = move
        self.score = self.heuristic() + self.dist_to_here

    def __hash__(self):
        return hash(self.puz)

    def __eq__(self, other):
        eq = True
        assert type(other) == State
        for i in range(len(self.puz)):
            for j in range(len(self.puz[i])):
                if self.puz[i][j] != other.puz[i][j]:
                    return False
        return True

    def __str__(self):
        stuff = ""
        for i in self.puz:
            for j in i:
                stuff = stuff + str(j) + " "
            stuff = stuff + "\n"
        return stuff
    def is_goal(self):
        flatPuz = flatten(self.puz)
        for i in range(len(flatPuz) - 1):
            if flatPuz[i] != i+1: return False
        if flatPuz[-1] == 0: return True
        else: return False

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

    def make_adj_states(self):
        states = []
        temp = list(map(list, self.puz))
        gap_i, gap_j = find_gap(temp)
        # Down swap
        if gap_i > 0:
            swap = temp[gap_i-1][gap_j]
            temp[gap_i][gap_j] = swap
            temp[gap_i-1][gap_j] = 0
            u_swap = State(temp, self, "D", self.dist_to_here+1)
            states.append(u_swap)
        # Up swap
        temp = list(map(list, self.puz))
        if gap_i < len(temp)-1:
            swap = temp[gap_i+1][gap_j]
            temp[gap_i][gap_j] = swap
            temp[gap_i+1][gap_j] = 0
            d_swap = State(temp, self, "U", self.dist_to_here+1)
            states.append(d_swap)
        # Right swap
        temp = list(map(list, self.puz))
        if gap_j > 0:
            swap = temp[gap_i][gap_j-1]
            temp[gap_i][gap_j] = swap
            temp[gap_i][gap_j-1] = 0
            r_swap = State(temp, self, "R", self.dist_to_here+1)
            states.append(r_swap)
        # Left swap
        temp = list(map(list, self.puz))
        if gap_j < len(temp[gap_i])-1:
            swap = temp[gap_i][gap_j+1]
            temp[gap_i][gap_j] = swap
            temp[gap_i][gap_j+1] = 0
            l_swap = State(temp, self, "L", self.dist_to_here+1)
            states.append(l_swap)
        return states

    def heuristic(self):
        moves = []
        score = 0
        # print ("Width of puzzle: ", len(self.puz))
        for i in range(len(self.puz)):
            for j in range(len(self.puz[0])):
                if self.puz[i][j] == 0:
                    row = len(self.puz[i])-1
                    col = len(self.puz[i])-1
                    total = math.fabs(i - row) + math.fabs(j - col)
                    moves.append(total)
                else:
                    row = (self.puz[i][j]-1) // len(self.puz[i])
                    col = (self.puz[i][j]-1) % len(self.puz[i])
                    total = math.fabs(i - row) + math.fabs(j - col)
                    moves.append(total)
        return sum(moves)
