import pygame as pg
import sys
import math

# Konstanter
WIDTH = 1000
HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Last inn bilder
background_img = pg.image.load('background.png')
player_img = pg.image.load('seahorse.png')  

# Definerer spillet
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
        self.player_img = pg.transform.scale(player_img, (100, 150))
        self.points = 0
        
    def redraw_window(self, player, rope):
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.player_img, (player.x, player.y))  
        rope.draw(self.screen)
        self.display_points()
        pg.display.update()
        
    def display_points(self):
        font = pg.font.SysFont('Arial', 26)
        text_img = font.render(f"Antall poeng: {self.points}", True, RED)
        self.screen.blit(text_img, (20, 20))
        
    def loss(self):
        font = pg.font.SysFont('Arial', 26)
        text_img = font.render(f"Du tapte! Du fikk {self.points} poeng.", True, RED)
        self.screen.blit(text_img, (20, 60))
        
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

# Definerer hoppetau
class Rope:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.angle = 0
        self.angular_speed = 0.08
        self.radius_multiplier = 1.15 

    def update(self):
        self.angle += self.angular_speed
        self.x = int(WIDTH // 2 + math.cos(self.angle) * (WIDTH // 4) * self.radius_multiplier)
        self.y = int(HEIGHT // 2 + math.sin(self.angle) * (HEIGHT // 4) * self.radius_multiplier)
        
    def draw(self, win):
        pg.draw.circle(win, self.color, (self.x, self.y), self.radius)

# Hovedspill loop

def main():
    game = Game()

    # Initialiserer spiller og hoppetau
    player = Player(WIDTH // 2 - 50, HEIGHT - 284, 100, 100, RED)
    rope = Rope(WIDTH // 2, HEIGHT // 2, 10, BLUE)

    clock = pg.time.Clock()

    # Kjører spillet
    run = True
    while run:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] and player.x > player.vel:
            player.x -= player.vel
        if keys[pg.K_RIGHT] and player.x < WIDTH - player.width - player.vel:
            player.x += player.vel
        if not player.isJumping:
            if keys[pg.K_SPACE]:
                player.isJumping = True
        else:
            if player.jumpCount >= -10:
                neg = 1
                if player.jumpCount < 0:
                    neg = -1
                player.y -= (player.jumpCount ** 2) * 0.5 * neg
                player.jumpCount -= 1
            else:
                player.isJumping = False
                player.jumpCount = 10

        rope.update()
        
        # Sjekk om spilleren hopper over tauet og legg til poeng
        if player.y < rope.y and rope.x - rope.radius < player.x < rope.x + rope.radius:
            game.points += 1
            
        # Sjekk om spilleren og tauet kolliderer og avslutt spillet
        player_rect = pg.Rect(player.x, player.y, player.width, player.height)
        rope_rect = pg.Rect(rope.x - rope.radius, rope.y - rope.radius, 2 * rope.radius, 2 * rope.radius)
        if player_rect.colliderect(rope_rect):
            run = False
            game.loss()  # Riktig måte å kalle loss-metoden på
            pg.display.update()  # Oppdater skjermen for å vise tapeteksten
            pg.time.delay(10000)  # Vent 10 sekunder før du avslutter pygame-vinduet

        game.redraw_window(player, rope)
        
        if player.y + player.height > HEIGHT:
            run = False
        
    pg.quit()
    sys.exit()

#if __name__ == "__main__":
main()

