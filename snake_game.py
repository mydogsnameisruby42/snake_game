import pygame
import random
import sys
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
#game variables
screen_width = 800
screen_height= 600
screen = pygame.display.set_mode((screen_width, screen_height))
game_running = True
game_state = "START"
clock = pygame.time.Clock()
grid_size = 20
food = pygame.Rect(200,200,grid_size, grid_size)
class Player:
    def __init__(self,x,y):
        self.color = GREEN
        self.speed = grid_size
        self.score = 0
        self.direction = "RIGHT"
        self.last_move_time = 0
        self.move_delay = 100
        self.body = [
            pygame.Rect(x,y,grid_size,grid_size), 
            pygame.Rect(x - grid_size, y, grid_size, grid_size), 
            pygame.Rect(x - grid_size*2, y, grid_size, grid_size)
        ]
        self.next_direction = "RIGHT"
        self.direction_changed = False
    def move(self):
        #movement code
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].topleft = self.body[i-1].topleft
        self.direction = self.next_direction
        if self.direction == "RIGHT":
            self.body[0].x += self.speed
        if self.direction == "LEFT":
            self.body[0].x -= self.speed
        if self.direction == "UP":
            self.body[0].y -= self.speed
        if self.direction == "DOWN":
            self.body[0].y += self.speed
    def hit_wall(self, screen_width,screen_height):
        #boundry code
        if self.body[0].right > screen_width:
            return True
        if self.body[0].left < 0:
            return True
        if self.body[0].bottom > screen_height:
            return True
        if self.body[0].top < 0:
            return True
        return False
    def reset(self, x, y):
        self.score = 0
        self.direction = "RIGHT"
        self.last_move_time = 0
        self.move_delay = 100
        self.body = [
            pygame.Rect(x,y,grid_size,grid_size), 
            pygame.Rect(x - grid_size, y, grid_size, grid_size), 
            pygame.Rect(x - grid_size*2, y, grid_size, grid_size)
        ]
        self.next_direction = "RIGHT"
        self.direction_changed = False
    def find_safe_food_position(self):
        while True:
            random_position = (random.randint(0, 39) * grid_size, random.randint(0,29) * grid_size)
            test_food = pygame.Rect(random_position[0], random_position[1],grid_size, grid_size)
            food_in_snake = False
            for segment in self.body:    
                if segment.colliderect(test_food):
                    food_in_snake = True
            if not food_in_snake:
                break
        return random_position                 
player = Player(400,300)
font = pygame.font.Font(None, 70)
score_font = pygame.font.Font(None, 36)
while game_running:
    #player movement code
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            game_running = False
        
        if game_state == "PLAYING":       
            #movement code
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and player.next_direction != "LEFT" and player.direction_changed == False:
                    player.next_direction = "RIGHT"
                    player.direction_changed = True
                if event.key == pygame.K_LEFT and player.next_direction != "RIGHT" and player.direction_changed == False:
                    player.next_direction = "LEFT"
                    player.direction_changed = True
                if event.key == pygame.K_UP and player.next_direction != "DOWN" and player.direction_changed == False:
                    player.next_direction = "UP"
                    player.direction_changed = True
                if event.key == pygame.K_DOWN and player.next_direction != "UP" and player.direction_changed == False:
                    player.next_direction = "DOWN"
                    player.direction_changed = True
        #start code
        if game_state == "START":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.last_move_time = current_time
                    game_state = "PLAYING"
        #reset code
        if game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player.reset(400,300)
                    player.last_move_time = current_time
                    safe_position = player.find_safe_food_position()
                    food.topleft = safe_position
                    game_state = "PLAYING"
    if game_state == "PLAYING":
        #more movement code
        if current_time - player.last_move_time >= player.move_delay:
            player.move()
            player.last_move_time += player.move_delay
            player.direction_changed = False
        #wall death code
        if player.hit_wall(screen_width, screen_height):
            game_state = "GAME_OVER"
        #segment death code
        for segment in player.body[1:]:
            if player.body[0].colliderect(segment):
                game_state = "GAME_OVER"
        #growing and food moveing code
        if player.body[0].colliderect(food):
            player.score += 1
            safe_position = player.find_safe_food_position()
            food.topleft = safe_position
            #if player.move_delay > 40:
                #player.move_delay -= 1
            player.body.append(player.body[-1].copy())
    #drawing code
    screen.fill(BLACK)
    if game_state == "START":
        start_text = font.render("Snake", True, GREEN)
        screen.blit(start_text, (320, 200))
        instruction_text = score_font.render("press space to start", True, WHITE)
        screen.blit(instruction_text, (280, 300))
    elif game_state == "PLAYING":
        for segment in player.body:
            pygame.draw.rect(screen, player.color, segment)
        pygame.draw.rect(screen, RED, food)
        score_text = score_font.render("Score: " + str(player.score), True, WHITE)
        screen.blit(score_text, (10,10))
    else:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (245,200))
        restart_text = score_font.render("press r to restart", True, WHITE)
        screen.blit(restart_text, (310, 300))
    pygame.display.flip()
    #controls max fps
    clock.tick(60)
pygame.quit()
sys.exit()