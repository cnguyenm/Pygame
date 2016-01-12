__author__ = 'uSER'
import sys
import pygame
import random

AUTHOR = 'Chau Minh Nguyen'
BLOCK_SIZE = 100
WIDTH = 800
HEIGHT = 600
INITIAL_SNAKE_LENGTH = 3
FPS = 2
FINAL_SCORE = 100
DRAW_GRID = True
COLOR1 = (255,0,0)
COLOR2 = (0,0,255)
SCORE_COLOR = (0,255,0)
YELLOW = (180,180,0)


def Game_Win(screen,player):
    largefont = pygame.font.SysFont(None,70)
    win_text  = largefont.render(player + " WIN!!", True,YELLOW)
    win_text_rect = win_text.get_rect()
    win_text_rect.center = int(WIDTH / 2), int(HEIGHT /2)

    medfont = pygame.font.SysFont(None,30)
    message      = medfont.render("Press R to restart,Q to quit", True,YELLOW)
    message_rect = message.get_rect()
    message_rect.center = int(WIDTH / 2), int(HEIGHT /2 + HEIGHT*1/10)

    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        screen.blit(win_text,win_text_rect)
        screen.blit(message,message_rect)
        pygame.display.update()
def update_score(screen,score1,score2):
    medfont = pygame.font.SysFont(None,30)
    player1_score = medfont.render("Player1: "+ str(score1),True,SCORE_COLOR)
    score1_rect = player1_score.get_rect()
    score1_rect.center = int(WIDTH * 8/10),int( HEIGHT * 1/12)
    screen.blit(player1_score,score1_rect)

    player2_score = medfont.render("Player2: "+ str(score2),True,SCORE_COLOR)
    score2_rect = player2_score.get_rect()
    score2_rect.center = int(WIDTH * 2/10),int( HEIGHT * 1/12)
    screen.blit(player2_score,score2_rect)

def get_initial_snake1( snake_length, width, height, block_size ):
    columns = width  // block_size
    rows    = height // block_size
    half_size= block_size // 2
    head_x  = columns // 2 + columns % 2
    head_y  = int (rows * 1/4)
    head_pos= (block_size * (head_x - 1) + half_size ,block_size * (head_y - 1) + half_size)
    snake_list = []

    for i in range(snake_length):
        snake_list.insert(0,(head_pos[0] - i*block_size,head_pos[1]))

    return snake_list

def get_initial_snake2( snake_length, width, height, block_size ):
    columns = width  // block_size
    rows    = height // block_size
    half_size= block_size // 2
    head_x  = columns // 2 + columns % 2
    head_y  = int (rows * 3/4)
    head_pos= (block_size * (head_x - 1) + half_size ,block_size * (head_y - 1) + half_size)
    snake_list = []

    for i in range(snake_length):
        snake_list.insert(0,(head_pos[0] - i*block_size,head_pos[1]))

    return snake_list


def pick_random_apple_position( snake_list_1,snake_list_2, width, height, block_size ):
    columns  = width  // block_size - 1
    rows     = height // block_size - 1
    half_size= block_size // 2
    apple_row    = random.randrange(0,rows)
    apple_column = random.randrange(0,columns)
    apple = (apple_column*block_size + half_size,apple_row*block_size + half_size)
    if apple in snake_list_1 or apple in snake_list_2:
        return  pick_random_apple_position( snake_list_1,snake_list_2, width, height, block_size )
    else:
        return apple

def update_direction( current_direction, new_direction ):
    valid_directions = ['up','down','left','right']
    if current_direction =='up':
        valid_directions.remove('down')
    elif current_direction == 'down':
        valid_directions.remove('up')
    elif current_direction == 'left':
        valid_directions.remove('right')
    elif current_direction == 'right':
        valid_directions.remove('left')

    if new_direction in valid_directions:
        return (new_direction)
    else:
        return (current_direction)

def update_snake( snake_list, direction, apple_position, block_size ):
    head_x,head_y = snake_list[-1]
    accel_x,accel_y=0,0
    eat = False
    if direction == 'up':
        accel_x = 0
        accel_y = -block_size
    elif direction == 'down':
        accel_x = 0
        accel_y = block_size
    elif direction == 'left':
        accel_x = -block_size
        accel_y = 0
    elif direction == 'right':
        accel_x = block_size
        accel_y = 0
    head_x += accel_x
    head_y += accel_y
    head = (head_x,head_y)
    snake_list.append(head)
    if apple_position in snake_list:
        eat = True
    else:
        del snake_list[0]


    return snake_list,eat
def is_snake_inside_window( snake_list, width, height ):

    head_x = snake_list[-1][0]
    head_y = snake_list[-1][1]
    if ( 0 < head_x < width and 0 < head_y < height):
        return True
    else:
        return False

def is_snake_hit_itself( snake_list ):
    head = snake_list[-1]
    for body in snake_list[:-1]:
        if head == body:
            return True
    return False

def is_snake_hit_another(snake_list_1,snake_list_2):
    head = snake_list_1[-1]
    for body in snake_list_2:
        if head == body:
            return True
    return False

def draw_grid( width, height, block_size,window):
    rows    = height // block_size
    columns = width  // block_size
    for row in range(rows+1):
        pygame.draw.line( window, (255, 255, 255), (0,row*block_size), (width , row*block_size) )
    for column in range(columns+1):
        pygame.draw.line( window, (255, 255, 255), (column*block_size,0), (column*block_size , height) )

def draw_snake( snake_list, color, block_size,window):
    for body in snake_list:
        left = body[0] - block_size//2
        top  = body[1] - block_size//2
        pygame.draw.rect(window,color,(left,top,block_size,block_size))
def draw_apple( apple_position, block_size, window ):
    color= random.randint(0,255), random.randint(0,255), random.randint(0,255)
    radius = int(block_size/2)
    pygame.draw.circle(window,color,apple_position,radius)



def main():
    pygame.init()
    pygame.mixer.init()
    window = pygame.display.set_mode( (WIDTH+1, HEIGHT+1) )
    pygame.display.set_caption( 'Snake game' )
    current_direction_1 = 'right'
    new_direction_1 = 'right'
    score1 = 0
    current_direction_2 = 'right'
    new_direction_2 = 'right'
    score2 = 0
    clock = pygame.time.Clock()

    eat_sound = pygame.mixer.Sound("explosion.wav")

    back_ground_music  = pygame.mixer.music
    back_ground_music.load('rubik.mp3')
    back_ground_music.set_volume(0.2)
    back_ground_music.play(-1,5.0)

    game_over_sound = pygame.mixer.Sound("gameoversound.wav" )
    game_over_sound.set_volume(0.3)
    # the list of squares in the snake, (x,y) are the center
    # positions of the square.
    snake_list1 = get_initial_snake1( INITIAL_SNAKE_LENGTH, WIDTH, HEIGHT, \
                                    BLOCK_SIZE )
    snake_list2 = get_initial_snake2( INITIAL_SNAKE_LENGTH, WIDTH, HEIGHT, \
                                    BLOCK_SIZE )
    # center position of apple
    apple_position = pick_random_apple_position( snake_list1,snake_list2,WIDTH, HEIGHT, \
                                             BLOCK_SIZE )
    # This is the main game loop.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_direction_1 = 'left'
                if event.key == pygame.K_RIGHT:
                    new_direction_1 = 'right'
                if event.key == pygame.K_DOWN:
                    new_direction_1 = 'down'
                if event.key == pygame.K_UP:
                    new_direction_1 = 'up'
                if event.key == pygame.K_a:
                    new_direction_2 = 'left'
                if event.key == pygame.K_d:
                    new_direction_2 = 'right'
                if event.key == pygame.K_w:
                    new_direction_2 = 'up'
                if event.key == pygame.K_s:
                    new_direction_2 = 'down'

        current_direction_1 = update_direction( current_direction_1, new_direction_1 )
        current_direction_2 = update_direction( current_direction_2, new_direction_2 )

        snake_list1, is_apple_eaten = update_snake( snake_list1, current_direction_1, \
                                                   apple_position, BLOCK_SIZE )
        if is_apple_eaten:
            eat_sound.play()
            apple_position = pick_random_apple_position( snake_list1,snake_list2, \
                                            WIDTH, HEIGHT, BLOCK_SIZE )
            score1 += 10
            if score1 >= FINAL_SCORE:
                Game_Win(window,"PLAYER 1")
        snake_list2, is_apple_eaten = update_snake( snake_list2, current_direction_2, \
                                                  apple_position, BLOCK_SIZE )
        if is_apple_eaten:
            eat_sound.play()
            apple_position = pick_random_apple_position( snake_list1,snake_list2, \
                                            WIDTH, HEIGHT, BLOCK_SIZE )
            score2 += 10
            if score2 >= FINAL_SCORE:
                Game_Win(window,"PLAYER 2")

        if not is_snake_inside_window( snake_list1, WIDTH, HEIGHT ) or  \
                                        is_snake_hit_itself( snake_list1 ) or \
                                        is_snake_hit_another(snake_list1,snake_list2):
            back_ground_music.stop()
            game_over_sound.play(loops=0)

            Game_Win(window,"PLAYER 2")
        if not is_snake_inside_window( snake_list2, WIDTH, HEIGHT )or  \
                                        is_snake_hit_itself( snake_list2 ) or \
                                        is_snake_hit_another(snake_list2,snake_list1) :
            back_ground_music.stop()
            game_over_sound.play(loops=0)
            Game_Win(window,"PLAYER 1")

        window.fill( (0,0,0) ) # black background
        if DRAW_GRID:
            draw_grid( WIDTH, HEIGHT, BLOCK_SIZE, window )
        draw_snake( snake_list1, COLOR1, BLOCK_SIZE, window )
        draw_snake( snake_list2, COLOR2, BLOCK_SIZE, window )

        draw_apple( apple_position, BLOCK_SIZE, window )
        update_score(window,score1,score2)
        # update the window with the last drawings
        pygame.display.update()

        # set fps (speed)
        clock.tick( FPS )
    pygame.quit()

if __name__ == '__main__':
    main()








