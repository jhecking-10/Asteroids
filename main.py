import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player


def game_loop():
    pygame.init()
    clock = pygame.time.Clock()
    dt: float = 0.0 # delta time stores decimal number of seconds

    updatable, drawable = group()
    create_player()
    game_screen = create_screen()
    
    while True:
        log_state()
        
        for event in pygame.event.get(): # Allows user to exit the game by closing the window
            if event.type == pygame.QUIT:
                return
                
        fill_screen(game_screen)
        updatable.update(dt)
        
        for object in drawable:
            draw(object, game_screen)
        pygame.display.flip()
        
        dt = clock.tick(60) / 1000

def fill_screen(screen):
    screen.fill("black")

def create_player():
    Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

def create_screen():
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def group():
    updatables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    Player.containers = (updatables, drawables)
    return updatables, drawables
    
def draw(object, screen):
    object.draw(screen)

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    game_loop()

if __name__ == "__main__":
    main()
