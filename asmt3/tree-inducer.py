import math, sys

def entropy(representatives):
    """
    Calculates the entropy of a given set

    @ representatives: the data set
    """
    rPubs  = 0
    dCrats = 0
    for r in representatives:
        if r.party == 'R':
            rPubs = rPubs + 1
        else:
            dCrats = dCrats + 1
    if len(representatives) == 0:
        return 0
    else:
        prob_R = rPubs / len(representatives)
        prob_D = dCrats / len(representatives)

    if prob_D == 0 and prob_R == 0:
        ent = 0
    elif prob_D == 0 and prob_R != 0:
        ent = - prob_R*(math.log2(prob_R))
    elif prob_R == 0 and prob_D != 0:
        ent = -(prob_D*(math.log2(prob_D)))
    else:
        ent = -(prob_D*(math.log2(prob_D))) - prob_R*(math.log2(prob_R))

    return ent


def gain(representatives, issue):
    """
    Calculates the information gain of a given set for one feature

    @representatives: the data set
    @issue          : the issue the calculate gain for
    """
    ent = entropy(representatives)
    groups = issue_votes(representatives, issue)
    # groups[0] = those who voted yay
    # groups[1] = those who voted nay
    # groups[2] = those who abstained

    ent1 = (len(groups[0])/len(representatives))*entropy(groups[0])
    ent2 = (len(groups[1])/len(representatives))*entropy(groups[1])
    ent3 = (len(groups[2])/len(representatives))*entropy(groups[2])
    sum_ent = ent1 + ent2 + ent3

    return ent - sum_ent


def tree_maker(representatives, node, issues, level = 0):
    """
    Builds a tree recursively using the Decision Tree algorithm

    @representatives: the data set
    @node           : the node from which the subtrees will stem
    @issues         : the list of issues previously used to make non-leaf nodes
    """
    best_gain   = -100 # Gain never gets below -100
    best_issue  = 0
    info_gain   = 0
    lvl         = level
    lvl         = lvl + 1
    issue_list  = issues # used to track already used issues
    rPubs       = _num_rep(representatives)
    dCrats      = _num_dec(representatives)


    # BASE CASES
    if len(representatives) == 0 or rPubs == dCrats:
        return Node(None, node.par_maj, lvl)

    # check if a data set is uniform
    if rPubs  == 0:
        return Node(None, 'D', lvl)
    if dCrats == 0:
        return Node(None, 'R', lvl)

    # Check if representatives all voted the same on an issue
    if are_votes_equal(representatives):
        # Check for the majority among these reps
        if single_majority(representatives) == None:
            return Node(None, majority(representatives, node), lvl)
        else:
            return Node(None, single_majority(representatives), lvl)

    # Check if there are no more issues to split from
    if len(issues) == 0:
        return Node(None, node.par_maj, lvl)
    # END of BASE CASES

    for i in issue_list:
        info_gain = gain(representatives, i)
        if info_gain > best_gain:  # > should make it so we pick the earliest issue if two have equal gain
            best_gain  = info_gain
            best_issue = i

    groups = issue_votes(representatives, best_issue)
    root = Node(_num_to_let(best_issue), 'undefined', lvl)
    if node == None:
        root.par_maj = single_majority(representatives)
    else:
        root.par_maj = node.par_maj

    root.party  = majority(representatives, root)

    # start recursion
    root.left   = tree_maker(groups[0], root, issue_list.difference([best_issue]), lvl)
    root.center = tree_maker(groups[1], root, issue_list.difference([best_issue]), lvl)
    root.right  = tree_maker(groups[2], root, issue_list.difference([best_issue]), lvl)

    return root


def parse_data(file):
    """
    Takes a file and returns a list of Reps built from the file data

    @file: the file/data to parse
    """
    reps = []
    inputfile = open(file)

    for line in inputfile:
        info = line.split('\t')

        rep_id = info[0]
        rep_id = rep_id[4:]        # get representative's id
        rep_party = info[1]        # get representative's party
        vote_data = info[2]        # get voting data
        fixed_vote_data = vote_data[:10]    # remove \t from voting data string

        # create Rep object and store in a list of representatives
        rep = Rep(rep_id, rep_party, fixed_vote_data)
        reps.append(rep)
    return reps


def make_tuning_set(training_set):
    """
    Builds a tuning set used to assess a trees accuracy
    Tuning set consists of every 4th element from a given data set

    @training_set: the data set to build from
    """
    tune_set = []
    for i in range(len(training_set)):
        if i%4 == 0:
            tune_set.append(training_set[i])
        else:
            continue
    return tune_set


def prune_tree(tree):
    """
    When implimented, clips branches of the given tree to improve overall accuracy

    @tree: the tree to prune
    """
    # :(
    return None


def tree_accuracy(tree, representatives):  # NOTE do first?
    """
    Returns a percentage representing how correct a tree is

    @tree: the tree to calculate accuracy
    """
    counter = 0
    cut_data = []
    issues = frozenset([0,1,2,3,4,5,6,7,8,9])
    for r in representatives:
        cut_data = representatives
        cut_data.remove(r)
        active = tree_maker(cut_data, None, issues)
        while active.is_leaf() == False:
            issue = active.issue
            vote = r.votes[issue]
            if vote == '+':
                active = active.left
            elif vote == '-':
                active = active.center
            else:
                active = active.right
        if active.party == r.party:
            counter = counter + 1
    return counter/len(representatives)


def tree_size(tree):
    """
    Calculates how many nodes are in a tree

    @tree: the tree to check size
    """
    if tree is None: return 0
    else:
        return (1 + tree_size(tree.left) + tree_size(tree.center) + tree_size(tree.right))


def issue_votes(representatives, issue):
    """
    Splits a given list into three groups by each element's vote on a given issue

    @representatives: the data set
    @issue          : the issue to split by votes from
    """
    yay = []
    nay = []
    abstain = []
    for r in representatives:
        if r.votes[issue] == '+':
            yay.append(r)
        elif r.votes[issue] == '-':
            nay.append(r)
        else:
            abstain.append(r)
    return [yay,nay,abstain]


def majority(representatives, node):
    """
    Majority calculator that pulls the majority from a parent node if the current node has no majority

    @representatives: the data set
    @node           : the current node
    """
    assert type(node) == Node
    rPubs = 0
    dCrats = 0
    for r in representatives:
        if r.party == 'R':
            rPubs = rPubs + 1
        else:
            dCrats = dCrats + 1
    if rPubs > dCrats:
        return 'R'
    elif dCrats > rPubs:
        return 'D'
    else:
        return node.par_maj


def single_majority(representatives):
    """
    Majority calculator that returns None if node has no majority

    @representatives: the data set
    """
    rPubs = 0
    dCrats = 0
    for r in representatives:
        if r.party == 'R':
            rPubs = rPubs + 1
        else:
            dCrats = dCrats + 1
    if rPubs > dCrats:
        return 'R'
    elif dCrats > rPubs:
        return 'D'
    else: return None


def are_votes_equal(representatives):
    """
    Checks if all elements of a given set voted the same way on a given issue

    @representatives: the data set
    """
    return all(votes == representatives[0].votes for votes in representatives)


def _num_rep(representatives):
    rPubs = 0
    for r in representatives:
        if r.party == 'R':
            rPubs = rPubs + 1
        else: continue
    return rPubs


def _num_dec(representatives):
    dCrats = 0
    for r in representatives:
        if r.party == 'D':
            dCrats = dCrats + 1
        else: continue
    return dCrats


def _num_to_let(num):
    return{0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}[num]


def _let_to_num(let):
    return{'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,}[let]


class Rep(object):
    """
    An object to define a representative
    Consists on an id, their party, and a list of their votes
    """
    def __init__(self, id, party, votes):
        self.id = id
        self.party = party
        self.votes = votes


    def __str__(self):
        """
        Returns a string representation of a representative
        """
        info = str(self.id) + " " + self.party + " " + str(self.votes)
        print(info)


class Node(object):
    """
    An object to be used as the building blocks for the decision tree
    Each turning point of a tree is a node or leaf (a node with no brances)
    """
    def __init__(self, issue, party, level, par_maj = None, left = None, center = None, right = None):
        self.issue   = issue     # issue stored in the node
        self.party   = party     # party stored in the node
        self.level   = level     # depth of the node
        self.par_maj = par_maj   # pointer to parent node's majority
        self.left    = left      # +
        self.center  = center    # -
        self.right   = right     # .


    def __str__(self):
        """
        Returns a string representation of the tree (node) structure
        """
        ret = ''
        if self.is_leaf(): return self.party
        else:
            ret += 'Issue ' + str(self.issue) + ':\n' + ('\t'*self.level)
            ret += '+ ' + str(self.left) + '\n' + ('\t'*self.level)
            ret += '- ' + str(self.center) + '\n' + ('\t'*self.level)
            ret += '. ' + str(self.right)
        return ret


    def is_leaf(self):
        """
        Checks if the current node is a leaf
        """
        if self.left is None and self.center is None and self.right is None:
            return True


# MAIN

if len(sys.argv) > 2:
    print("Need a file. ")
    sys.exit(1)

data = parse_data(sys.argv[1])
tune_set = make_tuning_set(data)
issues = frozenset([0,1,2,3,4,5,6,7,8,9])
tree = tree_maker(tune_set, None, issues)
print(tree)
print('Tree Accuracy: ', tree_accuracy(tree, data))
