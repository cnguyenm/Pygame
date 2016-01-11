
import pygame as pg
import math
white =(255,255,255)
black = (0,0,0)
red = (159,29,15)
green =(13,189,12)
blue = (19,4,159)
yellow = (255,255,0)
light_green = (0,255,255)
room_list = {
	0: {'number': 0,
	    'up':3,
	    'left':1,
	    'right':5},
	
	1: {'number':1,
		'right':0,
		 'up':2},
	
	2: {'number':2,
		'down':1,
		'right':3},
	
	3: {'number':3,
		'left':2,
		'right':4,
		'down':0},

	4:{'number':4,
		'left':3,
		'down':5},
	
	5:{'number':5,
		'left':0,
		'up':4}

	}	
pg.init()
pg.display.set_caption("Mazers")
game_display = pg.display.set_mode((800,600))
game_display.fill(black)


class Player(pg.sprite.Sprite):
	velocity_x = 0
	velocity_y = 0

	def __init__(self,x,y):
		super().__init__()
		self.image = pg.Surface([20,20])
		self.image.fill(white)
		
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		self.change_x = 0
		self.change_y = 0

		
		
	def change_speed(self,accel_x,accel_y):


#basically, when KEYUP: self.change_x = self.change_x - 5 = 5-5 = 0

		self.change_x += int(accel_x)
		self.change_y += int(accel_y)
	def update(self,walls):
		
		self.rect.x = self.rect.x + self.change_x
		block_hit_list = pg.sprite.spritecollide(self,walls,False)
		for block in block_hit_list:
			if self.change_x > 0:
				self.rect.right = block.rect.left
			else:
				self.rect.left = block.rect.right

		#remember, the position of lines are crazily important,
		#if we convert 68 and 69, when player hit the block, it will be too late because
		#player sprite is already in the block, so player will be bounced out
		self.rect.y = self.rect.y + self.change_y
		block_hit_list = pg.sprite.spritecollide(self,walls,False)
		for block in block_hit_list:
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom
class Wall(pg.sprite.Sprite):
	def __init__(self,color,x,y,width,height):
		super().__init__()
		self.image = pg.Surface([width,height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Room(object):
	wall_list = None
	enemy_sprite = None
	def __init__(self):
		walls =[
				#base walls
				[blue,0,0,10,200],
				[blue,0,300,10,300],
				
				[blue,780,0,20,200],
				[blue,780,300,10,300],
				
				[blue,0,0,300,20],
				[blue,500,0,300,20],
				
				[blue,0,580,200,20],
				[blue,300,580,500,20],
				]
		self.wall_list = pg.sprite.Group()
		self.enemy_sprite = pg.sprite.Group()
		for item in walls:
			wall = Wall(item[0],item[1],item[2],item[3],item[4])
			self.wall_list.add(wall)
class Room0(Room):
	def __init__(self):
		Room.__init__(self)
		walls =[ [blue,200,400,200,100],
				[blue,400,200,200,100],
				[blue,600,400,100,100],
				[blue,0,580,800,20],
				]
		for item in walls:
			wall = Wall(item[0],item[1],item[2],item[3],item[4])
			self.wall_list.add(wall)

class Room1(Room):
	def __init__(self):
		Room.__init__(self)
		walls =[ [red,200,400,200,100],
				[red,400,200,200,100],
				[red,600,400,100,100],
				[blue,0,0,20,600],
				[blue,0,580,800,20],
				]
		for item in walls:
			wall = Wall(item[0],item[1],item[2],item[3],item[4])
			self.wall_list.add(wall)
class Room2(Room):
	def __init__(self):
		Room.__init__(self)
		walls =[ [white,200,400,200,100],
				 [white,400,200,200,100],
				 [white,600,400,100,100],
				 [blue,0,0,20,600],
				 [blue,0,0,800,20]
				]
		for item in walls:
			wall = Wall(item[0],item[1],item[2],item[3],item[4])
			self.wall_list.add(wall)
class Room3(Room):
	def __init__(self):
		Room.__init__(self)
		walls =[ [black,200,400,200,100],
				[black,400,200,200,100],
				[black,600,400,100,100],
				[blue,0,0,800,20]
				]
		for item in walls:
			wall = Wall(item[0],item[1],item[2],item[3],item[4])
			self.wall_list.add(wall)
class Room4(Room):
	def __init__(self):
		Room.__init__(self)
		walls =[ [green,200,400,200,100],
				[green,400,200,200,100],
				[green,600,400,100,100],
				[blue,0,0,800,20],
				[blue,780,0,20,800]

				]
		for item in walls:
			wall = Wall(item[0],item[1],item[2],item[3],item[4])
			self.wall_list.add(wall)
class Room5(Room):
	def __init__(self):
		Room.__init__(self)
		walls =[ [yellow,200,400,200,100],
				[yellow,400,200,200,100],
				[yellow,600,400,100,100],
				[blue,0,580,800,20],
				[blue,780,0,20,600]

				]
		for item in walls:
			wall = Wall(item[0],item[1],item[2],item[3],item[4])
			self.wall_list.add(wall)



def room_label(msg):
	font = pg.font.SysFont("comicssans",40)
	text = font.render(msg,True,light_green)
	text_rect = text.get_rect()
	text_rect.center = (730),(40)
	game_display.blit(text,text_rect)

def main():
	
	rooms = []
	
	room = Room0()
	rooms.append(room)


	room = Room1()
	rooms.append(room)
	
	room = Room2()
	rooms.append(room)
	
	room = Room3()
	rooms.append(room)
	
	room = Room4()
	rooms.append(room)
	
	room = Room5()
	rooms.append(room)

	current_room_no = 0
	current_room = rooms[current_room_no]
	

	moving_sprite= pg.sprite.Group()
	player = Player(50,50)
	moving_sprite.add(player)

	clock = pg.time.Clock()
	exit = False
	time_play = 0

	while not exit:
		milliseconds = clock.tick(30) #when declare this tick(), game does not allow faster than this fps


		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit = True
			elif event.type == pg.KEYDOWN:

				if event.key == pg.K_UP:
					player.change_y = -5
					player.change_x = 0
				elif event.key == pg.K_DOWN:
					player.change_y = 5
					player.change_x = 0
				elif event.key == pg.K_LEFT:
					player.change_x = -5
					player.change_y = 0
				elif event.key == pg.K_RIGHT:
					player.change_x = 5
					player.change_y = 0

		#update the position and the interaction of moving_sprite(player)
		#with the other sprites


		player.update(current_room.wall_list)

		if player.rect.x < 15:
			current_room_no = room_list[current_room_no]["left"] 
			current_room=rooms[current_room_no]
			player.rect.x = 760
			player.rect.y = 400
		elif player.rect.x > 790:
			current_room_no =room_list[current_room_no]["right"]
			current_room=rooms[current_room_no] 
			player.rect.x = 30
			player.rect.y = 400
		elif player.rect.y < 15:
			current_room_no = room_list[current_room_no]["up"]
			current_room=rooms[current_room_no]
			player.rect.x = 400
			player.rect.y = 560
		elif player.rect.y > 580:
			current_room_no = room_list[current_room_no]["down"]
			current_room=rooms[current_room_no]
			player.rect.x = 400
			player.rect.y = 40
		time_play += milliseconds / 1000
		game_display.fill(black)
		room_label("Room "+str(current_room_no))
		
		moving_sprite.draw(game_display)
		current_room.wall_list.draw(game_display)
		pg.display.set_caption('time play = %0.2f' %(time_play))

		pg.display.flip()

	pg.quit()
if __name__ == "__main__":
    main()

	




