import pygame as pg
import sys
import random
import math
import json
import requests
import html
import textwrap

# Konstanter
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (100, 100, 255)
GREY = (142, 142, 142)
LIGHTRED = (255, 100, 100)
BEIGE = (225, 198, 153)
GREEN = (0, 255, 0)
BLACK = (0,0,0)

pg.font.init()
font = pg.font.SysFont("Verdana", 20)
score=0

laneR_Y = HEIGHT - 70
laneR_HEIGHT = 70

LOOPElane_X = 0
LOOPElane_WIDTH = WIDTH + 2000

SAND_X = WIDTH + 500
SAND_WIDTH = 700

START_X = 40
START_WIDTH = 5

plank_B_X = WIDTH + 420
plank_B_WIDTH = 10

plank_W_X = WIDTH + 430
plank_W_WIDTH = 30

# Last inn bilder

start_game_img = pg.transform.scale(pg.image.load('bilder/start_spill.png'), (300, 100))
start_img = next_img = pg.transform.scale(pg.image.load('bilder/start.png'), (250, 80))
next_img = pg.transform.scale(pg.image.load('bilder/neste.png'), (250, 80))
home_img = pg.transform.scale(pg.image.load('bilder/hjem.png'), (80, 50))
player_img = pg.transform.scale(pg.image.load('bilder/seahorse.png'), (80, 110))
reaction_img = pg.image.load('bilder/reaksjon.png')
jump_rope_img = pg.image.load('bilder/hoppetau.png')
long_jump_img = pg.image.load('bilder/lengde.png')
trivia_img = pg.image.load('bilder/natursti.png')
background_img = pg.image.load('bilder/background.png')
hippocampus_img = pg.image.load('bilder/hippocampus.png')
introduction_img = pg.image.load('bilder/introduksjon.png')
finish_img = pg.image.load('bilder/avslutt.png')
lane_img = pg.image.load('bilder/running_track.png')


screen = pg.display.set_mode((WIDTH, HEIGHT))

with open('highscore.txt', 'r') as file:
    data = json.load(file)

highscore = data['Highscore']['score']
username = data['Highscore']['username']