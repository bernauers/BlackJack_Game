#!/usr/bin/env python3

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Culbs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True #variable to control the game
print('Welcome to BlackJack. The Dealer will hit up to 17. Have fun!')
# cards class
class Card():
    def __init__(self, suit, rank):

        self.suit = suit
        self.rank = rank
        

    def __str__(self):
        return self.rank + ' of ' + self.suit

#TESTING
#test_card = Card(suits[2], ranks[4])  # produces six of spades
#print(test_card)
#END TESTING

# deck class
class Deck():
    def __init__(self):

        # an empty list
        self.deck = []

        # add in all the card
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

# shuffle function
    def shuffle(self):
        random.shuffle(self.deck)

# deal fuction
    def deal(self):
        single_card = self.deck.pop()
        return single_card

#TESTING 
#test_deck = Deck()

#print(len(test_deck.deck)) # result is 52 cards 
#END TESTING

class Hand(): 
    def __init__(self):
        #empty list to hold the cards delt 
        self.cards = [] 
        self.value = 0 
        self.aces = 0 #count the number of aces


    def add_card(self,card):
        #card passed in 
        # from Deck.deal() --> single Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1 

    def adjust_for_ace(self):
        #check value is over 21 and still have an ace
        while self.value > 21 and self.aces:
            self.value -= 10 
            self.aces -= 1 

#TESTING 
#est_deck = Deck()
#test_deck.shuffle()
#test_player = Hand()
#test_player.add_card(test_deck.deal())
#test_player.add_card(test_deck.deal())
#print(f'the value of the cards is {test_player.value}')

#for card in test_player.cards: 
#    print(card)
#END TESTING

# chips class 
class Chips():
    def __init__(self):
        self.total = 100 
        self.bet = 0 

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

#placing a bet
def take_bet(chips):
    while True: 
        try: 
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, please enter a number.')
        else: 
            if chips.bet > chips.total: 
                print(f"Sorry, your bet cannot be more than, {chips.total}")
            else: 
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand): 
    global playing

    while True: 
        x = input("Would you like to hit or stay? Enter 'h' or 's' ")

        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False 
        else: 
            print("Sorry, please enter a selction again.")
            continue 
        break


#function to display cards 
def show_some(player,dealer): 
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand Value:", player.value) #Test line to print out the numeric value of the hand

def show_all(player, dealer): 
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

#outcome functions
def player_busts(player,dealer,chips):
    print("Player busts!") 
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()

def push(player,dealer):
    print("Tie, its a push.")

player_chips = Chips() #default value is 100 chips 

#game logic 
while True: 

    #print(f"Round: {round_count}")

    newdeck = Deck()
    newdeck.shuffle()

    player_hand = Hand()
    player_hand.add_card(newdeck.deal())
    player_hand.add_card(newdeck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(newdeck.deal())
    dealer_hand.add_card(newdeck.deal())


    #ask player for bet
    take_bet(player_chips)

    show_some(player_hand, dealer_hand)

    while playing:
        #ask to hit or stand
        hit_or_stand(newdeck, player_hand)

        show_some(player_hand, dealer_hand)

        if player_hand.value > 21: 
            player_busts(player_hand,dealer_hand,player_chips)
            break
#if player hasn't busted, dealer plays until hand reaches 17 
    if player_hand.value <= 21: 
        while dealer_hand.value < 17:
            hit(newdeck,dealer_hand)

        show_all(player_hand,dealer_hand)

        if dealer_hand.value > 21: 
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value: 
            player_wins(player_hand,dealer_hand,player_chips)
        else: 
            push(player_hand,dealer_hand)
    
    if player_chips.total == 0: 
        print("\nAll out of chips! Thanks for playing")
        break

    #inform player of thier chips 
    print("\n Players chip total" , player_chips.total)

#Ask to play again 
    new_hand = input('Would you like to play another hand? Enter y (yes) or n (no) ')

    if new_hand[0].lower() == 'y':
        playing = True
        continue
    else: 
        print('Until next time!')
        break
 

