"""
	The game_over module
	===============

	Use it to create the Game Over screen.

	Available classes
	-----------------

	Game_over
"""

from tkinter import *
import main
import menu
from rank import *


class Game_over:
    """
		This Game_over class of the platforms game.
	"""

    def __init__(self, g, lab, id_s, score, a, p):
        """
			This is the Game Over builder, it initializes the rank, 
			the main go window with the title (Game Over), 
			the replay button and quitt button,
			and calls the draw_board (affiche_board) function.
			:param g: the link to the game class.
			:param lab: the text to display on screen, 
			if won : 'Well played'
			else : 'Game Over'
			:param id_s: the id of the sequence the player played with.
			:param score: the score that did the player.
			:param a: the achievement of the player.
			:param p: the pseudo of the player.
		"""
        self.p = p
        self.a = a
        self.score = score
        self.id_s = id_s
        self.g = g
        self.rank = Rank(self, "rank.txt")
        self.fenetre_go = Tk()
        self.fenetre_go.title(lab)
        self.fenetre_go.geometry("1000x600+50+50")
        self.fenetre_go.configure(bg="lightSteelBlue2")

        self.go_textes = lab
        self.go_label = Label(
            self.fenetre_go,
            text=self.go_textes,
            justify=CENTER,
            bg="lightSteelBlue2",
            font=("Times", 30, "bold"),
        )
        self.go_label.configure(fg="grey21")
        self.go_label.pack()

        # handle the resume label.
        self.resume = (
            "Vous avez fait un score de "
            + str(self.score)
            + " en parcourant "
            + str(self.a)
            + "%"
            + " de la séquence"
        )
        self.label_resume = Label(
            self.fenetre_go,
            text=self.resume,
            justify=CENTER,
            bg="lightSteelBlue2",
            font=("Times", 10, "bold"),
        )
        self.label_resume.pack()

        # handle the quit button.
        self.photo_quitter_go_screen = PhotoImage(
            master=self.fenetre_go, file="images/quitter_rouge.png"
        )
        self.quitte_go_screen = Button(
            self.fenetre_go,
            text="Quitter",
            command=self.Quitter_go,
            image=self.photo_quitter_go_screen,
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
        )
        self.quitte_go_screen.pack(side=BOTTOM)

        # handle the replay button.
        self.photo_replay = PhotoImage(master=self.fenetre_go, file="images/replay.png")
        self.replay = Button(
            self.fenetre_go,
            text="Quitter",
            command=self.Rejouer,
            image=self.photo_replay,
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
        )
        self.replay.pack(side=BOTTOM)

        self.affiche_board()
        self.fenetre_go.mainloop()

    def Quitter_go(self):
        """
			This function is used to quit the game over screen.
			Use del self to delete everything that is running from the game.
		"""
        self.g.running = False
        self.fenetre_go.quit()
        self.fenetre_go.destroy()
        del self

    def Rejouer(self):
        """
			The function used to restart the game after a Game Over.
		"""
        self.fenetre_go.quit()
        self.fenetre_go.destroy()

    def affiche_board(self):
        """
			The function used to display the board on the Game Over screen.
		"""
        # self.d = StringVar(self.fenetre_go)

        self.frame_go = Frame(self.fenetre_go, bg="lightSteelBlue2")
        self.canvas_go = Canvas(self.frame_go, bg="lightSteelBlue2")
        self.rank.fill_board(self.id_s, self.canvas_go)
        self.frame_go.pack(anchor="n")

        self.frame4 = Frame(self.fenetre_go, bg="lightSteelBlue2")
        self.frame4.pack(anchor="s")
        self.canvas_go.grid(row=0, column=0, rowspan=30, columnspan=4)
        self.canvas_go.configure(
            borderwidth=0,
            bg="lightSteelBlue2",
            highlightbackground="lightSteelBlue2",
            selectbackground="lightSteelBlue2",
            selectforeground="lightSteelBlue2",
        )

    def colougrey21(self):
        for i in self.rank.board:
            for j in self.rank.board[i]:
                if j[0] == self.p and j[1] == self.score and j[2] == str(self.a) + "%":
                    canvas_line.create_line(900, j, 890, j, arrow="last")
