"""
	The rank module
	===============

	Use it to create the rank.

	Available classes
	-----------------

	Rank
"""

from main import *
from tkinter import *


class Rank:
    """
		This is the rank class of the platforms game.
	"""

    def __init__(self, menu, path):
        """
			This is the Rank builder.
			:param menu: a link to the menu class
			:pram path: the path to the file where the rank is saved. 
		"""

        self.menu = menu
        self.pseudo = ""
        self.seq = ""
        self.s = ""
        self.a = ""
        self.path = path

        with open(path, "r") as infile:
            try:
                self.board = eval(infile.read().rstrip())
            except:
                self.board = dict()

    def add_player(self, seq, s, a):
        """
			This is the function that creates a new player.
			Each new player has a pseudo, a sequence (the one he plays with),
			a high score and an achievement (both calculated after the game).
			:param seq: the sequence id of the new player.
			:param s: the score of the new player.
			:param a: the achievement of the new player.
		"""

        self.sequence = seq
        self.score = s
        self.achievements = str(a) + "%"

        if self.sequence not in self.board:
            self.board[self.sequence] = [(self.pseudo, self.score, self.achievements)]
        else:
            self.board[self.sequence].append(
                (self.pseudo, self.score, self.achievements)
            )
            self.board[self.sequence] = sorted(
                self.board[self.sequence], key=lambda x: x[1], reverse=True
            )
            if len(self.board[self.sequence]) > 16:
                self.board[self.sequence].pop()

    def fill_board(self, k, fenetre):

        """
			This is the function that fills the rank board when
			a new player is registered.
			param k: the sequence id the player played with.
			param fenetre: the window on which you choose to display the rank board.
		"""
        self.f = fenetre
        cnt = 0
        if k in self.board:
            l = self.board[k]
            cnt += 1
        else:
            l = []

        matrix = [[0 for j in range(4)] for i in range(len(l) + 1)]
        for i in range(len(l) + 1):
            for j in range(4):
                matrix[i][j] = Label(self.f, relief=RIDGE, width=int(28))
                matrix[i][j].grid(row=i, column=j)
                matrix[i][j].configure(bg="lightSteelBlue2")

        header = ["Séquence", "Pseudo", "Score", "Achievements"]
        for i in range(len(header)):
            matrix[0][i]["text"] = header[i]

        if l:
            for i in range(1, len(l) + 1):
                matrix[i][0]["text"] = k
                for j in range(1, 4):
                    matrix[i][j]["text"] = l[i - 1][j - 1]

    def save_data(self):
        """
			This function is handling the save of the rank dictionnary.
		"""
        with open(self.path, "w") as infile:
            infile.write(str(self.board))
