import socket
import subprocess
from threading import *

def call():
	subprocess.call(["python", "3dtest.py"])

def create_a_server(port=5555):
	#get local ip
	local_ip=socket.gethostbyname(socket.gethostname())
	print('PLAYER OPTED TO CREATE THEIR OWN SERVER @ THEIR LOCATION:')
	print(local_ip)
	print('USING PORT:',port)
	
	restart=Timer(1,call)
	restart.start()
	subprocess.call(["python", "server.py"])
	pass
	