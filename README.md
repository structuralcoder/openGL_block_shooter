# openGL_block_shooter
### learning openGL and networking in the local area network for multiplayer connections to a server

---

### YOU'LL NEED PYTHON, PYGAME AND PYGLET TO RUN THIS CODE:
      GO TO THE "INSTALL-PYTHON/LIBS" FILE ON THIS REPOSITORY IF YOU DONT KNOW HOW

---

## THERE ARE 9 FILES AND 1 FOLDER YOU'LL NEED TO PUT INTO THE SAME DIR:

```
* sounds  (folder)
* 3dtest.py
* game.py
* guns.py
* localServe.py
* network.py
* server.py
* startupclient.py
* testlevel.txt
* texture.png
```

# WHAT THESE FILES DO

THE TEXTURE IMAGE IS FOR THE GEOMETRY SURFACES AND THE TESTLEVEL.TXT IS READ UPON THE GAME'S INITIATION.  A LIST OF BLOCK POSITIONS 
IN THE WORLD IS GIVEN AND DRAWN AS BRICKS TO CREATE THE TEST LEVEL.  

THE GUNS.PY FILE IS WERE ALL THE GUN INFO IS GOING TO BE HELD, RIGHT NOW, IT CONTAINS THE PISTOL, ASSAULT RIFLE AND PLASMA RIFLE

PLAYERS ARE NOW (V1.6 8-23-19) GIVEN THE OPTION TO START A NEW SERVER IF NONE CAN BE FOUND.  YOU CAN STILL START A SERVER INDEPENDANTLY
BY USING THE FOLLOWING:
        SERVER.PY CAN RUN ON A SEPERATE INSTANCE.  ON WINDOWS 10 I OPEN A POWERSHELL BY GOING TO THE DIR, CLICKING FILE AND
        OPENING A POWERSHELL FROM THE DIR LOCATION.  REMEMBER THAT WITH POWERSHELL, UNLIKE CMD, YOU'LL HAVE TO CALL PYTHON BEFORE THE FILENAME TO
        GET THE PROGRAM TO RUN.  
          -SERVER.PY WILL USE GAME.PY TO SET UP THE "GAME" CLASS USED TO PASS INFORMATION BETWEEN PLAYERS
HOWEVER, WHEN A NEW SERVER IS STARTED FROM THE POPUP WINDOW THE LOCAL IP IS TAKEN FROM THE COMPUTER AND THE PORT (ONLY) THAT WAS
SPECIFIED ON THE POPUP MENU (BY THE PLAYER) IS USED TO START UP A SERVER.  A NEW THREAD IS OPENED 1 SEC LATER AND THE GAME PROGRAM
RESTARTS.  IF THE SERVER CONNECTION POPUP STARTS AGAIN, BE SURE TO PLACE YOUR LOCAL IPv4 ADDRESS AND THE OPENED PORT INTO THE
SEARCH BOXES.

THE STARTUPCLIENT.PY FILE DEVELOPES THE SERVER CONNECTION POPUP IF NO IMMIDIATE CONNECTION IS MADE TO A RUNNING SERVER

THE LOCALSERVER.PY FILE DOES THE WORK OF CREATING A NEW THREAD AND TURNING ON THE NEW LOCAL SERVER WHEN THE PLAYER OPTS FOR ONE


3DTEST.PY IS THE CLIENT EACH PLAYER USES TO PLAY THE GAME.  THE BASE OF THIS PROGRAM WAS SUPPLIED USING github.com/fogleman/Minecraft.  
THANKS BE TO FOGLEMAN!!

3DTEST.PY WILL CREATE A "NET" OBJECT THROUGH THE NETWORK.PY FILE TO ESTABLISH A LINK TO THE SERVER

# WHAT YOU GET

---

### AS OF 8-23-2019:
  4 PLAYERS ARE ABLE TO CONNECT AND HAVE A GUN BATTLE. EACH PLAYER STARTS WITH A PISTOL AND PICKS UP A ASSAULT RIFLE OR PLASMA RIFLE. 
  WHEN ONE PLAYER REACHES <1 HP THEIR IMAGE NO LONGER APPEARS AND THE "DEAD" PLAYER IS NO LONGER ABLE TO SHOOT OR MOVE.  A 
  RESPAWN SCRIPT CYCLES THROUGH ALL THE AVAILABLE SPAWN POINTS AND SAVES THE LAST POSITION THAT IS AT LEAST 5 BLOCKS FROM ANY
  OTHER PLAYERS, WHO ARE AT THE SAME ELEVATION. ENEMY PLAYERS CAN BE CLOSER TO THE SPAWN POINT IF THEY ARE ABOVE OR BELOW.  WHEN
  KILLED, PLAYERS EXPERIENCE A "GOLDENEYE" DEATH ANIMATION.  THEY CAN STILL LOOK AROUND, BUT NO WALKING/SHOOTING AS A RED TRANSPARENT
  FILL BLOCK (BLOOD) DROPS OVER THEIR SCREEN.
  
  IF AN IMMIDIATE CONNECTION CAN BE MADE, THE PLAYER IS INSTANTLY TAKEN THERE. THE PLAYER HAS NO OPTIONS TO SEARCH OR START
  A NEW SERVER IF ONE ALREADY EXISTS.
  
  # CHORES
  
          LATEST FIXES (8-23-19): 
            1.SERVERS AND CLIENTS NO LONGER LOCK UP UPON PLAYER EXITS
            2.4 PLAYERS CAN NOW JOIN
            3.PLAYERS CAN SEARCH FOR GAMES IF THEY KNOW THE IP OR PORT
            4.PLAYERS CAN CREATE THEIR OWN SERVER INSTANCES, IF NONE CAN BE FOUND
            5.FIXED BUG WHERE SERVER.PY CRASHED IF GAME.PLAYERS CHANGED SIZE DURING ITERATION
            6.CHANGED GAME.PLAYERS FROM A LIST TO A DICT SO THAT ORIGINAL PLAYERS COULD LEAVE AND LATER PLAYERS COULD STAY IN GAME
            7.FIXED SERVER CLOSING WHEN NO MORE PLAYERS IN GAME
            8.CREATED RESPAWN LOGIC AND NEW SPAWN POINTS (OTHER THAN THE ORIGIN POINTS FOR THE 4 PLAYERS)
            9.LOCAL PLAYER HP AND HEALTH BAR SHOWN ABOVE
            10.WHEN KILLED, PLAYER EXPERIENCES "GOLDENEYE" RED OUT
            11.SCORES KEEPER ADDED.  PLAYERS GET ONE POINT PER KILL... LOOSE ONE POINT PER DEATH!
            12.FLIGHT TURNED OFF OUTSIDE OF EDIT_MODE
            13.BLOCK PLACEMENT RESERVED FOR EDIT_MODE
            14.FUCTION KEYS F1,F2,F3 ALLOW YOU TO PLACE 1,2 OR 3 BLOCKS STACKED ONTOP OF ONE ANOTHER
            15.BLOCK INVENTORY FOR EDIT MODE UPDATED, ALL BLOCK TYPES IN YOUR INVENTORY CAN BE SAVED TO THE TEST FILE, WHEN PLACED
            17.PLAYERS GET A RED FLASH ON THEIR SCREEN WHEN HIT BY OTHER PLAYERS
            18.ASSAULT RIFLES AND PLASMA RIFLES WERE ADDED
            19.RETICLES BASED ON THE GUN SELECTED HAVE BEEN ADDED, PLASMA RIFLE STILL NEEDS A RETICLE
            20.RECOIL WAS ADDED
            30.BOTH NEW GUNS ARE NOW PICKUPS ON THE MAP
            31.SEVERAL DEVELOPMENT ERRORS WERE FIXED ALONG THE WAY
            32.PLASMA RIFLE SHOOTS BLUE BLOCKS, NO RETICLE IS TO BE GIVEN
            
          SO OUR CURRENT BACKLOG LOOKS LIKE:
            1.SEARCH IP/PORT FOR MULTIPLE GAMES BEING PLAYED
            --
            3.CREATE LEVEL SELECT 
            4.CREATE PLAYER CUSTOMIZATION
            5.CREATE DIFFERANT GAMES ON SAME SERVER
            --
            7.CREATE STAIR BLOCKS AND MECHANICS
            8.GUN FIGHTS GET GLITCHY (BULLETS NO LONGER PROCESS, JUST PROCESSING VECTOR HITS.  PENDING TEST)
            --
            --
            11.CREATE AMMO
            12.CREATE MORE GUNS
            --
            14.CREATE CROUCH MECHANISM
            15.PLASMA BULLETS GO THROUGH WALLS
            16.PLASMA BULLETS DONT DEAL DAMAGE, THE HIT_TEST() FUNCTION STILL DETERMINES HIT
            
            
