import pygame

class ClientVariables:
	def __init__(self,ip,port):
		self.winSize=(0,0)
	
		self.inputBoxX=0
		self.inputBoxW=0
		self.inputBoxY=0
		self.inputBoxH=0
		
		self.ip=ip
		self.ip_color=(255, 255, 255)
		self.port=port
		self.port_color=(255, 255, 255)
		
		self.input=False
		
		self.submit=False
		self.submitPos=(0,0)
		self.submitSize=(100,100)
		self.submit_color=(0,255,200)
		
		self.create=False
		self.createPos=(0,0)
		self.createSize=(100,100)
		self.create_color=(0,255,0)
		
		self.return_variables=[]
		self.retry_to_connect=False


def display_startup_info(screen,clientVariables):
	if clientVariables.submit==False:
		#establish text 
		clientStartFont=pygame.font.SysFont('Arial', 30)
		clientSubmitFont=pygame.font.SysFont('Arial', 100)
		title=clientStartFont.render('NO SERVER FOUND WITH THE SAVED DATA', False, (255, 255, 255))
		ip=clientStartFont.render('IP : ', False, (55, 240, 250))
		port=clientStartFont.render('PORT: ', False, (55, 240, 250))
		ip_v=clientStartFont.render(clientVariables.ip, False, clientVariables.ip_color)
		port_v=clientStartFont.render(str(clientVariables.port), False, clientVariables.port_color)
		submit_button_text=clientSubmitFont.render('SEARCH', False, clientVariables.submit_color)
		create_button_text=clientSubmitFont.render('NEW', False, clientVariables.create_color)
		
		#reset screen
		screen.fill((0,0,0))
		
		#print title text
		winSize=clientVariables.winSize
		getTitleHalfW=title.get_width()/2
		getScreenHalfW=winSize[0]/2
		getTitleOffset=getScreenHalfW-getTitleHalfW
		screen.blit(title,(getTitleOffset,10))
		
		#draw input boxes
		inputBoxX=clientVariables.inputBoxX=winSize[0]/6
		inputBoxW=clientVariables.inputBoxW=winSize[0]/4
		inputBoxY=clientVariables.inputBoxY=winSize[1]/4
		inputBoxH=clientVariables.inputBoxH=winSize[1]/6
		
		ipW=ip.get_width()
		portW=port.get_width()
		
		pygame.draw.rect(screen,(82,82,82),(inputBoxX,inputBoxY,inputBoxW,inputBoxH))
		iptextX=inputBoxX-ipW#
		inputTextCentered=inputBoxY+((inputBoxH/2)-(ip.get_height()/2))
		screen.blit(ip,(iptextX,inputTextCentered))
		pygame.draw.rect(screen,(82,82,82),(inputBoxX*3.5,inputBoxY,inputBoxW,inputBoxH))
		porttextX=(inputBoxX*3.5)-portW
		screen.blit(port,(porttextX,inputTextCentered))
		
		#print current ip and port to the input boxes
		screen.blit(ip_v,(inputBoxX+10,inputTextCentered))
		screen.blit(port_v,((inputBoxX*3.5)+10,inputTextCentered))
		
		#print submit button
		submitW=submit_button_text.get_width()
		submitH=submit_button_text.get_height()
		clientVariables.submitSize=(submitW,submitH)
		getHalfSubmitSizeW=submitW/2
		getHalfSubmitSizeH=submitH/2
		submitX=getScreenHalfW-getHalfSubmitSizeW
		submitY=winSize[1]*.45
		x,y=clientVariables.submitPos=(submitX,submitY)
		screen.blit(submit_button_text,(x,y))
		
		#print "create new server" button
		createW=create_button_text.get_width()
		createH=create_button_text.get_height()
		clientVariables.createSize=(createW,createH)
		getHalfCreateSizeW=createW/2
		getHalfCreateSizeH=createH/2
		createX=getScreenHalfW-getHalfCreateSizeW
		createY=winSize[1]*.65
		x,y=clientVariables.createPos=(createX,createY)
		screen.blit(create_button_text,(x,y))
		
	else:
		#establish text 
		clientStartFont=pygame.font.SysFont('Arial', 30)
		clientSubmitFont=pygame.font.SysFont('Arial', 100)
		title=clientStartFont.render('SUBMITTING CHANGES', False, (255, 255, 255))
		ip=clientStartFont.render('IP : ', False, (55, 240, 250))
		port=clientStartFont.render('PORT: ', False, (55, 240, 250))
		ip_v=clientStartFont.render(clientVariables.ip, False, clientVariables.ip_color)
		port_v=clientStartFont.render(str(clientVariables.port), False, clientVariables.port_color)
		submit_button_text=clientSubmitFont.render('SUBMIT', False, clientVariables.submit_color)
		
		#reset screen
		screen.fill((0,0,0))
		
		#print title text
		winSize=clientVariables.winSize
		getTitleHalfW=title.get_width()/2
		getScreenHalfW=winSize[0]/2
		getTitleOffset=getScreenHalfW-getTitleHalfW
		screen.blit(title,(getTitleOffset,10))
		
		#draw input boxes
		inputBoxX=clientVariables.inputBoxX=winSize[0]/6
		inputBoxW=clientVariables.inputBoxW=winSize[0]/4
		inputBoxY=clientVariables.inputBoxY=winSize[1]/3
		inputBoxH=clientVariables.inputBoxH=winSize[1]/4
		
		ipW=ip.get_width()
		portW=port.get_width()
		
		pygame.draw.rect(screen,(82,82,82),(inputBoxX,inputBoxY,inputBoxW,inputBoxH))
		iptextX=inputBoxX-ipW#
		inputTextCentered=inputBoxY+((inputBoxH/2)-(ip.get_height()/2))
		screen.blit(ip,(iptextX,inputTextCentered))
		pygame.draw.rect(screen,(82,82,82),(inputBoxX*3.5,inputBoxY,inputBoxW,inputBoxH))
		porttextX=(inputBoxX*3.5)-portW
		screen.blit(port,(porttextX,inputTextCentered))
		
		#print current ip and port to the input boxes
		screen.blit(ip_v,(inputBoxX+10,inputTextCentered))
		screen.blit(port_v,((inputBoxX*3.5)+10,inputTextCentered))
	
	#if the user already tryed to reconnect via this window
	if clientVariables.retry_to_connect:
		RETRY=clientStartFont.render('COULDNT MAKE A CONNECTION TO THE SERVER', False, (255, 0, 0))
		getRETRYoffset=getScreenHalfW-(RETRY.get_width()/2)
		screen.blit(RETRY,(getRETRYoffset,20+title.get_height()))
	
	#final output to client window
	pygame.display.update()



"""
FUNTIONS FOR CHANGING THE IP AND PORT VARIABLES VIA THE TWO ON SCREEN INPUTS:
"""

def ip_box_selected(clientVariables):
	#print('ip box selected')
	clientVariables.ip_color=(0,255,0)
	clientVariables.port_color=(255,255,255)
	clientVariables.input='ip'

def port_box_selected(clientVariables):
	#print('port box selected')
	clientVariables.ip_color=(255,255,255)
	clientVariables.port_color=(0,255,0)
	clientVariables.input='port'

"""
-----------------------------------------------------------------------------------
"""

def try_submit(vars):
	#print('try_submit()')
	error=""
	ip=vars.ip.split('.')
	port=int(vars.port)
	if len(ip)<4:
		error='ERROR:: not enough "." to make a proper ip address \n'
	ii=0
	for i in ip:
		ii+=1
		interable='th'
		if ii==1:
			interable='st'
		if ii==2:
			interable='nd'
		if ii==3:
			interable='rd'
		if len(i)>3:
			error=error+'ERROR:: The '+str(ii)+interable+' position of your ip address has too many numbers ('+str(i)+') \n'
		if int(i)>255:
			error=error+'ERROR:: The '+str(ii)+interable+' position of your ip address cannot be greater than 255 ('+str(i)+')\n'
	
	if port<1024:
		error=error+"ERROR:: your port cant be less than 1024 \n"
	
	
	"""
	RETURN RESULTS
	"""
	
	
	if error!="":
		return error
	else:
		return 'goo'


def startupClient(runrun,ip,port,resetNetwork,retry_to_connect):
	clientVariables=ClientVariables(ip,port)
	clientVariables.return_variables=resetNetwork
	clientVariables.retry_to_connect=retry_to_connect
	game_name="3dtest"
	version='1.0'
	print(game_name,"startup client initiated")
	#######################################
	#PRODUCE A SCREEN
	infoObject = pygame.display.Info()
	winSize=(infoObject.current_w, infoObject.current_h)
	winSize=clientVariables.winSize = (800, 650)
	StartupClientWindow = pygame.display.set_mode(winSize)
	pygame.display.set_caption(game_name+' startup client')
	hertz=0
	while runrun:
		hertz+=1
		#print(runrun)
		for event in pygame.event.get():
			
			if event.type==12:
				runrun=False
				print("GAME QUIT")
				pygame.display.quit()
				pygame.quit()
			if event.type==2:
				if event.key==27:
					#ESC
					runrun=False
					print("GAME QUIT")
					pygame.display.quit()
					pygame.quit()
				if clientVariables.input!=False:
					key_pressed=pygame.key.name(event.key).replace('[','').replace(']','')
					try: 
						int(key_pressed)
						if clientVariables.input=='ip':
							if len(clientVariables.ip)<15:
								clientVariables.ip=clientVariables.ip+key_pressed
						
						if clientVariables.input=='port':
							newport=str(clientVariables.port)+key_pressed
							newport=int(newport)
							#ports between 1024–49151
							if newport<49152:
								clientVariables.port=newport
							else:
								print('port too large')
					except:
						if key_pressed=='backspace':
							if clientVariables.input=='ip':
								clientVariables.ip=clientVariables.ip[0:-1]
							if clientVariables.input=='port':
								clientVariables.port=str(clientVariables.port)
								clientVariables.port=clientVariables.port[0:-1]
								if len(clientVariables.port)==0:
									clientVariables.port=''
								else:int(clientVariables.port)
						if key_pressed=='.' and clientVariables.input=='ip':
							if len(clientVariables.ip)<12:
								#print(len(clientVariables.ip))
								clientVariables.ip=clientVariables.ip+key_pressed
							
						else:pass
			
			if event.type==6:
				x,y=event.pos
				if y>clientVariables.inputBoxY and y<(clientVariables.inputBoxY+clientVariables.inputBoxH) and clientVariables.submit==False:
					if x>clientVariables.inputBoxX and x<(clientVariables.inputBoxX+clientVariables.inputBoxW):
						ip_box_selected(clientVariables)
					elif x>(clientVariables.inputBoxX*3.5) and x<((clientVariables.inputBoxX*3.5)+clientVariables.inputBoxW):
						port_box_selected(clientVariables)
					else:
						clientVariables.input=False
						clientVariables.ip_color=(255, 255, 255)
						clientVariables.port_color=(255, 255, 255)
				else:
					clientVariables.input=False
					clientVariables.ip_color=(255, 255, 255)
					clientVariables.port_color=(255, 255, 255)
				
				if y>clientVariables.submitPos[1] and y<(clientVariables.submitPos[1]+clientVariables.submitSize[1]):
					if x>clientVariables.submitPos[0] and x<(clientVariables.submitSize[0]+clientVariables.submitPos[0]):
						try:
							#print('here')
							submission=try_submit(clientVariables)
						except:
							print('you hit "SUBMIT", but something went wrong...')
							print('NO ERROR WAS RETURNED FROM YOUR CUSTOM FUNCTION')
						else:
							if submission[0:5]=='ERROR':
								print(submission)
							elif submission=='goo':
								print('returned a proper ip and port:')
								clientVariables.submit=True
								clientVariables.return_variables=[str(clientVariables.ip),int(clientVariables.port)]
								#runrun=False
								pygame.display.quit()
								return(clientVariables.return_variables)
								pygame.quit()
				if y>clientVariables.createPos[1] and y<(clientVariables.createPos[1]+clientVariables.createSize[1]):
					if x>clientVariables.createPos[0] and x<(clientVariables.createPos[0]+clientVariables.createSize[0]):
						pygame.display.quit()
						return 'serve'
						pygame.quit()
				
		if hertz==1000:
			hertz=0
			display_startup_info(StartupClientWindow,clientVariables)
		
	if runrun==False:
		pygame.display.quit()
		pygame.quit()

