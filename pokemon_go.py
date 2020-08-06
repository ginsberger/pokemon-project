import pygame
import sys
import os
import random
from models.pokemon import update_pokemon_of_trainer
'''
Objects
'''

class Player(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''
    def __init__(self, path_image):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.image = pygame.image.load(os.path.join('images/', f"{path_image}"))
        self.rect  = self.image.get_rect()

    def control(self,x,y):
        '''
        control player movement
        '''
        self.movex += x
        self.movey += y

    def boundary_check(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > worldx:
            self.rect.right = worldx
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= worldy:
            self.rect.bottom = worldy
        

    def add_img(self, img, start_loction = (0, 0)):
        world.blit(img, start_loction)
        pygame.display.flip()

    def move_player(self,loction):
        self.add_img(backdrop)
        self.add_img(self.image, loction)

    def update(self):
        '''
        Update sprite position
        '''
        self.add_img(backdrop)
        self.boundary_check()
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # moving left
        # if self.movex < 0:
        self.frame += 1
        if self.frame > 3*ani:
            self.frame = 0
        # mouse_point = pygame.mouse.get_pos()

        # self.move_player(mouse_point)


'''
Setup
'''
worldx = 1200
worldy = 600

fps = 10        # frame rate
ani = 4        # animation cycles
clock = pygame.time.Clock()
pygame.init()
main = True

world = pygame.display.set_mode([worldx,worldy])
backdrop = pygame.image.load(os.path.join('images','open_background.jpg')).convert()
backdropbox = world.get_rect()
player = Player("player/player.png")   # spawn player
player_group = pygame.sprite.GroupSingle()
player_group.add(player)
steps = 10     # how fast to move

pygame.mixer.music.load("music/03.mp3")
pygame.mixer.music.play(loops=-1)

world.blit(backdrop, backdropbox)
pygame.display.flip()
clock = pygame.time.Clock()
clock.tick(1)

backdrop = pygame.image.load(os.path.join('images','background.jpg')).convert()
world.blit(backdrop, backdropbox)
pygame.display.flip()


pokemon_group = pygame.sprite.Group()
for img in os.listdir(os.path.join('images','pokemon')):
    pokemon = Player(f"pokemon/{img}")
    pokemon.rect.x = random.randint(0,worldx-100)
    pokemon.rect.y = random.randint(0,worldy-100)
    pokemon_group.add(pokemon)



'''
Main loop
'''

while main == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            main = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps,0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps,0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0,-steps)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.control(0,steps)
        
        if event.type == pygame.KEYUP:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False

    # player.update()
    # for pokemon in pokemon_group:
    #         pokemon.control(random.randint(0,worldx-100),random.randint(0,worldy-100))
    # pokemon_group.draw(world)
    

    for pokemon in pokemon_group:
        if pygame.sprite.spritecollideany(pokemon, player_group):
            pokemon.kill()
            


    player.update()
    player_group.draw(world) #refresh player position
    pokemon_group.draw(world)
    pygame.display.flip()
    clock.tick(fps)
    
