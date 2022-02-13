# coding=utf-8
import pygame
import sys
import pygame.mixer
from pygame.locals import *
import os

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"


def generique():
    pygame.init()
    pygame.mixer.init()
    musique = pygame.mixer.music.load("sounds/music.mp3")
    fenetre = pygame.display.set_mode((800, 600))
    BLACK = (0, 0, 0)
    welcome = "Bienvenue dans DNA-Reacher Quest"
    passer = "Appuyez sur [ESPACE] pour passer"
    scenario = [
        "-- XXIIIe siècle --",
        "Le progrès technique, la compréhension de l'espace-temps et du génome",
        "ont permis l'apparition de nombreuses innovations technologiques",
        "sur la miniaturisation extrême des systèmes",
        "Alors que l'humanité vivait il y a encore peu",
        " une époque douce, paisible et prospère",
        "et que la technologie, plus puissante que jamais",
        "servait le bien commun, les héros avaient disparus.",
        " ",
        "Mais le danger était de retour",
        "Des êtres de légende sortis des océans",
        "se sont avérés être des terribles techniciens du vivant",
        "et cherchent à récupérer leur place sur Terre",
        "en s'attaquant à l'unité la plus fondamentale",
        "de la vie humaine : l'ADN",
        "",
        "L'humanité se cachant en deshérence",
        "Il fallait contrer la menace",
        "pour préserver la paix",
        "",
        "Le mal transmis par les aquariens",
        "était encore inconnu de la médecine et des scientifiques",
        "Le cerveau des hommes ne suffisait pas",
        "il nous fallait l'aide de la machine",
        "l'informatique serait le dernier recours de l'humanité",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "Le vénérable professeur Frandalf le Blamson travaillait à un remède",
        "mais lui-même ayant atteint du mystérieux mal,",
        "Il fallait à tout prix l'aider",
        "Ses meilleurs padawans se mirent en quête",
        "de sauver leur maitre coûte que coûte",
        "Arnowan Liehnobi, Yodalex, Yayanakin Skywalker et Gab Solo",
        "vinrent à la rencontre de Chrislin l'Ambroiseur,",
        "un talentueux scientifique, pour tenter l'impossible",
        "Il fallait utiliser la technologie de miniaturisation",
        "pour permettre à Chrislin de défendre l'ADN",
        "du professeur le Blamson, sans quoi",
        "l'humanité serait perdue à jamais",
    ]
    scenar = []
    rectscen = []
    timer = 0
    font = pygame.font.Font(None, 50)
    wlcm = font.render(welcome, 3, (255, 0, 0))
    font = pygame.font.Font(None, 30)
    skip = font.render(passer, 1, (0, 0, 0))
    for i in range(0, len(scenario)):
        scenar.append(font.render(scenario[i], 3, (255, 255, 255)))
        rectscen.append(scenar[i].get_rect())
    continuer = True
    defil = False
    stop = False
    fond = pygame.image.load("images/bg22.png").convert_alpha()
    rectfond = fond.get_rect()
    fond = pygame.transform.scale(fond, (fenetre.get_size()[0], rectfond.height))

    pygame.mixer.music.play()
    for y in range(int((fenetre.get_size()[1]) / 2), -rectfond.height, -1):
        if stop:
            break
        i = 0
        pygame.time.delay(15)
        rectskip = skip.get_rect()
        fenetre.blit(
            skip, (((int(fenetre.get_size()[0] / 2)) - (rectskip.center[0]) + 10), 10)
        )
        rectwlcm = wlcm.get_rect()
        fenetre.blit(
            wlcm, (((int(fenetre.get_size()[0] / 2)) - (rectwlcm.center[0])), y * 0.8)
        )
        pygame.display.flip()
        fenetre.blit(fond, (0, (y - int((fenetre.get_size()[1]) / 2)) * 1.35))
        for i in range(0, len(scenario)):
            if stop:
                break
            fenetre.blit(
                scenar[i],
                (
                    ((int(fenetre.get_size()[0] / 2)) - (rectscen[i].center[0])),
                    (y * 0.8 + 200) + 50 * (i + 1),
                ),
            )
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        stop = True
            if pygame.time.get_ticks() > 75000:
                stop = True

    pygame.quit()


if __name__ == "__main__":
    generique()
