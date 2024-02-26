import pygame as pg
import sys
import random

# Konstanter
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Last inn bilder
start_img = pg.transform.scale(pg.image.load('start.png'), (300, 100))
next_img = pg.transform.scale(pg.image.load('neste.png'), (250, 80))
home_img = pg.transform.scale(pg.image.load('hjem.png'), (80, 50))
background_home_img = pg.image.load('home_background.png')
background1_img = pg.image.load('background1.png')
background_img = pg.image.load('background.png')

class Button:
    def __init__(self, img, color, rect):
        self.img = img
        self.color = color
        self.rect = rect

    def draw(self, screen):
        screen.blit(self.img, self.rect.topleft)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.background_img = pg.transform.scale(background_home_img, (WIDTH, HEIGHT))
        self.start_button = Button(start_img, WHITE, start_img.get_rect(topleft=(280, 430)))
        self.next_button = Button(next_img, WHITE, next_img.get_rect(topleft=(420, 400)))
        self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))
        self.display_next_button = False  # Kontrollflagg for å vise neste knapp
        self.reaction_game = None

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_img, (0, 0))
            if self.start_button:
                self.start_button.draw(self.screen)
            if self.home_button:
                self.home_button.draw(self.screen)
            if self.display_next_button:
                self.next_button.draw(self.screen)

            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif self.start_button is not None and self.start_button.is_clicked(event):
                    self.background_img = pg.transform.scale(background1_img, (WIDTH, HEIGHT))
                    self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))
                    self.display_next_button = True  # Sett flagg for å vise neste knapp
                    self.start_button = None
                elif self.home_button is not None and self.home_button.is_clicked(event):
                    self.background_img = pg.transform.scale(background_home_img, (WIDTH, HEIGHT))
                    self.start_button = Button(start_img, WHITE, start_img.get_rect(topleft=(280, 430)))
                    self.home_button = None
                    self.display_next_button = False
                elif self.next_button is not None and self.next_button.is_clicked(event):
                    self.background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
                    self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))
                    self.display_next_button = False
                    self.reaction_game = ReactionGame(self.screen, self.background_img)  # Send med skjermreferanse og bakgrunnsbilde
                    score = self.reaction_game.run()
                    print("Reaction game score:", score)

            self.clock.tick(60)

        pg.quit()
        sys.exit()

class ReactionGame(Game):
    def __init__(self, screen, background_img):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.score = 0
        self.time_limit = 60
        self.keys_to_press = []
        self.task_start_time = 0
        self.task_complete = False
        self.background_img = background_img
        self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))
        self.generate_task()
        self.keys_pressed = set()

    def generate_task(self):
        self.keys_to_press = random.sample([pg.K_a, pg.K_b, pg.K_c, pg.K_d, pg.K_e, pg.K_f, pg.K_g, pg.K_h, pg.K_i, pg.K_j, pg.K_k, pg.K_l, pg.K_m], 3)

    def run(self):
        start_time = pg.time.get_ticks()
        while True:
            current_time = pg.time.get_ticks()
            elapsed_time = (current_time - start_time) / 1000  # Konverter til sekunder

            # Sjekk om tidsbegrensningen er nådd
            if elapsed_time >= self.time_limit:
                break

            # Sjekk om gjeldende oppgave er fullført
            if self.task_complete:
                self.score += 1
                self.generate_task()  # Generer ny oppgave
                self.task_start_time = current_time
                self.task_complete = False
                self.keys_pressed = set()  # Nullstill tastetrykk

            # Tegn bakgrunnsbilde
            self.screen.blit(self.background_img, (0, 0))

            # Tegn klokke
            time_remaining = max(0, int(self.time_limit - elapsed_time))
            font = pg.font.Font(None, 36)
            clock_text = font.render(f"Tid som gjenstår: {time_remaining} sek", True, RED)
            self.screen.blit(clock_text, (10, 10))

            # Tegn oppgave
            task_text = font.render(f"Hold disse tre boksavene inne samtidig: {chr(self.keys_to_press[0])}, {chr(self.keys_to_press[1])}, {chr(self.keys_to_press[2])}", True, BLUE)
            text_rect = task_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(task_text, text_rect)

            # Tegn score på skjermen
            score_text = font.render(f"Poengsum: {self.score}", True, RED)
            self.screen.blit(score_text, (10, 90))

            pg.display.flip()

            # Sjekk for tastetrykk
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    self.keys_pressed.add(event.key)
                elif event.type == pg.KEYUP:
                    if event.key in self.keys_pressed:
                        self.keys_pressed.remove(event.key)

            # Sjekk om alle nødvendige taster holdes inne samtidig
            if set(self.keys_to_press).issubset(self.keys_pressed):
                self.task_complete = True

            self.clock.tick(60)

        return self.score





if __name__ == "__main__":
    game = Game()
    game.run()
