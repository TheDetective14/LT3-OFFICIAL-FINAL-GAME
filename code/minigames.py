from settings import *
from random import *
import time
import math
import sys

class MemoryGame:
    def __init__(self):

        # Colors and fonts
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BROWN = (139, 69, 19)
        self.GREEN = (34, 139, 34)
        self.FONT = pygame.font.Font(None, 74)
        self.SMALL_FONT = pygame.font.Font(None, 50)

    def display_text(self, text, position, font=None):
        if font is None:
            font = self.FONT
        text_surface = font.render(text, True, self.WHITE)
        self.screen.blit(text_surface, position)

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, self.BLACK, rect)
        button_text = self.SMALL_FONT.render(text, True, self.WHITE)
        self.screen.blit(button_text, (rect.x + (rect.width - button_text.get_width()) // 2, 
                                        rect.y + (rect.height - button_text.get_height()) // 2))
        pygame.display.update()

    def show_sequence(self, sequence, interval):
        for number in sequence:
            self.screen.fill(self.GREEN)
            pygame.draw.rect(self.screen, self.BROWN, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 20)
            self.display_text(str(number), (self.SCREEN_WIDTH // 2 - 20, self.SCREEN_HEIGHT // 2 - 20))
            pygame.display.update()
            time.sleep(interval)
            self.screen.fill(self.GREEN)
            pygame.draw.rect(self.screen, self.BROWN, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 20)
            pygame.display.update()
            time.sleep(0.5)

    def get_player_input(self, sequence_length):
        input_box = pygame.Rect(self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 - 25, 300, 50)
        user_input = ''
        player_sequence = []

        # Enlarge submit button
        button_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 75, self.SCREEN_HEIGHT // 2 + 60, 150, 50)
        button_text = "Submit"

        input_active = True
        start_time = time.time()

        while input_active and len(player_sequence) < sequence_length:
            self.screen.fill(self.GREEN)
            pygame.draw.rect(self.screen, self.BROWN, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 20)
            self.display_text(f"Enter number {len(player_sequence) + 1}/{sequence_length}:", 
                              (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2 - 80), self.SMALL_FONT)
            pygame.draw.rect(self.screen, self.WHITE, input_box)
            pygame.draw.rect(self.screen, self.BLACK, input_box, 2)
            
            input_surface = self.SMALL_FONT.render(user_input, True, self.BLACK)
            self.screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))
            
            self.draw_button(button_rect, button_text)

            elapsed_time = int(10 - (time.time() - start_time))
            timer_text = self.SMALL_FONT.render(f"Time: {elapsed_time}", True, self.WHITE)
            self.screen.blit(timer_text, (self.SCREEN_WIDTH - 150, 20))
            
            if elapsed_time <= 0:
                player_sequence.append(None)
                user_input = ''
                start_time = time.time()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and user_input:
                        try:
                            player_sequence.append(float(user_input))
                        except ValueError:
                            pass
                        user_input = ''
                        start_time = time.time()
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() or event.unicode == '.':
                        user_input += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos) and user_input:
                        try:
                            player_sequence.append(float(user_input))
                        except ValueError:
                            pass
                        user_input = ''
                        start_time = time.time()

        return player_sequence

    def check_sequence(self, player_input, correct_sequence, round_num):
        points_per_correct = 1 if round_num <= 2 else 2 if round_num in [3, 4] else 3
        correct_count = 0
        for i in range(min(len(player_input), len(correct_sequence))):
            if player_input[i] == correct_sequence[i]:
                correct_count += points_per_correct
        return correct_count

    def main_menu(self):
        self.screen.fill(self.GREEN)
        pygame.draw.rect(self.screen, self.BROWN, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 20)
        self.display_text("Memory Game!", (self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 - 100))

        start_button = pygame.Rect(self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2, 200, 50)
        exit_button = pygame.Rect(20, 20, 100, 50)

        self.draw_button(start_button, "Start")
        self.draw_button(exit_button, "Exit")

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        return True
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

    def play_game(self):
        minimum_score = 18
        while True:
            if not self.main_menu():
                break

            round_num = 1
            score = 0
            base_interval = 1.5
            running = True

            while running and round_num <= 5:
                self.screen.fill(self.GREEN)
                pygame.draw.rect(self.screen, self.BROWN, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 20)
                self.display_text(f"Round {round_num}", (self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2 - 20))
                pygame.display.update()
                time.sleep(1)

                if round_num == 3:
                    self.screen.fill(self.GREEN)
                    pygame.draw.rect(self.screen, self.BROWN, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 20)
                    self.display_text("Sequence increases by one!", (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2 - 40), self.SMALL_FONT)
                    self.display_text("Double digit numbers will now be included!", (self.SCREEN_WIDTH // 2 - 300, self.SCREEN_HEIGHT // 2 + 20), self.SMALL_FONT)
                    pygame.display.update()
                    time.sleep(2)

                elif round_num == 5:
                    self.screen.fill(self.GREEN)
                    pygame.draw.rect(self.screen, self.BROWN, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 20)
                    self.display_text("Sequence increases by one!", (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2 - 40), self.SMALL_FONT)
                    self.display_text("Double digit numbers will now be included!", (self.SCREEN_WIDTH // 2 - 300, self.SCREEN_HEIGHT // 2 + 20), self.SMALL_FONT)
                    pygame.display.update()
                    time.sleep(2)

                if round_num == 1 or round_num == 2:
                    sequence_length = 4
                    number_range = (0, 9)
                elif round_num == 3 or round_num == 4:
                    sequence_length = 5
                    number_range = (0, 99)
                    if round_num == 3:
                        base_interval = 1.0
                else:
                    sequence_length = 6
                    number_range = (0, 99)
                    base_interval = 0.3

                sequence = [random.randint(*number_range) for _ in range(sequence_length)]
                if round_num == 5:
                    sequence[random.randint(0, sequence_length - 1)] = round(math.pi, 5)

                self.show_sequence(sequence, base_interval)
                player_input = self.get_player_input(sequence_length)
                if player_input is None:
                    running = False
                    break

                correct_numbers = self.check_sequence(player_input, sequence, round_num)
                score += correct_numbers

                self.screen.fill(self.GREEN)
                pygame.draw.rect(self.screen, self.BROWN, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 20)
                self.display_text(f"{correct_numbers}/{sequence_length} Correct", (self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 - 20))
                self.display_text(f"Current Score: {score}", (self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 + 60), self.SMALL_FONT)
                pygame.display.update()
                time.sleep(2)

                correct_sequence_text = "Correct sequence: " + ' '.join(map(str, sequence))
                text_surface = self.SMALL_FONT.render(correct_sequence_text, True, self.WHITE)
                self.screen.fill(self.GREEN)
                pygame.draw.rect(self.screen, self.BROWN, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 20)
                self.screen.blit(text_surface, (self.SCREEN_WIDTH // 2 - text_surface.get_width() // 2, self.SCREEN_HEIGHT // 2 + 80))
                pygame.display.update()
                time.sleep(2)

                round_num += 1

            self.screen.fill(self.GREEN)
            pygame.draw.rect(self.screen, self.BROWN, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 20)

            if score >= minimum_score:
                self.display_text(f"Congratulations! Final Score: {score}", (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2 - 20))
            else:
                self.display_text("So close! Minimum Score: 18", (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2 - 20))
                self.display_text("Press any key to try again", (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2 + 60), self.SMALL_FONT)

                pygame.display.update()
                time.sleep(2)
                
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            waiting = False
