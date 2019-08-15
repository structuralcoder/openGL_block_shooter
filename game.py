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
STONE = tex_coords((2, 1), (2, 1), (2, 1))

startArray=[
#0
[(0,0,0),(0,0)],
[(0,0,-40),(180,0)],
[(17,3,-13),(-90,0)],
[(-21,3,-12),(0,0)]
]
class Player:
	def __init__(self,num):
		self.num=num
		playerStart=startArray[self.num]
		self.position=playerStart[0]
		self.rotation=playerStart[1]
		#----
		self.hp=100
		self.trigger=False
		
		#--BUILD PLAYER:
		self.head_size=0.2
		self.head_img= (3,1), (3,1), (0,2), (3,1)
		self.head_rotate=90
		#torso
		self.torso_width=0.2
		self.torso_height=0.2
		self.torso_img= BLACK
		self.torso_offset= (0, -0.45, 0)
		self.torso_twist= 20
		#biceps
		self.bicep_width=0.1
		self.bicep_height=0.125
		self.bicep_img= BLACK
		self.l_bicep_offset=(-.3, -0.35, 0)
		self.l_shoulder=10
		self.r_bicep_offset=(.3, -0.35, 0)
		self.r_shoulder=0
		#forearms
		self.forearm_width=0.08
		self.forearm_height=0.1
		self.forearm_img= STONE
		self.l_forearm_offset= (0, -0.2, 0)
		self.l_elbow=45
		self.r_forearm_offset= (0, -0.2, 0)
		self.r_elbow=90
		#
		self.leg_width=0.1
		self.leg_height=0.3
		self.leg_img= BLACK
		self.l_leg_offset=(-.125, -1, 0)
		self.l_stepAngle=0
		self.r_leg_offset=(.125, -1, 0)
		self.r_stepAngle=0	
		
		
		
class Bullet:
	def __init__(self,data):
		global BULLET_ID
		BULLET_ID+=1
		self.id=BULLET_ID
		info=data.split(':')
		replace=info[0].replace('(','').replace(')','')
		split=replace.split(',')
		self.origin=(float(split[0]),float(split[1]),float(split[2]))
		#----
		replace=info[1].replace('(','').replace(')','')
		split=replace.split(',')
		self.vector=(float(split[0]),float(split[1]),float(split[2]))
		self.position=self.origin
		self.batch=''
		#----
		self.owner=int(info[2])
		self.damage=int(info[3])
	
	def go(self):
		x,y,z=self.position
		dx,dy,dz=self.vector
		self.position=(x+dx,y+dy,z+dz)

BULLET_ID=0	
class Game:
	def __init__(self, id):
		#self.p1Went = False
		#self.p2Went = False
		self.ready = False
		self.id = id
		self.player_count = 1
		#self.moves = [None, None]
		self.wins = [0,0]
		#self.ties = 0
		self.players=[]
		self.bullets=[]
		
		self.add_player(id)
		
	def add_player(self,num):	
		self.players.append(Player(num))
		print('player added:')
		print(len(self.players),'players on server')
		self.player_count+=1
		

	#def get_player_move(self, p):
	#    """
	#    :param p: [0,1]
	#    :return: Move
	#    """
	#    return self.moves[p]
	#
	def update(self,num,data):
		
		data=data.split('/')
		try:
			self.players[num].position=data[0]
			self.players[num].rotation=data[1]
			#----
			
			#--BUILD PLAYER:
			self.players[num].head_size=data[2]
			self.players[num].head_img=data[3]
			self.players[num].head_rotate=data[4]
			#torso
			self.players[num].torso_width=data[5]
			self.players[num].torso_height=data[6]
			self.players[num].torso_img= data[7]
			self.players[num].torso_offset= data[8]
			self.players[num].torso_twist= data[9]
			#biceps
			self.players[num].bicep_width= data[10]
			self.players[num].bicep_height=data[11]
			self.players[num].bicep_img= data[12]
			self.players[num].l_bicep_offset=data[13]
			self.players[num].l_shoulder=data[14]
			self.players[num].r_bicep_offset=data[15]
			self.players[num].r_shoulder=data[16]
			#forearms
			self.players[num].forearm_width=data[17]
			self.players[num].forearm_height=data[18]
			self.players[num].forearm_img= data[19]
			self.players[num].l_forearm_offset= data[20]
			self.players[num].l_elbow=data[21]
			self.players[num].r_forearm_offset= data[22]
			self.players[num].r_elbow=data[23]
			#
			self.players[num].leg_width=data[24]
			self.players[num].leg_height=data[25]
			self.players[num].leg_img= data[26]
			self.players[num].l_leg_offset=data[27]
			self.players[num].l_stepAngle=data[28]
			self.players[num].r_leg_offset=data[29]
			self.players[num].r_stepAngle=data[30]
			#check if fire
			if data[31]!='x':
				#print(data[31])
				self.players[num].trigger=True
				self.bullets.append(Bullet(data[31]))
			else:
				self.players[num].trigger=False
			self.players[num].hp=int(data[33])
				
			
		except: print('couldnt change player',num,'data: len of data:',len(data),'/34')
		
		try:
			if data[32]!='x':
				#print(data[32])
				#print(type(data[32]))
				for bullet in self.bullets:
					if bullet.id == int(data[32]):
						self.bullets.remove(bullet)
						#print('bullet',bullet.id,'removed')
		except:
			print('couldnt make [',data[32],'] work @ data[32]')
		
	def connected(self):
		return self.ready
	
	def givehp(num,data):
		data=data.split(':')
		self.players[num].hp=int(data[1])
		
	#
	#def bothWent(self):
	#    return self.p1Went and self.p2Went
	#
	#def winner(self):
	#
	#    p1 = self.moves[0].upper()[0]
	#    p2 = self.moves[1].upper()[0]
	#
	#    winner = -1
	#    if p1 == "R" and p2 == "S":
	#        winner = 0
	#    elif p1 == "S" and p2 == "R":
	#        winner = 1
	#    elif p1 == "P" and p2 == "R":
	#        winner = 0
	#    elif p1 == "R" and p2 == "P":
	#        winner = 1
	#    elif p1 == "S" and p2 == "P":
	#        winner = 0
	#    elif p1 == "P" and p2 == "S":
	#        winner = 1
	#
	#    return winner
	#
	#def resetWent(self):
	#    self.p1Went = False
	#    self.p2Went = False
