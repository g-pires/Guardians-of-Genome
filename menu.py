"""
	The menu module
	===============

	Use it to create the menu.

	Available classes
	-----------------

	Menu
"""
from tkinter import *
from settings import *
import main
from rank import *
from tkinter import filedialog
import intro


class Menu:
    """
		This is the menu class of the platforms game.
	"""

    def __init__(self, fenetre):

        """
			This is the menu builder, it initializes the main menu window.
			:param fenetre: the window used to create the menu
		"""
        #intro.generique()
        self.rank = Rank(self, "rank.txt")
        self.fenetre = fenetre
        self.fenetre.title("Menu")
        self.fenetre.geometry("800x600+50+50")
        self.fenetre.configure(bg="lightSteelBlue2")

        # handle the title (name, font, background).
        self.textes = "Guardians of genome"
        self.label = Label(
            self.fenetre,
            text=self.textes,
            justify=CENTER,
            bg="lightSteelBlue2",
            font=("Times", 30, "bold"),
        )
        self.label.configure(fg="grey21")
        self.label.pack()

        # handle the play button.
        self.photo_joue = PhotoImage(file="images/jouer.png")
        self.joue = Button(
            self.fenetre,
            text="Jouer",
            command=self.Pseudo,
            image=self.photo_joue,
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
        )
        self.joue.pack(side=TOP, expand=YES)

        # handle the options button.
        self.photo_sett = PhotoImage(file="images/options.png")
        self.sett = Button(
            self.fenetre,
            text="Paramètres",
            command=self.Settings,
            image=self.photo_sett,
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
        )
        self.sett.pack(side=TOP, expand=YES)

        # handle the rank button.
        self.photo_rang = PhotoImage(file="images/classement.png")
        self.rang = Button(
            self.fenetre,
            text="Classement",
            command=self.Rang,
            image=self.photo_rang,
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
        )
        self.rang.pack(side=TOP, expand=YES)

        # handle the quit button.
        self.photo_quitter = PhotoImage(file="images/quitter_rouge.png")
        self.quitte = Button(
            self.fenetre,
            text="Quitter",
            command=self.Quitter,
            image=self.photo_quitter,
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
        )
        self.quitte.pack(side=TOP, expand=YES)

    def Pseudo(self):
        """
			This is the function that handle the Pseudo.
			You can change your pseudo and then play to the game.
		"""
        self.fenetre_pseudo = Tk()
        self.fenetre_pseudo = self.fenetre_pseudo
        self.fenetre_pseudo.geometry("800x600+50+50")
        self.fenetre_pseudo.configure(bg="lightSteelBlue2")
        self.p = StringVar(self.fenetre_pseudo)
        self.p.set("")

        def get_p(event):
            """
				Function used to get the pseudo value from the rank class.
				:param event: when <Enter> is pressed in the entry button.
			"""
            self.rank.pseudo = str(self.p.get())
            return self.rank.pseudo

            # handle the title label

        self.textes = "Choisissez un pseudo"
        self.label = Label(
            self.fenetre_pseudo,
            text=self.textes,
            justify=CENTER,
            bg="lightSteelBlue2",
            font=("Times", 30, "bold"),
        )
        self.label.configure(fg="grey21")
        self.label.pack(side=TOP, expand=YES)

        # handle the entry and textes aids
        self.frame2 = Frame(self.fenetre_pseudo, bg="lightSteelBlue2", height=400)
        self.pseudo_texte_aide = Label(
            self.frame2,
            text="Appuyez sur <Entrée> pour confirmer le pseudo",
            bg="lightSteelBlue2",
            font=10,
        )
        self.pseudo_texte_aide.grid(row=5, column=0, columnspan=3)
        self.pseudo_texte = Label(
            self.frame2,
            text="          Entrez un pseudo",
            bg="lightSteelBlue2",
            font=10,
        )
        self.pseudo_texte.grid(row=1, column=0)
        self.pseudo_button = Entry(self.frame2, textvariable=self.p)
        self.pseudo_button.grid(row=1, column=1)
        self.pseudo_button.bind("<Return>", get_p)

        self.frame2.pack(side=TOP, expand=YES)

        self.photo_joue2 = PhotoImage(
            master=self.fenetre_pseudo, file="images/jouer.png"
        )
        self.joue2 = Button(
            self.fenetre_pseudo,
            text="Jouer",
            command=self.Jouer,
            image=self.photo_joue2,
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
        )
        self.joue2.pack(side=TOP, expand=YES)

        # handle the quit button.
        self.photo_retour3 = PhotoImage(
            master=self.fenetre_pseudo, file="images/retour_rouge.png"
        )
        self.retour3 = Button(
            self.fenetre_pseudo,
            command=self.Retour3,
            image=self.photo_retour3,
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
        )
        self.retour3.pack(side=TOP, expand=YES)

        self.fenetre_pseudo.mainloop()

    def Jouer(self):
        """
			This is the method that runs the game when you click on the play button.
			If you submited a new sequence it will launch with this sequence,
			otherwise it will launch with the default sequence.
		"""
        try:
            main.men(self.rank, self.file)
        except:
            main.men(self.rank, SEQ)

    def Settings(self):
        """
			This is the settings function that handle the settings window.
			You can either see the commandes or import your own sequence. 
			The sequence has to be a .gb file, the ARNm sequence 
			and the protein sequence has to be on it. 
		"""
        self.fenetre2 = Tk()
        self.fenetre2 = self.fenetre2
        self.fenetre2.geometry("800x600+50+50")
        self.fenetre2.configure(bg="lightSteelBlue2")

        self.textes = "Options"
        self.label = Label(
            self.fenetre2,
            text=self.textes,
            justify=CENTER,
            bg="lightSteelBlue2",
            font=("Times", 30, "bold"),
        )
        self.label.configure(fg="grey21")
        self.label.pack()

        self.photo_commandes = PhotoImage(
            master=self.fenetre2, file="images/commandes_bleu.png"
        )
        self.commandes = Button(
            self.fenetre2,
            command=self.Commandes,
            image=self.photo_commandes,
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
        )
        self.commandes.pack(side=TOP, expand=YES)

        self.photo_parametres = PhotoImage(
            master=self.fenetre2, file="images/parametres_bleu.png"
        )

        self.frame = Frame(self.fenetre2, bg="lightSteelBlue2")

        self.browserbutton_texte = Label(
            self.frame, text="Importez une séquence \n ", bg="lightSteelBlue2", font=10
        )
        self.browserbutton_texte.grid(row=0, sticky=E)
        self.browserbutton = Button(
            master=self.frame,
            text="Browser",
            command=self.Browser,
            bg="lightSteelBlue2",
        )
        self.browserbutton.grid(row=2, column=0)

        self.frame.pack(side=TOP, expand=YES)

        self.photo_retour = PhotoImage(
            master=self.fenetre2, file="images/retour_rouge.png"
        )
        self.retour = Button(
            self.fenetre2,
            command=self.Retour,
            image=self.photo_retour,
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
        )
        self.retour.pack(side=TOP, expand=YES)

        self.fenetre2.mainloop()

    def Retour(self):
        """
			This the return button to come back to the previous 
			window by destroying the actual window.
		"""
        self.fenetre2.destroy()

    def Retour3(self):
        """
			This the return button to come back to the previous 
			window by destroying the actual window.
		"""
        self.fenetre_pseudo.destroy()

    def Browser(self):
        """
			This function is used to change the mRNA sequence of the game.
		"""
        self.pathlabel = Label(self.fenetre2)
        self.file = filedialog.askopenfilename()
        self.pathlabel.config(text=self.file)
        self.pathlabel.pack()
        self.fenetre2.deiconify()

    def Rang(self):
        """
			This function creates the rank board. 
			You can either see your pseudo, the sequence ID you play with, your highscore, and your achievements of the sequence.
			There is also the link to the dictionnary.
		"""
        self.fenetre4 = Tk()
        self.fenetre4 = self.fenetre4
        self.fenetre4.geometry("900x600+50+50")
        self.fenetre4.configure(bg="lightSteelBlue2")

        def Display():
            """
				Function used to display the board filled.
			"""
            self.rank.fill_board(self.d.get(), self.frame3)

        self.d = StringVar(self.fenetre4)
        try:
            self.d.set(self.rank.board[0])
        except:
            self.d.set("Choix de la séquence")

        self.frame3 = Frame(self.fenetre4)
        self.frame3.pack(anchor="n")

        self.frame4 = Frame(self.fenetre4, bg="lightSteelBlue2")
        self.display_option = OptionMenu(
            self.frame4,
            self.d,
            *self.rank.board if len(self.rank.board) > 0 else ["None"]
        )
        self.display_option.config(
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
            relief="raise",
        )
        self.display_option.pack(anchor="s")

        self.display = Button(
            self.frame4,
            text="Actualiser",
            command=Display,
            bg="lightSteelBlue2",
            highlightbackground="lightSteelBlue2",
            activebackground="lightSteelBlue2",
            relief="raise",
        )
        self.display.pack(anchor="s")

        self.frame4.pack(anchor="s")

        # handle the quit button.
        self.photo_quitter_rank_screen = PhotoImage(
            master=self.fenetre4, file="images/quitter_rouge.png"
        )
        self.quitte_rank_screen = Button(
            self.fenetre4,
            text="Quitter",
            command=self.Quitter_rank,
            image=self.photo_quitter_rank_screen,
            bg="lightSteelBlue2",
            borderwidth=0,
            highlightbackground="lightSteelBlue2",
            highlightcolor="lightSteelBlue2",
            activebackground="lightSteelBlue2",
        )
        self.quitte_rank_screen.pack(side=BOTTOM)

        self.rank.fill_board(0, self.frame3)

        self.fenetre4.mainloop()

    def Quitter(self):
        """
			This function is used to quit the menu.
		"""
        self.fenetre.destroy()

    def Quitter_rank(self):
        """
			This function is used to quit the rank screen.
		"""
        self.fenetre4.destroy()

    def Commandes(self):
        """
			This is the commands function. 
			It is used to be aware of the keys to press to play the game.
		"""
        self.fenetre3 = Tk()
        self.fenetre3 = self.fenetre3
        self.fenetre3.geometry("960x500+50+50")
        self.fenetre3.configure(bg="white")

        # image in the background
        self.canvas = Canvas(self.fenetre3, bg="white", height=250, width=300)

        self.image_commandes = Image.open("images/touches.png")
        self.fichier = ImageTk.PhotoImage(
            master=self.fenetre3, image=self.image_commandes
        )

        self.labelCommandes = Label(master=self.fenetre3, image=self.fichier)
        self.labelCommandes.fichier = self.fichier
        self.labelCommandes.place(x=0, y=0, relwidth=1, relheight=1)

        self.canvas.pack()

        self.fenetre3.mainloop()


if __name__ == "__main__":
    fenetre = Tk()
    Menu(fenetre)
    fenetre.mainloop()
