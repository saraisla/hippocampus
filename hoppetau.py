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
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))  # Opprett et skjermvindu
        self.clock = pg.time.Clock()  # Opprett en klokke for å styre oppdateringshastighet
        self.background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))  # Skaler bakgrunnsbildet til skjermstørrelsen
        self.player_img = pg.transform.scale(player_img, (100, 150))  # Skaler spillerens bilde
        self.points = 0  # Spillerens poengsum
        
    def redraw_window(self, player, rope):
        self.screen.blit(self.background_img, (0, 0))  # Tegn bakgrunnsbildet
        self.screen.blit(self.player_img, (player.x, player.y))  # Tegn spillerens figur
        rope.draw(self.screen)  # Tegn tauet
        self.display_points()  # Vis poengene på skjermen
        pg.display.update()  # Oppdater skjermen
        
    def display_points(self):
        font = pg.font.SysFont('Arial', 26)  # Definer en skrifttype
        text_img = font.render(f"Antall poeng: {self.points}", True, RED)  # Lag et bilde av teksten
        self.screen.blit(text_img, (20, 20))  # Tegn poengteksten på skjermen
        
    def loss(self):
        font = pg.font.SysFont('Arial', 26)  # Definer en skrifttype
        text_img = font.render(f"Du tapte! Du fikk {self.points} poeng.", True, RED)  # Lag et bilde av tapeteksten
        self.screen.blit(text_img, (20, 60))  # Tegn tapeteksten på skjermen

class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 5  # Spillerens hastighet
        self.isJumping = False  # Sjekk om spilleren hopper
        self.jumpCount = 10  # Antall hopp

# Definerer hoppetau
class Rope:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius  # Tauets radius
        self.color = color
        self.angle = math.pi/4  # Startvinkel for tauet
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

# Hovedspill loop
def main():
    game = Game()

    # Initialiserer spiller og hoppetau
    player = Player(WIDTH // 2 - 50, HEIGHT - 284, 80, 110, RED)
    rope = Rope(WIDTH // 2, HEIGHT // 2, 10, BLUE)
 
    clock = pg.time.Clock()  # Opprett en klokke

    # Kjører spillet
    run = True
    while run:
        clock.tick(60)  # Begren hastigheten til loopen til 60 FPS

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False  # Avslutt spillet hvis brukeren lukker vinduet

        keys = pg.key.get_pressed()

        # Beveg spilleren til venstre og høyre
        if keys[pg.K_LEFT] and player.x > player.vel:
            player.x -= player.vel
        if keys[pg.K_RIGHT] and player.x < WIDTH - player.width - player.vel:
            player.x += player.vel
        # Hopp hvis mellomromstasten trykkes og spilleren ikke allerede hopper
        if not player.isJumping:
            if keys[pg.K_SPACE]:
                player.isJumping = True
        else:
            # Utfør hopp
            if player.jumpCount >= -10:
                neg = 1
                if player.jumpCount < 0:
                    neg = -1
                player.y -= (player.jumpCount ** 2) * 0.5 * neg
                player.jumpCount -= 1
            else:
                player.isJumping = False
                player.jumpCount = 10

        rope.update()  # Oppdater tauets posisjon

        # Sjekk om spilleren hopper over tauet og legg til poeng
        if player.y < rope.y and rope.x - rope.radius < player.x < rope.x + rope.radius * 2:
            game.points += 1

        # Sjekk om spilleren og tauet kolliderer og avslutt spillet
        player_rect = pg.Rect(player.x, player.y, player.width, player.height)
        rope_rect = pg.Rect(rope.x - rope.radius, rope.y - rope.radius, 2 * rope.radius, 2 * rope.radius)
        if player_rect.colliderect(rope_rect):
            run = False  # Avslutt spillet
            game.loss()  # Vis tapeteksten
            pg.display.update()  # Oppdater skjermen for å vise tapeteksten
            pg.time.delay(7000)  # Vent 7 sekunder før pygame-vinduet avsluttes

        game.redraw_window(player, rope)  # Tegn spillet

        if player.y + player.height > HEIGHT:
            run = False  # Avslutt spillet hvis spilleren faller utenfor skjermen

    pg.quit()  # Avslutt Pygame
    sys.exit()  # Avslutt programmet

main()
