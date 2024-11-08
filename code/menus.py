from settings import *

class MainMenu:
    def __init__(self, display, gameStatemanager):
        
        self.display = display
        self.gameStatemanager = gameStatemanager

    def run(self):
        pass

class MemoryGame:
    def __init__(self, display, gameStateManager):
        
        self.display = display
        self.gameStateManager = gameStateManager

        # Load background image and fonts
        self.background_image = pygame.image.load(join('images', 'AR_Background.png'))
        self.pixel_font_display = pygame.font.Font(join('fonts', 'Minecraft.ttf'), 30)
        self.pixel_font_large = pygame.font.Font(join('fonts', 'Minecraft.ttf'), 24)
        self.pixel_font_small = pygame.font.Font(join('fonts', 'Minecraft.ttf'), 18)

        # Display setup
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Memory Puzzle Game")

        # Score tracking
        self.previous_score = 0
        self.high_score = 0
        
    # Default font
    def display_text(self, text, position, font=None):
        if font is None:
            font = self.pixel_font_display
        text_surface = font.render(text, True, 'white')
        self.screen.blit(text_surface, position)

    # Draws buttons
    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, 'brown', rect)
        button_text = self.pixel_font_small.render(text, True, 'white')
        self.screen.blit(button_text, (rect.x + (rect.width - button_text.get_width()) // 2, 
                                       rect.y + (rect.height - button_text.get_height()) // 2))

    def show_sequence(self, sequence, interval):
        for number in sequence:
            self.screen.blit(self.background_image, (0, 0))
            self.display_text(str(number), (WINDOW_WIDTH // 2 - 20, WINDOW_HEIGHT // 2 - 20))
            pygame.display.update()
            time.sleep(interval)
            self.screen.blit(self.background_image, (0, 0))
            pygame.display.update()
            time.sleep(0.5)

    def display_correct_sequence(self, sequence):
        """Displays the correct sequence to the player after the round ends."""
        self.screen.blit(self.background_image, (0, 0))
        self.display_text("Correct Sequence:", (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50))
        

        # Display each number in the correct sequence, spaced according to their widths
        x_start = WINDOW_WIDTH // 2 - (len(sequence) * 50) // 2  # Center the numbers
        for number in sequence:
            number_text = str(number)
            number_width = self.pixel_font_small.size(number_text)[0]  # Get width of the number text
            self.display_text(number_text, (x_start, WINDOW_HEIGHT // 2))
            x_start += number_width + 20  # Increment position for next number with some extra spacing
            
        pygame.display.update()
        time.sleep(3)  # Show for 3 seconds

    def get_player_input(self, sequence_length):
        """Makes the input box from which players add their numbers, and makes a submit box to confirm"""
        input_box = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 25, 300, 50)
        user_input = ''
        player_sequence = []

        button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 60, 150, 50)

        input_active = True
        start_time = time.time()

        while input_active and len(player_sequence) < sequence_length:
            self.screen.blit(self.background_image, (0, 0))

            self.display_text(f"Enter number {len(player_sequence) + 1}/{sequence_length}:", 
                              (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 100), self.pixel_font_small)
            pygame.draw.rect(self.screen, 'white', input_box)
            pygame.draw.rect(self.screen, 'black', input_box, 2)

            input_surface = self.pixel_font_small.render(user_input, True, 'black')
            self.screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

            self.draw_button(button_rect, "Submit")

            elapsed_time = int(10 - (time.time() - start_time))
            timer_text = self.pixel_font_small.render(f"Time: {elapsed_time}", True, 'white')
            self.screen.blit(timer_text, (WINDOW_WIDTH - 200, 150))

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
        """Checks if the sequence given by player is correct, and assign points based on the round number, and if correct"""
        points_per_correct = 1 if round_num <= 2 else 2 if round_num in [3, 4] else 3
        correct_count = 0
        for i in range(min(len(player_input), len(correct_sequence))):
            if player_input[i] == correct_sequence[i]:
                correct_count += points_per_correct
        return correct_count

    def main_menu(self):
        """Draws the main menu. It has the start and exit button, and shows the previous score and the highest score"""
        self.screen.blit(self.background_image, (0, 0))
        
        self.display_text("Memory Game!", (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 100))
        self.display_text(f"Previous Score: {self.previous_score}", (WINDOW_WIDTH // 2 - 400, WINDOW_HEIGHT // 2 + 150), self.pixel_font_small)
        self.display_text(f"High Score: {self.high_score}", (WINDOW_WIDTH // 2 - 400, WINDOW_HEIGHT // 2 + 200), self.pixel_font_small)

        start_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, 200, 50)
        exit_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, 200, 50)

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

    def run(self):
        """Main function of the game.
        1. Initializes mnimum score to pass
        2. Initializes round number
        3. Increases round number per level
        4. Initializes score and base interval
        5. Applies different conditions depending on the round number, especially at rounds 3,4 and 5
        6. Displays the current score after each round
        7. Checks if player has the minimum score to pass
        8. If player does, they pass the game. If not, they fail """
        minimum_score = 20
        while True:
            if not self.main_menu():
                break

            round_num = 1
            score = 0
            base_interval = 1.5
            running = True

            while running and round_num <= 5:
                self.screen.blit(self.background_image, (0, 0))
                
                self.display_text(f"Round {round_num}", (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 20))
                pygame.display.update()
                time.sleep(3)

                if round_num == 3:
                    self.screen.blit(self.background_image, (0, 0))
                    self.display_text("Sequence increases by one!", (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 40), self.pixel_font_small)
                    self.display_text("Double digit numbers will now be included!", (WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 + 40), self.pixel_font_small)
                    self.display_text("Two points each correct answer!", (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 ), self.pixel_font_small)
                    pygame.display.update()
                    time.sleep(4)
                if round_num == 5:
                    self.screen.blit(self.background_image, (0, 0))
                    self.display_text("Sequence increases by one!", (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 40), self.pixel_font_small)
                    self.display_text("Special number included!", (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 40), self.pixel_font_small)
                    self.display_text("Three points each correct answer!", (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 ), self.pixel_font_small)
                    pygame.display.update()
                    time.sleep(4)

                sequence_length = 4 
                number_range = (0, 99 if round_num >= 3 else 9)
                if round_num == 3:
                    sequence_length = 5
                    base_interval = 1.0
                elif round_num == 4:
                    sequence_length = 5
                    base_interval = 0.8

                    
                elif round_num == 5:
                    sequence_length = 6
                    base_interval = 0.3

                sequence = [random.randint(*number_range) for _ in range(sequence_length)]
                if round_num == 5:
                    sequence[random.randint(0, sequence_length - 1)] = round(math.pi,5)

                self.show_sequence(sequence, base_interval)
                player_input = self.get_player_input(sequence_length)

                if player_input is None:
                    running = False
                    continue

                score += self.check_sequence(player_input, sequence, round_num)
                self.display_correct_sequence(sequence)
                
                round_num += 1
                player_input = sequence
                
                self.screen.blit(self.background_image, (0, 0))
                
                self.display_text(f"Current Score: {score}", (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 -10 ))
                pygame.display.update()
                time.sleep(2)

            if score <= minimum_score or score >=minimum_score:
                self.previous_score = score
                self.high_score = max(self.high_score, self.previous_score)
            if running:
                self.screen.blit(self.background_image, (0, 0))
                
                self.display_text("Game Over!", (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50), self.pixel_font_large)
                if score >= minimum_score:
                    self.display_text("Congratulations! You Passed!", (WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2))
                else:
                    self.display_text("Try Again!", (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))
                self.display_text(f"Final Score: {score}", (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 60), self.pixel_font_small)
                self.display_text(f"Minimum Score: {minimum_score}", (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100), self.pixel_font_small)
                pygame.display.update()
                time.sleep(3)

class ContinentMatchGame:
    def __init__(self, display, gameStateManager):
        
        self.screen = display
        self.gameStateManager = gameStateManager
        
        pygame.display.set_caption("Continent Match")

        # Load background image and scale it to fit the screen
        self.background_image = pygame.image.load(join('images', 'geography.png')).convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (800, 600))

        # Define colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.dark_green = (0, 100, 0)

        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.timer_font = pygame.font.Font(None, 48)

        # Countries and continents
        self.countries = [
            ("Brazil", "South America"), ("Nigeria", "Africa"), ("China", "Asia"), 
            ("France", "Europe"), ("Australia", "Oceania"), ("Canada", "North America"), 
            ("Antarctica", "Antarctica"), ("Argentina", "South America"), ("Kenya", "Africa"), 
            ("Japan", "Asia"), ("Germany", "Europe"), ("New Zealand", "Oceania"),
            ("United States", "North America"), ("Chile", "South America"), ("Egypt", "Africa"), 
            ("India", "Asia"), ("Italy", "Europe"), ("Fiji", "Oceania"), ("Mexico", "North America"),
            ("Peru", "South America"), ("South Africa", "Africa"), ("Thailand", "Asia"), 
            ("United Kingdom", "Europe"), ("Papua New Guinea", "Oceania"), ("Cuba", "North America"),
            ("Colombia", "South America"), ("Ethiopia", "Africa"), ("Russia", "Asia"), 
            ("Spain", "Europe"), ("Philippines", "Asia"), ("Iceland", "Europe"), 
            ("Jamaica", "North America"), ("Uruguay", "South America"), ("Turkey", "Asia"), 
            ("Saudi Arabia", "Asia"), ("Portugal", "Europe"), ("Venezuela", "South America")
        ]

        # Screen setup
        self.box_width, self.box_height = 160, 80
        self.gap_x, self.gap_y = 30, 30
        self.time_limit = 40

        # Game variables
        self.reset_game()

    def reset_game(self):
        random.shuffle(self.countries)
        self.country_list = self.countries.copy()
        self.selected_country, self.correct_continent = self.country_list.pop()
        self.score = 0
        self.dragging = False
        self.game_start_time = time.time()
        self.running = True
        self.show_try_again = False

        # Position continent boxes
        top_row_start_x = (WINDOW_WIDTH - (4 * self.box_width + 3 * self.gap_x)) // 2
        bottom_row_start_x = (WINDOW_WIDTH - (3 * self.box_width + 2 * self.gap_x)) // 2
        top_row_y = (WINDOW_HEIGHT - 2 * self.box_height - self.gap_y) // 2
        bottom_row_y = top_row_y + self.box_height + self.gap_y
        
        self.continents = {
            "Africa": pygame.Rect(top_row_start_x, top_row_y, self.box_width, self.box_height),
            "Asia": pygame.Rect(top_row_start_x + (self.box_width + self.gap_x), top_row_y, self.box_width, self.box_height),
            "Europe": pygame.Rect(top_row_start_x + 2 * (self.box_width + self.gap_x), top_row_y, self.box_width, self.box_height),
            "North America": pygame.Rect(top_row_start_x + 3 * (self.box_width + self.gap_x), top_row_y, self.box_width, self.box_height),
            "South America": pygame.Rect(bottom_row_start_x, bottom_row_y, self.box_width, self.box_height),
            "Oceania": pygame.Rect(bottom_row_start_x + (self.box_width + self.gap_x), bottom_row_y, self.box_width, self.box_height),
            "Antarctica": pygame.Rect(bottom_row_start_x + 2 * (self.box_width + self.gap_x), bottom_row_y, self.box_width, self.box_height)
        }
        
        # Country box and try again button
        self.country_rect = pygame.Rect((WINDOW_WIDTH - self.box_width) // 2, bottom_row_y + self.box_height + self.gap_y, self.box_width, self.box_height)
        self.country_rect_original_pos = self.country_rect.topleft  # Store the original position
        self.try_again_button = pygame.Rect((WINDOW_WIDTH - 200) // 2, WINDOW_HEIGHT // 2 + 60, 200, 50)
        
        # Timer and score display positions
        self.timer_x = self.country_rect.x - 200
        self.score_x = self.country_rect.x + self.country_rect.width + 50
        self.text_y = self.country_rect.y

    def get_fitting_font(self, text, rect_width, rect_height, max_font_size=36):
        fitting_font = pygame.font.Font(None, max_font_size)
        while fitting_font.size(text)[0] > rect_width - 10 or fitting_font.size(text)[1] > rect_height - 10:
            max_font_size -= 2
            fitting_font = pygame.font.Font(None, max_font_size)
        return fitting_font

    def run(self):
        while self.running:
            self.screen.blit(self.background_image, (0, 0))  # Draw the background image
            current_time = time.time()
            elapsed_time = current_time - self.game_start_time
            remaining_time = max(0, self.time_limit - int(elapsed_time))

            # Game end conditions
            if self.score >= 5:
                self.display_text("YOU WIN", self.timer_font)
                pygame.time.delay(3000)
                break
            elif remaining_time == 0:
                self.display_text("Time's Up! You Lose!")
                self.show_try_again = True

            # Event handling
            self.handle_events()

            # Drawing elements
            self.draw_continents()
            self.draw_country()
            self.draw_timer_and_score(remaining_time)

            if self.show_try_again:
                self.draw_try_again_button()

            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.show_try_again and event.type == pygame.MOUSEBUTTONDOWN and self.try_again_button.collidepoint(event.pos):
                self.reset_game()
                self.show_try_again = False
            if event.type == pygame.MOUSEBUTTONDOWN and not self.show_try_again:
                if self.country_rect.collidepoint(event.pos):
                    self.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    self.dragging = False
                    if self.continents[self.correct_continent].colliderect(self.country_rect):
                        self.score += 1
                    if not self.country_list:
                        self.reset_game()
                    else:
                        self.selected_country, self.correct_continent = self.country_list.pop()
                    # Reset the country_rect to its original position
                    self.country_rect.topleft = self.country_rect_original_pos
            if event.type == pygame.MOUSEMOTION and self.dragging:
                # Set the center of country_rect to follow the mouse position
                self.country_rect.center = event.pos

    def draw_continents(self):
        for continent, rect in self.continents.items():
            pygame.draw.rect(self.screen, self.white, rect)
            fitting_font = self.get_fitting_font(continent, rect.width, rect.height)
            text = fitting_font.render(continent, True, self.dark_green)
            self.screen.blit(text, (rect.x + (rect.width - text.get_width()) // 2, rect.y + (rect.height - text.get_height()) // 2))

    def draw_country(self):
        pygame.draw.rect(self.screen, self.black, self.country_rect)
        fitting_font = self.get_fitting_font(self.selected_country, self.country_rect.width, self.country_rect.height)
        country_text = fitting_font.render(self.selected_country, True, self.white)
        self.screen.blit(country_text, (self.country_rect.x + (self.country_rect.width - country_text.get_width()) // 2, self.country_rect.y + 10))

    def draw_timer_and_score(self, remaining_time):
        timer_text = self.timer_font.render(f"Time: {remaining_time}", True, self.black)
        score_text = self.timer_font.render(f"Score: {self.score}", True, self.black)
        self.screen.blit(timer_text, (self.timer_x, self.text_y))
        self.screen.blit(score_text, (self.score_x, self.text_y))

    def draw_try_again_button(self):
        pygame.draw.rect(self.screen, self.white, self.try_again_button)
        try_again_text = self.font.render("TRY AGAIN", True, self.black)
        self.screen.blit(try_again_text, (self.try_again_button.x + (self.try_again_button.width - try_again_text.get_width()) // 2,
                                          self.try_again_button.y + (self.try_again_button.height - try_again_text.get_height()) // 2))

    def display_text(self, text, font):
        result_text = font.render(text, True, self.black)
        self.screen.blit(result_text, (WINDOW_WIDTH // 2 - result_text.get_width() // 2, WINDOW_HEIGHT // 2))

class JumbleGame:
    def __init__(self, display, gameStateManager):
        
        self.display = display
        self.gameStateManager = gameStateManager

        # Display
        self.SIZE = 1200
        self.screen = pygame.display.set_mode((self.SIZE, self.SIZE))
        pygame.display.set_caption("Jumble Mania: The Great Letter Escape!")
        
        # Colors
        self.WHITE = (255, 255, 255)

        # Default Fonts
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)

        # Load and scale images
        self.load_images()

        # Initialize clock
        self.clock = pygame.time.Clock()

    def load_images(self):
        self.background_intro = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'background 1 minigame.png')), (self.SIZE, self.SIZE)
        )
        self.background_image = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'background 2 minigame.png')), (self.SIZE, self.SIZE)
        )
        self.button_image = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'Start Button.png')), (200, 100)
        )
        self.hint_time_background_image = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'Hint.png')), (self.SIZE, 650)
        )
        self.tile_image = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'Tile Image.png')), (100, 70)
        )
        self.letter_background_image = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'Letter.png')), (90, 60)
        )
        self.submit_button_image = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'Submit Button.png')), (150, 75)
        )
        self.correct_image = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'Correct.png')), (200, 90)
        )
        self.incorrect_image = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'Incorrect.png')), (200, 90)
        )
        self.final_score_background_image = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'background total.png')), (self.SIZE, self.SIZE)
        )
        self.outro_background_image = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'background last minigame.png')), (self.SIZE, self.SIZE)
        )
        self.play_again_button_image = pygame.transform.scale(
            pygame.image.load(join('images', 'ace', 'Play Again Button.png')), (200, 100)
        )

    def get_word_data(self):
        return [
            ("glimpse", "A quick or brief look at something."),
            ("idle", "Not active or not in use."),
            ("keen", "Having a sharp edge or a strong interest."),
            ("noble", "Having high moral qualities or ideals."),
            ("omit", "To leave out or exclude."),
            ("quest", "A search or pursuit to achieve something."),
            ("urgent", "Requiring immediate attention."),
            ("vague", "Not clear or specific."),
            ("witty", "Showing quick and inventive verbal humor."),
            ("zeal", "Great energy or enthusiasm in pursuit of a cause."),
            ("dwell", "To live or reside in a place."),
            ("hinge", "A joint that allows two parts to swing together."),
            ("islet", "A small island."),
            ("mirth", "Joyfulness or amusement."),
            ("rift", "A crack or split in something."),
            ("trek", "A long, arduous journey."),
            ("adept", "Skilled or proficient at something."),
            ("crisp", "Firm, dry, and brittle."),
            ("dusk", "The time just before nightfall."),
            ("grief", "Deep sorrow, especially caused by loss."),
            ("vow", "A solemn promise."),
            ("pique", "To stimulate interest or curiosity."),
            ("tweak", "To make slight adjustments to something."),
            ("align", "To place in a straight line or proper position."),
            ("haven", "A place of safety or refuge."),
            ("mend", "To repair something that is broken."),
            ("utter", "To speak or say something."),
            ("avert", "To turn away or prevent something."),
            ("tangle", "To twist or knot together."),
            ("quaint", "Attractively unusual or old-fashioned."),
            ("abide", "To accept or act in accordance with something."),
            ("mundane", "Ordinary or commonplace."),
            ("kindle", "To ignite or inspire."),
            ("excel", "To perform exceptionally well."),
            ("unite", "To come together for a common purpose."),
            ("ample", "More than enough."),
            ("jargon", "Specialized language used by a particular group."),
            ("lucid", "Clear and easy to understand."),
            ("zenith", "The highest point or peak of something."),
            ("nuance", "A subtle difference in meaning or expression."),
            ("quirk", "A peculiar behavior or trait."),
            ("ally", "A partner or friend in a common cause."),
            ("gist", "The main point or essence of something."),
            ("knack", "A special skill or talent."),
            ("quell", "To suppress or put an end to."),
            ("nifty", "Particularly good, clever, or stylish."),
            ("vouch", "To assert or confirm the truth of something."),
            ("candid", "Honest and straightforward; open."),
            ("serene", "Calm, peaceful, and untroubled."),
            ("justice", "The quality of being fair."),
        ]

    def scramble_word(self, word):
        return ''.join(random.sample(word, len(word)))

    class Letter:
        def __init__(self, char, x, y):
            self.char = char
            self.rect = pygame.Rect(x, y, 70, 50)
            self.dragging = False
            self.offset_x = 0
            self.offset_y = 0

        def draw(self, screen, font, background_image):
            screen.blit(background_image, self.rect.topleft)
            text_surface = font.render(self.char, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def draw_text(self, text, font, color, rect):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def show_start_button(self):
        waiting = True
        while waiting:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background_intro, (0, 0))

            button_rect = self.button_image.get_rect(center=(self.SIZE // 2, self.SIZE // 2))
            self.screen.blit(self.button_image, button_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        waiting = False

            pygame.display.flip()

    def play_game(self):
        word_data = self.get_word_data()
        total_score = 0 
        while True:
            questions = random.sample(word_data, min(5, len(word_data)))

            for word, definition in questions:
                scrambled = self.scramble_word(word)
                letters = [self.Letter(char, 0, 0) for char in scrambled]
                running = True
                start_time = time.time()
                time_limit = 15
                result_image = None
                show_result = False
                result_time = 0
                correct_answer = ""

                tile_start_x = self.SIZE // 2 - (100 * len(scrambled) + 10 * (len(scrambled) - 1)) // 2
                tile_start_y = 350

                for i, letter in enumerate(letters):
                    letter.rect.topleft = (tile_start_x + i * (100 + 10), tile_start_y)

                while running:
                    self.screen.blit(self.background_image, (0, 0))
                    self.screen.blit(self.hint_time_background_image, (-30, -15))

                    self.draw_text(f"{definition}", self.font, self.WHITE, pygame.Rect(self.SIZE // 2, 260, 0, 0))
                    self.draw_text(f"Time left: {max(0, time_limit - int(time.time() - start_time))}", self.font, self.WHITE, pygame.Rect(self.SIZE // 2, 285, 0, 0))

                    for i in range(len(scrambled)):
                        self.screen.blit(self.tile_image, (tile_start_x + i * (100 + 10), tile_start_y))

                    for letter in letters:
                        letter.draw(self.screen, self.font, self.letter_background_image)

                    button_x = self.SIZE // 2 - 75
                    button_y = 470
                    self.screen.blit(self.submit_button_image, (button_x, button_y))

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            for letter in letters:
                                if letter.rect.collidepoint(event.pos):
                                    letter.dragging = True
                                    letter.offset_x = event.pos[0] - letter.rect.x
                                    letter.offset_y = event.pos[1] - letter.rect.y
                                    break

                            if button_x <= event.pos[0] <= button_x + 150 and button_y <= event.pos[1] <= button_y + 75:
                                sorted_letters = sorted(letters, key=lambda l: l.rect.x)
                                guessed_word = ''.join(letter.char for letter in sorted_letters)

                                if guessed_word == word:
                                    total_score += 1
                                    result_image = self.correct_image
                                else:
                                    result_image = self.incorrect_image
                                    correct_answer = word  
                                show_result = True
                                result_time = time.time()

                        elif event.type == pygame.MOUSEBUTTONUP:
                            for letter in letters:
                                letter.dragging = False
                            
                        elif event.type == pygame.MOUSEMOTION:
                            for letter in letters:
                                if letter.dragging:
                                    letter.rect.x = event.pos[0] - letter.offset_x
                                    letter.rect.y = event.pos[1] - letter.offset_y

                    if time.time() - start_time >= time_limit and not show_result:
                        result_image = self.incorrect_image
                        correct_answer = word  
                        show_result = True
                        result_time = time.time()
                    
                    if show_result:
                        result_x = self.SIZE // 2 - result_image.get_width() // 2
                        result_y = button_y + self.submit_button_image.get_height() + 10
                        self.screen.blit(result_image, (result_x, result_y))
                        if correct_answer:
                            self.draw_text(f"Correct answer: {correct_answer}", self.font, self.WHITE, pygame.Rect(self.SIZE // 2, result_y + 100, 0, 0))
                        if time.time() - result_time >= 1.5:  
                            show_result = False
                            break

                    pygame.display.flip()
                    self.clock.tick(60)

            # Final score
            self.screen.blit(self.final_score_background_image, (0, 0))
            self.draw_text(f"Your total score: {total_score}/{len(questions)}", self.big_font, self.WHITE, pygame.Rect(self.SIZE // 2, self.SIZE // 2 - 60, 0, 0))

            pygame.display.flip()
            time.sleep(2)

            # Outro background
            self.screen.blit(self.outro_background_image, (0, 0))
            
            if total_score >= 3:
                self.draw_text("Congratulations! You have escaped", self.big_font, self.WHITE, pygame.Rect(self.SIZE // 2, 90, 0, 0))
            else:
                self.draw_text("You've got this! A little more practice and you'll soar!", self.big_font, self.WHITE, pygame.Rect(self.SIZE // 2, 90, 0, 0))
            
            # Display the play again button only if score is 0, 1, or 2
            play_again_button_rect = None
            if total_score <= 2:
                play_again_button_rect = self.play_again_button_image.get_rect(center=(self.SIZE // 2, self.SIZE // 2 + 60))  
                self.screen.blit(self.play_again_button_image, play_again_button_rect)

            pygame.display.flip()

            # Outro function
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if total_score <= 2 and play_again_button_rect.collidepoint(event.pos):
                            total_score = 0  # Reset score when playing again
                            waiting = False

    def run(self):
        self.show_start_button()
        self.play_game()
        pygame.quit()

class MathRoomGame:
    def __init__(self, display, gameStateManger):

    # Initialize screen settings
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("BrainScape - Math Room")

    # Load images
        self.background_image = pygame.image.load(join('images', 'background.png'))
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.heart_image = pygame.image.load(join('images', 'heart.png'))
        self.heart_image = pygame.transform.scale(self.heart_image, (25, 25))

    # Set font settings
        self.pixel_font_display = pygame.font.Font(join('fonts', "Minecraft.ttf"), 30)
        self.pixel_font_large = pygame.font.Font(join('fonts', "Minecraft.ttf"), 24)
        self.pixel_font_small = pygame.font.Font(join('fonts', "Minecraft.ttf"), 18)

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
