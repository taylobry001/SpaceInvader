import pygame, random

#Initialize pygame
pygame.init()
pygame.mixer.init()

#Set display surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spaceship")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()


#LOAD ASSETS
player_img = pygame.image.load("player_ship.png")
alien_img = pygame.image.load("alien.png")
player_img = pygame.transform.scale(player_img, (60, 60))
alien_img = pygame.transform.scale(alien_img, (50, 50))

#LOAD SOUNDS
player_fire_sound = pygame.mixer.Sound("player_fire.wav")
alien_fire_sound = pygame.mixer.Sound("alien_fire.wav")
player_hit_sound = pygame.mixer.Sound("player_hit.wav")
alien_hit_sound = pygame.mixer.Sound("alien_hit.wav")
new_round_sound = pygame.mixer.Sound("new_round.wav")
breach_sound = pygame.mixer.Sound("breach.wav")


#Define Classes
class Game():
    """A class to help control and update gameplay"""

    def __init__(self, player, alien_group, player_bullet_group, alien_bullet_group):
        self.player = player
        self.alien_group = alien_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group
        self.round = 1

    def update(self):
        self.check_round_completion()
        pygame.display.flip()

    def draw(self):
        pass

    def shift_aliens(self):
        pass

    def check_collisions(self):
        pass

    def check_round_completion(self):
        if len(self.alien_group) == 0:
            self.start_new_round()

    def start_new_round(self):
        self.round += 1
        new_round_sound.play()

        for _ in range(5 + self.round):
            alien = Alien(
                random.randint(50, WINDOW_WIDTH - 50),
                random.randint(-200, -50),
                random.randint(1, 3),
                my_alien_bullet_group
            )
            self.alien_group.add(alien)

    def check_game_status(self, main_text, sub_text):
        breach_sound.play()
        self.pause_game(main_text, sub_text)

    def pause_game(self, main_text, sub_text):

        font_big = pygame.font.Font("Facon.ttf", 72)
        font_small = pygame.font.Font("Facon.ttf", 36)

        main_surface = font_big.render(main_text, True, (255, 255, 255))
        sub_surface = font_small.render(sub_text, True, (255, 255, 255))

        display_surface.blit(
            main_surface,
            (WINDOW_WIDTH // 2 - main_surface.get_width() // 2,
             WINDOW_HEIGHT // 2 - 60)
        )

        display_surface.blit(
            sub_surface,
            (WINDOW_WIDTH // 2 - sub_surface.get_width() // 2,
             WINDOW_HEIGHT // 2 + 20)
        )

        pygame.display.update()

        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        paused = False

    def reset_game(self):
        pass


class Player(pygame.sprite.Sprite):

    def __init__(self, bullet_group):
        super().__init__()
        self.image = player_img
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
        player_fire_sound.play()

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10


class Alien(pygame.sprite.Sprite):

    def __init__(self, x, y, velocity, bullet_group):
        super().__init__()
        self.image = alien_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity
        self.bullet_group = bullet_group

    def update(self):
        self.rect.y += self.velocity

        if self.rect.top > WINDOW_HEIGHT:
            self.reset()

    def fire(self):
        alien_fire_sound.play()
        pass

    def reset(self):
        self.rect.x = random.randint(50, WINDOW_WIDTH - 50)
        self.rect.y = random.randint(-200, -50)


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

#Create player group
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)

#Create alien group
my_alien_group = pygame.sprite.Group()

#Create Game object
my_game = Game(my_player, my_alien_group, my_player_bullet_group, my_alien_bullet_group)

#START FIRST ROUND
for _ in range(5):
    my_alien_group.add(
        Alien(
            random.randint(50, WINDOW_WIDTH - 50),
            random.randint(-200, -50),
            2,
            my_alien_bullet_group
        )
    )


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.fire()

    display_surface.fill((0, 0, 0))

    my_player_group.update()
    my_player_group.draw(display_surface)

    my_alien_group.update()
    my_alien_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(display_surface)

    my_game.update()
    my_game.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
