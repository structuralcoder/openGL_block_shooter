import pygame

def custom_vertices(x,y,z,w=.2,h=.5,d=.05):
	return [
		x-w,y+h,z-d, x-w,y+h,z+d, x+w,y+h,z+d, x+w,y+h,z-d,  # top
		x-w,y-h,z-d, x+w,y-h,z-d, x+w,y-h,z+d, x-w,y-h,z+d,  # bottom
		x-w,y-h,z-d, x-w,y-h,z+d, x-w,y+h,z+d, x-w,y+h,z-d,  # left
		x+w,y-h,z+d, x+w,y-h,z-d, x+w,y+h,z-d, x+w,y+h,z+d,  # right
		x-w,y-h,z+d, x+w,y-h,z+d, x+w,y+h,z+d, x-w,y+h,z+d,  # front
		x+w,y-h,z-d, x-w,y-h,z-d, x-w,y+h,z-d, x+w,y+h,z-d,  # back
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

BLACK = tex_coords((3,1), (3,1), (3,1))
SILVER = tex_coords((1,2),(1,2),(1,2))
WOOD_PLANKS = tex_coords((3,0), (3,0), (3,0))
VADER_FACE = tex_coords((0,2), (0,2), (0,2))
BULLET=tex_coords((3,1), (3,1), (3,1))
BLUE=tex_coords((0,3), (0,3), (0,3))


"""----------------------------------------------------------------------------------------"""
class pistol:
	def __init__(self):
		self.auto=False
		self.damage=20
		self.distance=40
		#color then vertices
		self.blocks=[SILVER,custom_vertices(0,0.13,-.30,.05,.05,.18),
			SILVER,custom_vertices(0,0.05,-.15,.04,.1,.02)
		]
		self.sound=pygame.mixer.Sound('sounds/380_gunshot.wav')
		self.bang_pos=(0,.15,-.5)
		self.reticle_color=(0,255,100)
		self.reticle=[
			#xy bott  xy top
			(-20,-1.5,-5,1.5)
			,(5,-1.5,20,1.5)
		]
		self.recoil=0
		
		#pyglet.graphics.vertex_list(4,('v4i', (x - n, y, x + n, y, x, y - n, x, y + n)))
"""----------------------------------------------------------------------------------------"""
class assault_rifle:
	def __init__(self):
		self.auto=True
		self.damage=2
		self.distance=30
		#color then vertices
		self.blocks=[BLACK,custom_vertices(0,0.13,-.20,.05,.05,.2),
			BLACK,custom_vertices(0,0.05,-.15,.02,.1,.02),
			WOOD_PLANKS,custom_vertices(0,0.08,.1,.04,.05,.2),
			BLACK,custom_vertices(0,0.13,-.30,.02,.02,.3),
			BLACK,custom_vertices(0,0.13,-.6,.035,.035,.05),
			BLACK,custom_vertices(0,0,-.32,.03,.1,.04),
			BLACK,custom_vertices(0,.2,-.2,.03,.04,.06)
		]
		self.sound=pygame.mixer.Sound('sounds/rifle_sound.wav')
		self.bang_pos=(0,.15,-.8)
		self.reticle_color=(255,80,0)
		self.reticle=[
			#xy bott  xy top
			(-10,2,10,4)
			,(-10,-4,10,-2)
			,(-10,-4,-8,4)
			,(8,-4,10,4)
		]
		self.recoil=10
		
"""----------------------------------------------------------------------------------------"""	
class plasma_rifle:
	def __init__(self):
		self.auto=False
		self.damage=50
		self.distance=20
		#color then vertices
		self.blocks=[BLUE,custom_vertices(0,0.13,-.20,.05,.05,.2),
			SILVER,custom_vertices(0,0.05,-.15,.02,.1,.02),
			BLACK,custom_vertices(0,0.1,-.25,.08,.04,.2),
			SILVER,custom_vertices(0,0.12,-.43,.09,.08,.05),
			BLACK,custom_vertices(0,0.12,-.45,.07,.07,.05),
		]
		self.sound=pygame.mixer.Sound('sounds/plasma_rifle_sound.wav')
		self.bang_pos=(0,.15,-.8)
		self.recoil=80
	
		
		
		
