import pygame
import sys
import random


pygame.init()


WIDTH, HEIGHT = 600, 400
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


player_size = 50
player_speed = 5


bullet_speed = 7


enemy_size = 30
enemy_speed = 2
enemy_spawn_rate = 30  


score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


clock = pygame.time.Clock()


player = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT - 2 * player_size, player_size, player_size)


bullets = []


enemies = []


font = pygame.font.Font(None, 36)


game_over = False


def reset_game():
    global player, bullets, enemies, score, game_over
    player = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT - 2 * player_size, player_size, player_size)
    bullets = []
    enemies = []
    score = 0
    game_over = False


def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("You Lose!", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))

    
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 40))
    restart_text = font.render("Restart", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - 40, HEIGHT // 2 + 40))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        
        if keys[pygame.K_SPACE]:
            bullets.append(pygame.Rect(player.centerx - 2, player.top, 4, 10))

        
        bullets = [bullet for bullet in bullets if bullet.y > 0]
        for bullet in bullets:
            bullet.y -= bullet_speed

        
        if random.randint(1, enemy_spawn_rate) == 1:
            enemy_x = random.randint(0, WIDTH - enemy_size)
            enemy_y = random.randint(-enemy_size, -10)
            enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size))

        
        for enemy in enemies:
            enemy.y += enemy_speed

       
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1

        
        for enemy in enemies:
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                score -= 2

       
        for enemy in enemies:
            if enemy.colliderect(player):
                game_over = True

    
    screen.fill(BLACK)

    if game_over:
        game_over_screen()
    else:
        pygame.draw.rect(screen, WHITE, player)

        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        for enemy in enemies:
            pygame.draw.rect(screen, WHITE, enemy)

        
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

    
    pygame.display.flip()

    
    clock.tick(FPS)

    
    if game_over:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 40)
        if restart_button_rect.collidepoint(mouse_x, mouse_y):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    reset_game()
                    pygame.event.clear()  
                    break
        pygame.event.clear()  
