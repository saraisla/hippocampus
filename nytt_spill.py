import pygame as pg
import sys
import random
import math

# Konstanter
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pg.font.init()
font = pg.font.SysFont("opticopperplate", 20)
score=0

# Last inn bilder
start_game_img = pg.transform.scale(pg.image.load('start_spill.png'), (300, 100))
next_img = pg.transform.scale(pg.image.load('neste.png'), (250, 80))
home_img = pg.transform.scale(pg.image.load('hjem.png'), (80, 50))
player_img = pg.transform.scale(pg.image.load('seahorse.png'), (80, 110))
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
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.background_home_img = pg.transform.scale(background_home_img, (WIDTH, HEIGHT))
        self.background_img = self.background_home_img
        self.start_game_button = Button(start_game_img, WHITE, start_game_img.get_rect(topleft=(280, 430)))
        self.reaction_button = Button(next_img, WHITE, next_img.get_rect(topleft=(420, 400)))
        self.jumping_rope_button = Button(next_img, WHITE, next_img.get_rect(topleft=(100, 400)))
        self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))
        self.display_reaction_button = False
        self.display_jumping_rope_button = False
        self.keys_to_press = None
        self.reaction_game = None
        self.jumping_rope_game = None
        self.result_text = None
        self.points=0

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_img, (0, 0))
            if self.start_game_button:
                self.start_game_button.draw(self.screen)
            if self.home_button:
                self.home_button.draw(self.screen)
            if self.display_reaction_button is True:
                self.reaction_button.draw(self.screen)
            if self.display_jumping_rope_button is True:
                self.jumping_rope_button.draw(self.screen)
                

            if self.result_text:
                self.screen.blit(self.result_text, (125, 250))

            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif self.start_game_button is not None and self.start_game_button.is_clicked(event):
                    self.background_img = pg.transform.scale(background1_img, (WIDTH, HEIGHT))
                    self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))
                    self.display_reaction_button = True
                    self.start_game_button = None
                elif self.home_button is not None and self.home_button.is_clicked(event):
                    self.background_img = self.background_home_img
                    self.start_game_button = Button(start_game_img, WHITE, start_game_img.get_rect(topleft=(280, 430)))
                    self.home_button = None
                    self.result_text = None
                    self.display_reaction_button = False
                    self.display_jumping_rope_button = False
                elif self.reaction_button is not None and self.reaction_button.is_clicked(event):
                    self.display_reaction_button = False
                    self.background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
                    self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))
                    self.reaction_game = ReactionGame(self.screen)
                    score = self.reaction_game.run()
                    self.points+=score
                    self.display_jumping_rope_button = True
                    self.result_text = font.render(f"Resultatet etter dette spillet er {self.points}", True, BLUE)
                elif self.jumping_rope_button is not None and self.jumping_rope_button.is_clicked(event):
                    self.background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
                    self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))
                    self.jumping_rope_game = JumpingRopeGame(self.screen)
                    score = self.jumping_rope_game.run()
                    self.points+=score
                    self.display_jumping_rope_button = False
                    self.result_text = font.render(f"Resultatet etter dette spillet er {self.points}", True, BLUE)

            self.clock.tick(60)

        pg.quit()
        sys.exit()
        
class MiniGame(Game):
    def __init__(self):
        super().__init__()
        self.clock = pg.time.Clock()
        self.score = 0
        self.background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
        self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))

class ReactionGame(MiniGame):
    def __init__(self, screen):
        self.screen = screen
        super().__init__()
        self.time_limit = 30
        self.keys_to_press = []
        self.task_complete = False
        self.keys_pressed = set()
        self.start_time = 0
        self.generate_task()

    def generate_task(self):
        self.keys_to_press = random.sample([pg.K_a, pg.K_b, pg.K_c, pg.K_d, pg.K_e, pg.K_f, pg.K_g, pg.K_h, pg.K_i, pg.K_j, pg.K_k, pg.K_l, pg.K_m, pg.K_n, pg.K_o, pg.K_p, pg.K_q, pg.K_r, pg.K_s, pg.K_t, pg.K_u, pg.K_v, pg.K_w, pg.K_x, pg.K_y, pg.K_z], 3)

    def check_task_complete(self):
        return all(key in self.keys_pressed for key in self.keys_to_press)

    def run(self):
        self.start_time = pg.time.get_ticks()
        while True:
            current_time = pg.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000

            if elapsed_time >= self.time_limit:
                return self.score

            self.screen.blit(self.background_img, (0, 0))

            time_remaining = max(0, int(self.time_limit - elapsed_time))
            clock_text = font.render(f"Tid som gjenstår: {time_remaining} sek", True, RED)
            self.screen.blit(clock_text, (10, 10))

            task_text = font.render(f"Hold disse tre boksavene inne samtidig: {chr(self.keys_to_press[0])}, {chr(self.keys_to_press[1])}, {chr(self.keys_to_press[2])}", True, BLUE)
            text_rect = task_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(task_text, text_rect)

            score_text = font.render(f"Poengsum: {self.score}", True, RED)
            self.screen.blit(score_text, (10, 90))

            self.home_button.draw(self.screen)

            pg.display.flip()

            # Oppdater keys_pressed-settet når knappene trykkes ned eller slippes
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    self.keys_pressed.add(event.key)
                elif event.type == pg.KEYUP:
                    if event.key in self.keys_pressed:
                        self.keys_pressed.remove(event.key)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.home_button.is_clicked(event):
                        self.background_img = pg.transform.scale(background_home_img, (WIDTH, HEIGHT))
                        return self.score

            if self.check_task_complete():
                print("Fullført")
                self.task_complete = True
                self.score += 1

            if elapsed_time >= self.time_limit or self.task_complete:
                self.generate_task()
                self.task_complete = False

            self.clock.tick(60)
        return self.score

class JumpingRopeGame(MiniGame):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.player = Player(WIDTH // 2 - 50, HEIGHT - 220, 80, 110, RED)
        self.rope = Rope(WIDTH//2, HEIGHT//2, 10, BLUE)
        self.running = True  # Definer running-variabelen her
        self.jump_over_rope = False

    def redraw_window(self, player, rope):
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(player_img, (self.player.x, self.player.y))  # Tegn spilleren som seahorse.png
        pg.draw.circle(self.screen, self.rope.color, (self.rope.x, self.rope.y), self.rope.radius)
        score_text = font.render(f"Poengsum: {self.score}", True, RED)
        self.screen.blit(score_text, (10, 90))
        self.home_button.draw(self.screen)


    def run(self):
        while self.running:  # Bruk self.running til å kontrollere løkken
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False  # Sett self.running til False når du vil avslutte

            keys = pg.key.get_pressed()

            # Beveg spilleren til venstre og høyre
            if keys[pg.K_LEFT] and self.player.x > self.player.vel:
                self.player.x -= self.player.vel
            if keys[pg.K_RIGHT] and self.player.x < WIDTH - self.player.width - self.player.vel:
                self.player.x += self.player.vel
            # Hopp hvis mellomromstasten trykkes og spilleren ikke allerede hopper
            if not self.player.isJumping:
                if keys[pg.K_SPACE]:
                    self.player.isJumping = True
            else:
                # Utfør hopp
                if self.player.jumpCount >= -10:
                    neg = 1
                    if self.player.jumpCount < 0:
                        neg = -1
                    self.player.y -= (self.player.jumpCount ** 2) * 0.5 * neg
                    self.player.jumpCount -= 1
                else:
                    self.player.isJumping = False
                    self.player.jumpCount = 10

            self.rope.update()  # Oppdater tauets posisjon

            # Sjekk om spilleren hopper over tauet og legg til poeng
            if self.player.y < self.rope.y and self.rope.x - self.rope.radius < self.player.x < self.rope.x + self.rope.radius * 2 and not self.jump_over_rope:
                self.score += 1
                self.rope.angular_speed+=0.005
                self.jump_over_rope = True
            elif self.player.y >= self.rope.y:
                self.jump_over_rope = False

            # Sjekk om spilleren og tauet kolliderer og avslutt spillet
            self.player_rect = pg.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            self.rope_rect = pg.Rect(self.rope.x - self.rope.radius, self.rope.y - self.rope.radius, 2 * self.rope.radius, 2 * self.rope.radius)
            if self.player_rect.colliderect(self.rope_rect):
                return self.score
                
            self.redraw_window(self.player, self.rope)  # Tegn spillet

            if self.player.y + self.player.height > HEIGHT:
                return self.score   # Avslutt spillet hvis spilleren faller utenfor skjermen

            pg.display.flip()


        return self.score  # Returner self.score når løkken er ferdig

class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 5
        self.isJumping = False
        self.jumpCount = 10

class Rope:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius  # Tauets radius
        self.color = color
        self.angle = -math.pi/1  # Startvinkel for tauet (endret til negativ verdi)
        self.angular_speed = 0.08  # Hastighet for svinging av tauet
        self.radius_multiplier = 1.15  # Multiplikator for å endre tauets lengde

    def update(self):
        self.angle += self.angular_speed  # Oppdater vinkelen til tauet
        # Beregn nye koordinater for tauet basert på vinkelen og multiplikatoren
        self.x = int(WIDTH // 2 + math.cos(self.angle) * (WIDTH // 4) * self.radius_multiplier)
        self.y = int(HEIGHT // 2 + math.sin(self.angle) * (HEIGHT // 4) * self.radius_multiplier)

    def draw(self, win):
        # Tegn tauet som en sirkel
        pg.draw.circle(win, self.color, (self.x, self.y), self.radius)




if __name__ == "__main__":
    game = Game()
    game.run()
