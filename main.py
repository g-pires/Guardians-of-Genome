"""
	The main module
	===============

	Use it to create the game.

	Available classes
	-----------------

	Game
"""

import pygame as pg
import random
from settings import *
from game_over import *
from sprites import *
from Bio import SeqIO
from os import path
from rank import *
from menu import *
from pygame import mixer


class Game:

    """
		This is the main class of the platforms game.
	"""

    def __init__(self, r, f):

        """
			This is the game builder.
                        :param r: rank management object
                        :param f: genbank file
                        :type r: Rank
                        :type f: str

		"""
        self.rank = r
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.gb = SeqIO.read(f, "gb")
        self.pos_start_codon = [
            int(i.location.start) for i in self.gb.features if i.type == "CDS"
        ][0]
        self.pos_stop_codon = [
            int(i.location.end) for i in self.gb.features if i.type == "CDS"
        ][0]
        self.seq = str(self.gb.seq).translate(str.maketrans("T", "U"))
        self.prot = [
            i.qualifiers["translation"][0] for i in self.gb.features if i.type == "CDS"
        ][0]
        # self.pos_start_codon=150
        # self.pos_stop_codon=280
        self.id = str(self.gb.id)
        self.s = self.id
        self.font_name = pg.font.match_font("arial")

    def new(self):

        """
			This is the level builder.
			The mains groups of sprites are defined.
			Some constants are initialized.
		"""

        self.last_state_score = 0
        self.achievement = 0
        self.score = 0
        self.pseudo = ""
        self.all_sprites = pg.sprite.Group()

        self.cds = Features_panels(30, 350, "cds_5utr")
        self.panel = pg.sprite.Group()
        self.panel.add(self.cds)

        self.platforms = pg.sprite.Group()
        for i in self.seq[:100]:
            g = Ground(Ground.count * 15, HEIGHT - 40, 15, 40, i)
            if g.state == self.pos_start_codon:
                start_codon = Features_panels(Ground.count * 20, 375, "codon_start")
                self.panel.add(start_codon)
            if g.state == self.pos_stop_codon:
                stop_codon = Features_panels(Ground.count * 20, 420, "codon_stop")
                self.panel.add(stop_codon)
            self.platforms.add(g)
            self.all_sprites.add(g)

        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.mobs = pg.sprite.Group()
        self.plat2 = pg.sprite.Group()
        self.ribo = Ribosome(-250, HEIGHT + 60)
        self.all_sprites.add(self.ribo)
        self.ribo_gr = pg.sprite.Group()
        self.ribo_gr.add(self.ribo)

        for i in PLATFORM_LIST:
            p = Platform(*i)
            self.all_sprites.add(p)
            self.platforms.add(p)
            self.plat2.add(p)

        self.escape = 0
        self.mobs_timer = 0
        self.last_aa = -1
        self.indice_plat = 0

        background1 = Background(0, 0)
        background2 = Background(1000, 0)
        self.gr_Background = pg.sprite.Group()
        self.gr_Background.add(background1)
        self.gr_Background.add(background2)

        self.run()
        if self.won:
            Game_over(
                self,
                "Well played",
                self.s,
                self.last_state_score + self.score,
                self.achievement,
                self.rank.pseudo,
            )
        else:
            Game_over(
                self,
                "Game over",
                self.s,
                self.last_state_score + self.score,
                self.achievement,
                self.rank.pseudo,
            )

    def run(self):

        """
			This is the main loop of the level.
		"""

        self.playing = True
        #self.son()
        self.won = False
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        Ground.count = 0
        if not self.rank.pseudo:
            self.rank.pseudo = "Invité"
        self.rank.add_player(
            self.s, self.last_state_score + self.score, self.achievement
        )
        self.rank.save_data()

    def events(self):

        """
			This is the events loop.
			The loop checks actions from the user.
		"""

        for event in pg.event.get():

            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def update(self):

        """
			This function update the state of all elements in the 
			level before they are displayed.
		"""

        self.all_sprites.update()
        self.check_player_platforms_collide()
        self.check_mobs_player_collide()
        self.check_mobs_ribo_collide()
        self.check_mobs_platforms_collide()
        self.check_player_ribo_collide()
        self.check_ribo_ground_collide()
        self.generate_mobs()
        self.generate_platforms()
        self.shift_world()

    def draw(self):

        """
			At each call of this function, the elements of the level
			are displayed on a black screen.
		"""

        self.gr_Background.draw(self.screen)
        self.panel.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.ribo_gr.draw(self.screen)
        for i in self.ribo.prot:
            i.draw(self.screen)

        self.write_text_on_screen(
            "Score : "
            + str(self.score + self.last_state_score)
            + "    "
            + str(self.achievement)
            + "%",
            22,
            BLACK,
            WIDTH / 2,
            15,
        )
        pg.display.flip()

    def write_text_on_screen(self, text, size, color, x, y):

        """
			This is the function that draws a text on the screen.
		"""

        font = pg.font.Font(self.font_name, 24)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def check_player_platforms_collide(self):

        """
			This method checks if the character is colliding with 
			a platform during his jump.
		"""

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if type(hits[0]) == Ground:
                    if hits[0].state > self.last_state_score:
                        self.last_state_score = hits[0].state
                        self.achievement = min(
                            round(
                                (self.last_state_score / (self.pos_stop_codon + 40))
                                * 100,
                                2,
                            ),
                            100,
                        )
                    if hits[0].state > 25:
                        self.ribo.vitesse = 4
                    if hits[0].state > self.pos_stop_codon + 40:
                        self.won = True
                        self.playing = False
                if self.player.pos.y < hits[0].rect.bottom:
                    self.player.pos.y = hits[0].rect.top + 0.1
                    self.player.vel.y = 0

    def check_mobs_player_collide(self):

        """
			This method checks if the character is colliding with 
			some monsters. 
		"""

        hit_mob = pg.sprite.spritecollide(self.player, self.mobs, False)
        if hit_mob:
            if (
                self.player.vel.y > 0
                and self.player.rect.bottom < hit_mob[0].rect.bottom
            ):
                hit_mob[0].kill()
                self.score += 5
            else:
                self.playing = False

    def check_mobs_platforms_collide(self):

        """
			This method checks if monsters are colliding with 
			the platforms. 
		"""

        hit_mob = pg.sprite.groupcollide(self.mobs, self.platforms, False, False)
        for mob, plat in hit_mob.items():
            mob.pos.y = plat[0].rect.top - 1
            mob.rect.bottom = plat[0].rect.top - 1
            mob.pos.x -= random.randint(1, MAX_SPEED_MOB)

    def check_mobs_ribo_collide(self):

        """
            This method checks if monsters are colliding with 
            a ribisome.
        """

        pg.sprite.spritecollide(self.ribo, self.mobs, True, pg.sprite.collide_circle)

    def check_player_ribo_collide(self):

        """
            This method checks if the player is colliding with 
            a ribosome
        """

        hit = pg.sprite.spritecollide(
            self.player, self.ribo_gr, False, pg.sprite.collide_circle
        )
        if hit:
            self.playing = False

    def check_ribo_ground_collide(self):

        """
            This method checks if the ribo is colliding with nucleotids 
            from the CDS. 
        """

        hits = pg.sprite.spritecollide(self.ribo, self.platforms, False)
        if hits:
            if type(hits[0]) == Ground and hits[0].state >= self.pos_stop_codon:
                self.ribo.vitesse = 0
                self.ribo.state = 0
            elif type(hits[0]) == Ground and hits[0].state >= self.pos_start_codon:
                aa = (hits[0].state - self.pos_start_codon) // 3
                if self.last_aa != aa:
                    self.ribo.add_aa(Amino_acid(27, self.prot[aa], self))
                    self.last_aa = aa

    def shift_world(self):

        """
			This method moves all the elements of the level towards
			the left when the player is moving to the right. The elements
			coming out of the screen are "killed". Wich means that they
			are removed from the sprties groups who they are belong.
		"""

        if self.player.rect.right > 5 / 8 * WIDTH:
            diff = self.player.rect.right - 5 / 8 * WIDTH
            self.player.pos.x -= diff
            tmp = False
            for plat in self.platforms:
                plat.rect.x -= diff
                if plat.rect.right < 0:
                    if type(plat) == Ground:
                        tmp = True
                    k = random.randint(1, 1000)
                    if k > 990:
                        self.escape = random.randint(100, 150)
                    else:
                        self.escape = 0
                    plat.kill()

            if tmp:
                try:
                    g = Ground(
                        Ground.last_g.rect.right + self.escape,
                        HEIGHT - 40,
                        15,
                        40,
                        self.seq[Ground.count],
                    )
                except:
                    g = Ground(
                        Ground.last_g.rect.right + self.escape, HEIGHT - 40, 15, 40, "A"
                    )
                if g.state == self.pos_start_codon:
                    start_codon = Features_panels(
                        Ground.last_g.rect.right + self.escape, 375, "codon_start"
                    )
                    self.panel.add(start_codon)
                if g.state == self.pos_stop_codon:
                    stop_codon = Features_panels(
                        Ground.last_g.rect.right + self.escape, 420, "codon_stop"
                    )
                    self.panel.add(stop_codon)
                self.platforms.add(g)
                self.all_sprites.add(g)

            for mob in self.mobs:
                mob.pos.x -= diff
                if mob.rect.right < 0:
                    mob.kill()

            for panel in self.panel:
                panel.rect.x -= diff
                if panel.rect.right < 0:
                    panel.kill()

            for back in self.gr_Background:
                back.rect.x -= 1
                if back.rect.right < 0:
                    back.kill()
                    self.gr_Background.add(
                        Background(Background.last_back.rect.right, 0)
                    )

            self.ribo.pos.x -= (diff - 0.5) if (diff - 0.5) > 0 else diff

    def generate_mobs(self):

        """
			This method generate randomly monsters controlled by the computer.
		"""

        time_now = pg.time.get_ticks()
        if time_now - self.mobs_timer > RATE_MOB + random.randint(-1000, 1000):
            self.mobs_timer = time_now
            m = Mob(random.randrange(800, 1200), 0)
            self.mobs.add(m)
            self.all_sprites.add(m)

    def generate_platforms(self):

        """
			This method generate randomly platforms.
		"""

        while len(self.plat2) < 6:
            width = random.choice([60, 150, 105])
            p = Platform(
                random.randrange(WIDTH - 30, WIDTH - 3),
                random.randrange(250, HEIGHT - 150),
                width,
                20,
                width,
            )
            if not pg.sprite.spritecollide(p, self.plat2, False):
                self.platforms.add(p)
                self.all_sprites.add(p)
                self.plat2.add(p)

    def son(self):

        """
            This method loads the song which is played in background during the game
        """

        mixer.init()
        mixer.music.load("sounds/komiku.mp3")
        mixer.music.play(loops=-1)


def men(r, f):
    g = Game(r, f)
    while g.running:
        g.new()

    pg.quit()
