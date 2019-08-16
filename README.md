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

THE GUNS.PY FILE IS WERE ALL THE GUN INFO IS GOING TO BE HELD, RIGHT NOW, IT ONLY CONTAINS THE PISTOL

PLAYERS ARE NOW (V1.2 8-15-19) GIVEN THE OPTION TO START A NEW SERVER IF NONE CAN BE FOUND.  YOU CAN STILL START A SERVER INDEPENDANTLY
BY USING THE FOLLOWING:
        SERVER.PY WILL, OF COURSE, NEED TO RUN ON A SEPERATE INSTANCE.  ON WINDOWS 10 I OPEN A POWERSHELL BY GOING TO THE DIR, CLICKING FILE AND
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

### AS OF 8-15-2019:
  4 PLAYERS ARE ABLE TO CONNECT AND HAVE A PISTOL BATTLE, ALL PLAYERS STILL FLY AND CAN PLACE BLOCKS/SAVE LOCALY.  
  WHEN ONE PLAYER REACHES <1 HP THEIR IMAGE NO LONGER APPEARS ON OTHER PLAYER'S SCREENS, THE "DEAD" PLAYER'S GHOST IS STILL THERE
  AND CAN STILL BE DAMAGED BUT CANNOT FIRE BACK.  RESPAWN STILL NEEDS TO BE WRITTEN
  
  IF AN IMMIDIATE CONNECTION CAN BE MADE, THEN THE PLAYER IS INSTANTLY TAKEN THERE. THE PLAYER HAS NO OPTIONS TO SEARCH OR START
  A NEW SERVER IF ONE ALREADY EXISTS.
  
  # CHORES
  
          LATEST FIXES (8-16-19): 
            1.SERVERS AND CLIENTS NO LONGER LOCK UP UPON PLAYER EXITS
            2.4 PLAYERS CAN NOW JOIN
            3.PLAYERS CAN SEARCH FOR GAMES IF THEY KNOW THE IP OR PORT
            4.PLAYERS CAN CREATE THEIR OWN SERVER INSTANCES, IF NONE CAN BE FOUND
            5.FIXED BUG WHERE SERVER.PY CRASHED IF GAME.PLAYERS CHANGED SIZE DURING ITERATION
            6.CHANGED GAME.PLAYERS FROM A LIST TO A DICT SO THAT ORIGINAL PLAYERS COULD LEAVE AND LATER PLAYERS COULD STAY IN GAME
            7.FIXED SERVER CLOSING WHEN NO MORE PLAYERS IN GAME
  
          SO OUR CURRENT BACKLOG LOOKS LIKE:
            1.SEARCH IP/PORT FOR MULTIPLE GAMES BEING PLAYED 
            2.CREATE RESPAWN AND SCOREBOARD
            3.CREATE LEVEL SELECT 
            4.CREATE PLAYER CUSTOMIZATION
            5.CREATE DIFFERANT GAMES ON SAME SERVER
            6.TURN OFF FLIGHT OUTSIDE OF EDIT MODE
            7.CREATE STAIR BLOCKS AND MECHANICS
            8.GUN FIGHTS GET GLITCHY
            9.REMOVE BLOCK PLACEMENT OUTSIDE OF EDIT MODE
            10.CREATE ABILITY TO PLACE DIFFERANT BLOCK TYPES AND 3 STACKED OR SINGLE STACKED BLOCKS IN EDIT MODE
            11.CREATE HP BAR AND AMMO
            12.CREATE MORE GUNS AND PICKUPS W/ MECHANICS
            13.FACE BLOCK LOOKS TO SELF.ROTATION[1] (Y AXIS)
            14.CREATE CROUCH MECHANISM
            15.CREATE DIE / HIT ANIMATION
            
