import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("BOOM")


étoile = pygame.image.load('étoile.png').convert_alpha()
bombe = pygame.image.load('bombe.png').convert_alpha()
arbres = pygame.image.load('arbres.png').convert_alpha()
nuages = pygame.image.load('nuages.png').convert_alpha()

sprite_droite1 = pygame.image.load('sprite_droite_1.png').convert_alpha()
sprite_droite2 = pygame.image.load('sprite_droite_2.png').convert_alpha()
sprite_droite3 = pygame.image.load('sprite_droite_3.png').convert_alpha()

sprite_gauche1 = pygame.image.load('sprite_gauche_1.png').convert_alpha()
sprite_gauche2 = pygame.image.load('sprite_gauche_2.png').convert_alpha()
sprite_gauche3 = pygame.image.load('sprite_gauche_3.png').convert_alpha()

largeur, longueur = 167, 167
sprite_droite1 = pygame.transform.scale(sprite_droite1, (largeur, longueur))
sprite_droite2 = pygame.transform.scale(sprite_droite2, (largeur, longueur))
sprite_droite3 = pygame.transform.scale(sprite_droite3, (largeur, longueur))

sprite_gauche1 = pygame.transform.scale(sprite_gauche1, (largeur, longueur))
sprite_gauche2 = pygame.transform.scale(sprite_gauche2, (largeur, longueur))
sprite_gauche3 = pygame.transform.scale(sprite_gauche3, (largeur, longueur))


walk_right_frames = [sprite_droite1, sprite_droite2, sprite_droite3, sprite_droite2]
walk_left_frames = [sprite_gauche1, sprite_gauche2, sprite_gauche3, sprite_gauche2]

current_frame_index = 0
animation_timer = 0
animation_speed = 5
current_character_image = sprite_droite1
character_direction = "right" 
frame_direction = 1

étoile = pygame.transform.scale(étoile, (30, 30))
bombe = pygame.transform.scale(bombe, (30, 30))

étoiles = []
bombes = []

position_protag = [fenetre.get_width() // 2 - largeur // 2, 355]

paysage = (0,0)
arial24 = pygame.font.SysFont("arial",24)
score = 0
game_over = False

clock = pygame.time.Clock()

musique = 'Food Mart - Tomodachi Life OST.mp3' 
pygame.mixer.music.load(musique)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) 


def dessiner():
    global score, fenetre, game_over, current_character_image 
    
    fenetre.fill((100,150,255))
    
    fenetre.blit(nuages, paysage)
    fenetre.blit(arbres, (0, fenetre.get_height() - arbres.get_height()))


    fenetre.blit(current_character_image, position_protag) 

    for star in étoiles:
        fenetre.blit(étoile, star)

    for boom in bombes:
        fenetre.blit(bombe, boom)

    score_total = arial24.render("Score: " + str(score), True, (255,255,255))
    fenetre.blit(score_total, (10,10))

    if game_over:
        game_over_text = arial24.render("VOUS AVEZ PERDU HAHAHAHA  Score final: " + str(score), True, (255, 0, 0))
        restart_text = arial24.render("Press 'R' to Restart", True, (255, 255, 255))
        
        text_rect = game_over_text.get_rect(center=(fenetre.get_width() // 2, fenetre.get_height() // 2 - 20))
        fenetre.blit(game_over_text, text_rect)
        
        restart_rect = restart_text.get_rect(center=(fenetre.get_width() // 2, fenetre.get_height() // 2 + 20))
        fenetre.blit(restart_text, restart_rect)

    pygame.display.flip()

def gererClavierEtSouris():
    global continuer, position_protag, game_over, current_frame_index, animation_timer, current_character_image, character_direction, frame_direction
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_game()

    if not game_over:
        touchesPressees = pygame.key.get_pressed()
        
        moving = False
        
        if touchesPressees[pygame.K_RIGHT] and position_protag[0] < fenetre.get_width() - current_character_image.get_width():
            position_protag[0] = position_protag[0] + 8
            character_direction = "right"
            moving = True
        elif touchesPressees[pygame.K_LEFT] and position_protag[0] > 0:
            position_protag[0] = position_protag[0] - 8
            character_direction = "left"
            moving = True
        

        if moving:
            animation_timer = animation_timer + 1
            if animation_timer >= animation_speed:
                animation_timer = 0
                
                current_frame_index += frame_direction
                
 
                if frame_direction == 1 and current_frame_index >= len(walk_right_frames) - 1:
                    frame_direction = -1 
                elif frame_direction == -1 and current_frame_index <= 0: 
                    frame_direction = 1 

            if character_direction == "right":
                current_character_image = walk_right_frames[current_frame_index]
            elif character_direction == "left":
                current_character_image = walk_left_frames[current_frame_index]
        else:
 
            current_frame_index = 0
            animation_timer = 0
            frame_direction = 1 
            if character_direction == "right":
                current_character_image = walk_right_frames[0] 
            else:
                current_character_image = walk_left_frames[0]


def reset_game():
    global score, étoiles, bombes, position_protag, game_over, continuer, current_frame_index, animation_timer, current_character_image, character_direction, frame_direction
    score = 0
    étoiles = []
    bombes = []
    position_protag = [fenetre.get_width() // 2 - largeur // 2, 355]
    game_over = False
    continuer = True
    
    current_frame_index = 0
    animation_timer = 0
    frame_direction = 1 
    current_character_image = walk_right_frames[0] 
    character_direction = "right"

continuer = True
while continuer:
    clock.tick(60)

    gererClavierEtSouris()

    if not game_over:

        if random.randint(1, 40) == 1:
            étoiles.append([random.randint(0, fenetre.get_width() - étoile.get_width()), -étoile.get_height()])
        if random.randint(1, 60) == 1:
            bombes.append([random.randint(0, fenetre.get_width() - bombe.get_width()), -bombe.get_height()])

        for i in range(len(étoiles)):
            étoiles[i][1] = étoiles[i][1] + 5
        for i in range(len(bombes)):
            bombes[i][1] = bombes[i][1] + 7

        protag_rect = pygame.Rect(position_protag[0], position_protag[1], current_character_image.get_width(), current_character_image.get_height())

        nouvelles_étoiles = []
        for star in étoiles:
            étoile_rect = pygame.Rect(star[0], star[1], étoile.get_width(), étoile.get_height())
            if protag_rect.colliderect(étoile_rect):
                score += 1
            elif star[1] < fenetre.get_height():
                nouvelles_étoiles.append(star)
        étoiles = nouvelles_étoiles

        nouvelles_bombes = []
        for boom in bombes:
            bombe_rect = pygame.Rect(boom[0], boom[1], bombe.get_width(), bombe.get_height())
            if protag_rect.colliderect(bombe_rect):
                game_over = True
            elif boom[1] < fenetre.get_height():
                nouvelles_bombes.append(boom)
        bombes = nouvelles_bombes

    dessiner()

pygame.quit()
sys.exit()