from constants import *
from main import *

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
            self.check_task_complete()
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
                        return self.score
                    
            if self.check_task_complete():
                self.score += 1
                self.task_complete = False
                self.generate_task()  # Flytt genereringen inn hit

            if elapsed_time >= self.time_limit:
                return self.score

            self.clock.tick(FPS)
        return self.score