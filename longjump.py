from constants import *
from main import *

class LongJumpGame(MiniGame):
    def __init__(self):
        super().__init__()
        self.player = PlayerLong()
        self.plank_w = self.player.plank_w
        self.sand = Lane(BEIGE, SAND_X, laneR_Y, SAND_WIDTH, laneR_HEIGHT)
        self.plank_b = Lane(BLACK, plank_B_X, laneR_Y, plank_B_WIDTH, laneR_HEIGHT)  
        self.start = Lane(RED, START_X, laneR_Y, START_WIDTH, laneR_HEIGHT)
        self.lane = Lane(GREY, LOOPElane_X, laneR_Y, LOOPElane_WIDTH, laneR_HEIGHT)
        self.countdown_timer = 3

    def run(self):
        run = True
        
        countdown_font = pg.font.SysFont("Verdana", 150)
        
        while self.countdown_timer > 0:
            screen.blit(self.background_img, (0, 0))
            countdown_text = countdown_font.render(f"{self.countdown_timer}", True, BLUE)
            screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
            pg.display.flip()
            pg.time.delay(1000) # Vent i 1 sekund
            self.countdown_timer -= 1
        
        while run:
            screen.blit(self.background_img, (0, 0))
            self.clock.tick(FPS)
            self.home_button.draw()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if not self.player.running:
                            self.player.start_movement()
                            self.player.jump()

        
            self.lane.move(self.sand, self.player)
            self.lane.draw()
            screen.blit(self.lane_img, (LOOPElane_X, laneR_Y))
            self.start.move(self.sand, self.player)
            self.start.draw()
            self.plank_b.move(self.sand, self.player)
            self.plank_b.draw()
            self.plank_w.move(self.sand, self.player)
            self.plank_w.draw()            
            self.sand.move(self.sand, self.player)
            self.sand.draw()
            self.player.move()
            self.player.draw()

            
            if self.player.rect.colliderect(self.sand.rect):
                run = False
                self.player.show_meters()
                pg.display.flip()
                pg.time.delay(3000)
                
            elif self.player.rect.colliderect(self.plank_w.rect):
                if not self.player.has_jumped:
                    self.player.dead()  # Vis melding om at spilleren er død
                    run = False
                    pg.display.flip()
                    pg.time.delay(3000)

                    
            # Oppdater poengsummen med antall meter hoppet
            self.score = self.player.meter * 10

            pg.display.flip()
            
        return int(self.score)
        pg.quit()
        sys.exit()
        
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
        self.plank_w = Lane(WHITE, plank_W_X, laneR_Y, plank_W_WIDTH, laneR_HEIGHT)
        self.running = False  
        self.meter = 0
        self.score=0
        self.has_jumped = False  # Legg til has_jumped attributt og sett til False
        self.player_img = pg.transform.scale(pg.image.load('seahorse.png'), (45, 55))  # Juster størrelsen

    def start_movement(self):
        self.running = True

    def jump(self):
        if self.running and self.y_pos == 505:
            if not self.has_jumped:
                self.has_jumped = True
                self.y_speed = -self.jump_h
            
    def move(self):
        if self.y_pos < 505:
            self.y_speed += self.y_gravity
        self.y_pos += self.y_speed

        if self.y_pos >= 505:
            self.y_pos = 505
            self.y_speed = 0
            self.meter = abs(505-self.plank_w.rect.x) / 150
        self.rect.y = self.y_pos - self.player_img.get_height()

    def draw(self):
        self.rect.y = self.y_pos
        screen.blit(self.player_img, self.rect) 
    
    def show_meters(self):
        text_img = font.render(f'Du har hoppet {self.meter:.1f} meter.', True, BLUE)
        text_rect = text_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_img, text_rect)
        
    def dead(self):
        text_img = font.render(f'Hoppet ble dessverre dødt', True, BLUE)
        text_rect = text_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_img, text_rect)

