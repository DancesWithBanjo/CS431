"""
This Connect Four player just picks a random spot to play. It's pretty dumb.
"""
__author__ = "Adam A. Smith" # replace my name with yours
__license__ = "MIT"
__date__ = "February 2018"

import random
import time
import collections
from pprint import pprint

class ComputerPlayer:
    def __init__(self, id, difficulty_level):
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        self.id = id
        self.diff = difficulty_level
        pass


    def pick_move(self, rack):
        """
        Pick the move to make. It will be passed a rack with the current board
        layout, column-major. A 0 indicates no token is there, and 1 or 2
        indicate discs from the two players. Column 0 is on the left, and row 0
        is on the bottom. It must return an int indicating in which column to
        drop a disc. The player current just pauses for half a second (for
        effect), and then chooses a random valid move.
        """
        rack = self.tup_to_list(rack)
        while True:
            play = self.move_eval(rack, self.id, 0, True)
            print("Column played: ", play)
            if rack[play][-1] == 0: return play

    def move_eval(self, rack, id, rec_lvl = 0, top = False):
        """
        Returns and integer representing the column for the best move
        rack is a 2d list (not tuple)
        id is the id of the player who's turn it is
        rec_lvl is current level of recursion
        top is a conditional checking if we are at the top level (of recursion)
        """
        diff = self.diff
        top = top
        quarts = self.quart_search(rack)
        moves = []
        score = 0
        # add all the scores together
        for i in range(len(quarts)):
            q_score = self.quart_score(quarts[i], rack, id)
            # Win Condition
            if q_score >= 100000000 or q_score <= -100000000: return q_score
            else: score = score + q_score

        # Reached max recursion depth
        if rec_lvl == diff:
            return score

        for i in range(len(rack)):
            # increment col height while the tile isn't empty
            for j in range(len(rack[i])):
                if rack[i][j] != 1 or rack[i][j] != 2:
                    rack[i][j] = id    # Need to make rack into 2d list
                    break

            move = self.move_eval(rack, self.flip_player(id), rec_lvl+1), i
            moves.append(move)
            self.rmv_top_disk(rack[i])  # Removes previous move

        # Extrapolate best move
        best_score = 0
        slot = None
        # MAX move
        if id == self.id:
            for i in moves:
                if i[0] >= best_score:
                    best_score = i[0]
                    slot = i[1]
                if best_score <= 0:
                    if i[0] < best_score:
                        best_score = i[0]
                        slot = i[1]
        # MIN move
        if id != self.id:
            for i in moves:
                if i[0] <= best_score:
                    best_score = i[0]
                    slot = i[1]
                if best_score >= 0:
                    if i[0] < best_score:
                        best_score = i[0]
                        slot = i[1]
        # Check for equal scoring moves
        options = []
        for i in moves:
            print(i)
            if best_score == i[0]: options.append(i[1])

        # Bias the left move
        print(options)
        if len(options) > 0: slot = options[0]
        if rec_lvl == 0: top = True

        if rec_lvl > 0: return best_score
        if top == True: return slot

    def quart_search(self, rack):
        """
        Takes in a rack
        Returns a list of all possible quartets.
        """
        quarts = []
        for i in range(len(rack)):
            for j in range(len(rack[i])):
                # horizontal to the right
                quart = []  # list of positions (tuples)
                for k in range(4):
                    # check if quartet search goes out of bounds
                    if i+k >= len(rack):
                        break
                    else:
                        pos = i+k, j
                        quart.append(pos)
                if len(quart) == 4: quarts.append(quart)

                # diagonal to the top right
                quart = []
                for k in range(4):
                    if i+k >= len(rack) or j+k >= len(rack[i])-1:
                        break
                    else:
                        pos = i+k, j+k
                        quart.append(pos)
                if len(quart) == 4: quarts.append(quart)

                # straight up
                quart = []
                for k in range(4):
                    if j+k >= len(rack[i])-1:
                        break
                    else:
                        pos = i, j+k
                        quart.append(pos)
                if len(quart) == 4: quarts.append(quart)

                # diagonal to the top left
                quart = []
                for k in range(4):
                    if i-k < 0 or j+k >= len(rack[i])-1:
                        break
                    else:
                        pos = i-k, j+k
                        quart.append(pos)
                if len(quart) == 4: quarts.append(quart)
        return quarts


    def quart_score(self, quart, rack, id):
        """
        Takes a quartet, the rack parenting the quart, and the players id
        Uses the contents of the quartet and calculate its score
        Positive if the quartet is filled with the main player's id
        Negative if the quartet is filled with the opponent's id
        """
        score = 0
        discs = []
        for i in range(len(quart)):
            coord = quart[i]
            x = coord[0]
            y = coord[1]
            disc = rack[x][y]
            discs.append(disc)
        counter = collections.Counter(discs)  # a hash of discs mapped to number of occurences
        print(counter)
        print(counter[self.id])
        if 1 in counter and 2 in counter:
            return 0
        else:
            if self.id in counter and self.flip_player(self.id) not in counter:
                if counter[self.id] == 1 and counter[0] == 3:
                    score = 1
                if counter[self.id] == 2 and counter[0] == 2:
                    score = 10
                if counter[self.id] == 3 and counter[0] == 1:
                    score = 100
                if counter[self.id] == 4:
                    score = 100000000
            if self.flip_player(self.id) in counter and self.id not in counter:
                if counter[self.flip_player(self.id)] == 1 and counter[0] == 3:
                    score = -1
                if counter[self.flip_player(self.id)] == 2 and counter[0] == 2:
                    score = -10
                if counter[self.flip_player(self.id)] == 3 and counter[0] == 1:
                    score = -100
                if counter[self.flip_player(self.id)] == 4:
                    score = -100000000
        return score

    def flip_player(self, id):
        """
        Takes in a player id and returns the other player's id
        """
        if id == 1: return 2
        else: return 1

    def tup_to_list(self, tup):
        """
        Converts a 2D tuple into 2D list
        """
        return list(map(list, tup))

    def rmv_top_disk(self, column):
        """
        Takes in a column and removes the top disk (1 or 2)
        """
        col = column
        for i in col:
            if col[-i] == 1 or col[-i] == 2:
                col[-i] = 0
                break
            else: continue

    def is_col_full(self, column):
        """
        Takes a column and checks if all of its elements or 1's or 2's
        """
        col = column
        if col[-1] == 1 or col[-1] == 2: return True
        else: return False
