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

        self.buttons = [self.start_game_button, self.home_button, self.next_button,
                        self.reaction_button, self.jumping_rope_button, self.long_jump_button,
                        self.trivia_button]

        self.points = 0
        self.input_box = pg.Rect(300, 350, 145, 32)
        self.active = False
        self.text = "Brukernavn: "
        self.color = BLACK
        self.username_shown = True
        
    def draw_buttons(self):
        for button in self.buttons:
            if button.display:
                button.draw()

    def draw_text(self):
        texts = [self.result_text, self.finish_text, self.finish2_text]
        heights = [50, 80, 110]
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


    def reaction(self):
        print("kjører")
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

        self.background_img = pg.transform.scale(finish_img, (WIDTH, HEIGHT))

        self.finish_text = font.render(f"Nå er hippocampusspillet ferdig!", True, BLUE)
        self.result_text = font.render(f"Du fikk til sammen {self.points} poeng! Bra jobba!", True, BLUE)
        self.finish2_text = font.render(f"Trykk på hjem-knappen hvis du vil starte hele spillet på nytt!", True, BLUE)

        with open(file, "a") as fil:
            fil.write(f'{self.points} poeng. \n')
            
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
                        self.active = not self.active
                        self.text = " "
                    else:
                        self.active = False

                if event.type == pg.KEYDOWN:
                    if self.active:
                        if event.key == pg.K_RETURN:
                            print(self.text)
                            with open(file, "a") as fil:
                                fil.write(f'{self.text} har ')
                             
                            self.text = " "
                            self.username_shown = False
                        elif event.key == pg.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode                
                
                else:
                    for button in self.buttons:
                        if button.display and button.is_clicked(event):
                            button.action()
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
        self.clock = pg.time.Clock()
        self.score = 0
        self.background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
        self.home_button.display = True

class ReactionGame(MiniGame):
    def __init__(self):
        super().__init__()
        self.time_limit = 30
        self.task_complete = False
        self.keys_pressed = []
        self.start_time = 0
        self.generate_task()
        
    def generate_task(self):
        self.keys_to_press = []
        self.keys = [pg.K_a, pg.K_b, pg.K_c, pg.K_d, pg.K_e, pg.K_f, pg.K_g, pg.K_h, pg.K_i, pg.K_j, pg.K_k, pg.K_l, pg.K_m, pg.K_n, pg.K_o, pg.K_p, pg.K_q, pg.K_r, pg.K_s, pg.K_t, pg.K_u, pg.K_v, pg.K_w, pg.K_x, pg.K_y, pg.K_z]
        for i in range (3):
            key= random.choice(self.keys)
            self.keys_to_press.append(key)
            self.keys.remove(key)
        
    def check_task_complete(self):
        correct = 0
        for i in self.keys_to_press:
            if i in self.keys_pressed:
                correct += 1
        return correct == 3
                
    def run(self):
        self.start_time = pg.time.get_ticks()
        while True:
            self.screen.blit(self.background_img, (0, 0))
            self.home_button.draw()
            
            current_time = pg.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000
            if elapsed_time >= self.time_limit:
                return self.score
            
            time_remaining = max(0, int(self.time_limit - elapsed_time))
            clock_text = font.render(f"Tid som gjenstår: {time_remaining} sek", True, RED)
            self.screen.blit(clock_text, (10, 10))
            
            task_text = font.render(f"Tast disse boksene: {chr(list(self.keys_to_press)[0]).upper()}, {chr(list(self.keys_to_press)[1]).upper()}, {chr(list(self.keys_to_press)[2]).upper()}", True, BLUE)
            text_rect = task_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(task_text, text_rect)
            
            score_text = font.render(f"Poengsum: {self.score}", True, RED)
            self.screen.blit(score_text, (10, 90))
            
            pg.display.flip()
            
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    self.keys_pressed.append(event.key)
                elif event.type == pg.KEYUP:
                    if event.key in self.keys_pressed:
                        self.keys_pressed.remove(event.key)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.home_button.is_clicked(event):
                        print("Trykket")
                        return self.score
            if self.check_task_complete():
                self.task_complete = True
                self.score += 1

            if elapsed_time >= self.time_limit or self.task_complete:
                self.generate_task()
                self.task_complete = False
            self.clock.tick(FPS)
        return self.score
    
class JumpingRopeGame(MiniGame):
    def __init__(self):
        super().__init__()
        self.player = PlayerRope(WIDTH // 2 - 50, HEIGHT - 220, 80, 110, RED)
        self.rope = Rope(WIDTH//2, HEIGHT//2, 10, BLUE)
        self.running = True 
        self.jump_over_rope = False

    def redraw_window(self, player, rope):
        screen.blit(self.background_img, (0, 0))
        screen.blit(player_img, (self.player.x, self.player.y))
        pg.draw.circle(screen, self.rope.color, (self.rope.x, self.rope.y), self.rope.radius)
        score_text = font.render(f"Poengsum: {self.score}", True, RED)
        screen.blit(score_text, (10, 90))
        self.home_button.draw()


    def run(self):
        while self.running: 
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False  
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT] and self.player.x > self.player.vel:
                self.player.x -= self.player.vel
            if keys[pg.K_RIGHT] and self.player.x < WIDTH - self.player.width - self.player.vel:
                self.player.x += self.player.vel
            # hopp hvis mellomromstasten trykkes og playeren ikke allerede hopper
            if not self.player.isJumping:
                if keys[pg.K_SPACE]:
                    self.player.isJumping = True
            else:
                if self.player.jumpCount >= -10:
                    neg = 1
                    if self.player.jumpCount < 0:
                        neg = -1
                    self.player.y -= (self.player.jumpCount ** 2) * 0.5 * neg
                    self.player.jumpCount -= 1
                else:
                    self.player.isJumping = False
                    self.player.jumpCount = 10

            self.rope.update()  # Oppdaterer tauets posisjon

            if self.player.y < self.rope.y and self.rope.x - self.rope.radius < self.player.x < self.rope.x + self.rope.radius * 2 and not self.jump_over_rope:
                self.score += 1
                self.rope.angular_speed+=0.005
                self.jump_over_rope = True
            elif self.player.y >= self.rope.y:
                self.jump_over_rope = False

            self.player_rect = pg.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            self.rope_rect = pg.Rect(self.rope.x - self.rope.radius, self.rope.y - self.rope.radius, 2 * self.rope.radius, 2 * self.rope.radius)
            if self.player_rect.colliderect(self.rope_rect):
                return self.score
                
            self.redraw_window(self.player, self.rope) 

            if self.player.y + self.player.height > HEIGHT:
                return self.score

            pg.display.flip()


        return self.score 

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
        self.radius = radius  
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
        
        
class LongJumpGame(MiniGame):
    def __init__(self):
        super().__init__()
        self.player = PlayerLong()
        self.sand = self.player.sand
        self.plank_b = Lane(BLACK, plank_B_X, laneR_Y, plank_B_WIDTH, laneR_HEIGHT)  
        self.plank_w = Lane(WHITE, plank_W_X, laneR_Y, plank_W_WIDTH, laneR_HEIGHT)
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

            # Deretter tegn resten av spillmiljøet
        
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
        self.player_img = pg.image.load('seahorse.png')  # Last inn spillerens bilde
        self.player_img = pg.transform.scale(self.player_img, (45, 55))  # Juster størrelsen

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
            self.meter = abs(505-self.sand.rect.x) / 100
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
        
class TriviaGame(MiniGame):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.question_count = 0
        self.questions = []
        self.question = None
        self.options = []
        self.selected_option = None
        self.correct_answer = None
        self.option_rects = []
        self.correct_img = pg.transform.scale(pg.image.load('correct.png'), (WIDTH, HEIGHT))

    def present_questions(self):
        self.options= []
        if self.question_count < 10:
            question_data = self.questions[self.question_count]
    
            self.question = question_data['question']
            incorrect_answers = question_data['incorrect_answers']
            self.correct_answer = question_data['correct_answer']
                    
            self.options.append(self.correct_answer)
            for answers in incorrect_answers:
                self.options.append(answers)
            random.shuffle(self.options)
            self.question_count += 1
            
    def draw_questions(self):
        y = 70
        option_text_height = font.get_height()
        
        wrapped_question = textwrap.wrap(self.question, width=50)
        for line in wrapped_question:
            question_text = font.render(line, True, BLUE)
            screen.blit(question_text, (50, y))
            y += 50
        
        for option in self.options:
            # Lager alternativtekstens bakgrunnsbilde
            option_text = font.render((option), True, BLACK)
            option_text_rect = option_text.get_rect(topleft=(50, y))
            
            # Justerer størrelsen på alternativets bakgrunnsbilde etter tekstens størrelse
            option_background = pg.image.load("alternative.png")
            option_background = pg.transform.scale(option_background, (option_text_rect.width + 40, option_text_rect.height + 40))
        
            # Finner ut hvor tekstboksen skal plasseres i forhold til bakgrunnsbildet
            text_x = (option_background.get_width() - option_text_rect.width) // 2
            text_y = (option_background.get_height() - option_text_rect.height) // 2
            
            option_text_rect.topleft = (50 + text_x, y + text_y)
            
            # Tegner alternativets bakgrunnsbilde og tekst
            screen.blit(option_background, (50, y))
            screen.blit(option_text, (50 + text_x, y + text_y))
            
            self.option_rects.append(option_text_rect)
            y += option_text_height + 40  # Legg til litt mellomrom mellom alternativene


    def run(self):
        url = "https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=multiple"
        response = requests.get(url)
        data = json.loads(response.text)
        self.questions = data.get('results')

        screen.blit(self.background_img, (0, 0))
        self.home_button.draw()
        
        self.present_questions()
        self.draw_questions()
        
        pg.display.flip()

        run = True
        while run:
            screen.blit(self.background_img, (0, 0))
            self.clock.tick(FPS)
            self.home_button.draw()

            for event in pg.event.get():
                if event.type == pg.QUIT or self.home_button.is_clicked(event):
                    run = False  
                elif event.type == pg.MOUSEBUTTONDOWN:
                    i = 0
                    for option_rect in self.option_rects:
                        if i<4:
                            if option_rect.collidepoint(event.pos):
                                if self.options[i] == self.correct_answer:
                                    self.score += 1
                                    screen.blit(self.correct_img, (0, 0))
                                    pg.display.flip()
                                    pg.time.delay(1500)

                                if self.question_count < len(self.questions):
                                    screen.blit(self.background_img, (0, 0))  # Tegn bakgrunnen
                                    self.home_button.draw()  # Tegn hjemknappen
                                    self.present_questions()
                                    self.draw_questions()
                                    pg.display.flip()
                                    break
                                else:
                                    run = False
                                i += 1
        return self.score             

game = Game()
game.run()
