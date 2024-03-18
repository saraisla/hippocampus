from constants import *
from main import *


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
                    
            self.options.append(html.unescape(self.correct_answer))
            for answers in incorrect_answers:
                self.options.append(html.unescape(answers))
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