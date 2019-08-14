import socket
from _thread import *
import pickle
from game import Game

server = "10.0.0.59"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
	global idCount
	conn.send(str.encode(str(p)))
	
	reply = ""
	while True:
		try:
			data = conn.recv(4096).decode()
			#print(data)
			if gameId in games:
				game = games[gameId]
			#
				if not data:
					break
				else:
					conn.sendall(pickle.dumps(game))
					if data == "reset":
						game.resetWent()
					elif data != "get":
						game.update(p, data)
					for bullet in game.bullets:
						x,y,z=bullet.position
						dx,dy,dz=bullet.vector
						dx=dx/2
						dy=dy/2
						dz=dz/2
						bullet.position=(x+dx,y+dy,z+dz)
						
						x,y,z=bullet.position
						if y<=-2 or y>10 or abs(x)>100 or abs(z)>100:
							game.bullets.remove(bullet)
							#print('bullet removed')
					
				
				
		except:
			print('server.py didnt get data')
			break

	print("Lost connection")
	try:
		del games[gameId]
		print("Closing Game", gameId)
	except:
		pass
	idCount -= 1
	conn.close()

running=True
gameId=1
while running:
	conn, addr = s.accept()
	print("Connected to:", addr)

	idCount += 1
	p = 0
	gameId = (idCount - 1)//2
	if idCount % 2 == 1:
		games[gameId] = Game(gameId)
		print("Creating a new game...")
	else:
		p = 1
		games[gameId].add_player(p)

	start_new_thread(threaded_client, (conn, p, gameId))