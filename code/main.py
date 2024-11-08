from settings import *
from sprites import *
from menus import *
from player import *
from groups import *
from gamemanager import *

class Game:
    def __init__(self):
        # Setup
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("BrainScape")
        pygame.font.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.collide_points = pygame.sprite.Group()

        self.music = pygame.mixer.Sound(join('audio', 'BGM', 'Background Music.mp3'))
        self.music.play(loops = -1)

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Walls'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.display_surface, self.all_sprites, self.collision_sprites)
    
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update(dt)

            self.gameStateManager = GameStateManager('Main Menu')

            self.display_surface.fill('black')            
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
            
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()