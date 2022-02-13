"""
    The sprites module
    ==================

    Use it to import the different elements of the game.

    Available classes
    -----------------

    Player
    Mob
    Block
    |-> Ground
    |-> Platform
    Ribosome
    Amino_acid
    Features_panels
    Background
"""

from settings import *
import pygame as pg
from collections import deque
from pygame import mixer

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    """
        Use it to create the character controlled by the player.
    """

    d = {
        "jump": pg.transform.scale(pg.image.load("images/playjump.PNG"), (27, 50)),
        "stand": pg.transform.scale(pg.image.load("images/playstand.PNG"), (27, 50)),
        "run_right": [
            pg.transform.scale(pg.image.load("images/playrun1.PNG"), (34, 50)),
            pg.transform.scale(pg.image.load("images/playrun2.PNG"), (34, 50)),
        ],
        "run_left": [
            pg.transform.scale(
                pg.transform.flip(pg.image.load("images/playrun1.PNG"), True, False),
                (37, 50),
            ),
            pg.transform.scale(
                pg.transform.flip(pg.image.load("images/playrun2.PNG"), True, False),
                (37, 50),
            ),
        ],
    }

    def __init__(self, game):

        """
            This is the character builder.
            :type game: Game
        """
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = Player.d["stand"]
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.rect.center = self.pos
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.tmp_son = 1

        self.walking = False
        self.jumping = False
        self.last_update = 0
        self.current_frame = 0

    def jump(self):

        """
            This is the jump method of the character.
            If and only if the feet of the character are on a platform then it can jump.
        """

        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def update(self):

        """
            overridden method from pygame.sprite.Sprite
            update the movements of the character                         
        """
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()

        if keys[pg.K_q]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x < 0:
            self.pos.x = 0

        if self.pos.y > HEIGHT + 2000:
            self.game.playing = False

        if self.tmp_son and self.pos.y > HEIGHT:
            self.son()
            self.tmp_son = 0

        self.rect.bottomleft = self.pos

    def son(self):

        """this method loads the wilhelm cry that is played when the character falls from the ARNm sequence.
        """

        mixer.init()
        mixer.music.load("sounds/cri.mp3")
        mixer.music.play()

    def animate(self):

        """
            This is the animate method of the character.
            Update the sprite sheet of the character.
        """

        now = pg.time.get_ticks()

        if self.acc.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 2
                if self.vel.x > 0:
                    self.image = Player.d["run_right"][self.current_frame]
                else:
                    self.image = Player.d["run_left"][self.current_frame]

            bottomleft = self.rect.bottomleft
            self.rect = self.image.get_rect()
            self.rect.bottomleft = bottomleft
        else:
            self.image = Player.d["stand"]
            bottomleft = self.rect.bottomleft
            self.rect = self.image.get_rect()
            self.rect.bottomleft = bottomleft


class Mob(pg.sprite.Sprite):

    """
        Use it to create a character controlled by the computer.
    """

    def __init__(self, x, y):

        """
            This is the character builder.
            :param x: starting abscissa of the high left corner of the character 
            :param y: starting ordinate of the high left corner of the character
            :type x: int
            :type y: int
        """

        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/mob.PNG")
        self.image = pg.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)

    def update(self):

        """
            overridden method from pygame.sprite.Sprite
            update the movements of the character                         
        """

        self.pos.x -= 0
        self.pos.y += 10
        self.rect.bottomleft = self.pos


class Block(pg.sprite.Sprite):

    """
        This is the mother class of blocks used in game.
    """

    def __init__(self, x, y, w, h, c):

        """
            This is the Block  builder.
            :param x: abscissa of the high left corner of the object
            :param y: ordinate of the high left corner of the object
            :param w: width of the object
            :param h: height of the object
            :param c: image of the object
            :type x: int
            :type y: int
            :type w: int
            :type h: int
            :type c: Surface 
        """

        pg.sprite.Sprite.__init__(self)
        self.image = c
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform(Block):

    """
        Use it to create the platforms used in game.
    """

    d = {
        150: pg.image.load("images/150.PNG"),
        105: pg.image.load("images/105.PNG"),
        60: pg.image.load("images/60.PNG"),
    }

    def __init__(self, x, y, w, h, t):

        """
            This is the Platform  builder.
            :param x: abscissa of the high left corner of the platform
            :param y: ordinate of the high left corner of the platform
            :param w: width of the platform
            :param h: height of the platform
            :param t: type of platform
            :type x: int
            :type y: int
            :type w: int
            :type h: int
            :type t: int {150, 105, 60}
        """

        self.image = pg.transform.scale(Platform.d[t], (t, 35))
        Block.__init__(self, x, y, w, h, self.image)


class Ground(Block):

    """
        Use it to create to create the ground of the game.
        Each platform is a nucleotid.
    """

    d_sp = {
        "A_up": pg.image.load("images/A1.png"),
        "A_down": pg.image.load("images/A2.png"),
        "U_up": pg.image.load("images/U1.png"),
        "U_down": pg.image.load("images/U2.png"),
        "C_up": pg.image.load("images/C1.png"),
        "C_down": pg.image.load("images/C2.png"),
        "G_up": pg.image.load("images/G1.png"),
        "G_down": pg.image.load("images/G2.png"),
    }

    d = {"A": RED, "U": GREEN, "C": BLUE, "G": YELLOW}
    count = 0

    def __init__(self, x, y, w, h, nuc):

        """
            This is the Ground builder.
            :param x: abscissa of the high left corner of the nucleotid
            :param y: ordinate of the high left corner of the nucleotid
            :param w: width of the nucleotid
            :param h: height of the nucleotid
            :param nuc: type of nucleotid
            :type x: int
            :type y: int
            :type w: int
            :type h: int
            :type nuc: str
        """
        if Ground.count % 2:
            self.image = Ground.d_sp[nuc + "_up"]
        else:
            self.image = Ground.d_sp[nuc + "_down"]
        self.image = pg.transform.scale(self.image, (15, 54))
        Block.__init__(self, x, y, w, h, self.image)
        self.nuc = nuc
        Ground.last_g = self
        Ground.count += 1
        self.state = Ground.count


class Ribosome(pg.sprite.Sprite):

    """
        Use it to create a ribosome in the game.
    """

    def __init__(self, x, y):

        """
            This is the Ribosome builder
            :param x: abscissa of mid-bottom of the ribosome
            :param y: ordinate of mid-bottom of the ribosome
            :type x: int
            :type y: int
        """

        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/ribosome.png")
        self.image = pg.transform.scale(self.image, (300, 340))
        self.radius = 100
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)
        self.vitesse = 0
        self.prot = deque([])
        self.state = 0

    def update(self):

        """
            Overridden method from pygame.sprite.Sprite.
            Update the movements of the ribosome and 
            the protein being synthesized.
        """

        self.pos.x += self.vitesse
        self.pos.y += 0
        self.rect.midbottom = self.pos

        if self.rect.right > 40:
            self.state = 1

        if self.rect.right < 40 and self.state:
            self.pos.x = 40 - (300 / 2)

        if self.rect.left > (WIDTH + 100):
            self.state = 0
            self.pos.x = -500

        for i in range(len(self.prot)):
            self.prot[i].x = int(self.pos[0]) + (20 if i % 2 else 0)

    def add_aa(self, aa):

        """
            This method is used to add an amino acid to the protein
            being synthesized.
            :param aa: amino acid
            :type aa: Amino_acid
        """

        if len(self.prot) > 8:
            self.prot.pop()
            self.prot.appendleft(aa)
        else:
            self.prot.appendleft(aa)
        for i in range(len(self.prot)):
            self.prot[i].x = self.rect.center[0] + (20 if i % 2 else 0)
            self.prot[i].y = 340 - 50 * i


class Amino_acid:

    """
        Use it to create an amino acid.
    """

    def __init__(self, radius, text, game):

        """
            This is the Amino_acid builder
            :param radius: radius of the circle 
            :param text: label of the circle
            :type radius: int
            :type text: str
            :type game: Game
        """

        self.x = None
        self.y = None
        self.col = (140, 179, 217)
        self.radius = radius
        self.text = text
        self.game = game

    def draw(self, screen):

        """
            This method is used to draw an amino acid in the game.
            :type screen: Screen
        """

        pg.draw.circle(screen, self.col, (self.x, self.y), self.radius)
        self.game.write_text_on_screen(self.text, 10, BLACK, self.x, self.y - 10)


class Features_panels(pg.sprite.Sprite):

    """
        Use it to add panels in the game.
    """

    d = {
        "cds_5utr": pg.image.load("images/CDS_5_utr_panneau.png"),
        "codon_start": pg.image.load("images/start_panneau.png"),
        "codon_stop": pg.image.load("images/stop_3_utr_panneau.png"),
    }

    d_dim = {
        "cds_5utr": (275, 275),
        "codon_start": (275, 275),
        "codon_stop": (165, 165),
    }

    def __init__(self, x, y, i):

        """
            This is the Features_panels builder
            :param x: abscissa of the high left corner of the panel
            :param y: ordinate of the high left corner of the panel
            :param i: type of panel
            :type x: int
            :type y: int
            :type i: str {"cds_5utr", "codon_start", "codon_stop"}
        """
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(Features_panels.d[i], Features_panels.d_dim[i])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Background(pg.sprite.Sprite):

    """
        Use it to add background in the game.
    """

    image = pg.image.load("images/background.png")

    def __init__(self, x, y):

        """
            This is the Background builder
            :param x: abscissa of the high left corner of the background
            :param y: ordinate of the high left corner of the background
            :type x: int
            :type y: int
        """

        pg.sprite.Sprite.__init__(self)
        self.rect = Background.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        Background.last_back = self
