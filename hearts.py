#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import random
import playingCard as pc


class new_player:  # The player object class. New players are created with each new game
    def __init__(self, index):
        self.is_human = False
        self.index = index
        
        self.score = 0  # The total points earned across all rounds
        
        self.hand = set()
        self.taken = set()
        self.hand_suits = set()
    
    
    def update_hand_info(self):
        self.hand_suits = set()
        for card in self.hand:
            self.hand_suits.add(card[0])
        return
    
    
    def has_two_clubs(self):
        if "C2" in self.hand:
            return True
        else:
            return False
    
    
    def has_suit(self, suit):
        if suit in self.hand_suits:
            return True
        else:
            return False
    
    
    def take_cards(self, cards):
        for card in cards:
            self.taken.add(card)
    
    
    def has_monarch(self, game):
        if self.taken == game.monarch:
            return True
        else:
            return False
    
    
    def update_score(self):
        points = 0
        for card in self.taken:
            if card[0] == "H":
                points += 1
            elif card == "SQ":
                points += 13
        self.score += points
        self.taken = set()
    
    
    def add_cards(self, cards):
        for card in cards:
            self.hand.add(card)
    
    
    def discard_cards(self, game):
        cards = []
        if self.is_human:
            for i in range(1,4):
                print("\nYour hand:", self.hand)
                valid_choice = False
                while not valid_choice:
                    discarded_card = input("Please enter a card to discard ({0} of 3): ".format(i))
                    if discarded_card in self.hand:
                        cards.append(discarded_card)
                        self.hand.remove(discarded_card)
                        valid_choice = True
                    else:
                        print("Please enter a card from your hand...")
        else:
            for i in range(1,4):
                hand_list = list(self.hand)
                discarded_card = random.choice(hand_list)
                cards.append(discarded_card)
                self.hand.remove(discarded_card)
        
        target_player = game.players[(self.index + 1) % 4]
        target_player.add_cards(cards)


    def get_optimal_play(self, suit):
        pass
    
    
    def take_turn(self, trick):
        suit = trick.suit
        viable = []
        self.update_hand_info()
        
        if self.has_two_clubs():
            viable.append("C2")
        
        elif suit == "":
            viable = list(self.hand)
        
        elif self.has_suit(suit):
            print("SUIT!")
            for held_card in self.hand:
                if held_card[0] == suit:
                    viable.append(held_card)
        else:
            viable = list(self.hand)

        if self.is_human:
            valid_choice = False
            print("Your Hand: ", self.hand)
            print("Your Take: ", self.taken)
            print("You can play one of the following cards:", viable)
            while not valid_choice:
                played_card = input("Please enter a card to play: ")
                if played_card in viable:
                    valid_choice = True
                else:
                    print("Please enter a card from your viable cards...")
            print("You have played {0}".format(played_card))
        else:
            played_card = random.choice(viable)
            print("Player {0} has played {1}".format(self.index, played_card))
        
        if suit == "":
            trick.suit = played_card[0]
        
        self.hand.remove(played_card)
        return played_card


class new_game:  # The game object class. A game contains multiple rounds, and ends when any player's score exceeds 50
    def __init__(self):
        self.players = [new_player(0), new_player(1), new_player(2), new_player(3)]
        self.player_count = len(self.players)
        self.monarch = {"HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", "HK", "SQ"}
        self.over = False
    
    
    def player_query(self):
        options = ["y", "n"]
        valid_choice = False
        while not valid_choice:
            play_query = input("The game can be quite long, so I've included an option that will make random choices for you and speed the game along.\nDo you wish to play the game yourself? [y/n]: ")
            if play_query.lower() in options:
                valid_choice = True
                if play_query.lower() == "y":
                    self.players[0].is_human = True
                    print("You are Player 0\n")
            else:
                print("Please select one of the options provided...")
    
    
    def update_player_scores(self, game):
        monarch = None
        for player in self.players:
            if player.has_monarch(game):
                monarch = player
    
        for player in self.players:
            if monarch is None:
                player.update_score()
            elif player != monarch:
                player.score += 26
    
    
    def scoreboard(self):
        print("\n> SCORES:")
        for player in self.players:
            print("| Player {0}: {1} points |".format(player.index, str(player.score).zfill(2)))
        print("")
    
    
    def is_over(self):
        for player in self.players:
            if player.score >= 50:
                return True
        return False
    
    
    def announce_winner(self):
        min_score = None
        winners = []
        tie = False
        
        for player in self.players:
            if min_score is None:
                min_score = player.score
                winners.append(str(player.index))
            
            elif player.score < min_score:
                min_score = player.score
                winners = []
                winners.append(str(player.index))
                tie = False
            
            elif player.score == min_score:
                winners.append(str(player.index))
                tie = True
        
        if tie:
            winner_string = ",".join(winners)
            print("\n=== Players {0} have tied for the win! ===\n".format(winner_string))
        else:
            print("\n=== Player {0} has won! ===\n".format(winners[0]))


class new_round:  # The round object class. Each round contains multiple tricks, and ends when the players are out of cards.
    def deal_player_hands(self, game):
        deck = pc.generateDeck()
        deck = pc.shuffleCards(deck)
        self.hands = pc.dealCards(deck, 0, game.player_count)
    
    
    def reset_player_points(self, game):
        for i in range(0, game.player_count):
            game.players[i].hand = set(self.hands[i])
            game.players[i].points = 0
    
    
    def get_trick_starter(self, game):
        for player in game.players:
            if player.has_two_clubs():
                self.next_trick_starter = player
    
    
    def discard_step(self, game):
        for player in game.players:
            player.discard_cards(game)
            

    def __init__(self, game):
        player_count = len(game.players)
        self.next_trick_starter = None
        
        self.deal_player_hands(game)
        self.reset_player_points(game)
        self.get_trick_starter(game)

    
    def is_over(self, game):
        if len(game.players[0].hand) == 0:
            game.update_player_scores(game)
            return True
        else:
            return False


class new_trick:  # The trick object class. A trick ends when each player has played a card.
    def set_trick_order(self, game):
        start_index = game.players.index(self.owner)
        for i in range(0, len(game.players)):
            j = (i + start_index) % 4
            self.order.append(game.players[j])
    
    
    def __init__(self, rounde, game):
        self.cards = []
        self.suit = ""
        
        self.owner = rounde.next_trick_starter
        self.order = []
        self.set_trick_order(game)
    
    
    def give_take(self, rounde):
        max_value = 0
        for i in range(0, len(self.cards)):
            card = self.cards[i]
            played_by = self.order[i]
            
            if card[0] == self.suit:
                value = int(pc.convertFaceToNumber(card)[1:])
                if value == 1:
                    value = 14
                if value > max_value:
                    self.owner = played_by
                    max_value = value
        self.owner.take_cards(self.cards)
        print("> Player {0} takes the trick.".format(self.owner.index))
        
        rounde.next_trick_starter = self.owner
    
    
    def play_trick(self, rounde):
        for player in self.order:
            played_card = player.take_turn(self)
            self.cards.append(played_card)
            
        self.give_take(rounde)
    

def run_game():
    current_game = new_game()
    current_game.player_query()
    
    print("\n ░░░  ░░░    ░░      ░░   ░░░░░░░░░░   ░░░░░░░░░░   ░░░░░░░░░░   ░░░░░░░░░░   ░░░░░░░░░░    ░░░  ░░░   \n░░  ░░  ░░   ░░      ░░   ░░           ░░      ░░   ░░      ░░       ░░       ░░           ░░  ░░  ░░\n░░      ░░   ░░░░░░░░░░   ░░░░░░░░░░   ░░░░░░░░░░   ░░░░░░░░         ░░       ░░░░░░░░░░   ░░      ░░\n ░░    ░░    ░░      ░░   ░░           ░░      ░░   ░░      ░░       ░░               ░░    ░░    ░░ \n   ░░░░      ░░      ░░   ░░░░░░░░░░   ░░      ░░   ░░      ░░       ░░       ░░░░░░░░░░      ░░░░   \n")
    print("> A new game is starting...")
    while not current_game.is_over():
        print("> A new round is starting...")
        current_round = new_round(current_game)
        current_round.discard_step(current_game)
        while not current_round.is_over(current_game):
            print("\n> A new trick is starting...")
            current_trick = new_trick(current_round, current_game)
            current_trick.play_trick(current_round)
        current_game.scoreboard()
        input("Press enter to continue...")
    current_game.announce_winner()


while True:
    run_game()
    input("Press enter to play again...")