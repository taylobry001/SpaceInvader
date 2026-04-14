import pygame, random

#Initialize pygame
pygame.init()

#Set display surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spaceship")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()


#Define Classes
class Game():
    """A class to help control and update gameplay"""

    def __init__(self, player, alien_group, player_bullet_group, alien_bullet_group):
        self.player = player
        self.alien_group = alien_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group
        pass

    def update(self):
        pygame.display.flip()
        pass

    def draw(self):
        pass

    def shift_aliens(self):
        pass

    def check_collisions(self):
        pass

    def check_round_completion(self):
        pass

    def start_new_round(self):
        pass

    def check_game_status(self, main_text, sub_text):
        pass

    def pause_game(self, main_text, sub_text):
        pass

    def reset_game(self):
        pass


class Player(pygame.sprite.Sprite):
    """A class to model a spaceship the user can control"""

    def __init__(self, bullet_group):
        super().__init__()

        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10

        self.speed = 8
        self.bullet_group = bullet_group

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed

    def fire(self):
        bullet = PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)
        self.bullet_group.add(bullet)

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10


class Alien(pygame.sprite.Sprite):

    def __init__(self, x, y, velocity, bullet_group):
        super().__init__()
        pass

    def update(self):
        pass

    def fire(self):
        pass

    def reset(self):
        pass


class PlayerBullet(pygame.sprite.Sprite):

    def __init__(self, x, y, bullet_group):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
        self.bullet_group = bullet_group

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class AlienBullet(pygame.sprite.Sprite):

    def __init__(self, x, y, bullet_group):
        super().__init__()
        pass

    def update(self):
        pass


#Create bullet groups
my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group()

#Create a player group and Player object
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)

#Create an alien group
my_alien_group = pygame.sprite.Group()

#Create a Game object
my_game = Game(my_player, my_alien_group, my_player_bullet_group, my_alien_bullet_group)
my_game.start_new_round()


#The main game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.fire()

    #Fill the display
    display_surface.fill((0, 0, 0))

    #Update and display all sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_alien_group.update()
    my_alien_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(display_surface)

    #Update and draw Game object
    my_game.update()
    my_game.draw()

    #Update the display and tick clock
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()
