import pygame as pg
import sys
from variabler import *

# Initiere pygame
pg.init() 

font = pg.font.SysFont('Arial', 26)

class Bane:
    def __init__(self, farge, x, y, w, h):
        self.farge = farge
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fart = 0
        self.aks = -0.12
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
    
    def beveg(self):
        if not pg.Rect.colliderect(sand.rect, spiller.rect):
            self.fart += self.aks
            self.x += self.fart
            self.rect.x = self.x
        
    def draw(self, surface):
        pg.draw.rect(surface, self.farge, self.rect)

class Spiller:
    def __init__(self):
        self.y_pos = 505
        self.y_gravity = 1
        self.jump_h = 20
        self.y_speed = 0  
        self.running = False  
        self.rect = pg.Rect(10, self.y_pos, 30, 50)
        self.meter = 0  # variabel for å holde styr på antall hopp
        self.start_jump_pos = 0  # lagrer startposisjonen til den svarte klossen ved hoppet

    def start_bevegelse(self):
        self.running = True
        self.start_jump_pos = sand.rect.x  # lagrer posisjonen til den svarte klossen når hoppet starter

    def hopp(self):
        if self.running and self.y_pos == 505:
            self.y_speed = -self.jump_h
            self.start_jump_pos = sand.rect.x  # oppdaterer posisjonen til den svarte klossen når hoppet starter

    def beveg(self):
        if self.y_pos < 505:
            self.y_speed += self.y_gravity
        self.y_pos += self.y_speed

        if self.y_pos > 505:
            self.y_pos = 505
            self.y_speed = 0
            self.meter = abs(sand.rect.x - self.start_jump_pos) / 150  # måler hopplengden fra den svarte klossen
            # Dividerer med 150 for å konvertere piksler til meter

    def draw(self, surface):
        self.rect.y = self.y_pos
        pg.draw.rect(surface, GREEN, self.rect)
    
    def vis_meter(self, surface):  # Funksjon for å vise antall meter på skjermen
        text_img = font.render(f'Du har hoppet {self.meter:.1f} meter.', True, BLACK)
        surface.blit(text_img, (220, 280))
        
    def dødt(self, surface):  # Funksjon for si at hoppet ble dødt
        text_img = font.render(f'Hoppet ble dessverre dødt.', True, BLACK)
        surface.blit(text_img, (220, 280))
            
background_img = pg.image.load('background.png')
background_img = pg.transform.scale(background_img, SIZE)

surface = pg.display.set_mode(SIZE)

clock = pg.time.Clock()

sand = Bane(BEIGE, SAND_X, BANER_Y, SAND_WIDTH, BANER_HEIGHT)
bane = Bane(GREY, LOOPEBANE_X, BANER_Y, LOOPEBANE_WIDTH, BANER_HEIGHT)
start = Bane(RED, START_X, BANER_Y, START_WIDTH, BANER_HEIGHT)
planke_b = Bane(BLACK, PLANKE_B_X, BANER_Y, PLANKE_B_WIDTH, BANER_HEIGHT)
planke_w = Bane(WHITE, PLANKE_W_X, BANER_Y, PLANKE_W_WIDTH, BANER_HEIGHT)
spiller = Spiller()

run = True

while run:
    clock.tick(FPS)

    surface.blit(background_img, (0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False  
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if not spiller.running:
                    spiller.start_bevegelse()
                spiller.hopp()
    
    if pg.Rect.colliderect(sand.rect, spiller.rect):
        spiller.vis_meter(surface)  # Vis antall meter før spillet avsluttes
    
    elif pg.Rect.colliderect(spiller.rect, planke_w.rect):
        run = False
        spiller.dødt(surface)  # Kaller dødt funksjonen
        pg.display.flip()  # Display tekst før delay
        pg.time.delay(3000)  # Delay på 3000 millisekunder (3 sekunder)

    spiller.beveg()  
    bane.beveg()
    bane.draw(surface)
    start.beveg()
    start.draw(surface)
    planke_b.beveg()
    planke_b.draw(surface)
    planke_w.beveg()
    planke_w.draw(surface)
    sand.beveg()
    sand.draw(surface)
    spiller.draw(surface)

    pg.display.flip()

pg.quit()
sys.exit()
