import random

from dealer import Dealer
from deck import Deck
from player import Player

class Game():
    def __init__(self,deckAmount):
        self.deck = Deck(deckAmount)

        bankroll = 1e7
        self.betAmount = 10
        self.originalbet = 10
        self.player = Player("p1",bankroll,self.betAmount)
        self.dealer = Dealer()




    def play_round(self):
        self.betAmount = self.originalbet
        self.player.hand.cards = []
        self.dealer.hand.cards = []
        for i in range(2):
            self.player.hand.cards.append(self.deck.draw())
            self.dealer.hand.cards.append(self.deck.draw())

        if self.dealer.hand.value() == 21:
            if self.player.hand.value() != 21:
                self.player.amountWon = self.player.amountWon - self.betAmount
                self.dealer.amountWon = self.dealer.amountWon + self.betAmount
                self.dealer.gamesWon +=1
                self.player.totalBet +=self.betAmount
                return
            else:
                return

        if self.player.hand.value() == 21:
            self.player.amountWon = self.player.amountWon + 1.5* self.betAmount
            self.dealer.amountWon = self.dealer.amountWon - 1.5*self.betAmount
            self.player.gamesWon += 1
            self.player.totalBet += self.betAmount
            return

        while self.player.is_bust() == False:
            player_move = self.player.play_hand(self.dealer.hand.cards[0])
            if player_move == "stand":
                break
            elif player_move == "double":
                self.player.hand.cards.append(self.deck.draw())
                self.betAmount = 2 * self.player.bet
                break
            else:
                self.player.hand.cards.append(self.deck.draw())

        if self.player.is_bust():
            self.player.amountWon = self.player.amountWon - self.betAmount
            self.dealer.amountWon = self.dealer.amountWon + self.betAmount
            self.dealer.gamesWon += 1
            self.player.totalBet += self.betAmount
            return

        else:
            while self.dealer.play_hand() != "stand":
                self.dealer.hand.cards.append(self.deck.draw())
                if self.dealer.hand.value() > 21:
                    break
            if self.dealer.hand.value() > 21 or self.dealer.hand.value() < self.player.hand.value():
                self.player.amountWon = self.player.amountWon + self.betAmount
                self.dealer.amountWon = self.dealer.amountWon - self.betAmount
                self.player.gamesWon += 1
                self.player.totalBet += self.betAmount
            elif self.dealer.hand.value() == self.player.hand.value():
                return
            else:
                self.player.amountWon = self.player.amountWon - self.betAmount
                self.dealer.amountWon = self.dealer.amountWon + self.betAmount
                self.dealer.gamesWon += 1
                self.player.totalBet += self.betAmount









def main():

    game = Game(1)
    gamesPlayed = 1000000
    for i in range(gamesPlayed):
        game.play_round()

    print("The player won",game.player.gamesWon, "games")
    print("The dealer won",game.dealer.gamesWon,"games")
    print("The player won ",game.player.amountWon)
    print("The dealer won ",game.dealer.amountWon)
    print("Dealer's edge", game.dealer.amountWon/game.player.totalBet *100)

if __name__ == '__main__':
    main()
