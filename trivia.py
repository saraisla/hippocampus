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
        self.correct_answer = None
        self.option_rects = []
        self.correct_img = pg.transform.scale(pg.image.load('bilder/correct.png'), (WIDTH, HEIGHT))

    def present_questions(self):
        self.options = []  # Nullstill listen over alternativer
        if self.question_count < 10:
            question_data = self.questions[self.question_count]

            self.question = html.unescape(question_data['question'])
            incorrect_answers = question_data['incorrect_answers']
            self.correct_answer = html.unescape(question_data['correct_answer'])

            self.options.append(self.correct_answer)
            for answer in incorrect_answers:
                self.options.append(html.unescape(answer))
            random.shuffle(self.options)

    def draw_questions(self):
        self.option_rects = []  # Nullstill listen over rektangler for alternativer
        y = 70  # Juster startposisjonen for spørsmålet
        option_text_height = font.get_height()

        # Tegn spørsmålet
        wrapped_question = textwrap.wrap(self.question, width=50)
        for line in wrapped_question:
            question_text = font.render(line, True, BLUE)
            screen.blit(question_text, (50, y))
            y += 50

        # Tegn alternativer
        for option in self.options:
            option_text = font.render(option, True, BLACK)
            option_text_rect = option_text.get_rect()

            # Juster størrelsen på bakgrunnsbildet til alternativet
            option_background = pg.image.load("bilder/alternative.png")
            option_background = pg.transform.scale(option_background, (option_text_rect.width + 40, option_text_rect.height + 40))

            # Finn posisjonen for alternativteksten
            text_x = (option_background.get_width() - option_text.get_width()) // 2
            text_y = (option_background.get_height() - option_text.get_height()) // 2

            # Plasser alternativteksten midt i bakgrunnsbildet
            text_pos = (50 + text_x, y + text_y)

            # Plasser rektangel for alternativet i samme posisjon som teksten
            option_text_rect.topleft = (50+text_x, y+text_y)

            # Tegn bakgrunnsbilde og tekst for alternativet
            screen.blit(option_background, (50, y))
            screen.blit(option_text, text_pos)

            # Legg til rektangel for alternativet i listen
            self.option_rects.append(option_text_rect)
            y += option_background.get_height() + 30  # Legg til litt mellomrom mellom alternativene






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
                    for i, option_rect in enumerate(self.option_rects):
                        if option_rect.collidepoint(event.pos):
                            print(self.options[i])
                            selected_option = self.options[i]
                            if selected_option == self.correct_answer:
                                self.score += 1
                                screen.blit(self.correct_img, (0, 0))
                                pg.display.flip()
                                pg.time.delay(1500)
                                screen.blit(self.background_img, (0, 0))  # Endre tilbake til standard bakgrunn
                                pg.display.flip()  # Oppdater skjermen

                            if self.question_count < len(self.questions) - 1:  # Endret betingelsen her
                                self.question_count += 1
                                self.present_questions()
                                self.draw_questions()
                                pg.display.flip()
                            else:
                                run = False  # Avslutt løkken når alle spørsmål er besvart

        return self.score
