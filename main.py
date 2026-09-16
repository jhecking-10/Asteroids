import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def game_loop():
    pygame.init()
    clock = pygame.time.Clock()
    dt: float = 0.0 # delta time stores decimal number of seconds
    font = pygame.font.Font(None, 34)

    updatable, drawable, asteroids, shots = group()
    game_screen = create_screen()
    create_asteroid_field()
    player = create_player()
    
    while True:
        log_state()
        
        for event in pygame.event.get(): # Allows user to exit the game by closing the window
            if event.type == pygame.QUIT:
                return
                
        fill_screen(game_screen)
        updatable.update(dt)
        player.shot_cooldown -= dt

        # Check if player collides with any asteroid
        for a in asteroids:
            if Player.collides_with(player, a):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for a in asteroids:
            for shot in shots:
                if Shot.collides_with(shot, a):
                    log_event("asteroid_shot")
                    shot.kill()
                    a.split()

        # Display number of shots fired and number of asteroids spawned in
        # Will later use to calculate accuracy percentage
        asteroid_count = len(asteroids)
        text_surface = font.render(f"Asteroids present: {asteroid_count} | Shots fired: {player.shots_fired}", True, "white")
        game_screen.blit(text_surface, (10, 10))
        
        for object in drawable:
            draw(object, game_screen)
        pygame.display.flip()  
        
        dt = clock.tick(60) / 1000

def fill_screen(screen):
    screen.fill("black")

def create_player():
    return Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

def create_screen():
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def create_asteroid_field():
    AsteroidField()

def group():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroid = pygame.sprite.Group()
    shot = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroid, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shot, updatable, drawable)
    return updatable, drawable, asteroid, shot
    
def draw(object, screen):
    object.draw(screen)

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    game_loop()

if __name__ == "__main__":
    main()
