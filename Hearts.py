from __future__ import print_function
from timeit import default_timer as timer

from Deck import Deck
from Card import Card, Suit, Rank
from Player import Player
from Trick import Trick
from PlayerTypes import PlayerTypes
from Variables import *
import Hand
import State

'''
Change auto to False if you would like to play the game manually.
This allows you to make all passes, and plays for all four players.
When auto is True, passing is disabled and the computer plays the
game by "guess and check", randomly trying moves until it finds a
valid one.
'''

#Players must be unique
allRandom = [Player("Random 1", PlayerTypes.Random), Player("Random 2", PlayerTypes.Random), 
						 Player("Random 3", PlayerTypes.Random), Player("Random 4", PlayerTypes.Random)]
allHuman = [Player("Human 1", PlayerTypes.Human), Player("Human 2", PlayerTypes.Human), 
					  Player("Human 3", PlayerTypes.Human), Player("Human 4", PlayerTypes.Human)]
oneHuman = [Player("Human 1", PlayerTypes.Human), Player("Random 2", PlayerTypes.Random), 
					  Player("Random 3", PlayerTypes.Random), Player("Random 4", PlayerTypes.Random)]
oneNaiveMin_allRandom = [Player("NaiveMin 1", PlayerTypes.NaiveMinAI), Player("Random 2", PlayerTypes.Random), 
					  				  Player("Random 3", PlayerTypes.Random), Player("Random 4", PlayerTypes.Random)]

oneNaiveMin_oneHuman = [Player("NaiveMin 1", PlayerTypes.NaiveMinAI), Player("Human 2", PlayerTypes.Human), 
					  				    Player("Random 3", PlayerTypes.Random), Player("Random 4", PlayerTypes.Random)]

oneNaiveMax_allRandom = [Player("NaiveMax 1", PlayerTypes.NaiveMaxAI), Player("Random 2", PlayerTypes.Random), 
					  				  Player("Random 3", PlayerTypes.Random), Player("Random 4", PlayerTypes.Random)]

oneNaiveMax_allNaiveMin = [Player("NaiveMin 1", PlayerTypes.NaiveMinAI), Player("NaiveMin 2", PlayerTypes.NaiveMinAI), 
					  				       Player("NaiveMin 3", PlayerTypes.NaiveMinAI), Player("NaiveMax 4", PlayerTypes.NaiveMaxAI)]

thePlayers = oneNaiveMin_allRandom

#Only necessary state is the current trick and all previously played tricks.
class Hearts:
	def __init__(self):

		self.roundNum = 0
		self.trickNum = 0 # initialization value such that first round is round 0
		self.dealer = -1 # so that first dealer is 0
		#self.passes = [1, -1, 2, 0] # left, right, across, no pass
		self.allTricks = []
		self.currentTrick = Trick()
		self.allTricks < self.currentTrick
		self.trickWinner = -1
		self.heartsBroken = False
		self.losingPlayer = None
		#self.passingCards = [[], [], [], []]


		# Make four players

		self.players = thePlayers

		'''
		Player physical locations:
		Game runs clockwise

			p3
		p2		p4
			p1

		'''

		# Generate a full deck of cards and shuffle it
		self.newRound()

	def handleScoring(self):
		p, highestScore = None, 0
		if printsOn:
			print ("\nScores:\n")
		shotMoon = False
		for player in self.players:
			if player.roundscore == 26:
				shotMoon = True
		for player in self.players:
			if shotMoon and player.roundscore != 26:
				player.score += 26
			elif not shotMoon:
				player.score += player.roundscore
			player.roundscore = 0
			if printsOn:
				print (player.name + ": " + str(player.score))
			if player.score > highestScore:
				p = player
				highestScore = player.score
			self.losingPlayer = p



	def newRound(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.roundNum += 1
		self.trickNum = 0
		self.trickWinner = -1
		self.heartsBroken = False
		self.dealer = (self.dealer + 1) % len(self.players)
		self.dealCards()
		self.currentTrick = Trick()
		self.allTricks = []
		#self.passingCards = [[], [], [], []]
		for p in self.players:
			p.discardTricks()

	def getFirstTrickStarter(self):
		for i,p in enumerate(self.players):
			if p.hand.contains2ofclubs:
				self.trickWinner = i

	def dealCards(self):
		i = 0
		while(self.deck.size() > 0):
			self.players[i % len(self.players)].addCard(self.deck.deal())
			i += 1


	def evaluateTrick(self):
		self.trickWinner = self.currentTrick.winner
		p = self.players[self.trickWinner]
		p.trickWon(self.currentTrick)
		self.printCurrentTrick()
		if printsOn:
			print (p.name + " won the trick.")
		# print 'Making new trick'
		self.currentTrick = Trick()
		self.allTricks < self.currentTrick
		if printsOn:
			print (self.currentTrick.suit)


	def passCards(self, index):
		print (self.printPassingCards())
		passTo = self.passes[self.trickNum] # how far to pass cards
		passTo = (index + passTo) % len(self.players) # the index to which cards are passed
		while len(self.passingCards[passTo]) < cardsToPass: # pass three cards
			passCard = None
			while passCard is None: # make sure string passed is valid
				passCard = self.players[index].play(option='pass')
				if passCard is not None:
					# remove card from player hand and add to passed cards
					self.passingCards[passTo].append(passCard)
					self.players[index].removeCard(passCard)

	def distributePassedCards(self):
		for i,passed in enumerate(self.passingCards):
			for card in passed:
				self.players[i].addCard(card)
		self.passingCards = [[], [], [], []]


	def printPassingCards(self):
		out = "[ "
		for passed in self.passingCards:
			out += "["
			for card in passed:
				out += card.__str__() + " "
			out += "] "
		out += " ]"
		return out


	def playersPassCards(self):

		self.printPlayers()
		if not self.trickNum % 4 == 3: # don't pass every fourth hand
			for i in range(0, len(self.players)):
				print # spacing
				self.printPlayer(i)
				self.passCards(i % len(self.players))

			self.distributePassedCards()
			self.printPlayers()

	#Check if a card is a valid play in the current state
	def isValidCard(self, card, player):
		if card is None:
			return False

		# if it is not the first trick and no cards have been played:
		if self.trickNum != 0 and self.currentTrick.cardsInTrick == 0:
			if card.suit == Suit(hearts) and not self.heartsBroken:
				# if player only has hearts but hearts have not been broken,
				# player can play hearts
				if not player.hasOnlyHearts():
					if printsOn:
						print ("Hearts have not been broken.")
					return False

		# player tries to play off suit but has trick suit
		# print(self.currentTrick.suit)
		# print (card)
		if self.currentTrick.suit != Suit(-1) and card.suit != self.currentTrick.suit:
			 if player.hasSuit(self.currentTrick.suit):
					if printsOn:
						print ("Must play the suit of the current trick.")
					return False

		#Can't play hearts or queen of spades on first hand
		if self.trickNum == 0:
			if card.suit == Suit(hearts):
				if printsOn:
					print ("Hearts cannot be broken on the first hand.")
				return False
			elif card.suit == Suit(spades) and card.rank == Rank(queen):
				if printsOn:
					print ("The queen of spades cannot be played on the first hand.")
				return False

	 #  #Can't lead with hearts unless hearts broken
		# if self.currentTrick.cardsInTrick == 0:
		# 	if card.suit == Suit(hearts) and not self.heartsBroken:
		# 		print ("Hearts not yet broken.")
		# 		return False

		#Valid otherwise
		return True

	#Can be edited to use isValidCard to make method more efficient
	def playTrick(self, start):
		shift = 0
		if self.trickNum == 0:
			startPlayer = self.players[start]
			addCard = startPlayer.play(option="play", c='2c')
			startPlayer.removeCard(addCard)

			self.currentTrick.addCard(addCard, start)

			shift = 1 # alert game that first player has already played

		# have each player take their turn
		for i in range(start + shift, start + len(self.players)):
			self.printCurrentTrick()
			curPlayerIndex = i % len(self.players)
			self.printPlayer(curPlayerIndex)
			curPlayer = self.players[curPlayerIndex]
			addCard = None

			while addCard is None: # wait until a valid card is passed


				addCard = curPlayer.play(auto=auto) # change auto to False to play manually
				# print(curPlayer.name, "playing: "),
				# print(addCard)

				# the rules for what cards can be played
				# card set to None if it is found to be invalid
				if addCard is not None:

					#set to None if card is invalid based on rules
					if self.isValidCard(addCard, curPlayer) == False:
						addCard = None
					else: 
						#change game state according to card

						#hearts broken
						if addCard.suit == Suit(hearts):
							self.heartsBroken = True
						if addCard.suit == Suit(spades) and addCard.rank == Rank(queen):
							self.heartsBroken = True

			curPlayer.removeCard(addCard)
			self.currentTrick.addCard(addCard, curPlayerIndex)

		self.evaluateTrick()
		self.trickNum += 1

	# print player's hand
	def printPlayer(self, i):
		p = self.players[i]
		if printsOn:
			print (p.name + "'s hand: " + str(p.hand))

	# print all players' hands
	def printPlayers(self):
		for p in self.players:
			if printsOn:
				print (p.name + ": " + str(p.hand))

	# show cards played in current trick
	def printCurrentTrick(self):
		trickStr = '\nCurrent table:\n'
		trickStr += "Trick suit: " + self.currentTrick.suit.__str__() + "\n"
		for i, card in enumerate(self.currentTrick.trick):
			if self.currentTrick.trick[i] is not 0:
				trickStr += self.players[i].name + ": " + str(card) + "\n"
			else:
				trickStr += self.players[i].name + ": None\n"
		if printsOn:
			print (trickStr)

	def getWinner(self):
		minScore = 200 # impossibly high
		winner = None
		for p in self.players:
			if p.score < minScore:
				winner = p
				minScore = p.score
		return winner

	#Plays a game and returns winning player
	def playGame(self):
		hearts = self
		# play until someone loses
		while hearts.losingPlayer is None or hearts.losingPlayer.score < maxScore:
			while hearts.trickNum < totalTricks:
				if printsOn:
					print ("Round", hearts.roundNum)
				if hearts.trickNum == 0:
					# if not auto:
					# 	hearts.playersPassCards()
					hearts.getFirstTrickStarter()
				if printsOn:
					print ('\nPlaying trick number', hearts.trickNum + 1)
				hearts.playTrick(hearts.trickWinner)

			# tally scores
			hearts.handleScoring()

			# new round if no one has lost
			if hearts.losingPlayer.score < maxScore:
				if printsOn:
					print ("New round")
				hearts.newRound()

		if printsOn:
			print # spacing
			print (hearts.getWinner().name, "wins!")

		winner = hearts.getWinner()

		#Game over: Reset all player fields
		for p in self.players:
			p.score = 0
			p.roundScore = 0
			p.hand = Hand.Hand()
			p.tricksWon = []

		return winner

def main():

	while True:
		try: 
			numGames = int(raw_input("How many games to play?\n"),10)
			break
		except ValueError:
			print("Not a valid number. Try again.")

	#Timing start
	start = timer()

	# Play numGames and store the number of times each player has won
	# Player names must be unique
	numWins = {thePlayers[0].name:0, thePlayers[1].name:0, thePlayers[2].name:0, thePlayers[3].name:0}

	for i in range(0,numGames):
		hearts = Hearts()
		State.state = hearts
		winningPlayer = hearts.playGame()
		numWins[winningPlayer.name] += 1

	#Timing end
	end = timer()

	p0 = thePlayers[0].name
	p0_wins = numWins[p0]
	p1 = thePlayers[1].name
	p1_wins = numWins[p1]
	p2 = thePlayers[2].name
	p2_wins = numWins[p2]
	p3 = thePlayers[3].name
	p3_wins = numWins[p3]
	print("-----------------------")
	print("Win Rates (Total Games:", numGames, ")")
	print("-----------------------")
	print(p0, ":" ,"%.2f%%"%(100 * float(p0_wins)/float(numGames))),
	print(p1, ":" ,"%.2f%%"%(100 * float(p1_wins)/float(numGames))),
	print(p2, ":" ,"%.2f%%"%(100 * float(p2_wins)/float(numGames))),
	print(p3, ":" ,"%.2f%%"%(100 * float(p3_wins)/float(numGames)))

	print("Time elapsed:", (end-start))


if __name__ == '__main__':
	main()
