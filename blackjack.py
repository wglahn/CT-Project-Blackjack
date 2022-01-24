import random
import os
import time

'''
Blackjack: OOP Virtual Blackjack Game

classes : 
    Dealer: this class is the user interface and handles all logic based
            on the rules of Blackjack.

        Attributes:
            card_count: number of cards in the dealers hand used to 
                determine the column of the displayed card
            deck = instantiates the deck
            hand: cards in the dealer's hand
            player: instantiates the player
            seat: used to determine the row for the dealer's printed cards

        Methods:
            clear_table: clears screen
            deal: deals the initial cards
            display_item: prints text to screen in designated position
            muck_cards: clears hands of dealer nad player
            play_blackjack: initiates Blackjack game
            set_card_pos: determines position of printed playing card
            total_hand: totals a given hand

    Player: stores all data associated with the player

        Attributes:
            bet: stores the amount of the player's wager
            card_count: numbe of cards in the player's hand used to 
                determine the column of the displayed card       
            hand: cards in the player's hand
            seat: used to determine the row for the players's printed cards
            total: amount of money the player has (defaults at $200 to start)

    Deck: creates a deck of cards and issues a random card upon request

        Attributes:
            cards: a deck of 52 cards
            suites: hearts, diamonds, clubs, spades
            values: ace(11), king(10), queen(10), jack(10), 10, 9, 8, 7, 6, 5, 4, 3, 2
            
        Methods:
            card: issues card
            shuffle_cards: creates random deck of 52 cards

'''

class Dealer():
    def __init__(self):
        self.hand = []
        self.card_count = 0
        self.seat = 1
        self.player = Player()
        self.deck = Deck()

    def play_blackjack(self):
        su = '\033[04m' #start of underline
        eu = '\033[0m' #end of underline

        self.clear_table()
        print("\nWelcome to Blackjack!\n")

        while True:
            action = input("You currently have $" + "{:.2f}".format(self.player.total) + ". How much would you like to wager? ")
            if not action.isnumeric():
                # Non numeric bet entered
                print("Too many drinks for you! You're cut off!\n")
            else:
                if float(action) > self.player.total:
                    print("Nice try wise guy! No loans!\n")
                else:
                    if float(action) < 1.00:
                        print("Need some practice? No free hands sorry :(\n")
                    else:
                        self.player.bet = int(action)
                        self.deal()

                        # check for player blackjack
                        if self.total_hand(self.player.hand) == 21:
                            self.display_item(self.player.seat,self.set_card_pos(self.player.card_count),"BLACKJACK!")

                        # check for dealer blackjack
                        if self.total_hand(self.hand) == 21:
                            # show dealer second card
                            self.card_count -= 1
                            self.display_item(self.seat,self.set_card_pos(self.card_count),self.hand[1]["card"])
                            self.card_count += 1
                            self.display_item(self.seat,self.set_card_pos(self.card_count),"BLACKJACK!")
                            print()

                        if self.total_hand(self.player.hand) == 21 and self.total_hand(self.hand) == 21:
                            # Push
                            print("\nPush")
                        elif self.total_hand(self.player.hand) == 21 and self.total_hand(self.hand) != 21:
                            # if the player has blackjack and the dealer does not
                            self.player.total += (self.player.bet * 1.5)
                        elif self.total_hand(self.player.hand) != 21 and self.total_hand(self.hand) == 21:
                            # if the dealer has blackjack and the player does not
                            self.player.total -= self.player.bet
                        else:

                            # player choices
                            while True:
                                action = input("What would you like to do: " + su + "H" + eu + \
                                    "it or " + su + "S" + eu + "tand? ")

                                if action.lower() == "hit" or action.lower() == "h":
                                    self.player.hand.append(self.deck.card())
                                    self.display_item(self.player.seat,self.set_card_pos(self.player.card_count),self.player.hand[-1]["card"])
                                    self.player.card_count += 1
                                    if self.total_hand(self.player.hand) > 21:
                                        busted = False # second chance
                                        while True:
                                            ace = False
                                            for card in self.player.hand:
                                                if card['value'] == 11 and ace == False:
                                                    ace = True
                                                    card['value'] = 1
                                            if self.total_hand(self.player.hand) > 21 and ace == False:
                                                self.display_item(self.player.seat,self.set_card_pos(self.player.card_count),"BUSTED!")
                                                self.player.total -= self.player.bet
                                                busted = True
                                                break
                                            elif self.total_hand(self.player.hand) <= 21:
                                                busted = False
                                                break
                                        if busted == True:
                                            break

                                elif action.lower() == "stand" or action.lower() =="s":
                                    # dealers turn
                                    # show dealer second card
                                    self.card_count -= 1
                                    self.display_item(self.seat,self.set_card_pos(self.card_count),self.hand[1]["card"])
                                    self.card_count += 1

                                    while True:
                                        if self.total_hand(self.hand) <= 21 and self.total_hand(self.hand) >= 17:
                                            # dealer stands
                                            if self.total_hand(self.hand) > self.total_hand(self.player.hand):
                                                # dealer has better hand
                                                self.display_item(self.seat,self.set_card_pos(self.card_count),"YOU LOSE!")
                                                self.player.total -= self.player.bet
                                            elif self.total_hand(self.hand) < self.total_hand(self.player.hand):
                                                # player has better hand
                                                self.display_item(self.player.seat,self.set_card_pos(self.player.card_count),"YOU WIN!")
                                                self.player.total += self.player.bet
                                            elif self.total_hand(self.hand) == self.total_hand(self.player.hand):
                                                self.display_item(self.player.seat,self.set_card_pos(self.player.card_count),"PUSH!")    
                                            break
                                        elif self.total_hand(self.hand) > 21:
                                            busted = False # second chance
                                            while True:
                                                ace = False
                                                for card in self.hand:
                                                    if card['value'] == 11 and ace == False:
                                                        ace = True
                                                        card['value'] = 1
                                                if self.total_hand(self.hand) > 21 and ace == False:
                                                    self.display_item(self.seat,self.set_card_pos(self.card_count),"BUSTED!")
                                                    self.display_item(self.player.seat,self.set_card_pos(self.player.card_count),"YOU WIN!")
                                                    self.player.total += self.player.bet
                                                    busted = True
                                                    break
                                                elif self.total_hand(self.player.hand) <= 21:
                                                    busted = False
                                                    break
                                            if busted == True:
                                                break

                                        else:
                                            # add card to dealer hand
                                            self.hand.append(self.deck.card())
                                            self.display_item(self.seat,self.set_card_pos(self.card_count),self.hand[-1]["card"])
                                            self.card_count += 1

                                    break # break out of hand

                        if self.player.total != 0:
                            action = input('\n\nWould you like to play again? ')
                            if action.lower() == 'no' or action.lower() == 'n':
                                self.clear_table()
                                if self.player.total > 1000:
                                    print("You won $" + "{:.2f}".format((self.player.total - 200)) + ". WOW! You're ready for the pro circuit!")
                                elif self.player.total > 200:
                                    print("You won $" + "{:.2f}".format((self.player.total - 200)) + ". You beat the house. Good job!")
                                elif self.player.total == 200:
                                    print("You broke even. Go home and practice!")
                                elif self.player.total < 200:
                                    print("You lost $" + "{:.2f}".format((200 -self.player.total)) + ". Thanks for playing! Come back any time!")

                                break
                            elif action.lower() == 'yes' or action.lower() == 'y':
                                self.muck_cards()
                            else:
                                self.muck_cards()
                                print("Not sure what you're tring to say...so let's play...")
                        else:
                            print()
                            print("Only thing left in those pockets of yours are broken dreams! You're broke! Hit the road!")
                            break

    def deal(self):
        self.clear_table()
        self.deck.shuffle_cards()

        # Dealer's cards
        self.hand.append(self.deck.card())
        self.hand.append(self.deck.card())

        self.display_item(self.seat,0,"Dealer:")
        self.display_item(self.seat,self.set_card_pos(self.card_count),self.hand[0]["card"])
        self.card_count += 1
        self.display_item(self.seat,self.set_card_pos(self.card_count),"[?]")
        self.card_count += 1

        # Player's cards
        self.display_item(self.player.seat,0,"Player:")
        self.player.hand.append(self.deck.card())
        self.player.hand.append(self.deck.card())
    
        for card in self.player.hand:
            self.display_item(self.player.seat,self.set_card_pos(self.player.card_count),card["card"])
            self.player.card_count += 1

    def display_item(self, seat, spacing, text):
        print(f'\033[{seat};{spacing}f{text}')
 
    def set_card_pos(self,card_count):
        time.sleep(.7) # pause for effect
        spacing = 10
        if card_count > 0:
            for c in range(card_count):
                spacing += 5
        return spacing

    def total_hand(self, hand):
        return sum(map(lambda card: card['value'], hand))

    def clear_table(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def muck_cards(self):
        self.hand.clear()
        self.card_count = 0
        self.player.hand.clear()
        self.player.card_count = 0        

class Player():
    def __init__(self):
        self.hand = []
        self.card_count = 0
        self.seat = 2
        self.bet = 0
        self.total = 200.00

class Deck():
    def __init__(self):
        self.cards = []
        self.suites = {"C":"\u2663","S":"\u2660","D":"\u2666","H":"\u2665"}
        self.values = ["A","K","Q","J",10,9,8,7,6,5,4,3,2]

    def card(self):
        #returns last card in deck
        return self.cards.pop()

    def shuffle_cards(self):
        #clear card list
        self.cards.clear()

        #re-populate card list
        for s in self.suites.values():
            for v in self.values:
                # set value of card
                val = 0
                if v == "A":
                    val = 11
                elif v == "K" or v == "Q" or v == "J":
                    val = 10
                else:
                    val = int(v)

                self.cards.append({"card":"["+str(v) + s +"]", "value": val})

        #randomize card list
        random.shuffle(self.cards)

init_dealer = Dealer()
init_dealer.play_blackjack()