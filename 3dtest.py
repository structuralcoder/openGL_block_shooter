from __future__ import division

import sys
import math
import random
import time
import threading
import guns
import pygame
import localServe


from startupclient import *
#from cube_textures import *
from collections import deque
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse
from network import Network

pygame.init()

TICKS_PER_SEC = 60

# Size of sectors used to ease block loading.
SECTOR_SIZE = 16

WALKING_SPEED = 5
FLYING_SPEED = 15

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0 # About the height of a block.
# To derive the formula for calculating jump speed, first solve
#    v_t = v_0 + a * t
# for the time at which you achieve maximum height, where a is the acceleration
# due to gravity and v_t = 0. This gives:
#    t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
#    s = s_0 + v_0 * t + (a * t^2) / 2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2
BULLET_WIDTH = .02

if sys.version_info[0] >= 3:
	xrange = range

def import_weapons(item):
	if item=='pistol':
		returner = guns.pistol()
		return returner
	pass


def cube_vertices(x, y, z, n):
	""" Return the vertices of the cube at position x, y, z with size 2*n.
	"""
	return [
		x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
		x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
		x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
		x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
		x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
		x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
	]
	
def tall_vertices(x,y,z,w=.2,h=.5):
	return [
		x-w,y+h,z-w, x-w,y+h,z+w, x+w,y+h,z+w, x+w,y+h,z-w,  # top
		x-w,y-h,z-w, x+w,y-h,z-w, x+w,y-h,z+w, x-w,y-h,z+w,  # bottom
		x-w,y-h,z-w, x-w,y-h,z+w, x-w,y+h,z+w, x-w,y+h,z-w,  # left
		x+w,y-h,z+w, x+w,y-h,z-w, x+w,y+h,z-w, x+w,y+h,z+w,  # right
		x-w,y-h,z+w, x+w,y-h,z+w, x+w,y+h,z+w, x-w,y+h,z+w,  # front
		x+w,y-h,z-w, x-w,y-h,z-w, x-w,y+h,z-w, x+w,y+h,z-w,  # back
	]


def tex_coord(x, y, n=4):
	""" Return the bounding vertices of the texture square.
	"""
	m = 1.0 / n
	dx = x * m
	dy = y * m
	return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
	""" Return a list of the texture squares for the top, bottom and side.
	"""
	top = tex_coord(*top)
	bottom = tex_coord(*bottom)
	side = tex_coord(*side)
	result = []
	result.extend(top)
	result.extend(bottom)
	result.extend(side * 4)
	return result
	
def face_coords(top, bottom, front, side):
	""" Return a list of the texture squares for the top, bottom and side.
	"""
	top = tex_coord(*top)
	bottom = tex_coord(*bottom)
	front = tex_coord(*front)
	side = tex_coord(*side)
	result = []
	result.extend(top)
	result.extend(bottom)
	result.extend(side*3)
	result.extend(front)
	return result

TEXTURE_PATH = 'texture.png'

TEXTURES={}
GRASS = tex_coords((1, 0), (0, 1), (0, 0));TEXTURES['GRASS']=GRASS
SAND = tex_coords((1, 1), (1, 1), (1, 1));TEXTURES['SAND']=SAND
BRICK = tex_coords((2, 0), (2, 0), (2, 0));TEXTURES['BRICK']=BRICK
STONE = tex_coords((2, 1), (2, 1), (2, 1));TEXTURES['STONE']=STONE
BLACK = tex_coords((3,1), (3,1), (3,1));TEXTURES['GRASS']=GRASS
RED = tex_coords((3,2),(3,2),(3,2));TEXTURES['RED']=RED
WOOD_PLANKS = tex_coords((3,0), (3,0), (3,0));TEXTURES['BLACK']=BLACK
VADER_FACE = tex_coords((0,2), (0,2), (0,2));TEXTURES['VADER_FACE']=VADER_FACE
BULLET=tex_coords((1,2),(1,2),(1,2));TEXTURES['BULLET']=BULLET
SILVER = tex_coords((1,2),(1,2),(1,2));TEXTURES['SILVER']=SILVER
BANG = tex_coords((2,2),(2,2),(2,2));TEXTURES['BANG']=BANG

FACES = [
	( 0, 1, 0),
	( 0,-1, 0),
	(-1, 0, 0),
	( 1, 0, 0),
	( 0, 0, 1),
	( 0, 0,-1),
]

def normalize(position):
	""" Accepts `position` of arbitrary precision and returns the block
	containing that position.
	Parameters
	----------
	position : tuple of len 3
	Returns
	-------
	block_position : tuple of ints of len 3
	"""
	x, y, z = position
	x, y, z = (int(round(x)), int(round(y)), int(round(z)))
	return (x, y, z)


def sectorize(position):
	""" Returns a tuple representing the sector for the given `position`.
	Parameters
	----------
	position : tuple of len 3
	Returns
	-------
	sector : tuple of len 3
	"""
	x, y, z = normalize(position)
	x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
	return (x, 0, z)

class level:
	def __init__(self,type,anchor,xx=None,yy=None,zz=None):
		self.type=type
		self.x=int(anchor[0])
		self.y=int(anchor[1])
		self.z=int(anchor[2])
		#---------
		self.xx=xx
		self.yy=yy
		self.zz=zz


inspect_guns=True
inspect_which='pistol'
weapons={
#name =   x 	y    z  auto\dam 
#		  0     1    2   3   4
'pistol':import_weapons('pistol'),
}
weapon_batch={}

#class Player:
class peopleCube:
#	def __init__(self,window, num, player):
	def __init__(self,player):
#		#SETUP PLAYER ATTRIBUTES:
		self.num=player.num
		self.connected=True
#		self.pos=player.position
#		self.pos_under=(player.position[0],player.position[1]-1,player.position[2])
#		self.rotation=player.rotation
#		#----
#		self.hp=100
		self.moving=0
#		
#		#--BUILD PLAYER:
		self.head_size=float(player.head_size);#print(self.head_size)
		
		self.head_img=face_coords((3,1), (3,1), (0,2), (3,1))
		self.head_rotate=90
		self.head_batch= pyglet.graphics.Batch()
		#torso
		self.torso_width=0.2
		self.torso_height=0.2
		self.torso_img= BLACK
		self.torso_offset= (0, -0.45, 0)
		self.torso_twist= 20
		self.torso_batch= pyglet.graphics.Batch()
		#biceps
		self.bicep_width=0.1
		self.bicep_height=0.125
		self.bicep_img= BLACK
		self.l_bicep_offset=(-0.3, -0.35, 0)
		self.l_shoulder=10
		self.r_bicep_offset=(.3, -0.35, 0)
		self.r_shoulder=0
		self.l_bicep_batch= pyglet.graphics.Batch()
		self.r_bicep_batch= pyglet.graphics.Batch()
		#forearms
		self.forearm_width=0.08
		self.forearm_height=0.1
		self.forearm_img= STONE
		self.l_forearm_offset= (0, -0.2, 0)
		self.l_elbow=-45
		self.r_forearm_offset= (0, -0.2, 0)
		self.r_elbow=-90
		self.l_forearm_batch= pyglet.graphics.Batch()
		self.r_forearm_batch= pyglet.graphics.Batch()
		#legs
		self.leg_width=0.1
		self.leg_height=0.3
		self.leg_img= BLACK
		self.l_leg_offset=(-.125, -1, 0)
		self.l_stepAngle=0
		self.r_leg_offset=(.125, -1, 0)
		self.r_stepAngle=0
		self.leg_swing=1
		self.l_leg_batch= pyglet.graphics.Batch()
		self.r_leg_batch= pyglet.graphics.Batch()
		
		#setup guns
		self.trigger=False
		self.equip=['pistol']
		self.out=0
		self.auto=weapons[self.equip[self.out]].auto
		self.damage=weapons[self.equip[self.out]].damage
		self.gun_distance=weapons[self.equip[self.out]].distance
		print(self.gun_distance)
		self.bang_batch=pyglet.graphics.Batch()
		self.gun_sound=weapons[self.equip[self.out]].sound
		self.hit_sound=pygame.mixer.Sound('sounds/got_hit.wav')
		self.animate_hit=False
	
	def stop(self):
		self.moving=0


class Model(object):

	def __init__(self):

		# A Batch is a collection of vertex lists for batched rendering.
		self.batch = pyglet.graphics.Batch()

		# A TextureGroup manages an OpenGL texture.
		self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())

		# A mapping from position to the texture of the block at that position.
		# This defines all the blocks that are currently in the world.
		self.world = {}
		self.people = {}
		self.players = []
		self.projectiles={}
		self.bullets={}

		# Same mapping as `world` but only contains blocks that are shown.
		self.shown = {}

		# Mapping from position to a pyglet `VertextList` for all shown blocks.
		self._shown = {}

		# Mapping from sector to a list of positions inside that sector.
		self.sectors = {}

		# Simple function queue implementation. The queue is populated with
		# _show_block() and _hide_block() calls
		self.queue = deque()

		self.local_player=0
		self.iterable=0
		
		self._initialize()
		
		

	def _initialize(self):
		""" Initialize the world by placing all the blocks.
		"""
		n = 80  # 1/2 width and height of world
		s = 1  # step size
		y = 0  # initial y height
		for x in xrange(-n, n + 1, s):
			for z in xrange(-n, n + 1, s):
				# create a layer stone and grass everywhere.
				self.add_block((x, y - 2, z), WOOD_PLANKS, immediate=False)
				self.add_block((x, y - 3, z), STONE, immediate=False)
				if x in (-n, n) or z in (-n, n):
					# create outer walls.
					for dy in xrange(-2, 3):
						self.add_block((x, y + dy, z), STONE, immediate=False)

		# generate the hills randomly
		#o = n - 10
		#for _ in xrange(1):
		#    a = 1#random.randint(-o, o)  # x position of the hill
		#    b = -10#random.randint(-o, o)  # z position of the hill
		#    c = -1  # base of the hill
		#    h = 5#random.randint(1, 6)  # height of the hill
		#    s = 2#random.randint(4, 8)  # 2 * s is the side length of the hill
		#    d = 0  # how quickly to taper off the hills
		#    t = random.choice([GRASS, SAND, BRICK])
		#    for y in xrange(c, c + h):
		#        for x in xrange(a - s, a + s + 1):
		#            for z in xrange(b - s, b + s + 1):
		#                if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
		#                    continue
		#                if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
		#                    continue
		#                self.add_block((x, y, z), t, immediate=False)
		#        s -= d  # decrement side lenth so hills taper off
		#
		#generate based on lvl text file
		openlvl=open('testlevel.txt')
		world_objects=[]
		for line in openlvl:
			line="".join(line.split())
			if len(line)<2:
				continue
			elif line[0]=='#':
				continue
				
			line=line.replace('(','').replace(')','')
			blk=line.split(':')
			pos=blk[0].split(',')
			color=blk[1]
			#class level(self,type,anchor,xx=None,yy=None,zz=None)
			world_objects.append(level(color,(pos)))
			
		openlvl.close()
		
		for l in world_objects:
			x=l.x;
			y=l.y
			z=l.z
			#BRICK, GRASS, SAND, STONE
			t=BLACK
			"""
			put together texture dict
			"""
			if l.type=='BRICK':
				t=BRICK
			if l.type=='GRASS':
				t=GRASS
			if l.type=='SAND':
				t=SAND
			if l.type=='STONE':
				t=STONE
			if l.type=='BLACK':
				t=BLACK
			if l.type=='WOOD_PLANKS':
				t=WOOD_PLANKS
			if l.type=='SILVER':
				t=SILVER
			#			ie  x   z  y
			#self.add_block((x, y, z), t, immediate=False)
			self.add_block((x, y, z), t, immediate=False)
			#print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
			#print('block added: ')
			#print('x: '+str(type(x))+' :: '+ str(x))
			#print('y: '+str(type(y))+' :: '+ str(y))
			#print('z: '+str(type(z))+' :: '+ str(z))
			
		
		for w in weapons:
			weapon_batch[w]=pyglet.graphics.Batch()
			x=0
			while x < len(weapons[w].blocks):
				texture_data=BRICK
				#print(texture_data)
				pos=(0,-0.35,-2)
				weapon_batch[w].add(24, GL_QUADS, self.group,
					('v3f/static', weapons[w].blocks[x+1]),
					('t2f/static', weapons[w].blocks[x]))
				x+=2
			
		
		
	def hit_test(self, position, vector, max_distance=8):
		""" Line of sight search from current position. If a block is
		intersected it is returned, along with the block previously in the line
		of sight. If no block is found, return None, None.
		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position to check visibility from.
		vector : tuple of len 3
			The line of sight vector.
		max_distance : int
			How many blocks away to search for a hit.
		"""
		variable1=None
		variable2=None
		m = 8
		x, y, z = position
		dx, dy, dz = vector
		previous = None
		people_poses={}
		for num in game.players:
			if num!=self.local_player:
				peep=game.players[num]
				people_poses[num]=peep.position
		try:max_distance=int(self.players[self.local_player].gun_distance)
		except:
			print('max_distance wont convert @ hit_test')
			print('gun_distance found:',self.players[self.local_player].gun_distance)
		for _ in xrange(max_distance * m):
			key = normalize((x, y, z))
			if key!=previous:
				#check if player is able to be hit with your bullet
				for n in people_poses:
					pos=people_poses[n]
					px,py,pz=pos
					if y>(py-1.5) and y<(py+.4):
						#print('y in range for player',n)
						if x>(px-.44) and x<(px+.44):
							#print('x in range for player',n)
							if z>(pz-.44) and z<(pz+.44):
								#print('z hit player',n)
								if self.iterable>=100:
									self.iterable=0
								#print('player',n,'hit',self.iterable)
								self.iterable+=1
								variable1=n
								variable2=None
								
			if key != previous and key in self.world and variable1==None:
				return key, previous
			previous = key
			x, y, z = x + dx / m, y + dy / m, z + dz / m
		return variable1, variable2

	def exposed(self, position):
		""" Returns False is given `position` is surrounded on all 6 sides by
		blocks, True otherwise.
		"""
		x, y, z = position
		for dx, dy, dz in FACES:
			if (x + dx, y + dy, z + dz) not in self.world:
				return True
		return False

	def add_block(self, position, texture, immediate=True):
		""" Add a block with the given `texture` and `position` to the world.
		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to add.
		texture : list of len 3
			The coordinates of the texture squares. Use `tex_coords()` to
			generate.
		immediate : bool
			Whether or not to draw the block immediately.
		"""
		if position in self.world:
			self.remove_block(position, immediate)
		self.world[position] = texture
		self.sectors.setdefault(sectorize(position), []).append(position)
		if immediate:
			if self.exposed(position):
				self.show_block(position)
			self.check_neighbors(position)

	def add_player(self,player, immediate=True):
		self.players.append(peopleCube(player))
		#print((self.players))
		"""bang_batch"""
		vertex_data=cube_vertices(0, 0, 0, 0.15)
		texture_data = list(BANG)
		self.players[int(player.num)].bang_batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))
		""""""
		position=player.position
		texture=player.head_img
		if position in self.people:
			self.remove_player(player)
		self.people[player.num] = texture
		self.sectors.setdefault(sectorize(position), []).append(position)
		#print(immediate)
		if immediate:
			if self.exposed(position):
				self.show_people(player,position)
			self.check_neighbors(position)
		
	
	def add_bullet(self,bullet, immediate=True):
		position=bullet.position
		x,y,z=position
		if y>-2:
			if position not in self.bullets:
				self.bullets[position]=bullet
				self.bullets[position].batch=pyglet.graphics.Batch()
				#print('bullet added')
			texture=BULLET
			#if position in self.projectiles:
			#	self.remove_bullet(position, immediate)
			self.projectiles[position] = texture
			self.sectors.setdefault(sectorize(position), []).append(position)
			if immediate:
				if self.exposed(position):
					self.show_bullet(bullet)
				#self.check_neighbors(position)
	
	def remove_block(self, position, immediate=True):
		""" Remove the block at the given `position`.
		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to remove.
		immediate : bool
			Whether or not to immediately remove block from canvas.
		"""
		del self.world[position]
		#print('deleted block from the world:',list(position))
		self.sectors[sectorize(position)].remove(position)
		if immediate:
			if position in self.shown:
				self.hide_block(position)
			self.check_neighbors(position)
	
	def remove_player(self, player, immediate=True):
		try:del self.people[player.num]
		except:pass
		player.connected=False
		#print(str(position)+' deleted')
		for num in game.players:
			pl=game.players[num]
			if pl.num==player.num:
				position=pl.position
				self.sectors[sectorize(position)].remove(position)
				if immediate:
					if position in self._shown:
						del self._shown[position]
				break

	def remove_bullet(self, position):
		del self.projectiles[position]
		#print(str(position)+' deleted')
		self.sectors[sectorize(position)].remove(position)
			
	def check_neighbors(self, position):
		""" Check all blocks surrounding `position` and ensure their visual
		state is current. This means hiding blocks that are not exposed and
		ensuring that all exposed blocks are shown. Usually used after a block
		is added or removed.
		"""
		x, y, z = position
		for dx, dy, dz in FACES:
			key = (x + dx, y + dy, z + dz)
			if key not in self.world:
				continue
			if self.exposed(key):
				if key not in self.shown:
					self.show_block(key)
			else:
				if key in self.shown:
					self.hide_block(key)

	def show_block(self, position, immediate=True):
		""" Show the block at the given `position`. This method assumes the
		block has already been added with add_block()
		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to show.
		immediate : bool
			Whether or not to show the block immediately.
		"""
		pass_up=False
		if position in self.world:
			texture = self.world[position]
			self.shown[position] = texture
		else:
			pass_up=True
		
		if pass_up==False:
			if immediate:
				self._show_block(position, texture)
			else:
				self._enqueue(self._show_block, position, texture)

	def show_people(self,player, position, immediate=True):
		if position in self.people:
			texture = self.people[player.num]
		
		#self.shown[position] = texture
		#print(self.shown[position])
		if immediate:
			self._show_people(player)
		else:
			self._enqueue(self._show_block, position, texture)
	
	def show_bullet(self,bullet, immediate=True):
		if bullet.position in self.projectiles:
			texture = self.projectiles[bullet.position]
		
		self.shown[bullet.position] = texture
		#print(self.shown[position])
		if immediate:
			self._show_bullet(bullet)
			
	def _show_block(self, position, texture):
		""" Private implementation of the `show_block()` method.
		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to show.
		texture : list of len 3
			The coordinates of the texture squares. Use `tex_coords()` to
			generate.
		"""
		x, y, z = position
		vertex_data = cube_vertices(x, y, z, 0.5)
		texture_data = list(texture)
		
		# create vertex list
		# FIXME Maybe `add_indexed()` should be used instead
		self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))
			
	def _show_people(self,player):
		global weapon_batch
		#show head
		texture=self.players[int(player.num)].head_img
		vertex_data = cube_vertices(0, 0, 0, float(player.head_size))
		texture_data = list(texture)
		self._shown[player.position] = self.players[int(player.num)].head_batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))
		print('player',player.num,'was added to the _shown list')
		#show torso
		texture=self.players[int(player.num)].torso_img
		#x,y,z=player.torso_offset
					# tall_vertices(x,y,z, w=0.2, h=0.5)
		vertex_data = tall_vertices(0,0,0, player.torso_width,player.torso_height)
		texture_data = list(texture)
		self._shown[player.position] = self.players[int(player.num)].torso_batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))
		#show left arm
		texture=self.players[int(player.num)].bicep_img
					# tall_vertices(x,y,z,w=0.2, h=0.5)
		vertex_data = tall_vertices(0,0,0, player.bicep_width,player.bicep_height)
		texture_data = list(texture)
		self._shown[player.position] = self.players[int(player.num)].l_bicep_batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))
		texture=self.players[int(player.num)].forearm_img
					# tall_vertices(x,y,z,w=0.2, h=0.5)
		vertex_data = tall_vertices(0,0,0, player.forearm_width,player.forearm_height)
		texture_data = list(texture)
		self._shown[player.position] = self.players[int(player.num)].l_forearm_batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))
		
		
		#show right arm
		texture=self.players[int(player.num)].bicep_img
					# tall_vertices(x,y,z,w=0.2, h=0.5)
		vertex_data = tall_vertices(0,0,0, player.bicep_width,player.bicep_height)
		texture_data = list(texture)
		self._shown[player.position] = self.players[int(player.num)].r_bicep_batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))
		texture=self.players[int(player.num)].forearm_img
					# tall_vertices(x,y,z,w=0.2, h=0.5)
		vertex_data = tall_vertices(0,0,0, player.forearm_width,player.forearm_height)
		texture_data = list(texture)
		self._shown[player.position] = self.players[int(player.num)].r_forearm_batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))
		#show left leg
		texture=self.players[int(player.num)].leg_img
					# tall_vertices(x,y,z,w=0.2, h=0.5)
		vertex_data = tall_vertices(0,0,0, player.leg_width,player.leg_height)
		texture_data = list(texture)
		self._shown[player.position] = self.players[int(player.num)].l_leg_batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))
			
		#show right leg
		texture=self.players[int(player.num)].leg_img
					# tall_vertices(x,y,z,w=0.2, h=0.5)
		vertex_data = tall_vertices(0,0,0, player.leg_width,player.leg_height)
		texture_data = list(texture)
		self._shown[player.position] = self.players[int(player.num)].r_leg_batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))
	
	
	def _show_bullet(self, bullet):
		#replace=bullet.position.replace('(','').replace(')','')
		#split=replace.split(',')
		#dposition=(float(split[0]),float(split[1]),float(split[2]))
		x, y, z = bullet.position
		vertex_data = cube_vertices(x, y, z, BULLET_WIDTH)
		texture_data = list(BULLET)
		#print(texture_data)
		
		self._shown[bullet.position] = self.bullets[bullet.position].batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))
	
	
	def hide_block(self, position, immediate=True):
		""" Hide the block at the given `position`. Hiding does not remove the
		block from the world.
		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to hide.
		immediate : bool
			Whether or not to immediately remove the block from the canvas.
		"""
		self.shown.pop(position)
		if immediate:
			self._hide_block(position)
		else:
			self._enqueue(self._hide_block, position)
	

	def _hide_block(self, position):
		""" Private implementation of the 'hide_block()` method.
		"""
		self._shown.pop(position).delete()
	

	
	def show_sector(self, sector):
		""" Ensure all blocks in the given sector that should be shown are
		drawn to the canvas.
		"""
		for position in self.sectors.get(sector, []):
			if position not in self.shown and self.exposed(position):
				self.show_block(position, False)

	def hide_sector(self, sector):
		""" Ensure all blocks in the given sector that should be hidden are
		removed from the canvas.
		"""
		for position in self.sectors.get(sector, []):
			if position in self.shown:
				self.hide_block(position, False)

	def change_sectors(self, before, after):
		""" Move from sector `before` to sector `after`. A sector is a
		contiguous x, y sub-region of world. Sectors are used to speed up
		world rendering.
		"""
		before_set = set()
		after_set = set()
		pad = 4
		for dx in xrange(-pad, pad + 1):
			for dy in [0]:  # xrange(-pad, pad + 1):
				for dz in xrange(-pad, pad + 1):
					if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
						continue
					if before:
						x, y, z = before
						before_set.add((x + dx, y + dy, z + dz))
					if after:
						x, y, z = after
						after_set.add((x + dx, y + dy, z + dz))
		show = after_set - before_set
		hide = before_set - after_set
		for sector in show:
			self.show_sector(sector)
		for sector in hide:
			self.hide_sector(sector)

	def _enqueue(self, func, *args):
		""" Add `func` to the internal queue.
		"""
		self.queue.append((func, args))

	def _dequeue(self):
		""" Pop the top function from the internal queue and call it.
		"""
		func, args = self.queue.popleft()
		func(*args)

	def process_queue(self):
		""" Process the entire queue while taking periodic breaks. This allows
		the game loop to run smoothly. The queue contains calls to
		_show_block() and _hide_block() so this method should be called if
		add_block() or remove_block() was called with immediate=False
		"""
		start = time.process_time()
		while self.queue and time.process_time() - start < 1.0 / TICKS_PER_SEC:
			self._dequeue()

	def process_entire_queue(self):
		""" Process the entire queue with no breaks.
		"""
		while self.queue:
			self._dequeue()

def save(win):
	print('saving...')
	creation=''
	saveFile=open('testlevel.txt','w+')
	for loc in win.model.world.keys():
		if loc[1]<-1:
			continue
		bl=0
		for tex in win.inventory:
			if win.model.world[loc] == tex:
				i=0
				for _ in saveFile:
					i+1
				saveFile.seek(0,i)
				ll=str(loc)+':'+win.block_names[bl]+'\n'
				creation=creation+ll
				continue
			else:bl+=1
	saveFile.write(creation)
	saveFile.close()
	print('saved!')



class Window(pyglet.window.Window):
	
	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(*args, **kwargs)

		# Whether or not the window exclusively captures the mouse.
		self.exclusive = False

		# When flying gravity has no effect and speed is increased.
		self.flying = False

		# Strafing is moving lateral to the direction you are facing,
		# e.g. moving to the left or right while continuing to face forward.
		#
		# First element is -1 when moving forward, 1 when moving back, and 0
		# otherwise. The second element is -1 when moving left, 1 when moving
		# right, and 0 otherwise.
		self.strafe = [0, 0]

		# Current (x, y, z) position in the world, specified with floats. Note
		# that, perhaps unlike in math class, the y-axis is the vertical axis.
		self.position = (0, 0, 0)

		# First element is rotation of the player in the x-z plane (ground
		# plane) measured from the z-axis down. The second is the rotation
		# angle from the ground plane up. Rotation is in degrees.
		#
		# The vertical plane rotation ranges from -90 (looking straight down) to
		# 90 (looking straight up). The horizontal rotation range is unbounded.
		self.rotation = (0, 0)

		# Which sector the player is currently in.
		self.sector = None

		# The crosshairs at the center of the screen.
		self.reticle = None

		# Velocity in the y (upward) direction.
		self.dy = 0

		# A list of blocks the player can place. Hit num keys to cycle.
		#self.inventory = [BRICK, GRASS, SAND]

		# The current block the user can place. Hit num keys to cycle.
		#self.block = self.inventory[0]

		# Convenience list of num keys.
		self.num_keys = [
			key._1, key._2, key._3, key._4, key._5,
			key._6, key._7, key._8, key._9, key._0]
			
		#same as above but for function keys:added by Jesse:
		self.function_keys = [
			key.F1, key.F2, key.F3, key.F4, key.F5,
			key.F6, key.F7, key.F8, key.F9, key.F10,
			key.F11, key.F12, key.F12]

		# Instance of the model that handles the world.
		self.model = Model()

		# The label that is displayed in the top left of the canvas.
		self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
			x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
			color=(0, 0, 0, 255))
		
		#JESSE'S VARIABLES:
		self.saveButton=pyglet.text.Label('SAVE', font_name='Arial', font_size=18,
			x=self.width*.75, y=self.height-10, anchor_x='left', anchor_y='top',
			color=(0, 0, 0, 255))
		
		self.settings=pyglet.text.Label('', font_name='Arial', font_size=18,
			x=20, y=50, anchor_x='left', anchor_y='top',
			color=(0, 0, 0, 255))
			
		self.healthbar=(15,self.height-30,self.width-30,15,0,255,0)
		self.healthbar_container=(10,self.height-35,self.width-20,25,0,0,0)
		self.score = pyglet.text.Label('', font_name='Arial', font_size=18,
							x=self.width*.80, y=self.height - 40, anchor_x='left', anchor_y='top',
							color=(0, 0, 0, 255))
		#						height		width   color   drop
		#						0			1		2		3
		self.blood_overlay=(self.height,self.width,(255,0,0,.30),0)
		
			
		"""edit mode variables"""
		self.edit_mode=0
		self.multi_block_pile=1
		#default self.inventory turned off @ lines 872 and 875, continued below:
		self.inventory = [BRICK, GRASS, SAND,BLACK,WOOD_PLANKS,SILVER]
		self.block_names = ['BRICK', 'GRASS', 'SAND','BLACK','WOOD_PLANKS','SILVER']
		self.placing_block = 0
		self.block = self.inventory[0]
		
		"""battle mode variables"""
		self.bang='x'
		self.barrel={}
		self.auto_recoil=60
		self.no_more_bullet='x'
		self.hp=100
		self.hit=False
		self.respawn=0
		self.born=0
		
		self.bang_pos={
			'pistol':(0,.15,-.5)
		}
		
		
		
		game = net.send('get')
		num=len(game.players)-1
		self.model.local_player=self.local_player=num
		print('local_player is player #',num)
		self.position=game.players[self.local_player].position
		self.rotation=game.players[self.local_player].rotation
		#self.get_back_in_the_game()
		
		
		
		# This call schedules the `update()` method to be called
		# TICKS_PER_SEC. This is the main game event loop.
		pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)

	def set_exclusive_mouse(self, exclusive):
		""" If `exclusive` is True, the game will capture the mouse, if False
		the game will ignore the mouse.
		"""
		super(Window, self).set_exclusive_mouse(exclusive)
		self.exclusive = exclusive

	def get_sight_vector(self):
		""" Returns the current line of sight vector indicating the direction
		the player is looking.
		"""
		x, y = self.rotation
		# y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
		# is 1 when looking ahead parallel to the ground and 0 when looking
		# straight up or down.
		m = math.cos(math.radians(y))
		# dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
		# looking straight up.
		dy = math.sin(math.radians(y))
		dx = math.cos(math.radians(x - 90)) * m
		dz = math.sin(math.radians(x - 90)) * m
		return (dx, dy, dz)

	def get_motion_vector(self):
		""" Returns the current motion vector indicating the velocity of the
		player.
		Returns
		-------
		vector : tuple of len 3
			Tuple containing the velocity in x, y, and z respectively.
		"""
		if any(self.strafe):
			self.model.players[self.local_player].moving=1
			x, y = self.rotation
			strafe = math.degrees(math.atan2(*self.strafe))
			y_angle = math.radians(y)
			x_angle = math.radians(x + strafe)
			if self.flying:
				m = math.cos(y_angle)
				dy = math.sin(y_angle)
				if self.strafe[1]:
					# Moving left or right.
					dy = 0.0
					m = 1
				if self.strafe[0] > 0:
					# Moving backwards.
					dy *= -1
				# When you are flying up or down, you have less left and right
				# motion.
				dx = math.cos(x_angle) * m
				dz = math.sin(x_angle) * m
			else:
				dy = 0.0
				dx = math.cos(x_angle)
				dz = math.sin(x_angle)
		else:
			dy = 0.0
			dx = 0.0
			dz = 0.0
		return (dx, dy, dz)
	
	def update(self, dt):
		global game
		""" This method is scheduled to be called repeatedly by the pyglet
		clock.
		Parameters
		----------
		dt : float
			The change in time since the last call.
		"""
		self.model.process_queue()
		sector = sectorize(self.position)
		if sector != self.sector:
			self.model.change_sectors(self.sector, sector)
			if self.sector is None:
				self.model.process_entire_queue()
			self.sector = sector
		m = 8
		dt = min(dt, 0.2)
		for _ in xrange(m):
			self._update(dt / m)
		
		
		#update player
		try:
			pass_string=str(self.position)+'/'+str(self.rotation)#0/1
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].head_size)		#2
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].head_img)			#3
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].head_rotate)		#4
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].torso_width)		#5
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].torso_height)     #6
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].torso_img)        #7
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].torso_offset)     #8
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].torso_twist)      #9
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].bicep_width)      #10
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].bicep_height)     #11
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].bicep_img)        #12
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].l_bicep_offset)   #13
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].l_shoulder)       #14
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].r_bicep_offset)   #15
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].r_shoulder)       #16
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].forearm_width)    #17
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].forearm_height)   #18
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].forearm_img)      #19
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].l_forearm_offset) #20
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].l_elbow)          #21
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].r_forearm_offset) #22
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].r_elbow)          #23
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].leg_width)        #24
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].leg_height)       #25
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].leg_img)          #26
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].l_leg_offset)     #27
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].l_stepAngle)      #28
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].r_leg_offset)     #29
			pass_string=pass_string+'/'+str(self.model.players[self.local_player].r_stepAngle)      #30
			pass_string=pass_string+'/'+str(self.bang)												#31
			pass_string=pass_string+'/'+str(self.no_more_bullet)									#32	
			pass_string=pass_string+'/'+str(self.born)												#33
			pass_string=pass_string+'/'+str(self.hit)		#34										#33
			
			game = net.send(pass_string)
			self.hp=game.players[self.local_player].hp
		except:
			print('couldnt update local_player info')
			print('LENGTH OF self.model.players: ',len(self.model.players))
		
		
		if len(game.players)<len(self.model.players):
			players_lost=[]
			for pl in self.model.players:
				players_lost.append(pl)
				for n in game.players:
					g=game.players[n]
					if g.num==pl.num:
						players_lost.remove(pl)
			for pl in players_lost:
				self.model.remove_player(pl)
					
		
		
		self.bang='x'
		if self.no_more_bullet!='x':
			self.no_more_bullet='x'
		
		
		self.model.bullets={}
		
		try:
			for bullet in game.bullets:
				self.model.add_bullet(bullet)
		except:pass
		
		"""move legs"""
		if self.strafe[0]==0 and self.strafe[1]==0:
			self.model.players[self.local_player].moving=0
		
		if self.model.players[self.local_player].moving==1:
			angle=self.model.players[self.local_player].l_stepAngle
			if angle>30:
				self.model.players[self.local_player].leg_swing=-3
			elif angle<-30:
				self.model.players[self.local_player].leg_swing=3
			self.model.players[self.local_player].l_stepAngle+=self.model.players[self.local_player].leg_swing
			#print(self.model.players[self.local_player].l_stepAngle)
			self.model.players[self.local_player].r_stepAngle-=self.model.players[self.local_player].leg_swing
		else:
			self.model.players[self.local_player].l_stepAngle=0
			self.model.players[self.local_player].r_stepAngle=0
		
			
		
		
	def _update(self, dt):
		""" Private implementation of the `update()` method. This is where most
		of the motion logic lives, along with gravity and collision detection.
		Parameters
		----------
		dt : float
			The change in time since the last call.
		"""
		# walking
		speed = FLYING_SPEED if self.flying else WALKING_SPEED
		d = dt * speed # distance covered this tick.
		dx, dy, dz = self.get_motion_vector()
		# New position in space, before accounting for gravity.
		dx, dy, dz = dx * d, dy * d, dz * d
		# gravity
		if not self.flying:
			# Update your vertical speed: if you are falling, speed up until you
			# hit terminal velocity; if you are jumping, slow down until you
			# start falling.
			self.dy -= dt * GRAVITY
			self.dy = max(self.dy, -TERMINAL_VELOCITY)
			dy += self.dy * dt
		# collisions
		x, y, z = self.position
		x, y, z = self.collide((x + dx, y + dy, z + dz), PLAYER_HEIGHT)
		self.position=(x,y,z)
		
	def collide(self, position, height):
		""" Checks to see if the player at the given `position` and `height`
		is colliding with any blocks in the world.
		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position to check for collisions at.
		height : int or float
			The height of the player.
		Returns
		-------
		position : tuple of len 3
			The new position of the player taking into account collisions.
		"""
		# How much overlap with a dimension of a surrounding block you need to
		# have to count as a collision. If 0, touching terrain at all counts as
		# a collision. If .49, you sink into the ground, as if walking through
		# tall grass. If >= .5, you'll fall through the ground.
		pad = 0.25
		p = list(position)
		np = normalize(position)
		for face in FACES:  # check all surrounding blocks
			for i in xrange(3):  # check each dimension independently
				if not face[i]:
					continue
				# How much overlap you have with this dimension.
				d = (p[i] - np[i]) * face[i]
				if d < pad:
					continue
				for dy in xrange(height):  # check each height
					op = list(np)
					op[1] -= dy
					op[i] += face[i]
					if tuple(op) not in self.model.world:
						continue
					p[i] -= (d - pad) * face[i]
					if face == (0, -1, 0) or face == (0, 1, 0):
						# You are colliding with the ground or ceiling, so stop
						# falling / rising.
						self.dy = 0
					break
		return tuple(p)
			

	def on_mouse_press(self, x, y, button, modifiers):
		""" Called when a mouse button is pressed. See pyglet docs for button
		amd modifier mappings.
		Parameters
		----------
		x, y : int
			The coordinates of the mouse click. Always center of the screen if
			the mouse is captured.
		button : int
			Number representing mouse button that was clicked. 1 = left button,
			4 = right button.
		modifiers : int
			Number representing any modifying keys that were pressed when the
			mouse button was clicked.
		"""
		if self.exclusive:
			vector = self.get_sight_vector()
			block, previous = self.model.hit_test(self.position, vector)
			if (button == mouse.RIGHT) or \
					((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
				# ON OSX, control + left click = right click.
				if previous and self.edit_mode==1:
					self.model.add_block(previous, self.block)
					if self.multi_block_pile>1:
						previous=(previous[0],previous[1]+1,previous[2])
						self.model.add_block(previous, self.block)
					if self.multi_block_pile>2:
						previous=(previous[0],previous[1]+1,previous[2])
						self.model.add_block(previous, self.block)
			elif button == pyglet.window.mouse.LEFT:
				#if playing a game
				if self.bang=='x' and self.hp>0 and self.edit_mode==0:
					x,y,z=self.position
					tup=(x,y,z)
					dx, dy, dz=vector
					#self.model.hit_test(self, position, vector, max_distance=8)\
					hit_return=self.model.hit_test(self.position,vector)
					self.bang=[hit_return[0],self.model.players[self.local_player].damage]
					#print (self.bang)
					
					
				#else if edit_mode is on
				elif self.edit_mode==1:
					vector = self.get_sight_vector()
					block = self.model.hit_test(self.position, vector)[0]
					if block:
						x,y,z=block
						self.model.remove_block((x,y,z))
		else:
			if x>=self.width*.75 and x<=(self.width*.75)+70:
				if y>self.height-40:
					save(self)
			else:
				self.set_exclusive_mouse(True)
				
	def on_mouse_release(self, x, y, button, modifiers):
		"""used by JESSE to release trigger"""
		if button == pyglet.window.mouse.LEFT and self.bang!='x':
			self.bang='x'
			#print('off trigger')
		self.auto_recoil=60
		
	def on_mouse_motion(self, x, y, dx, dy):
		""" Called when the player moves the mouse.
		Parameters
		----------
		x, y : int
			The coordinates of the mouse click. Always center of the screen if
			the mouse is captured.
		dx, dy : float
			The movement of the mouse.
		"""
		if self.exclusive:
			m = 0.15
			x, y = self.rotation
			x, y = x + dx * m, y + dy * m
			y = max(-90, min(90, y))
			self.rotation = (x, y)
	def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
		self.on_mouse_motion(x, y, dx, dy)

	def on_key_press(self, symbol, modifiers):
		""" Called when the player presses a key. See pyglet docs for key
		mappings.
		Parameters
		----------
		symbol : int
			Number representing the key that was pressed.
		modifiers : int
			Number representing any modifying keys that were pressed.
		"""
		if self.hp>0:
			if symbol == key.W:
				self.strafe[0] -= 1
			elif symbol == key.S:
				self.strafe[0] += 1
			elif symbol == key.A:
				self.strafe[1] -= 1
			elif symbol == key.D:
				self.strafe[1] += 1
			elif symbol == key.SPACE:
				if self.dy == 0:
					self.dy = JUMP_SPEED
			elif symbol == key.ESCAPE:
				self.set_exclusive_mouse(False)
			elif symbol == key.TAB and self.edit_mode==1:
				self.flying = not self.flying
			elif symbol in self.num_keys:
				index = (symbol - self.num_keys[0]) % len(self.inventory)
				self.block = self.inventory[index]
				self.placing_block=index
			elif symbol in self.function_keys:
				number_of_blocks=int(symbol)-65469
				self.multi_block_pile=number_of_blocks

	def on_key_release(self, symbol, modifiers):
		""" Called when the player releases a key. See pyglet docs for key
		mappings.
		Parameters
		----------
		symbol : int
			Number representing the key that was pressed.
		modifiers : int
			Number representing any modifying keys that were pressed.
		"""
		if symbol == key.W:
			self.strafe[0] += 1
		elif symbol == key.S:
			self.strafe[0] -= 1
		elif symbol == key.A:
			self.strafe[1] += 1
		elif symbol == key.D:
			self.strafe[1] -= 1

	def on_resize(self, width, height):
		""" Called when the window is resized to a new `width` and `height`.
		"""
		# label
		self.label.y = height - 10
		# reticle
		if self.reticle:
			self.reticle.delete()
		x, y = self.width // 2, self.height // 2
		n = 10
		self.reticle = pyglet.graphics.vertex_list(4,
			('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
		)

	def set_2d(self):
		""" Configure OpenGL to draw in 2d.
		"""
		width, height = self.get_size()
		glDisable(GL_DEPTH_TEST)
		viewport = self.get_viewport_size()
		glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def set_3d(self):
		""" Configure OpenGL to draw in 3d.
		"""
		width, height = self.get_size()
		glEnable(GL_DEPTH_TEST)
		viewport = self.get_viewport_size()
		glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(65.0, width / float(height), 0.1, 60.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		x, y = self.rotation
		glRotatef(x, 0, 1, 0)
		glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
		x, y, z = self.position
		glTranslatef(-x, -y, -z)
	
	def set_person(self,person):
		""" Configure OpenGL to draw in 3d.
		"""
		glMatrixMode(GL_MODELVIEW)
		#glLoadIdentity()
		
		x, y, z = person.position
		#z-=2
		glTranslatef(x, y, z)
		
		x,y = person.rotation
		#x+=180
		glRotatef(-x, 0, 1, 0)
		
		#print(person.position)
	
	def position_torso(self,player):
		self.set_3d()
		self.set_person(player)
		"""draw torso"""
		x, y, z = player.torso_offset
		#print(x,y,z)
		glTranslatef(x, y, z)
		r = player.torso_twist
		glRotatef(-r, 0, 1, 0)
		self.model.players[int(player.num)].torso_batch.draw()
		
		
	
	def position_arms(self,player):
		global weapon_batch
		
		self.set_3d()
		self.set_person(player)
		r = player.torso_twist
		glRotatef(-r, 0, 1, 0)
		"""left arm"""
		#bicep
		x1, y1, z1 = player.l_bicep_offset
		glTranslatef(x1, y1, z1)
		r1 = player.l_shoulder
		glRotatef(-r1, 1, 0, 0)
		self.model.players[int(player.num)].l_bicep_batch.draw()
		#forearm
		r2 = player.l_elbow
		if r2>90:r2=90
		glRotatef(-r2, 1, 0, 0)
		x2, y2, z2 = player.l_forearm_offset
		z2-=r2*0.00125
		glTranslatef(x2, y2, z2)
		self.model.players[int(player.num)].l_forearm_batch.draw()
		
		
		"""reset"""
		self.set_3d()
		self.set_person(player)
		r = player.torso_twist
		glRotatef(-r, 0, 1, 0)
		
		"""right arm"""
		glRotatef(player.rotation[1], 1, 0, 0)
		#bicept
		x, y, z = player.r_bicep_offset
		glTranslatef(x, y, z)
		r1 = player.r_shoulder
		glRotatef(-r1, 1, 0, 0)
		self.model.players[int(player.num)].r_bicep_batch.draw()
		#forearm
		r2 = player.r_elbow
		if r2>90:r2=90
		glRotatef(-r2, 1, 0, 0)
		x, y, z = player.r_forearm_offset
		z-=r2*0.00125
		glTranslatef(x, y, z)
		#elbow offset to 90
		self.model.players[int(player.num)].r_forearm_batch.draw()
		"""SHOW WEAPON"""
		w=self.model.players[player.num].equip[self.model.players[player.num].out]
		hand=player.forearm_height/2
		glTranslatef(0,hand,0)
		glRotatef(-90,1,0,0)
		glRotatef(player.torso_twist,0,1,0)
		weapon_batch[w].draw()
		if player.trigger:
			self.model.players[player.num].gun_sound.play()
			x,y,z=self.bang_pos[w]
			glTranslatef(x,y,z)
			self.model.players[player.num].bang_batch.draw()
			#self.bullet_hit(player.position)
			#hit_test(self, position, vector, max_distance=8)
			#block=self.hit_test(self.position,self.get_sight_vector(self.position))[0]
			
			
	
		
	def position_legs(self,player):
		#print('position_legs')
		self.set_3d()
		self.set_person(player)
		"""left leg"""
		x,y,z = player.l_leg_offset
		glTranslatef(x/2,y/2,z/2)
		r = player.l_stepAngle
		glRotatef(-r, 1, 0, 0)
		glTranslatef(x/2,y/2,z/2)
		self.model.players[int(player.num)].l_leg_batch.draw()
		
		self.set_3d()
		self.set_person(player)
		"""right leg"""
		x,y,z = player.r_leg_offset
		glTranslatef(x/2,y/2,z/2)
		r = player.r_stepAngle
		glRotatef(-r, 1, 0, 0)
		glTranslatef(x/2,y/2,z/2)
		self.model.players[int(player.num)].l_leg_batch.draw()
		
	
	def unpack(self,player):
		if type(player.position) is str:
			pos=player.position.replace('(','').replace(')','')
			pos=pos.split(',')
			player.position=(float(pos[0]),float(pos[1]),float(pos[2]))
		if type(player.rotation) is str:
			rot=player.rotation.replace('(','').replace(')','')
			rot=rot.split(',')
			player.rotation=(float(rot[0]),float(rot[1]))
		#torso
		player.torso_width=float(player.torso_width)
		player.torso_height=float(player.torso_height)
		player.torso_twist=float(player.torso_twist)
		if type(player.torso_img) is str:
			player.torso_img=player.torso_img.replace('[','').replace(']','')
			list=player.torso_img.split(',')
			player.torso_img=[]
			for x in player.torso_img:
				player.torso_img.append(float(x))
		if type(player.torso_offset) is str:
			player.torso_offset=player.torso_offset.replace('(','').replace(')','')
			list=player.torso_offset.split(',')
			player.torso_offset=(float(list[0]),float(list[1]),float(list[2]))
		#arms
		if type(player.l_bicep_offset) is str:
			player.l_bicep_offset=player.l_bicep_offset.replace('(','').replace(')','')
			list=player.l_bicep_offset.split(',')
			player.l_bicep_offset=(float(list[0]),float(list[1]),float(list[2]))
		if type(player.r_bicep_offset) is str:
			player.r_bicep_offset=player.r_bicep_offset.replace('(','').replace(')','')
			list=player.r_bicep_offset.split(',')
			player.r_bicep_offset=(float(list[0]),float(list[1]),float(list[2]))
		player.l_elbow=float(player.l_elbow)
		player.bicep_width=float(player.bicep_width)
		player.bicep_height=float(player.bicep_height)
		player.forearm_height=float(player.forearm_height)
		player.forearm_width=float(player.forearm_width)
		player.r_elbow=float(player.r_elbow)
		player.l_shoulder=float(player.l_shoulder)
		player.r_shoulder=float(player.r_shoulder)
		if type(player.l_forearm_offset) is str:
			player.l_forearm_offset=player.l_forearm_offset.replace('(','').replace(')','')
			list=player.l_forearm_offset.split(',')
			player.l_forearm_offset=(float(list[0]),float(list[1]),float(list[2]))
		if type(player.r_forearm_offset) is str:
			player.r_forearm_offset=player.r_forearm_offset.replace('(','').replace(')','')
			list=player.r_forearm_offset.split(',')
			player.r_forearm_offset=(float(list[0]),float(list[1]),float(list[2]))
		if type(player.bicep_img) is str:
			player.bicep_img=player.bicep_img.replace('[','').replace(']','')
			list=player.bicep_img.split(',')
			player.bicep_img=[]
			for x in list:
				player.bicep_img.append(float(x))
		if type(player.forearm_img) is str:
			player.forearm_img=player.forearm_img.replace('[','').replace(']','')
			list=player.forearm_img.split(',')
			player.forearm_img=[]
			for x in list:
				player.forearm_img.append(float(x))
		#legs
		if type(player.l_leg_offset) is str:
			player.l_leg_offset=player.l_leg_offset.replace('(','').replace(')','')
			list=player.l_leg_offset.split(',')
			player.l_leg_offset=(float(list[0]),float(list[1]),float(list[2]))
		if type(player.r_leg_offset) is str:
			player.r_leg_offset=player.r_leg_offset.replace('(','').replace(')','')
			list=player.r_leg_offset.split(',')
			player.r_leg_offset=(float(list[0]),float(list[1]),float(list[2]))
		player.l_stepAngle=float(player.l_stepAngle)
		player.r_stepAngle=float(player.r_stepAngle)
		player.leg_width=float(player.leg_width)
		player.leg_height=float(player.leg_height)
			
	
	def on_draw(self):
		""" Called by pyglet to draw the canvas.
		"""
		self.clear()
		self.set_3d()
		glColor3d(1, 1, 1)
		self.model.batch.draw()
		
		for num in game.players:
			person=game.players[num]
			self.set_3d()
			self.unpack(person)
			
			try: 
				self.model.players[int(person.num)]
			except:
				print('player',person.num,'added')
				self.model.add_player(person)
			try:
				if person.num!=self.local_player and person.hp>0:
					self.set_person(person)
					x,y=person.rotation
					glRotatef(y, 1, 0, 0)
					self.model.players[int(person.num)].head_batch.draw()
					self.position_torso(person)
					#self.position_arms(person)
					self.position_legs(person)
				if person.hp>0:
					self.position_arms(person)
				if person.animate_hit==True:
					if person.num==self.local_player:
						self.hit=True
					
				
					
			except:
				pass
		
		self.set_3d()
		if self.edit_mode==1:
			self.draw_focused_block()
		self.set_2d()
		if self.edit_mode==1:
			self.draw_label()
		else:
			self.draw_hud()
			pass
		self.draw_reticle()
		if self.hp<1 and self.respawn==0:
			self.die()
		if self.hit==True:
			self.been_hit()
		#elif game.players[self.local_player].hit_animation==True:
		#	self.die()
		if self.respawn=='x':
			print('self.respawn',self.respawn)
			self.get_back_in_the_game()
	
	def get_back_in_the_game(self):
		print('get_back_in_the_game()')
		self.respawn=0
		self.born+=1
		player_poses=[]
		rand=random.randint(0,len(game.spawn_points)-1)
		goTo=game.spawn_points[rand]
		#print('random respawn to start with:',goTo)
		for num in game.players:
			player=game.players[num]
			#print(player)
			if player.hp>0:
				player_poses.append(player.position)
		for pos in player_poses:
			x,y,z=pos
			for spawn in game.spawn_points:
				point=spawn[0]
				px,py,pz=point
				if abs(abs(x)-abs(px))>5:
					if abs(abs(z)-abs(pz))>5:
						goTo=spawn
		#print(goTo)
		self.position=goTo[0]
		self.rotation=goTo[1]
	def been_hit(self):
		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
		h,w,c,drop=self.blood_overlay
		r,g,b,a=c
		glColor4d(r,g,b,a)
		glRectf(0,0,w,h)
		self.hit=False
		
	
	def die(self):
		#height		width   color   drop
		#0			1		2		3
		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
		h,w,c,drop=self.blood_overlay
		r,g,b,a=c
		glColor4d(r,g,b,a)
		glRectf(0,h+drop,w,h)
		drop-=7
		if h+drop<1:
			drop=0
			self.respawn='x'
			print('run player',self.local_player,'respawn')
		self.blood_overlay=(h,w,c,drop)
		
		
	def draw_focused_block(self):
		""" Draw black edges around the block that is currently under the
		crosshairs.
		"""
		vector = self.get_sight_vector()
		block = self.model.hit_test(self.position, vector)[0]
		if block:
			try:x, y, z = block
			except:
				block=game.players[block].position
				x,y,z=block
			vertex_data = cube_vertices(x, y, z, 0.51)
			glColor3d(0, 0, 0)
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
			pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

	def draw_label(self):
		""" Draw the label in the top left of the screen.
		"""
		print('draw_label()')
		x, y, z = self.position
		rx, ry = self.rotation
		self.label.text = '%02d (%.2f, %.2f, %.2f) (%d,  %d)' % (
			pyglet.clock.get_fps(), x, y, z, rx, ry)
		self.label.draw()
		self.saveButton.draw()
		#show status of the settings being used in edit mode
		self.settings.text = str(self.multi_block_pile)+' '+self.block_names[self.placing_block]
		self.settings.draw()
		
	def draw_hud(self):
		"""draw player game info to the heads-up-display"""
		#print('draw_hud')
		guy=game.players[self.local_player]
		hp_perc=guy.hp/100
		x,y,w,h,r,g,b=self.healthbar_container
		glColor3d(r,g,b)
		glRectf(x,y,x+w,y+h)
		x,y,w,h,r,g,b=self.healthbar
		glColor3d(r,g,b)
		glRectf(x,y,(x+w)*hp_perc,y+h)
		self.score.text='SCORE: '+str(guy.score)
		self.score.draw()

	def draw_reticle(self):
		""" Draw the crosshairs in the center of the screen.
		"""
		glColor3d(0, 0, 0)
		self.reticle.draw(GL_LINES)


def setup_fog():
	""" Configure the OpenGL fog properties.
	"""
	# Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
	# post-texturing color."
	glEnable(GL_FOG)
	# Set the fog color.
	glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
	# Say we have no preference between rendering speed and quality.
	glHint(GL_FOG_HINT, GL_DONT_CARE)
	# Specify the equation used to compute the blending factor.
	glFogi(GL_FOG_MODE, GL_LINEAR)
	# How close and far away fog starts and ends. The closer the start and end,
	# the denser the fog in the fog range.
	glFogf(GL_FOG_START, 20.0)
	glFogf(GL_FOG_END, 60.0)


def setup():
	""" Basic OpenGL configuration.
	"""
	# Set the color of "clear", i.e. the sky, in rgba.
	glClearColor(0.5, 0.69, 1.0, 1)
	# Enable culling (not rendering) of back-facing facets -- facets that aren't
	# visible to you.
	glEnable(GL_CULL_FACE)
	# Set the texture minification/magnification function to GL_NEAREST (nearest
	# in Manhattan distance) to the specified texture coordinates. GL_NEAREST
	# "is generally faster than GL_LINEAR, but it can produce textured images
	# with sharper edges because the transition between texture elements is not
	# as smooth."
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	setup_fog()

def startup_a_server():
	"""
	IF THE PLAYER OPTS TO CREATE THEIR OWN SERVER @ THE LOCAL MACHINE
	ALL THEY HAVE TO DO IS SPECIFY THE PORT, OR IT WILL BE SET TO 5555
	
	localServe.create_a_server( specify a port )
	"""
	localServe.create_a_server()

retry_to_connect=False
def main(GAME_START,resetNetwork=['0',0]):
	global retry_to_connect
	global game
	user_network_reset_check=''
	if GAME_START==True:
		print('joined game #',game.id)
		window = Window(width=800, height=600, caption='3dtest', resizable=True)
		# Hide the mouse cursor and prevent the mouse from leaving the window.
		window.set_exclusive_mouse(True)
		setup()
		pyglet.app.run()
	
	else:
		user_network_reset_check=startupClient(running,ip_variable,port_variable,resetNetwork,retry_to_connect)
	if type(user_network_reset_check)==list:
		#print(user_network_reset_check)
		retry_to_connect=True
		check_network(running,user_network_reset_check[0],user_network_reset_check[1])
	elif user_network_reset_check=='serve':
		startup_a_server()

		
ip_variable="10.0.0.59"
port_variable=5555

running=True

net= ''
game = ''

def check_network(running,ip_variable,port_variable):
	global net
	global game
	net = Network(ip_variable,port_variable)
	resetNetwork=[ip_variable,port_variable]
	if running:
		"""check to make sure the saved ip and port find an active server on the local network"""
		GAME_START=True
		connected=net.p
		if connected==None:
			print("COULDN'T GET P (net.p()) :: NO NETWORK ESTABLISHED \n NO PLAYER NUMBER GIVEN")
			GAME_START=False
		else:
			#print('connected to server :: given number:',int(connected)-1)
			try:
				game=net.send('get')
				
			except:
				print("couln't get <game>")
				GAME_START=False
		main(GAME_START,resetNetwork)

check_network(running,ip_variable,port_variable)
	
