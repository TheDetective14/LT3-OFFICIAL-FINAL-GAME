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

class MathRoomGame:
    def __init__(self):
    # Initialize screen settings
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("BrainScape - Math Room")

    # Load images
        self.background_image = pygame.image.load("background.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.heart_image = pygame.image.load("heart.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (25, 25))

    # Set font settings
        self.pixel_font_display = pygame.font.Font("Minecraft.ttf", 30)
        self.pixel_font_large = pygame.font.Font("Minecraft.ttf", 24)
        self.pixel_font_small = pygame.font.Font("Minecraft.ttf", 18)

    # Define olors
        self.dark_text_color = (40, 40, 40)
        self.clue_text_color = (60, 60, 60)
        self.faded_text_color = (40, 40, 40, 100)
        self.highlighted_text_color = (137, 207, 240)

    # Initialize game variables
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.selected_option = 0
        self.current_question_index = 0
        self.total_questions = 5
        self.mistakes_count = 0
        self.lives_count = 3
        self.score = 0  # Player's score


    # Pool of Math Questions
        self.questions_pool = [
        {"question": "A train travels 120 miles at 60 mph. How long is the journey?", 
        "clue": "Use: time = distance / speed.", 
        "options": ["1 hour", "2 hours", "3 hours"], 
        "answer": "2 hours"},
        
        {"question": "Solve 2(x - 4) = 10. What is x?", 
        "clue": "Expand and solve for x.", 
        "options": ["9", "7", "10"], 
        "answer": "9"},
        
        {"question": "A circle's diameter is 14 cm. What is its circumference? (Use pi = 3.14)", 
        "clue": "Circumference = pi x diameter.", 
        "options": ["28 cm", "44 cm", "14 cm"], 
        "answer": "44 cm"},
        
        {"question": "If 3x + 2 = 11, what is x?", 
        "clue": "Isolate x in the equation.", 
        "options": ["3", "2", "5"], 
        "answer": "3"},
        
        {"question": "A rectangular garden is 12 m long and 5 m wide. What is the area?", 
        "clue": "Area = length x width.", 
        "options": ["60 m²", "70 m²", "40 m²"], 
        "answer": "60 m²"},
        
        {"question": "The sum of three consecutive even numbers is 48. What are they?", 
        "clue": "Let the numbers be x, x+2, x+4.", 
        "options": ["14, 16, 18", "12, 14, 16", "10, 12, 14"], 
        "answer": "14, 16, 18"},
        
        {"question": "For a triangle with sides 7, 8, and 9, what is the area?", 
        "clue": "Use Heron's formula.", 
        "options": ["26.83", "27.00", "25.00"], 
        "answer": "26.83"},
        
        {"question": "For a right triangle with side lengths in a 3:4 ratio, what is the hypotenuse?", 
        "clue": "Use the Pythagorean theorem: a² + b² = c².", 
        "options": ["5", "7", "8"], 
        "answer": "5"},
        
        {"question": "Calculate 2^3 + 3^2. What is the result?", 
        "clue": "Calculate the powers before adding.", 
        "options": ["17", "18", "19"], 
        "answer": "17"},
        
        {"question": "A rectangle has a perimeter of 36 cm, and its length is twice the width. What are the dimensions?", 
        "clue": "Set up equations for length and width.", 
        "options": ["6 cm by 12 cm", "8 cm by 16 cm", "9 cm by 18 cm"], 
        "answer": "6 cm by 12 cm"},
        
        {"question": "What is the probability of rolling a 7 with two dice?", 
        "clue": "Count the combinations for a sum of 7.", 
        "options": ["1/6", "1/12", "1/36"], 
        "answer": "1/6"},
        
        {"question": "For p(x) = x² - 5x + 6, what are the roots?", 
        "clue": "Factor the polynomial.", 
        "options": ["-2 and -3", "1 and 6", "0 and 5"], 
        "answer": "-2 and -3"},
        
        {"question": "The father-son age ratio is 7:2. If the son is 8, how old is the father?", 
        "clue": "Use the ratio to find the father's age.", 
        "options": ["16", "28", "32"], 
        "answer": "28"},
        
        {"question": "What is the least common multiple (LCM) of 12 and 18?", 
        "clue": "Find multiples of each number.", 
        "options": ["36", "72", "24"], 
        "answer": "36"},
        
        {"question": "What is the slope of the line 2y - 4x = 8?", 
        "clue": "Rearrange to slope-intercept form.", 
        "options": ["2", "4", "1"], 
        "answer": "2"},
        
        {"question": "In a bag with 5 red, 6 blue, and 9 green marbles, what is the probability of drawing a blue marble?", 
        "clue": "Total marbles = 5 + 6 + 9.", 
        "options": ["2/5", "3/10", "1/2"], 
        "answer": "3/10"},
        
        {"question": "Solve for x in 5x - 3 = 2x + 9.", 
        "clue": "Combine like terms to find x.", 
        "options": ["4", "5", "6"], 
        "answer": "4"},
        
        {"question": "What is the measure of an interior angle in a regular hexagon?", 
        "clue": "Use: (n-2) * 180 / n.", 
        "options": ["120", "108", "135"], 
        "answer": "120"},
        
        {"question": "In a right triangle with legs of 6 cm and 8 cm, what is the hypotenuse?", 
        "clue": "Use the Pythagorean theorem.", 
        "options": ["10", "12", "14"], 
        "answer": "10"},
        
        {"question": "What is x in |2x - 3| = 5?", 
        "clue": "Consider both cases for absolute values.", 
        "options": ["-1 and -4", "-4 and 1", "-1 and 4"], 
        "answer": "-1 and 4"},
        
        {"question": "What does the equation x² + 6x + 9 = 0 factor into?", 
        "clue": "Look for perfect squares.", 
        "options": ["(x + 3)²", "(x + 4)²", "(x - 3)²"], 
        "answer": "(x + 3)²"},
        
        {"question": "One company has 3 times the employees of another. If the smaller has 12, how many does the larger have?", 
        "clue": "Multiply to find the answer.", 
        "options": ["36", "24", "12"], 
        "answer": "36"},
        
        {"question": "If f(x) = 3x² - 2x + 1, what is f(2)?", 
        "clue": "Substitute 2 into the function.", 
        "options": ["5", "9", "15"], 
        "answer": "9"},
        
        {"question": "A number multiplied by 4 and decreased by 12 gives 8. What is the number?", 
        "clue": "Set up 4x - 12 = 8 and solve.", 
        "options": ["5", "6", "7"], 
        "answer": "5"},
        
        {"question": "A bottle has a water-juice ratio of 3:1. If there are 12 liters total, how much water is there?", 
        "clue": "Find 3 parts of the total mixture.", 
        "options": ["9 liters", "8 liters", "6 liters"], 
        "answer": "9 liters"}
    ]
        self.questions = self.get_random_questions(self.total_questions)


    def get_random_questions(self, num_questions=5):
        """
        Selects a random subset of questions from the question pool. 
        """
        random_questions = random.sample(self.questions_pool, num_questions)
        for question in random_questions:
            random.shuffle(question["options"])
        return random_questions
    

    def draw_wrapped_text(self, surface, text, font, color, rect, line_height=30):
        """
        Draws text within a specified rectangle to ensure the text fits both the height and width constraints. This ensures that the text is clearly visible against the background image without obscuring important elements.
        """
        words = text.split()
        lines = []
        line = ""
        for word in words:
            test_line = line + word + " "
            test_line_surface = font.render(test_line, True, color)
            if test_line_surface.get_width() > rect.width:
                lines.append(line)
                line = word + " "
            else:
                line = test_line
        lines.append(line)

        y = rect.y
        for line in lines:
            line_surface = font.render(line, True, color)
            line_rect = line_surface.get_rect(center=(rect.centerx, y + line_height // 2))
            surface.blit(line_surface, line_rect)
            y += line_height

    def draw_centered_text(self, surface, text, font, color, rect, alpha=255):
        """
        Center-align the text within the specified area.
        """
        text_surface = font.render(text, True, color)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery))
        surface.blit(text_surface, text_rect)

    def draw_lives(self):
        """
        Displays the player's remaining lives with heart assets at the top right corner of the screen. 
        """
        lives_text = self.pixel_font_small.render("Lives:", True, self.dark_text_color)
        self.screen.blit(lives_text, (self.width - 20 - lives_text.get_width() - (self.lives_count * 30), 12))

        for i in range(self.lives_count):
            self.screen.blit(self.heart_image, (self.width - 50 - (i * 30), 10))

    def draw_score(self):
        """
        Display the player's score at the top-left corner of the screen.
        """
        score_text = self.pixel_font_small.render(f"Score: {self.score}/{self.total_questions}", True, self.dark_text_color)
        self.screen.blit(score_text, (20, 12))

    def show_feedback(self, message, color):
        """
        Shows feedback messages to the user indicating whether they chose the right answer or not. 
        """
        self.screen.blit(self.background_image, (0, 0))
        text_area_rect = pygame.Rect((self.width - 600) // 2, (self.height - 320) // 2, 600, 320)
        self.draw_centered_text(self.screen, message, self.pixel_font_large, color, text_area_rect)
        pygame.display.flip()
        pygame.time.wait(1000)


    def display_end_screen(self, is_successful):
        """
        Displays an end screen with a success or failure message based on the player's performance.
        """
        self.screen.blit(self.background_image, (0, 0))
        end_message = "Congratulations! You've conquered the Math Challenge!" if is_successful else """You have no more lives left. Please try again."""
        text_area_rect = pygame.Rect((self.width - 600) // 2, (self.height - 150) // 2, 600, 320)
        self.draw_wrapped_text(self.screen, end_message, self.pixel_font_display, self.dark_text_color, text_area_rect)
        pygame.display.flip()
        pygame.time.wait(3000)


    def run_game_loop(self):
        """
        Main game loop where questions are presented, player input is processed, and score and lives are updated based on player responses.
        """
        while self.is_running:
        # Display background, lives, and score
            self.screen.blit(self.background_image, (0, 0))
            self.draw_lives()
            self.draw_score()  # Draw score on screen

        # Check if game has ended
            if self.current_question_index >= self.total_questions or self.lives_count <= 0:
                break

        # Get the current question and options.
            question_data = self.questions[self.current_question_index]
            question_text = question_data["question"]
            clue_text = question_data["clue"]
            options = question_data["options"]

        # Display background, lives, and score
            text_area_rect = pygame.Rect((self.width - 600) // 2, (self.height - 320) // 2, 600, 320)
            question_rect = pygame.Rect(text_area_rect.x, text_area_rect.y, text_area_rect.width, 80)
            self.draw_wrapped_text(self.screen, question_text, self.pixel_font_large, self.dark_text_color, question_rect)

            clue_rect = pygame.Rect(text_area_rect.x, question_rect.bottom + 10, text_area_rect.width, 30)
            self.draw_wrapped_text(self.screen, f"Clue: {clue_text}", self.pixel_font_small, self.clue_text_color, clue_rect)

            option_start_y = clue_rect.bottom + 20
            for i, option in enumerate(options):
                alpha = 255 if i == self.selected_option else 100
                color = self.highlighted_text_color if i == self.selected_option else self.faded_text_color
                option_rect = pygame.Rect(text_area_rect.x, option_start_y + i * 40, text_area_rect.width, 30)
                self.draw_centered_text(self.screen, option, self.pixel_font_large, color, option_rect, alpha)



        # Handle player input 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if options[self.selected_option] == question_data["answer"]:
                            self.current_question_index += 1
                            self.selected_option = 0
                            self.score += 1  # Increment score for a correct answer
                            self.show_feedback("Correct!", self.dark_text_color)
                        else:
                            self.mistakes_count += 1
                            self.lives_count -= 1
                            self.show_feedback("Incorrect. Try again!", (200, 0, 0))

            pygame.display.flip()
            self.clock.tick(30)


    # Show end screen screen after game loop.
        self.display_end_screen(self.current_question_index == self.total_questions)

    def run(self):
        "Starts the game loop and handles game exit."

        self.run_game_loop()
        pygame.quit()