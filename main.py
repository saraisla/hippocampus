from constants import *

class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.clock = pg.time.Clock()
        self.hippocampus_img = pg.transform.scale(hippocampus_img, (WIDTH, HEIGHT))
        self.background_img = self.hippocampus_img

        self.start_game_button = Button(start_game_img, WHITE, start_game_img.get_rect(topleft=(250, 430)), self.start_game)
        self.next_button = Button(next_img, WHITE, next_img.get_rect(topleft=(420, 400)), self.next_game)
        self.reaction_button = Button(start_img, WHITE, start_img.get_rect(topleft=(420, 400)), self.reaction)
        self.jumping_rope_button = Button(start_img, WHITE, start_img.get_rect(topleft=(420, 400)), self.jumping_rope)
        self.long_jump_button = Button(start_img, WHITE, start_img.get_rect(topleft=(420, 400)), self.long_jump)
        self.trivia_button = Button(start_img, WHITE, start_img.get_rect(topleft=(420, 400)), self.trivia)
        self.home_button = Button(home_img, WHITE, home_img.get_rect(topleft=(700, 20)), self.home)
        self.lane_img = pg.transform.scale(lane_img, (LOOPElane_WIDTH, laneR_HEIGHT))
        self.start_game_button.display = True

        self.reaction_game = None
        self.jumping_rope_game = None
        self.long_jump_game = None
        self.trivia_game = None

        self.result_text = None
        self.finish_text = None
        self.finish2_text = None
        self.highscore_text = None

        self.buttons = [self.start_game_button, self.home_button, self.next_button,
                        self.reaction_button, self.jumping_rope_button, self.long_jump_button,
                        self.trivia_button]

        self.points = 0
        self.input_box = pg.Rect(300, 350, 145, 32)
        self.username = ""

        self.active = False
        self.text = "Brukernavn: "
        self.color = BLACK
        self.username_shown = True
        
    def draw_buttons(self):
        for button in self.buttons:
            if button.display:
                button.draw()

    def draw_text(self):
        texts = [self.result_text, self.finish_text, self.finish2_text, self.highscore_text]
        heights = [50, 80, 110, 150]
        n=0
        for text in texts:
            if text:
                text_rect = text.get_rect(center=(WIDTH // 2, heights[n]))
                screen.blit(text, text_rect)
            n+=1
            
        if self.username_shown == True:
            pg.draw.rect(screen, WHITE, (self.input_box.x + 3, self.input_box.y + 3, self.input_box.w - 6, self.input_box.h - 6))
            text_surface = font.render(self.text, True, self.color)
            width = max(200, text_surface.get_width() + 10)
            self.input_box.w = width
            screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))
            pg.draw.rect(screen, self.color, self.input_box, 3)
            pg.display.flip()

    def start_game(self):
        self.background_img = pg.transform.scale(introduction_img, (WIDTH, HEIGHT))
        self.home_button.display = True
        self.next_button.display = True
        self.points = 0         

    def next_game(self):
        self.background_img = pg.transform.scale(reaction_img, (WIDTH, HEIGHT))
        self.reaction_button.display = True

    def home(self):
        for button in self.buttons:
            button.display = False
            
        self.background_img = self.hippocampus_img
        self.start_game_button.display = True
        
        self.finish_text = None
        self.finish2_text = None
        self.result_text = None
        self.highscore_text = None


    def reaction(self):
        print(self.username)
        self.reaction_game = ReactionGame()
        score = self.reaction_game.run()
        self.points += score

        self.background_img = pg.transform.scale(jump_rope_img, (WIDTH, HEIGHT))

        self.jumping_rope_button.display = True
        self.result_text = font.render(f"Resultatet ditt etter reaksjonsspillet er {self.points} poeng", True, BLUE)

    def jumping_rope(self):
        self.jumping_rope_game = JumpingRopeGame()
        score = self.jumping_rope_game.run()
        self.points += score

        self.background_img = pg.transform.scale(long_jump_img, (WIDTH, HEIGHT))

        self.long_jump_button.display = True
        self.result_text = font.render(f"Resultatet ditt etter hoppetauspillet er {self.points} poeng", True, BLUE)

    def long_jump(self):
        self.long_jump_game = LongJumpGame()
        score = self.long_jump_game.run()
        self.points += score

        self.background_img = pg.transform.scale(trivia_img, (WIDTH, HEIGHT))

        self.trivia_button.display = True
        self.result_text = font.render(f"Resultatet ditt etter lengdehoppspillet er {self.points} poeng", True, BLUE)

    def trivia(self):
        self.trivia_game = TriviaGame()
        score = self.trivia_game.run()
        self.points += score
        
        if self.points > highscore:
            data['Highscore']['score'] = self.points
            data['Highscore']['username'] = self.username

            # Skriv de oppdaterte dataene tilbake til filen
            with open('highscore.txt', 'w') as file:
                json.dump(data, file)
            self.highscore_text = font.render(f"Du fikk til sammen {self.points} poeng! Det er ny rekord! Gratulerer!", True, RED)

        else:
            self.highscore_text = font.render(f"Du fikk til sammen {self.points} poeng! Highscoren er det {data['Highscore']['username']} som har med {data['Highscore']['score']} poeng.", True, RED)
            
        self.background_img = pg.transform.scale(finish_img, (WIDTH, HEIGHT))

        self.result_text = None
        self.finish_text = font.render(f"Nå er hippocampusspillet ferdig!", True, BLUE)
        self.finish2_text = font.render(f"Trykk på hjem-knappen hvis du vil starte hele spillet på nytt!", True, BLUE)


    def run(self):
        running = True
        while running:
            screen.blit(self.background_img, (0, 0))

            self.draw_buttons()
            self.draw_text()

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.username = self.text
                        self.active = not self.active
                        self.text = " "
                    else:
                        self.active = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                        self.username+= event.unicode

                for button in self.buttons:
                    if button.display and button.is_clicked(event):
                        button.action()
                        self.text = " "
                        self.username_shown = False
                        break

            self.clock.tick(FPS)
        pg.quit()
        sys.exit()


class Button:
    def __init__(self, img, color, rect, action):
        self.img = img
        self.color = color
        self.rect = rect
        self.action = action
        self.display = False

    def draw(self):
        screen.blit(self.img, self.rect.topleft)
        
    def is_clicked(self, event):
        if self.display == True:
            if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.display = False
                return True
        return False
        
class MiniGame(Game):
    def __init__(self):
        super().__init__()
        self.screen = screen
        self.score = 0
        self.background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
        self.home_button.display = True

from reaction import *
from jumprope import *
from longjump import *
from trivia import *

game = Game()
game.run()