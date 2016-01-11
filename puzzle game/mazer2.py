import pygame as pg

white =(255,255,255)
black = (0,0,0)
red = (159,29,15)
green =(13,189,12)
blue = (19,4,159)
yellow = (255,255,0)
light_green = (0,255,255)

clock = pg.time.Clock()
display_height = 600
display_width = 800





class Player(pg.sprite.Sprite):
	change_x = 0
	change_y = 0
	level = None
	def __init__(self,x,y):
		super().__init__()
		self.width = 30
		self.height = 50
		self.image = pg.Surface([self.width,self.height])

		self.image.fill(white)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		
		
	def calc_grav(self):
		if self.change_y == 0:
			self.change_y = 1
			#when player jump, self.change_y will decrease slowly due to this.
			#until self.change_y == 0, the player will fall
		else:
			self.change_y += 0.35
		#see if we are on the ground, it will stop
		if self.change_y >= 0 and self.rect.y >= display_height - self.rect.height:
			self.change_y = 0
			self.rect.y =display_height - self.height
		
	def jump(self):
	#to see if there is any platform below us
		self.rect.y += 2
		platform_hit_list = pg.sprite.spritecollide(self,self.level.platform_list,False)
		self.rect.y -= 2
#see if it is able jump, only if it is touching sth, or the ground
		if len(platform_hit_list) > 0 or self.rect.bottom >= display_height:
			self.change_y = -10
	def change_speed(self,x,y):
		self.change_x += x
		self.change_y += y
	def shoot_right(self,game_display,x,y):
		#basicall, 1.find the direction, the player is facing
		#2. from that direction, shoot a bullet. Cool

		shooting = True
		while shooting:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					quit()
			x +=30
			pg.draw.rect(game_display,white,[x,y,15,15])
			
			if x > self.rect.x + 700:
				shooting = False

			pg.display.update()
			clock.tick(60)
	def shoot_left(self,game_display,x,y):
		#basicall, 1.find the direction, the player is facing
		#2. from that direction, shoot a bullet. Cool

		shooting = True
		while shooting:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					quit()
			
			pg.draw.rect(game_display,white,[x,y,15,15])
			x -=30
			if x  < self.rect.x - 700:
				shooting = False

			pg.display.update()
			clock.tick(60)

				
				


	def update(self):
		self.calc_grav()

		self.rect.x += self.change_x
		
		block_hit_list = pg.sprite.spritecollide(self,self.level.platform_list,False)
		for block in block_hit_list:
				if self.change_x > 0:
					self.rect.right = block.rect.left
				elif self.change_x < 0:
					self.rect.left = block.rect.right

		#remember, the position of lines are crazily important,
		#if we convert 68 and 69, when player hit the block, it will be too late because
		#player sprite is already in the block, so player will be bounced out
		self.rect.y += self.change_y
		
		block_hit_list = pg.sprite.spritecollide(self,self.level.platform_list,False)
		for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
		            if self.change_y > 0:
		                   self.rect.bottom = block.rect.top
		                   

		                    
		            elif self.change_y < 0:
		                   self.rect.top = block.rect.bottom
		            

		            self.change_y = 0
 
            # Stop our vertical movement
class Platform(pg.sprite.Sprite):
	def __init__(self,color,x,y,width,height):
		super().__init__()
		self.image = pg.Surface([width,height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
class Moving_platform(Platform):
	change_x = 0
	change_y = 0
	boundary_top = 0
	boundary_bottom = 0
	boundary_left = 0
	boundary_right = 0
	player = None
	level = None

	def update(self):
	
		
		self.rect.x += self.change_x
	#use sprite.collide_rect: to determine if two sprite are collided
		hit = pg.sprite.collide_rect(self,self.player)
		if hit:
			if self.change_x > 0:
				self.player.rect.left = self.rect.right
			else:
				self.player.rect.right =  self.rect.left

		self.rect.y += self.change_y
		hit = pg.sprite.collide_rect(self,self.player)
		if hit:
			if self.change_y > 0:
				self.player.rect.top = self.rect.bottom
			else:
				self.player.rect.bottom =  self.rect.top
		#boundary
		if self.rect.bottom >= self.boundary_bottom or self.rect.top <= self.boundary_top:
			self.change_y *= -1

		cur_pos = self.rect.x - self.level.world_total_shift
		if cur_pos > self.boundary_right or cur_pos < self.boundary_left:
			self.change_x *= -1




class level(object):
	platform_list = None
	enemy_list = None
	world_shift_limit = 0
	world_total_shift = 0
	def __init__(self,player):
		self.platform_list = pg.sprite.Group()
		self.enemy_list = pg.sprite.Group()
		self.player = player
		self.background = None
	def update(self):
		self.platform_list.update()
		self.enemy_list.update()
	def draw(self,game_display):
		game_display.fill(black)
#		background_image = pg.image.load("mazer.2.jpg").convert()
#		game_display.blit(background_image,(self.world_total_shift//3,0))
		self.platform_list.draw(game_display)
		self.enemy_list.draw(game_display)
	def world_shift(self,shift_x):
		self.world_total_shift += shift_x
		
		for platform in self.platform_list:
			platform.rect.x += shift_x
		for enemy in self.enemy_list:
			enemy.rect.x += shift_x

class level0(level):
	def __init__(self,player):
		level.__init__(self,player)
		self.level = 0
		self.world_shift_limit = -2000
		platforms =[ 
					[blue,60,60,200,50],
					[blue,500,60,200,50],
					[blue,60,400,200,50],
					[blue,500,400,200,50],
					[blue,400,300,200,50],
					
					[blue,500,300,1200,50],
					[blue,700,400,400,50],
					[blue,600,200,1200,50],
					[blue,600,500,800,50],
					[white,2500,550,50,50]
				]
		for item in platforms:
			platform = Platform(item[0],item[1],item[2],item[3],item[4],)
			#platform.player = self.player
			self.platform_list.add(platform)

		block = Moving_platform(blue,10,500,40,40)
		block.player = self.player
		block.level = self
		block.change_y = -5
		block.boundary_top = 400
		block.boundary_bottom = 550

		self.platform_list.add(block)

class level1(level):
	def __init__(self,player):
		level.__init__(self,player)

		platforms =[ 
					[red,60,60,200,50],
					[red,500,60,200,50],
					[red,60,400,200,50],
					[red,500,400,200,50],
					[red,400,300,200,50],
					
					[red,500,300,1200,50],
					[red,700,400,400,50],
					[red,600,200,1200,50],
					[red,600,500,800,50]
					
				]
		for item in platforms:
			platform = Platform(item[0],item[1],item[2],item[3],item[4],)
			platform.player = self.player
			self.platform_list.add(platform)

		block = Moving_platform(red,10,500,30,40)
		block.player = self.player
		block.level = self
	
		block.change_x = 4
		block.boundary_right =150
		block.boundary_left = 5

		self.platform_list.add(block)
def main():
	pg.init()
	game_display = pg.display.set_mode((display_width,display_height))
	pg.display.set_caption("Mazer2")
	game_display.fill(black)

	current_level_no = 0

	player = Player(40,300)

	level_list =[]
	level_list.append(level0(player))
	level_list.append(level1(player))
	
	current_level = level_list[current_level_no]

	player.level = current_level


	
	moving_sprite = pg.sprite.Group()
	moving_sprite.add(player)
	exit = False
	while not exit:
		for event in pg.event.get():
			
			if event.type == pg.QUIT:
				exit = True
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_LEFT:
					player.change_speed(-5,0)
				elif event.key == pg.K_RIGHT:
					player.change_speed(5,0)
				elif event.key == pg.K_UP:
					player.jump()
				elif event.key == pg.K_d:
					player.shoot_right(game_display,player.rect.x + player.width,player.rect.y + 20)
				elif event.key == pg.K_an:
					player.shoot_left(game_display,player.rect.x,player.rect.y + 20)

			elif event.type == pg.KEYUP:
				if event.key == pg.K_LEFT and player.change_x < 0:
					player.change_speed(5,0)
				elif event.key == pg.K_RIGHT and player.change_x > 0:
					player.change_speed(-5,0)
		moving_sprite.update()
		current_level.update()

#		if player.rect.right > display_width: 
#			player.rect.right = display_width
#		if player.rect.left < 0: 
#			player.rect.left =0 
	#remember the position of line	

#shift the world the left, to deceive the player that he is going to
#the right, but actually, the world is shifting to the left
		if player.rect.x > 700:
			diff =  700 - player.rect.x
			player.rect.x = 700
			current_level.world_shift(diff)
		elif player.rect.x < 150:
			diff = 150 - player.rect.x
			player.rect.x = 150
			current_level.world_shift(diff) 

		#upgrade to the new level:
		if current_level.world_total_shift < current_level.world_shift_limit:
			if current_level_no < len(level_list)-1:
				player.rect.x = 120
				player.rect.y = 750
				current_level_no += 1
				current_level = level_list[current_level_no]
				player.level = current_level

		current_level.draw(game_display)
		moving_sprite.draw(game_display)
		clock.tick(30)
		pg.display.flip()
		

pg.quit()
if __name__ == "__main__":
    main()
