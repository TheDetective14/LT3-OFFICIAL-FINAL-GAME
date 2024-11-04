from settings import *
from minigames import *
from gamemanager import GameStateManager

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.display_surface = display
        self.state, self.frame_index = 'down', 0
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-1, -1)

        self.gameStateManager = GameStateManager('Hall')
        
        self.Hall = Hall(self.display_surface, self.gameStateManager)
        self.ARMinigame = MemoryGame(self.display_surface, self.gameStateManager)
        self.mathMinigame = MathRoomGame(self.display_surface, self.gameStateManager)
        self.geoMinigame = ContinentMatchGame(self.display_surface, self.gameStateManager)
        self.englishMinigame = JumbleGame(self.display_surface, self.gameStateManager)

        self.states = {
            'Hall':self.Hall,
            'AR': self.ARMinigame,
            'Math': self.mathMinigame,
            'Geography': self.geoMinigame,
            'English': self.englishMinigame,
            }
        
        self.direction = pygame.Vector2()
        self.speed = 200
        self.collision_sprites = collision_sprites

    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)
    
    def input(self):        
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self,dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
    
    def teleport(self):
        proximity_points = {
            "abstract_reasoning": pygame.Rect(655, 795, 20, 20)
        }
        if self.hitbox_rect.colliderect(proximity_points["abstract_reasoning"]):
            self.gameStateManager = GameStateManager('AR')
            self.states[self.gameStateManager.get_state()].run()
                    
    def animate(self, dt):
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])] 

    def update(self, dt):
        self.input()
        self.move(dt)
        self.teleport()
        #self.animate(dt)