from random import randint
import sys
from Card import Card, Suit

clubs = 0
diamonds = 1
spades = 2
hearts = 3
suits = ["c", "d", "s", "h"]

class Hand:
	def __init__(self):

		self.clubs = []
		self.diamonds = []
		self.spades = []
		self.hearts = []
		
		# create hand of cards split up by suit
		self.hand = [self.clubs, self.diamonds, 
					self.spades, self.hearts]

		self.contains2ofclubs = False

	def size(self):
		return len(self.clubs) + len(self.diamonds) + len(self.spades) + len(self.hearts)

	def addCard(self, card):
		if card.suit == Suit(clubs):
			if card.rank.rank == 2:
				self.contains2ofclubs = True
			self.clubs.append(card)
		elif card.suit == Suit(diamonds):
			self.diamonds.append(card)
		elif card.suit == Suit(spades):
			self.spades.append(card)
		elif card.suit == Suit(hearts):
			self.hearts.append(card)
		else:
			print 'Invalid card'

		if self.size() == 13:
			for suit in self.hand:
				suit.sort()

	def updateHand(self):
		self.hand = [self.clubs, self.diamonds, 
					self.spades, self.hearts]

	def getRandomCard(self):
		suit = randint(0,3)
		suit = self.hand[suit]
		while len(suit) == 0:
			suit = randint(0,3)
			suit = self.hand[suit] 
		index = randint(0, len(suit)-1)

		return suit[index]



	def strToCard(self, card):
		if len(card) == 0: return None
		
		suit = card[len(card)-1].lower() # get the suit from the string
		
		try:
			suitIden = suits.index(suit)
		except:
			print 'Invalid suit'
			return None

		cardRank = card[0:len(card)-1] # get rank from string
		
		try:
			cardRank = cardRank.upper()
		except AttributeError:
			pass

		# convert rank to int
		if cardRank == "J":
			cardRank = 11
		elif cardRank == "Q":
			cardRank = 12
		elif cardRank == "K":
			cardRank = 13
		elif cardRank == "A":
			cardRank = 14
		else:
			try:
				cardRank = int(cardRank)
			except:
				print "Invalid card rank."
				return None

		return cardRank, suitIden

	def containsCard(self, cardRank, suitIden):
		for card in self.hand[suitIden]:
			if card.rank.rank == cardRank:
				cardToPlay = card
					
				# remove cardToPlay from hand
				# self.hand[suitIden].remove(card)
				
				# update hand representation
				# self.updateHand()
				return cardToPlay
		return None

	def playCard(self, card):
		cardInfo = self.strToCard(card)

		if cardInfo is None:
			return None
		else:
			cardRank, suitIden = cardInfo[0], cardInfo[1]
		
		# see if player has that card in hand
		return self.containsCard(cardRank, suitIden)

	def removeCard(self, card):
		suitId = card.suit.iden
		for c in self.hand[suitId]:
			if c == card:
				if suitId == clubs and card.rank.rank == 2:
					self.contains2ofclubs = False
				# print "Removing:", c.__str__()
				self.hand[card.suit.iden].remove(c)
				self.updateHand()

	def hasOnlyHearts(self):
		# print "len(self.hearts):",len(self.hearts)
		# print "self.size():",self.size()
		return len(self.hearts) == self.size()

	def __str__(self):
		handStr = ''
		for suit in self.hand:
			for card in suit:
				handStr += card.__str__() + ' '
		return handStr

#-----------------NEW METHODS-----------------------

	#takes in a array of cards and returns the one with the lowest rank
	@staticmethod
	def lowestCard(card_arr):
		# if(len(card_arr)==0): print("card_arr empty!")
		min_rank = sys.maxsize
		min_card = None
		for card in card_arr:
			if card.rank.rank < min_rank:
				min_card = card
				min_rank = card.rank.rank
		# if min_card is None: print("min card is none!")
		return min_card

	@staticmethod
	#takes in a hand of cards split in to 4 suit arrays and returns a random card
	def randomCard(validHand):
		suit = randint(0,3)
		suit = validHand[suit]
		while len(suit) == 0:
			suit = randint(0,3)
			suit = validHand[suit] 
		index = randint(0, len(suit)-1)
		return suit[index]

	@staticmethod
	def highestCard(card_arr):
		# if(len(card_arr)==0): print("card_arr empty!")
		max_rank = -sys.maxsize
		max_card = None
		for card in card_arr:
			if card.rank.rank > max_rank:
				max_card = card
				max_rank = card.rank.rank
		# if min_card is None: print("min card is none!")
		return max_card


