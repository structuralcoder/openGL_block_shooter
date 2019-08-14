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



class pistol:
	def __init__(self):
		self.auto=False
		self.damage=30
		#color then vertices
		self.blocks=[SILVER,custom_vertices(0,0.13,-.30,.05,.05,.18),
			SILVER,custom_vertices(0,0.05,-.15,.04,.1,.02)
		]
		self.sound=pygame.mixer.Sound('sounds/380_gunshot.wav')
	
		
		
		
		