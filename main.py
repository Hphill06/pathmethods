
import sys
from tkinter import END
import pygame as p
import time as t
import random

from copy import copy 


sys.path.insert(0, 'path_methods')


#stuff needed for program to run
valley_1 = [(0,200),(100,200),(100,300),(250,300),(250,100),(400,100),(400,200),(600,200)] #path to follow
rounds_ene = { #type of enemies to spawn
	'1':[10,[3,6]],
	'2':[10,[2,10],[2,1],[1,2],[2,1],[1,2],[2,1],[1,2]],
	'3':[10,[1,5],[2,3],[2,3],[1,15]]
}
settings_width_height = 600,400




p.init()
class Button():
	def __init__(self,pos,size,function,col):#need to add image
		
		
		self.funct = function
		self.pos = pos
		self.size = size
		self.col = col

	def rect(self):
		rect = p.Rect(self.pos,self.size)
		return rect

	def is_clicked(self,pos):
		if self.rect().collidepoint(pos):
			return True
		return False
		
class tower():
	def __init__(self,type):
		self.types = [
			['name','dmg','atk_speed','cost','size'],
			['normal',2,1,0,(30,30)]
		]


class Enemy():
	def __init__(self,power,path,start):
		
		self.types = [
		['color','speed','type','health'],
		['red',50,'normal',1,(20,20),[0,0]],
		['blue',25,'normal',1,(25,25),[1,2]],
		['black',15,'normal',1,(20,20),[2,2]]
		]
		self.color = self.types[power][0]
		self.speed = self.types[power][1]
		self.type = self.types[power][2]
		self.health = self.types[power][3]
		self.size = self.types[power][4]
		self.current_pos = start
		self.path = path
		self.last_checkpoint = 0
		self.live = False
		self.made_end = False
		self.die = self.types[power][5]
		self.death = self.types[power][5]
	def spawn(self):
		self.live = True
	def rect(self):
		rect = p.Rect(self.current_pos,self.size)
		return rect
	def check_lessThan(self,xy):
		return (self.path[self.last_checkpoint][xy] < self.path[self.last_checkpoint+1][xy])
	def check_equal(self,xy):
		return (self.path[self.last_checkpoint][xy] == self.path[self.last_checkpoint+1][xy])
	def check_greaterThan(self,xy):
		return (self.path[self.last_checkpoint][xy] > self.path[self.last_checkpoint+1][xy])
	
	def caculate_speed(self,dt):
		if (self.check_lessThan(0)):#x<x2, right
			self.xvol = self.speed 
		if self.check_equal(0):
			self.xvol = 0
		if self.check_greaterThan(0):
			self.xvol = -(self.speed)
		if self.check_equal(1):#y==y2,no up no down
			self.yvol = 0
		if self.check_lessThan(1):# y <y2, down
			self.yvol = self.speed
		if self.check_greaterThan(1): #y > y2, up
			self.yvol = -(self.speed)
		self.yvol *= dt
		self.xvol *= dt
	def which_moving(self):
		if self.xvol > 0 and self.yvol ==0:
			return 'right'
		if self.xvol == 0 and self.yvol > 0:
			return 'down'
		if self.xvol == 0 and self.yvol < 0:
			return 'up'
		if self.xvol < 0 and self.yvol == 0:
			return 'left'
	def isclicked(self,click):
		if self.rect().collidepoint(click):
			self.live = False
			self.made_end = False
			print(str(click) + ' poped ' + self.color + ' | ' + str(self.current_pos)  )
			return True
			
		return False
	def update(self,dt):
		self.xvol = 0
		self.yvol = 0
		
		if self.live == True:
			if self.xvol == 0 and self.yvol == 0:
				self.caculate_speed(dt)
			if self.current_pos[0] == self.path[self.last_checkpoint+1][0] and self.current_pos[1] == self.path[self.last_checkpoint+1][1]:
				
				self.last_checkpoint += 1
				self.xvol = 0
				self.yvol = 0
				
			else:
				want_pos = (self.current_pos[0] +self.xvol,self.current_pos[1]+self.yvol)
				
				self.current_pos = (self.current_pos[0] +self.xvol,self.current_pos[1]+self.yvol)
				#print(self.which_moving())
				if self.which_moving() == 'right':
					if self.current_pos[0] + self.xvol > self.path[self.last_checkpoint+1][0] and self.current_pos[1] + self.yvol == self.path[self.last_checkpoint+1][1]:
						self.current_pos = self.path[self.last_checkpoint+1]
					else:
						self.current_pos = (self.current_pos[0] +self.xvol,self.current_pos[1]+self.yvol)
				
				if self.which_moving() == 'down':
					if self.current_pos[0]+ self.xvol == self.path[self.last_checkpoint+1][0] and self.current_pos[1] + self.yvol > self.path[self.last_checkpoint+1][1]:
						self.current_pos = self.path[self.last_checkpoint+1]
					else:
						self.current_pos = (self.current_pos[0] +self.xvol,self.current_pos[1]+self.yvol)
				if self.which_moving() == 'up':
					if self.current_pos[0]+ self.xvol == self.path[self.last_checkpoint+1][0] and self.current_pos[1] + self.yvol < self.path[self.last_checkpoint+1][1]:
						self.current_pos = self.path[self.last_checkpoint+1]
					else:
						self.current_pos = (self.current_pos[0] +self.xvol,self.current_pos[1]+self.yvol)
				
				#print(self.current_pos)
					
				if self.current_pos >= self.path[len(self.path) -1]:
					self.live = False
					self.made_end = True
					print('end')
					
class Map():
	def __init__(self,path,round1):
		self.path = path
		self.cur_round = round1
		self.setup()
	def setup(self):
		self.rounds_arr = []
		for i in range(len(rounds_ene)):
			print("here")
			enearr = []
			temp_arr_ene = rounds_ene[str(i+1)][1:]
			
			for x in temp_arr_ene:
				
				for e in range(x[1]):
					enearr.append(Enemy(x[0],self.path,self.path[0]))
					
			tempround = Round(rounds_ene[str(i+1)][0],enearr)
			self.rounds_arr.append(tempround)
		
	
		
			
class Round():
	def __init__(self,max,ene):
		self.ene_unspawned = ene
		self.ene_spawned = []
		self.max = max
		self.started = False
		self.end = False
	def send_next(self):
		
		self.ene_spawned.append(self.ene_unspawned.pop(0))
		for i in self.ene_spawned:
			if i.live != True:
				i.spawn()
				self.since_last_sent = t.time()
				#print(i)
		#print((len(self.ene_spawned)))
			

	def update(self,dt):
		if (len(self.ene_spawned)) < self.max and (len(self.ene_unspawned) != 0 and ((t.time()-self.since_last_sent) > 0.5)):
			self.send_next()
			
			

		if len(self.ene_unspawned) == 0 and len(self.ene_spawned) == 0:
			#print('round over!')
			self.end = True
			self.started = False
			
			
		cur = 0
		for i in self.ene_spawned:
			
			i.update(dt)
			if i.made_end:
				self.ene_spawned.pop(cur)
			cur +=1
				
	def click(self,click):
		cur = 0 #len(self.ene_spawned)
		for i in self.ene_spawned:
			
			if i.isclicked(click):
				self.ene_spawned.pop(cur)
				
				if i.color != 'red':
					#print('non red')
					for b in range(i.die[1]):
						#print('spawn ' + str(i.die[0]) +' ' +  str(b))
						test = copy(i)
						
						power = i.die[0]
						test.color = test.types[power][0]
						test.speed = test.types[power][1]
						test.type = test.types[power][2]
						test.health = test.types[power][3]
						test.size = test.types[power][4]		
						test.die = test.types[power][5]
						test.live = False
						self.made_end = False

						#print(test.color)
						test.speed = random.randint(15,100) #test.speed + random.randint(-,100)
						self.ene_unspawned.insert(0, test)
				for x in range(i.die[1]):
					self.send_next()		
			
				break
			cur += 1
			
			
			
	def start(self,map):
		if map.rounds_arr[map.cur_round].started != True:
			self.alive = 0
			self.started = True
			self.since_last_sent = t.time()
			
	def rects(self):
		self.temp = []
		for i in self.ene_spawned:
			if i.live:
				self.temp.append((i.color,i.rect()))
		return self.temp
class Main():
	'''
 gamestate (0 menu, 1 game)
 
 
 	'''
	def update_fps(self):
		fps = 'fps:'+str(int(self.clock.get_fps()))
		fps_text = self.font.render(fps, 1, p.Color("coral"))
		return fps_text
	def game(self):
		self.clock = p.time.Clock()
		fps = self.fps
		map = Map(valley_1,0)
		time = 0
		start_time = 0
		self.pre_time = t.time()
		but = Button((0,0),(25,25),map.rounds_arr[map.cur_round].start,'green')
		#var = but.is_clicked((1,1))
		
		
		while (self.gameState == 1):
			self.screen.fill('grey')
			self.screen.blit(self.update_fps(), (10,0))
			self.screen.blit(self.font.render('time:'+str(round((time-start_time),2)), 1, p.Color("coral")), (10,20))
			#get delta time
			self.now = t.time()
			self.dt = self.now - self.pre_time
			self.pre_time = self.now
			
			for e in p.event.get():
				if e.type == p.MOUSEBUTTONDOWN:
					#print(p.mouse.get_pos())
					
					try:
						map.rounds_arr[map.cur_round].click(p.mouse.get_pos())
						'''
						
						#print(len(map.rounds_arr[map.cur_round].ene_spawned))
						if map.rounds_arr[map.cur_round].started != True:
							map.rounds_arr[map.cur_round].start()
							start_time = t.time()
							time = t.time()
						'''
						if but.is_clicked(p.mouse.get_pos()):
							but.funct(map)
							start_time = t.time()
							time = t.time()
							
							
					except IndexError:
						
						pass
			
			#print(map.cur_round)
			try:
				if map.rounds_arr[map.cur_round].started :
					
					map.rounds_arr[map.cur_round].update(self.dt)
					
					time = t.time()
					arr = map.rounds_arr[map.cur_round].rects()
					for i in arr:
						
						p.draw.rect(self.screen,i[0],i[1])
				else:
					
					p.draw.rect(self.screen,but.col,but.rect())
				if map.rounds_arr[map.cur_round].end:
					map.cur_round +=1
			except IndexError:
				#print('won')
				pass
			self.clock.tick(fps)
			p.display.update()
				
	def setup_pygame(self,title,width,height):
		screen = p.display.set_mode((width,height))
		p.display.set_caption(title)
		return screen
	

	
	def __init__(self,gamestate):
		self.gameState = gamestate
		self.font = p.font.SysFont("Arial", 18)
		self.fps = 120
		while self.gameState != 2:
			
			WIDTH , HEIGHT = 600,400
			self.screen = self.setup_pygame('window_title', WIDTH, HEIGHT)
			if(self.gameState == 0):
				self.menu()
			if (self.gameState == 1):
				
				self.game()
			break
game = Main(1)
