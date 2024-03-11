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
LIGHTBLUE = (100, 100, 255)
GREY = (142, 142, 142)
LIGHTRED = (255, 100, 100)
BEIGE = (225, 198, 153)
GREEN = (0, 255, 0)
BLACK = (0,0,0)

pg.font.init()
font = pg.font.SysFont("opticopperplate", 20)
score=0

laneR_Y = HEIGHT - 70
laneR_HEIGHT = 70

SAND_X = WIDTH + 500
SAND_WIDTH = 700

LOOPElane_X = 0
LOOPElane_WIDTH = WIDTH + 500

START_X = 40
START_WIDTH = 5

plank_B_X = WIDTH + 420
plank_B_WIDTH = 10

plank_W_X = WIDTH + 430
plank_W_WIDTH = 30


# Last inn bilder
start_game_img = pg.transform.scale(pg.image.load('start_spill.png'), (300, 100))
next_img = pg.transform.scale(pg.image.load('neste.png'), (250, 80))
home_img = pg.transform.scale(pg.image.load('hjem.png'), (80, 50))
player_img = pg.transform.scale(pg.image.load('seahorse.png'), (80, 110))
background_home_img = pg.image.load('home_background.png')
background1_img = pg.image.load('background1.png')
background_img = pg.image.load('background.png')

screen = pg.display.set_mode((WIDTH, HEIGHT))

class Button:
    def __init__(self, img, color, rect):
        self.img = img
        self.color = color
        self.rect = rect

    def draw(self):
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
        self.clock = pg.time.Clock()
        self.background_home_img = pg.transform.scale(background_home_img, (WIDTH, HEIGHT))
        self.background_img = self.background_home_img
        self.start_game_button = Button(start_game_img, WHITE, start_game_img.get_rect(topleft=(280, 430)))
        self.reaction_button = Button(next_img, WHITE, next_img.get_rect(topleft=(420, 400)))
        self.jumping_rope_button = Button(next_img, WHITE, next_img.get_rect(topleft=(100, 400)))
        self.long_jump_button = Button(next_img, WHITE, next_img.get_rect(topleft=(200, 300)))
        self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))
        self.display_reaction_button = False
        self.display_jumping_rope_button = False
        self.display_long_jump_button = False
        self.keys_to_press = None
        self.reaction_game = None
        self.jumping_rope_game = None
        self.long_jump_game = None
        self.result_text = None
        self.points=0

    def run(self):
        running = True
        while running:
            screen.blit(self.background_img, (0, 0))
            if self.start_game_button:
                self.start_game_button.draw()
            if self.home_button:
                self.home_button.draw()
            if self.display_reaction_button is True:
                self.reaction_button.draw()
            if self.display_jumping_rope_button is True:
                self.jumping_rope_button.draw() 
            if self.display_long_jump_button is True:
                self.long_jump_button.draw()

            if self.result_text:
                screen.blit(self.result_text, (125, 250))

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
                    self.display_long_jump_button = False
                elif self.reaction_button is not None and self.reaction_button.is_clicked(event):
                    self.display_reaction_button = False
                    self.background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
                    self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))
                    self.reaction_game = ReactionGame()
                    score = self.reaction_game.run()
                    self.points+=score
                    self.display_jumping_rope_button = True
                    self.result_text = font.render(f"Resultatet etter dette spillet er {self.points}", True, BLUE)
                elif self.jumping_rope_button is not None and self.jumping_rope_button.is_clicked(event):
                    self.background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
                    self.display_jumping_rope_button = False
                    self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)))
                    self.jumping_rope_game = JumpingRopeGame()
                    score = self.jumping_rope_game.run()
                    self.points+=score
                    self.display_long_jump_button = True
                    self.result_text = font.render(f"Resultatet etter dette spillet er {self.points}", True, BLUE)
                elif self.long_jump_button is not None and self.long_jump_button.is_clicked(event):
                    self.background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
                    self.display_long_jump_button = False
                    self.long_jump_game = LongJumpGame()
                    score = self.long_jump_game.run()
                    self.points += score
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
    def __init__(self):
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

            screen.blit(self.background_img, (0, 0))

            time_remaining = max(0, int(self.time_limit - elapsed_time))
            clock_text = font.render(f"Tid som gjenstår: {time_remaining} sek", True, RED)
            screen.blit(clock_text, (10, 10))

            task_text = font.render(f"Hold disse tre boksavene inne samtidig: {chr(self.keys_to_press[0])}, {chr(self.keys_to_press[1])}, {chr(self.keys_to_press[2])}", True, BLUE)
            text_rect = task_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(task_text, text_rect)

            score_text = font.render(f"Poengsum: {self.score}", True, RED)
            screen.blit(score_text, (10, 90))

            self.home_button.draw()

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
    def __init__(self):
        super().__init__()
        self.player = PlayerRope(WIDTH // 2 - 50, HEIGHT - 220, 80, 110, RED)
        self.rope = Rope(WIDTH//2, HEIGHT//2, 10, BLUE)
        self.running = True  # Definer running-variabelen her
        self.jump_over_rope = False

    def redraw_window(self, player, rope):
        screen.blit(self.background_img, (0, 0))
        screen.blit(player_img, (self.player.x, self.player.y))  # Tegn playeren som seahorse.png
        pg.draw.circle(screen, self.rope.color, (self.rope.x, self.rope.y), self.rope.radius)
        score_text = font.render(f"Poengsum: {self.score}", True, RED)
        screen.blit(score_text, (10, 90))
        self.home_button.draw()


    def run(self):
        while self.running:  # Bruk self.running til å kontrollere løkken
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False  # Sett self.running til False når du vil avslutte

            keys = pg.key.get_pressed()

            # move playeren til venstre og høyre
            if keys[pg.K_LEFT] and self.player.x > self.player.vel:
                self.player.x -= self.player.vel
            if keys[pg.K_RIGHT] and self.player.x < WIDTH - self.player.width - self.player.vel:
                self.player.x += self.player.vel
            # jump hvis mellomromstasten trykkes og playeren ikke allerede jumper
            if not self.player.isJumping:
                if keys[pg.K_SPACE]:
                    self.player.isJumping = True
            else:
                # Utfør jump
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

            # Sjekk om playeren jumper over tauet og legg til poeng
            if self.player.y < self.rope.y and self.rope.x - self.rope.radius < self.player.x < self.rope.x + self.rope.radius * 2 and not self.jump_over_rope:
                self.score += 1
                self.rope.angular_speed+=0.005
                self.jump_over_rope = True
            elif self.player.y >= self.rope.y:
                self.jump_over_rope = False

            # Sjekk om playeren og tauet kolliderer og avslutt spillet
            self.player_rect = pg.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            self.rope_rect = pg.Rect(self.rope.x - self.rope.radius, self.rope.y - self.rope.radius, 2 * self.rope.radius, 2 * self.rope.radius)
            if self.player_rect.colliderect(self.rope_rect):
                return self.score
                
            self.redraw_window(self.player, self.rope)  # Tegn spillet

            if self.player.y + self.player.height > HEIGHT:
                return self.score   # Avslutt spillet hvis playeren faller utenfor skjermen

            pg.display.flip()


        return self.score  # Returner self.score når løkken er ferdig

class PlayerRope:
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


class Lane:
    def __init__(self, color, x, y, w, h):
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fart = 0
        self.aks = -0.12
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
    
    def move(self, sand, player):
        if not pg.Rect.colliderect(sand.rect, player.rect):
            self.fart += self.aks
            self.x += self.fart
            self.rect.x = self.x
        
    def draw(self):
        pg.draw.rect(screen, self.color, self.rect)

class PlayerLong:
    def __init__(self):
        self.y_pos = 505  # Startposisjon
        self.y_gravity = 1
        self.jump_h = 20
        self.y_speed = 0  
        self.rect = pg.Rect(10, self.y_pos, 30, 50)  # Rektangelstørrelse
        self.running = False  
        self.meter = 0  # Variabel for å holde styr på antall hopp
        self.start_jump_pos = 0  # Lagrer startposisjonen til den svarte klossen ved hoppet
        self.sand = Lane(BEIGE, SAND_X, laneR_Y, SAND_WIDTH, laneR_HEIGHT)
        self.score=0
        self.has_jumped = False  # Legg til has_jumped attributt og sett til False

    def start_movement(self):
        self.running = True
        self.start_jump_pos = self.sand.rect.x  # Lagrer posisjonen til den svarte klossen når hoppet starter

    def jump(self):
        if self.running and self.y_pos == 505:
            if not self.has_jumped:
                self.has_jumped = True
                self.y_speed = -self.jump_h
                self.start_jump_pos = self.sand.rect.x
            

    def move(self):
        if self.y_pos < 505:
            self.y_speed += self.y_gravity
        self.y_pos += self.y_speed

        if self.y_pos >= 505:
            self.y_pos = 505
            self.y_speed = 0
            self.meter = abs(505 - self.sand.rect.x) / 100
            # Måler hoppets lengde fra den svarte klossen
            # Dividerer med 150 for å konvertere piksler til meter

    def draw(self):
        self.rect.y = self.y_pos
        pg.draw.rect(screen, GREEN, self.rect)
    
    def show_meters(self):
        text_img = font.render(f'Du har hoppet {self.meter:.1f} meter.', True, BLACK)
        screen.blit(text_img, (220, 280))
        
    def dead(self):
        text_img = font.render(f'Hoppet ble dessverre dødt', True, BLACK)
        screen.blit(text_img, (220, 280))


class LongJumpGame(MiniGame):
    def __init__(self):
        super().__init__()
        self.player = PlayerLong()
        self.sand = self.player.sand
        self.plank_b = Lane(BLACK, plank_B_X, laneR_Y, plank_B_WIDTH, laneR_HEIGHT)  
        self.plank_w = Lane(WHITE, plank_W_X, laneR_Y, plank_W_WIDTH, laneR_HEIGHT)
        self.start = Lane(RED, START_X, laneR_Y, START_WIDTH, laneR_HEIGHT)
        self.lane = Lane(GREY, LOOPElane_X, laneR_Y, LOOPElane_WIDTH, laneR_HEIGHT)

    def run(self):
        run = True
        while run:
            screen.blit(self.background_img, (0, 0))
            self.clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if not self.player.running:
                            self.player.start_movement()
                            self.player.jump()

            # Deretter tegn resten av spillmiljøet
            self.sand.move(self.sand, self.player)
            self.sand.draw()
            self.lane.move(self.sand, self.player)
            self.lane.draw()
            self.start.move(self.sand, self.player)
            self.start.draw()
            self.plank_b.draw()
            self.plank_b.move(self.sand, self.player)
            self.plank_w.draw()
            self.plank_w.move(self.sand, self.player)
            self.player.move()
            self.player.draw()

            # Sjekk for kollisjon med sanden
            if self.player.rect.colliderect(self.player.sand.rect):
                if not self.player.has_jumped:  # Sjekk om spilleren har hoppet
                    run = False
                    self.player.dead()
                    pg.display.flip()
                    pg.time.delay(3000)
                else:
                    run = False
                    self.player.show_meters()
                    pg.display.flip()
                    pg.time.delay(3000)
                    
            # Oppdater poengsummen med antall meter hoppet
            self.score = self.player.meter * 10

            pg.display.flip()
            
        return int(self.score)



        
        pg.quit()
        sys.exit()


game = Game()
game.run()


