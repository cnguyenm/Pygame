import sys
import pygame
import random

########################### Global Constants ##############################

# change this with your name
AUTHOR = 'Chau Minh Nguyen'

# block_size is the width and height of a square of the snake.
# also, diameter of the apple is equal to block_size
# BLOCK_SIZE should be divisible by 2 in this implementation
BLOCK_SIZE = 10

# width of the screen
# WIDTH should be divisible by BLOCK_SIZE in this implementation
WIDTH = 800

# height of the screen
# HEIGHT should be divisible by BLOCK_SIZE in this implementation
HEIGHT = 600

# initial length of the snake, i.e., number of squares snake has.
INITIAL_SNAKE_LENGTH = 6

# frames per second. this is effectively speed of snake in this program.
# read this if you are not familiar:
# https://en.wikipedia.org/wiki/Frame_rate
FPS = 20

# draws the grid to the screen to help see what is going on.
DRAW_GRID = False

###########################################################################

######################## Useful definitions ###############################

# snake_list: 
# -----------
# this is a list of tuples, every tuple correspond to
# a square of the snake. each tuple has the center position
# of the corresponding square, i.e.: (x,y).
# the width and the height of all squares is BLOCK_SIZE.
# the last element of this list is the head of the snake and
# second last is the square after the head, etc.
# type: list of tuples. each tuple contains two integers.

# apple_position:
# --------------
# this is the center position of the apple. the diameter of the apple
# is always BLOCK_SIZE. you cannot initialize the apple in the snake.
# type: tuple of two integers.

############################################################################

# This function returns the initial snake_list (see above) given the below
# parameters. The initial snake is expected to be in the center of the screen.
#
# More specifically:
#
# If there are odd number of squares in the columns:
#    Then the snake head must be exactly in the middle row.
# If there are even number of squares in the columns:
#    Then the snake head must be (num_rows / 2) th row.
# Similarly,
# If there are odd number of squares in the rows:
#    Then the snake head must be exactly in the middle column.
# If there are even number of squares in the rows:
#    Then the snake head must be (num_cols / 2) th column.
#
# By definition:
# number of columns = width / block_size
# number of rows = height / block_size 
# 
# PARAMETERS:
# snake_length: length of the snake, type: integer
# width       : width of the window, type: integer
# height      : height of the window, type: integer
# block_size  : width and height of a square of the snake, type: integer
# RETURNS:
# snake_list, type: list of tuples. each tuple contains two integers.
#
# Some test cases: (We will use more test cases when grading.)
# case_A1:
# get_initial_snake( 3, 900, 900, 100 )
# [(250, 450), (350, 450), (450, 450)]
# case_A2:
# get_initial_snake( 3, 900, 600, 100 )
# [(250, 250), (350, 250), (450, 250)]
# case_A3:
# get_initial_snake( 3, 1000, 1000, 100 )
# [(250, 450), (350, 450), (450, 450)]
# case_A4:
# get_initial_snake( 7, 900, 900, 50 )
# [(125, 425), (175, 425), (225, 425), (275, 425), (325, 425), (375, 425), (425, 425)]
#
# Please see visualizations for each test case in the Project page.
def get_initial_snake( snake_length, width, height, block_size ):
    columns = width  // block_size
    rows    = height // block_size
    half_size= block_size // 2
    head_x  = columns // 2 + columns % 2
    head_y  = rows    // 2 + rows    % 2
    head_pos= (block_size * (head_x - 1) + half_size ,block_size * (head_y - 1) + half_size)
    snake_list = []

    for i in range(snake_length):
        snake_list.insert(0,(head_pos[0] - i*block_size,head_pos[1]))

    return snake_list

		
# This function returns the center of a random apple position in the screen.
# (1) The apple_position cannot be under the snake. (2) The apple_position cannot be
# outside of the screen. (3) And the apple position must be aligned in the rows
# and columns.
#
# PARAMETERS:
# snake_list: list of tuples, every tuple correspond to a square of the snake
#							type: list of tuples. each tuple contains two integers.
# width: width of the window, type: integer
# height: height of the window, type: integer
# block_size: width and height of a square of the snake, type: integer
# RETURNS:
# apple_position, type: tuple contains two integers
#
# Since this is a randomized function, you may not produce the exact same
# results, but your apple_point should be always: (1) in the screen,
# (2) not under the snake, (3) aligned with the rows and columns.
#
# Some test cases: (We will use more test cases when grading.)
# case_B1:
# pick_random_apple_position( [(250, 450), (350, 450), (450, 450)], 900, 900, 100 )
# (650, 250)
# case_B2:
# pick_random_apple_position( [(450, 150), (350, 150), (350, 250), (350, 350), (350, 450), (350, 550), (450, 550), (550, 550), (650, 550), (650, 650), (650, 750)], 900, 900, 100 )
# (350, 750)
# case_B3:
# pick_random_apple_position( [(225, 375), (225, 325), (225, 275), (275, 275), (325, 275), (375, 275), (425, 275), (475, 275), (525, 275), (525, 325)], 900, 900, 50 )
# (325, 825)
# 
# Please see visualizations for each test case in the Project page.
def pick_random_apple_position( snake_list, width, height, block_size ):
    columns  = width  // block_size - 1
    rows     = height // block_size - 1
    half_size= block_size // 2
    apple_row    = random.randrange(0,rows)
    apple_column = random.randrange(0,columns)
    apple = (apple_column*block_size + half_size,apple_row*block_size + half_size)
    if apple in snake_list:
        return  pick_random_apple_position( snake_list, width, height, block_size )
    else:
        return apple

# In this function, we update the direction of the snake.
# current_direction is the direction snake currently going,
# new_direction is the user's input direction.
#
# We will return the the new direction given current_direction
# and new_direction with the snake logic. (If snake goes right
# and user inputs to go left, snake will continue going right.)
# 
# PARAMETERS:
# current_direction: current direction of the snake, type: string
#     one of the following: 'right', 'left', 'up', 'down'
# new_direction: new direction of snake, type: string
#     one of the following: 'right', 'left', 'up', 'down'
# RETURNS:
# new_direction, type: string
#
# Some test cases: (We will use more test cases when grading.)
# case_C1:
# update_direction( 'up', 'right' )
# right
# case_C2:
# update_direction( 'down', 'left' )
# left
# case_C3:
# update_direction( 'left', 'left' )
# left
# case_C4:
# update_direction( 'left', 'right' )
# left
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
# This function updates snake's position using the direction.
# In other terms, snake moves a single step. After this move, there are
# four cases. (1) snake is still safe, (2) snake is still safe and ate
# the apple, (3) snake is out of the window and hence game over,
# (4) snake hit itself and hence game over.
#
# In this function, we will only move the snake and check if it eats the
# apple. We will just report this information and the necessary actions 
# will be done in the main() function.
# 
# If Snake eats the Apple, it should extend its head to the apple_position
# and get one square bigger. Please see case_D3 below.
#
# PARAMETERS:
# snake_list: list of tuples, every tuple correspond to a square of the snake
#							type: list of tuples. each tuple contains two integers
# direction: current direction of snake, type: string
#							one of the following: 'right', 'left', 'up', 'down'
# apple_position: the center position of the apple, type: tuple contains two integers
# block_size: width and length of a square of the snake, type: integer
# RETURNS:
# A tuple containing (snake_list, is_apple_eaten)
# snake_list: updated snake_list after the move, 
#					type: list of tuples. each tuple contains two integers
# is_apple_eaten: did the snake it apple after this move, type: boolean
#
# Some test cases: (We will use more test cases when grading.)
# case_D1:
# update_snake( [(150, 450), (250, 450), (350, 450), (450, 450)], 'right', (550, 250), 100 )
# ([(250, 450), (350, 450), (450, 450), (550, 450)], False)
# case_D2:
# update_snake( [(550, 650), (550, 750), (650, 750), (750, 750), (750, 650), (750, 550), (750, 450)], 'up', (850, 750), 100 )
# ([(550, 750), (650, 750), (750, 750), (750, 650), (750, 550), (750, 450), (750, 350)], False)
# case_D3:
# update_snake( [(450, 850), (350, 850), (250, 850), (150, 850), (150, 750), (150, 650), (150, 550)], 'up', (150, 450), 100 )
# ([(450, 850), (350, 850), (250, 850), (150, 850), (150, 750), (150, 650), (150, 550), (150, 450)], True)
# 
# Please see visualizations for each test case in the Project page.
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


# This function checks if the snake is inside the window.
# (Just checking whether the head of the snake inside the window
# is enough.)
#
# We will use this function to terminate the game, since the game is over
# when the snake hits the wall (goes outside the window).
#
# PARAMETERS:
# snake_list: list of tuples, every tuple correspond to a square of the snake
#							type: list of tuples. each tuple contains two integers
# width: width of the window, type: integer
# height: height of the window, type: integer
# RETURNS:
# Returns whether snake inside the window, type: boolean
#
# Some test cases: (We will use more test cases when grading.)
# case_E1:
# is_snake_inside_window( [(550, 450), (650, 450), (750, 450), (850, 450)], 900, 900 )
# True
# case_E2:
# is_snake_inside_window( [(650, 450), (750, 450), (850, 450), (950, 450)], 900, 900 )
# False
# case_E3:
# is_snake_inside_window( [(150, 250), (150, 350), (150, 450), (150, 550), (250, 550), (350, 550), (350, 650), (350, 750), (350, 850)], 900, 900 )
# True
# case_E4:
# is_snake_inside_window( [(150, 350), (150, 450), (150, 550), (250, 550), (350, 550), (350, 650), (350, 750), (350, 850), (350, 950)], 900, 900 )
# False
def is_snake_inside_window( snake_list, width, height ):

    head_x = snake_list[-1][0]
    head_y = snake_list[-1][1]
    if ( 0 < head_x < width and 0 < head_y < height):
        return True
    else:
        return False
# This function checks if the snake has hit itself.
#
# We will use this function to terminate the game, since the game is over
# when the snake hits itself.
# 
# PARAMETERS:
# snake_list: list of tuples, every tuple correspond to a square of the snake
#							type: list of tuples. each tuple contains two integers
# RETURNS:
# Returns whether snake has hit itself, type: boolean
# 
# Some test cases: (We will use more test cases when grading.)
# case_F1:
# is_snake_hit_itself( [(350, 250), (250, 250), (250, 350), (250, 450), (250, 550), (350, 550)] )
# False
# case_F2:
# is_snake_hit_itself( [(650, 850), (550, 850), (450, 850), (350, 850), (250, 850), (150, 850), (150, 750), (150, 650), (150, 550), (150, 450), (150, 350), (150, 250)] )
# False
# case_F3:
# is_snake_hit_itself( [(150, 550), (150, 450), (150, 350), (150, 250), (250, 250), (350, 250), (450, 250), (450, 350), (450, 450), (350, 450), (250, 450), (150, 450)] )
# True
def is_snake_hit_itself( snake_list ):
    head = snake_list[-1]
    for body in snake_list[:-1]:
        if head == body:
            return True
    return False
# This function draws the grid to the window using couple of
# pygame.draw.line() functions.
# 
# Remember the syntax here:
# https://www.pygame.org/docs/ref/draw.html#pygame.draw.line
#
# Example: pygame.draw.line( window, (255, 255, 255), (0, 0), (100, 100) )
# will draw a line to the window from (0,0) to (100,100) with white color.
#
# Please do not change the width option in the above function call.
# width = 1 seems to be okay in practice.
#
# Lastly, this function should draw all lines with the color white.
# If you need help with RGB color-model, please
# refer to: https://en.wikipedia.org/wiki/RGB_color_model
#
# PARAMETERS:
# width: width of the window, type: integer
# height: height of the window, type: integer
# block_size: width and height of a square of the snake, type: integer
# window: the window that the grid will be drawn, type: pygame.window
# RETURNS:
# None
def draw_grid( width, height, block_size,window):
    rows    = height // block_size
    columns = width  // block_size
    for row in range(rows+1):
        pygame.draw.line( window, (255, 255, 255), (0,row*block_size), (width , row*block_size) )
    for column in range(columns+1):
        pygame.draw.line( window, (255, 255, 255), (column*block_size,0), (column*block_size , height) )

# This function draws the snake on the window using couple of
# pygame.draw.rect() functions.
# 
# Remember the syntax here:
# https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect 
#
# Example: pygame.draw.rect( window, (255,255,255), (100,100,50,50) ) 
# will draw a rectangle whose upper left corner is (100,100) and
# whose width = 50 and height = 50.
#
# Also remember that we keep track of the centers of the squares,
# however pygame.draw.rect expects the left upper corner of the
# rectangle to draw.
#
# Lastly, this function should draw all squares with a 
# random color. This will make the snake look like moving.
# If you need help with RGB color-model, please
# refer to: https://en.wikipedia.org/wiki/RGB_color_model
#
# PARAMETERS:
# snake_list: list of tuples, every tuple correspond to a square of the snake
#							type: list of tuples. each tuple contains two integers
# block_size: width and height of a square of the snake, type: integer
# window: the window that the snake will be drawn, type: pygame.window
# RETURNS:
# None
def draw_snake( snake_list, block_size,window):
    for body in snake_list:
        left = body[0] - block_size//2
        top  = body[1] - block_size//2
        color= random.randint(0,255), random.randint(0,255), random.randint(0,255)
        pygame.draw.rect(window,color,(left,top,block_size,block_size))


# This function draws the apple on the screen using 
# pygame.draw.circle() function.
# 
# Remember the syntax here:
# https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle
#
# Example: pygame.draw.circle( window, (255,255,255), (100,100), 50 )
# will draw a circle whose center position is (100,100) and radius = 50.
#
# Lastly, this function should draw the circle with a random color.
# If you need help with RGB color-model, please
# refer to: https://en.wikipedia.org/wiki/RGB_color_model
#
# PARAMETERS:
# apple_position, type: tuple contains two integers
# block_size: width and height of a square of the snake, type: integer
# window: the window that the apple will be drawn, type: pygame.window
# RETURNS:
# None
def draw_apple( apple_position, block_size, window ):
    color= random.randint(0,255), random.randint(0,255), random.randint(0,255)
    radius = int(block_size/2)
    pygame.draw.circle(window,color,apple_position,radius)


def main():
	#initializations
	pygame.init()
	window = pygame.display.set_mode( (WIDTH+1, HEIGHT+1) )
	pygame.display.set_caption( 'Snake game' )

	# current direction of the snake: right, left, up, down
	current_direction = 'right'
	# new direction of the snake: right, left, up, down
	new_direction = 'right'

	# clock is helping us to set FPS
	clock = pygame.time.Clock()

	# the list of squares in the snake, (x,y) are the center
	# positions of the square.
	snake_list = get_initial_snake( INITIAL_SNAKE_LENGTH, WIDTH, HEIGHT, \
									BLOCK_SIZE )

	# center position of apple
	apple_position = pick_random_apple_position( snake_list, WIDTH, HEIGHT, \
												 BLOCK_SIZE )

	# This is the main game loop.
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					new_direction = 'left'
				if event.key == pygame.K_RIGHT:
					new_direction = 'right'
				if event.key == pygame.K_DOWN:
					new_direction = 'down'
				if event.key == pygame.K_UP:
					new_direction = 'up'

		current_direction = update_direction( current_direction, new_direction )

		snake_list, is_apple_eaten = update_snake( snake_list, current_direction, \
									    		   apple_position, BLOCK_SIZE )

		if is_apple_eaten:
			apple_position = pick_random_apple_position( snake_list, \
											WIDTH, HEIGHT, BLOCK_SIZE )

		if not is_snake_inside_window( snake_list, WIDTH, HEIGHT ) or  \
										is_snake_hit_itself( snake_list ):
			break
			
		window.fill( (0,0,0) ) # black background
		if DRAW_GRID:
			draw_grid( WIDTH, HEIGHT, BLOCK_SIZE, window )
		draw_snake( snake_list, BLOCK_SIZE, window )
		draw_apple( apple_position, BLOCK_SIZE, window )

		# update the window with the last drawings
		pygame.display.update()

		# set fps (speed)
		clock.tick( FPS )

	pygame.quit()

if __name__ == '__main__':
	main()
