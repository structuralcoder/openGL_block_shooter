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
		self.score=0
		self.born=0
		
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
		#
		self.animate_hit=False
		self.equip=[]
		self.out=0
		
		

BULLET_ID=0			
class Bullet:
	def __init__(self,data):
		global BULLET_ID
		BULLET_ID+=1
		self.id=BULLET_ID
		info=data.split('*')
		self.owner=int(info[0].replace('player:',''))
		self.gun=info[1].replace('gun:','')
		replace=info[2].replace('position:','').replace('(','').replace(')','')
		split=replace.split(',')
		print('position',split)
		self.origin=(float(split[0]),float(split[1]),float(split[2]))
		replace=info[4].replace('rotation:','').replace('(','').replace(')','')
		split=replace.split(',')
		print('rotation',split)
		self.rotation=(float(split[0]),float(split[1]))
		#----
		replace=info[3].replace('vector:','').replace('(','').replace(')','')
		split=replace.split(',')
		self.vector=(float(split[0]),float(split[1]),float(split[2]))
		self.position=self.origin
		#----
	
	def go(self):
		x,y,z=self.position
		dx,dy,dz=self.vector
		self.position=(x+dx,y+dy,z+dz)

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
		self.players={}
		self.bullets=[]
		
		self.spawn_points=startArray
		self.spawn_points.append([(-17,0,-20),(90,0)])
		self.spawn_points.append([(-7,0,-2),(-90,0)])
		self.spawn_points.append([(11,0,-4),(0,0)])
		self.spawn_points.append([(15,0,-14),(-90,0)])
		self.spawn_points.append([(8,0,-34),(0,0)])
		self.spawn_points.append([(-11,0,-36),(90,0)])
		
		self.add_player(id)
		
		
	def add_player(self,num):
		self.players[num]=Player(num)
		#print(self.players[num])
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
			self.players[num].animate_hit=data[34]
			#check if fire
			if data[31]!='x':
				#print(data[31])
				self.players[num].trigger=True
				if data[31].find('(')==-1:
					int_it=data[31].replace('[','').replace(']','')
					int_it=int_it.split(',')
					try: 
						if int_it[0]=='None':
							pass
						else:
							check=0
							n=int(int_it[0]);#print(n)
							check=1
							if self.players[n].hp>0:
								check=2
								dam=int(int_it[1]);#print(dam)
								check+=1
								print('player',n,'hp is @',self.players[n].hp)
								print('player',n,'takes',dam,'points of damage')
								self.players[n].hp-=dam
								self.players[n].animate_hit=True
								
								
								if self.players[n].hp<1:
									self.players[num].score+=1
								print('player',n,'hp is @',self.players[n].hp)
					except:
						printStr=''
						if check>0:
							printStr='player'+str(n)+'passed @ line 200 game.py\n'
						if check>1:
							printStr=printStr+'enemy player hp > 0\n'
						if check>2:
							printStr=printStr+'damage converted to int'
						
						
						if check==0:
							printStr='error with the player number:: '+str(data[31])
						print(printStr)
						print('couldnt pass damage!!')
					#self.bullets.append(Bullet(data[31]))
			else:
				self.players[num].trigger=False
			#self.players[num].hp=int(data[33])
			if int(data[33])>self.players[num].born:
				self.players[num].born+=1
				self.players[num].hp=100
				self.players[num].score-=1
			
			equip=data[35].replace('[','').replace(']','').replace("'",'')
			equip=equip.split(', ')
			self.players[num].equip=equip
			self.players[num].out=int(data[36])
			
			
		except: print('couldnt change player',num,'data: len of data:',len(data),'/37')
		
		try:
			#new bullet
			if data[32]!='x':
				print('add bullet')
				self.bullets.append(Bullet(data[32]))
		except:
			print('couldnt make [',data[32],'] work @ data[32]')
		
		for bullet in self.bullets:
			bullet.go()
		
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
