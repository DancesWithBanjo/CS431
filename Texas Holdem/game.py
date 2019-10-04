import random
import keras
import os, sys
import numpy as np
from itertools import combinations
import csv
import pandas
import random

# run export PYTHONIOENCODING=utf-8
# to get unicodes to work in gitbash

# make net an input

def make_deck():
    """
    Creates a deck of 52 cards
    """
    deck = []
    for i in range(1,5):
        for j in range(1,14):
            card = (i,j)
            deck.append(card)
    return deck

def best_hand(hands):
    """
    Finds the highest rank hand out of a list of hands

    @hands: the list of hands to check
    """
    best_val = 0
    sum = 0
    hand = None
    for h in hands:
        for t in h:
            sum = sum + t[1]
        if sum > best_val:
            best_val = sum
            hand = h

    return hand

def print_cards(cards):
    """
    Prints cards to a user readable form

    @cards: the cards to print
    """
    string = ''
    for c in cards:
        suit = c[0]
        if suit == 1:
            suit = "\u2665" # heart
        elif suit == 2:
            suit = "\u2660" # Spade
        elif suit == 3:
            suit = "\u2666" # Diamond
        else:
            suit = "\u2663" # club

        num = c[1]
        if num == 11:
            num = 'J'
        elif num == 12:
            num = 'Q'
        elif num == 13:
            num = 'K'
        else:
            num = str(num)

        string = string + num + suit + ' '
    return string

def increase(pot, amount, player):
    """
    Increases the pot by a set amount

    @pot: the pot to increase
    @amount: the amount to increase by
    @player: who the amount is coming from
    """
    pot = pot + amount
    player.cash = player.cash - amount
    return pot

def scan_cards(player, river):
    """
    Returns the best hand and its rank for a player

    @player: the player whos cards to check
    @river: the cards on the table
    """
    best_rank = 0
    cards = player.hand + river
    hands = combinations(cards, 5) # find all 5 card hands
    best_hands = []
    for h in hands:
        flat = list(sum(h, ()))
        prep = np.zeros(shape=(10,))
        j = 0
        for i in flat:
            prep[j] = i
            j = j+1
        input = np.zeros(shape=(1,10))
        input[0] = prep
        rank = np.argmax(player.ai.predict(input)[0])

        if rank == best_rank:
            best_hands.append(h)
        if rank > best_rank:
            best_rank = rank
            best_hands = []
            best_hands.append(h)
    final_hand = best_hand(best_hands)
    return (best_rank, final_hand)

def opp_turn(player, river, round_players):
    """
    The AI player action

    @player: the player whos turn it is
    @river: the cards on the table
    @round_players: the active players
    """
    rank, hand = scan_cards(player, river)
    player.best_rank = rank
    rand = random.random()

    if player.cash == 0:
        player.check()
    else:
        if rank == 0:
            if rand <= .5: player.check()
            else: player.fold(round_players)
        elif rank == 1:
            if rand <= .33: player.check()
            elif rand <= .66 and rand > .33: player.opp_raise(rank)
            else: player.fold(round_players)
        elif rank == 2:
            if rand <= .33: player.check()
            elif rand <= .66 and rand > .33: player.opp_raise(rank)
            else: player.fold(round_players)
        elif rank == 3:
            if rand <= .5: player.check()
            elif rand <= .95 and rand > .5: player.opp_raise(rank)
            else: player.fold(round_players)
        else:
            player.opp_raise(rank)

    print ('')
    if player.action == 'raise':
        print (player.name, 'chooses to raise $', player.ante)
    else: print (player.name, 'chooses to ', player.action)
    print ('')

def player_names(players):
    """
    Returns a string of the player names

    @players: the players to name
    """
    string = ''
    for p in players:
        string = string + p.name + ', '
    return string


# The map for card rank conversion
hand_name = {
    0: 'Nothing in hand',
    1: 'One pair',
    2: 'Two pairs',
    3: 'Three of a kind',
    4: 'Straight',
    5: 'Flush',
    6: 'Full house',
    7: 'Four of a kind',
    8: 'Straight flush',
    9: 'Royal flush'
}

def play(num_opp, ai):
    """
    Primary play function

    @num_players: the number of opponents
    @ai: the ai file for the opponents to use
    """
    print ('')
    print ('')
    print ('Welcome to Texas Hold\'em!')
    print ('This program is for those who are already familiar with the game\'s rules.')
    print ('If you wish to end the game at anytime, enter 0 on your turn.')
    print ('Good luck and may the cards be in your favour!')
    print ('')
    print ('')

    players = []
    deck = make_deck()
    random.shuffle(deck)
    river = []
    cash = 1000
    pot = 0

    # Setup players
    you = Player([], 'You', cash, keras.models.load_model(ai))
    players.append(you)

    if num_opp == 1:
        player2 = Player([], 'Player 2', cash, keras.models.load_model(ai))
        players.append(player2)

    elif num_opp == 2:
        player2 = Player([], 'Player 2', cash, keras.models.load_model(ai))
        player3 = Player([], 'Player 3', cash, keras.models.load_model(ai))
        players.append(player2)
        players.append(player3)

    elif num_opp == 3:
        player2 = Player([], 'Player 2', cash, keras.models.load_model(ai))
        player3 = Player([], 'Player 3', cash, keras.models.load_model(ai))
        player4 = Player([], 'Player 4', cash, keras.models.load_model(ai))
        players.append(player2)
        players.append(player3)
        players.append(player4)
    else:
        print ('I guess you\'re playing alone then...')


    players = tuple(players)

    game_over = False
    round = 0
    round_players = []
    for p in players:
        round_players.append(p)
    for i in range(2):
        for p in players:
            p.hand.append(deck.pop())

    while game_over != True:
        # If we've gone passed the 3rd round (someone got some money), reset the river and active players
        if len(round_players) == 0:
            print ('')
            for p in players:
                if p.cash != 0:
                    p.hand = []
                    round_players.append(p)
            river = []
            round = 0
            deck = make_deck()
            random.shuffle(deck)
            for i in range(2):
                for p in players:
                    p.action = ''
                    p.hand.append(deck.pop())

        # Kill one card, as is tradition and setup river
        deck.pop()
        if len(river) < 3:
            while len(river) < 3:
                river.append(deck.pop())
                river.append(deck.pop())
                river.append(deck.pop())
        else:
            river.append(deck.pop())

        players_done = False
        while players_done != True:

            for p in players:
                p.met = False

            # Player's turn
            if you.action != 'fold':
                print('Your hand: ', print_cards(you.hand))
                print('Table: ', print_cards(river))
                print('')
                print ('Players left: ', player_names(round_players))
                print('')
                print('Pot: $',pot)
                print('Your cash: $', you.cash)

                valid = False
                while valid != True:
                    print ('')
                    inp = input('Type 1 to raise, 2 to check, or 3 to fold: ')
                    print ('')
                    inp = int(inp)

                    if inp == 1:
                        you.action = 'raise'
                        valid = True
                        able = False
                        while able != True:
                            print ('You have $', you.cash)
                            inp = input('How much will you raise? ')
                            print ('')
                            inp = int(inp)
                            if inp > you.cash:
                                print('You don\'t have enough.')
                            else:
                                pot = increase(pot, inp, you)
                                able = True
                                you.done = True
                                you.ante = inp
                    elif inp == 2:
                        you.check()
                        valid = True
                    elif inp == 3:
                        you.fold(round_players)
                        valid = True
                    elif inp == 0:
                        print ('Goodbye')
                        sys.exit(1)
                    else:
                        print ('Please enter a valid input.')

            # Triggger opponent turns
            # If pc raised, then opponents meet or fold
            players_done = True
            for p in round_players:
                if you.action == 'raise' and p.name != 'You':
                    p.meet(you.ante, round_players)
                elif p.name != 'You' and p.met == False:
                    opp_turn(p, river, round_players)
                else:
                    continue
                pot = increase(pot, p.ante, p)
                # Round ends when all players fold or check
                if p.action != 'check':
                    players_done = False

            # If there's only one player left, they win by default
            if len(round_players) == 1:
                p = round_players[0]
                if p.name == 'You':
                    print (p.name, 'win by default!')
                else:
                    print (p.name, 'wins by default!')
                if p.name == 'You':
                    print (p.name, 'get $', pot)
                else:
                    print (p.name, 'gets $', pot)

                p.cash = p.cash + pot
                pot = 0
                round = 3
                round_players = []
                players_done = True
            # find highest raise
            else:
                if players_done == False:
                    ante = 0
                    for p in round_players:
                        if p.ante > ante:
                            ante = p.ante

                # If someone raised, make everyone meet the raise or fold
                if players_done == False:
                    for p in round_players:
                        if ante > p.ante:
                            diff = ante - p.ante
                            if p.name == 'You':
                                valid = False
                                while valid != True:
                                    print ('The highest raise is', ante, 'You have raised ', p.ante)
                                    inp = input('Type 1 to raise, 2 to meet the raise, or 3 to fold: ')
                                    print ('')
                                    inp = int(inp)

                                    if inp == 1:
                                        you.action = 'raise'
                                        valid = True
                                        able = False
                                        while able != True:
                                            print ('You have $', you.cash)
                                            inp = input('How much will you raise? ')
                                            inp = int(inp)
                                            if inp > you.cash:
                                                print('You don\'t have enough.')
                                            elif inp < diff:
                                                print ('You need to raise at least', diff)
                                            else:
                                                pot = increase(pot, inp, you)
                                                able = True
                                                you.done = True
                                    elif inp == 2:
                                        pot = increase(pot, diff, you)
                                        you.action = 'check'
                                        valid = True
                                    elif inp == 3:
                                        you.fold(round_players)
                                        valid = True
                                    else:
                                        print ('Please enter a valid input.')
                            else:
                                p.meet(diff, round_players)
                players_done = True




        # See who wins
        if round == 2:
            print ('')

            hands = {}
            player_hands = {}
            for p in round_players:
                rank, hand = scan_cards(p, river)
                hands[hand] = rank
                player_hands[hand] = p

            best_hand = max(hands, key=hands.get)
            best_rank = hands[best_hand]
            player = player_hands[best_hand]

            # Show the results
            if player.name == 'You':
                print(player.name, ' have the best hand:', print_cards(best_hand))
            else:
                print(player.name, ' has the best hand:', print_cards(best_hand))

            print('The hand is a', hand_name[best_rank])

            if player.name == 'You':
                print (player.name, 'get $', pot)
            else:
                print (player.name, 'gets $', pot)

            round_players = []

            # distribute cash and clear pot
            player.cash = player.cash + pot
            pot = 0

            # If you still have no money, game over
            if you.cash == 0:
                game_over = True
                print ('Game over! You ran out of money!')
                sys.exit(1
                )
            print ('')
            print ('Starting next round.')
        round = round + 1
        print ('')


class Player(object):
    def __init__(self, hand, name, cash, ai):
        self.id = id
        self.name = name
        self.hand = hand
        self.cash = cash
        self.ai = ai
        self.action = ''
        self.done = False
        self.ante = 0
        self.best_rank = 0
        self.met = False

    def check(self):
        self.action = 'check'
        self.done = True

    def fold(self, round_players):
        self.action = 'fold'
        self.done = True
        round_players.remove(self)

    def meet(self, ante, round_players):
        rand = random.random()
        offer = 0

        if self.best_rank == 0:
            if rand < .3: offer = ante
            else: self.fold(round_players)
        elif self.best_rank == 1:
            if rand < .5 and rand >= .3: offer = ante
            else: self.fold(round_players)
        else:
            offer = ante

        if self.action == 'fold':
            print (self.name, 'chooses to fold.')
        else: print (self.name, 'meets the raise.')
        print ('')

        self.cash = self.cash - offer
        self.ante = self.ante + offer
        self.met = True

    def opp_raise(self, rank):
        self.action = 'raise'
        offer = 0

        # If you're about to lose, go ahead and offer it all
        if self.cash < 50: offer = self.cash

        # Set raise ranges
        if rank == 1:
            if self.cash < 100: offer = self.cash // 10
            else: offer = self.cash // 100
        elif rank == 2:
            if self.cash < 100: offer = self.cash // 20
            else: offer = self.cash // 90
        elif rank == 3:
            if self.cash < 100: offer = self.cash
            else: offer = self.cash // 70
        elif rank == 4:
            if self.cash < 150: offer = self.cash
            else: offer = self.cash // 50
        elif rank ==5:
            if self.cash < 200: offer = self.cash
            else: offer = self.cash // 40
        else:
            if self.cash < 200: offer = self.cash
            else: offer = self.cash // 30

        # alter funds as needed
        money = random.randint(offer//2, offer)
        self.cash = self.cash - money
        self.ante = self.ante + money




if len(sys.argv) < 3:
    print ('')
    print("Need to enter number of opponents and the ai file.")
    sys.exit(1)

if int(sys.argv[1]) > 3:
    print ('')
    print("The max number of opponents is 3.")
    sys.exit(1)

if int(sys.argv[1]) < 0:
    print ('')
    print("You may want to be alone, but you can't be less than alone.")
    sys.exit(1)

play(int(sys.argv[1]), sys.argv[2])
