# HOW TO INSTALL PYTHON

## GETTING STARTED

---

#### THE FOLLOWING IS WORKING AS OF 8-15-19 ON WINDOWS

* GO TO python.org AND SELECT "DOWNLOADS" FROM THE TOP MENU
* JUST UNDER THE MENU, YOU SHOULD SEE A YELLOW BUTTON THAT SAYS SOMETHING LIKE "DOWNLOAD PYTHON 3.7.4" (OR WHATEVER THE LATEST VERSION IS)
* COMPLETE THE SETUP WIZARD AFTER THE DOWNLOAD COMPLETES 
* OPEN CMD (COMMAND PROMT), ON WINDOWS 10 JUST TYPE "CMD" INTO THE SEARCH BAR ON THE TASK BAR
* TYPE python INTO THE COMMAND LINE AND HIT **ENTER**, YOU SHOULD GET SOMETHING LIKE THIS:
```
C:\Users\*YOUR-NAME-HERE*>python
Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 21:26:53) [MSC v.1916 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

IF YOU DONT GET THE ABOVE INFORMATION, THEN YOUR COMPUTER IS HAVING TROUBLE FINDING YOUR NEWLY INSTALLED PYTHON PROGRAM.  YOU CAN HELP
YOUR COMPUTER BY EDITING YOUR *ENVIRONMENT VARIABLES* TO HELP YOUR COMPUTER FIND PYTHON.  IF YOU DIDNT HAVE ANY TROUBLE WITH THE DOWNLOAD
AND YOU GOT SOMETHING LIKE THE ABOVE CODE RETURNED FROM CMD THEN SKIP THE NEXT STEP

---

## EDITING YOUR ENVIRONMENT

---

  IF YOUR COMPUTER IS HAVING TROUBLE FINDING THE PROGRAM YOUR REQUESTING VIA *CMD* THEN WE HAVE TO "CARVE OUT A PATH" TO HELP THE 
  COMPUTER TO FIND WHAT IT NEEDS.  FIRST OPEN **FILE EXPLORER** EITHER BY TYPING IT OUT IN THE SEARCH BAR OR BY SELECTING THE FILE
  ON YOUR TASKBAR (IF YOU STILL SHOW A PICTURE OF A FILE ON YOUR TASKBAR).  ON THE LEFT PAN, NAVIGATE TO YOUR HARD DRIVE'S ROOT DIR.
  
  YOU CAN DO THIS BY SELECTING *THIS PC* (ON WINDOWS 10)(*MY COMPUTER* ON OTHER VERSIONS)  MOST OF THE TIME, YOUR HARD DRIVE IS
  LABELED C:\, BUT SOME PEOPLE MAY BE USING A D:\ DRIVE OR WHATEVER.  YOU'LL SEE SOME OF THE FOLLOWING FILES IN YOUR ROOT DIRECTORY:
  ```
  * DRIVERS
  * PROGRAM FILES
  * PROGRAM FILES(x86)
  * USERS
  * ETC...
  ```
  
  #### FIND python.exe
  IN THE SEARCH BAR AT THE TOP-RIGHT, TYPE "python".  THIS MAY TAKE A WHILE TO GET ALL YOUR RESULTS.  WHAT YOU ARE LOOKING FOR IS
  THE PYTHON.EXE (EXECUTABLE)(APPLICATION).  THERE ARE PROBABLY GOING TO BE SOME OTHER FILES LINGERING AROUND IN THE SEARCH THAT SAY
  *python* BUT THESE ARE NOT THE DIRECTORIES YOU WANT.  ONE FILE I KEEP FINDING IS FULL OF SHORTCUTS AND WONT WORK FOR OUR FIX.  
  
  IF YOU CAN FIND THE PYTHON.EXE THEN YOU CAN FIND THE FOLDER IT IS IN.  MAKE SURE YOUR **FILE EXPLORER** IS CONFIGURED TO VIEW->DETAILS
  TO BETTER FIND THE FILE WE WANT.  MINE IS JUST LABELED "python" ANDS SHOWS AS AN *Application* IN THE *Details* VIEW OF MY 
  **FILE EXPLORER**
  
  #### GET THE APPLICATION'S ADDRESS
  WHEN YOU FIND THE PYTHON APPLICATION, RIGHT-CLICK ON IT AND SELECT *PROPERTIES* AT THE BOTTOM OF THE POPUP MENU.  LOOK FOR THE 
  APPLICATION'S **LOCATION**.  MINE LOOKS LIKE:
  `C:\Users\*USER_NAME_HERE*\AppData\Local\Programs\Python\Python37-32`
  
  COPY-PASTE THE **LOCATION** INTO THE **FILE EXPLORER** ADDRESS BAR AND YOU SHOULD SEE A SET OF FOLDERS AND FILES THAT INCLUDE SOME
  OF THE FOLLOWING:
   ```
    * Lib
    * libs
    * Scripts
    * Tools
    * LICENSE
    * NEWS
    * python
    * etc...
   ```
   
   IF YOU GOT THE ABOVE THEN YOU'VE FOUND IT!  IF NOT, KEEP LOOKING (NOT SURE WHAT ELSE TO TELL YA)  IF YOU LOOK AT THE **EXPLORER**'S
   ADDRESS BAR AGAIN, YOU'LL SEE THE LAST FOLDER (DIR)(DIRECTORY) SHOULD BE LABELED 'Python' WITH YOUR VERSION (mines 3.7) -32:
   ` i.e. Python37-32`
   
   THE ABOVE IS THE DIR (FOLDER) YOU WANT.  SELECT IT BY GOING "UP" A DIRECTORY OR BY SELECTING IT ON THE ADDRESS BAR. RIGHT-CLICK
   AND COPY THE FOLDER.  IN THE LONG RUN, THE FOLDER IS FINE WHERE IT IS, BUT WE WANT TO MAKE THIS TUITORIAL EASY TO UNDERSTAND SO
   WE ARE GOING TO PUT A COPY OF THIS FOLDER IN OUR HARD DRIVE'S ROOT DIR.  NAVIGATE BACK TO THE C:\(OR WHATEVER YOUR HARD DRIVE IS)
   AND RIGHT-CLICK -> PASTE TO THE ROOT DIR.  
   
   #### MOVE THAT FOLDER CLOSER TO HOME
   RIGHT CLICK THE COPIED FOLDER WE JUST PLACED IN THE HARD DRIVE ROOT DIR AND RENAME IT, SIMPLY, "python".  NOW WE KNOW EXACTLY WHERE 
   
   #### EDIT YOUR ENVIRONMENT
   OUR PYTHON.EXE IS.  SO NOW WE CAN EASILY CARVE A PATH FOR OUR COMPUTER.  CLOSE EVERYTHING AND OPEN **CONTROL PANEL**
   
   DEPENDING ON WHAT VERSION OF WINDOWS YOUR ON, YOUR GOING TO SEE EITHER *SYSTEM* OR *SYSTEM & SECURITY*.  IF YOU SEE *SYSTEM & 
   SECURITY*, SELECT IT AND THEN *SYSTEM*. 
   
  A NEW WINDOW WILL APPEAR. ON THE LEFT-HAND SIDE, SELECT *ADVANCED SYSTEM SETTINGS*. ANOTHER WINDOW WILL POPUP, TOWARDS THE BOTTOM
  SELECT *ENVIRONMENT VARIABLES...*
  
  YET ANOTHER POPUP WINDOW.  YOU'LL SEE TWO BOXES, ONE ON TOP OF THE OTHER.  THE BOX AT THE BOTTOM OF THE WINDOW IS THE ONE WE WANT.
  SCROLL DOWN THE LIST AND SELECT **Path** FROM THE MENU.  DOUBLE-CLICK TO OPEN OUR LAST POPUP.
  
  YOUR GOING TO GET ONE OF TWO THINGS HERE, DEPENDING ON YOUR VERSION OF WINDOWS:
    ```
    A. A SMALL POPUP WITH TWO SEPERATE INPUT LINES
    B. A LARGE POPUP WITH A LARGE LIST GOING DOWN THE LEFT-HAND SIDE AND SOME BUTTONS (NEW,EDIT,ETC...) GOING DOWN THE RIGHT-HAND SIDE
    ```
   ##### IF OPTION A.:
   
   ---
   
   IN THE BOTTOM INPUT LINE YOU'LL SEE SOME TEXT THAT LOOKS LIKE THIS:
   `C:\Program Files (x86)\Intel\iCLS Client\;C:\Program Files (x86)\Microsoft SQL Server\140\Tools\Binn\;%SYSTEMROOT%\System32\OpenSSH\;`
   THESE ARE YOUR CURRENT ENVIRONMENT PATHS  BE SURE NOT TO DELETE ANY OF THE DATA WITHIN THIS INPUT LINE.  EACH PATH IS AN ADDRESS
   WHERE YOUR COMPUTER GOES LOOKING FOR REQUIRED FILES TO EXICUTE THE COMMANDS YOUR ASKING IT TO.  EACH PATH IS SEPERATED BY A 
   SEMI-COLON (;).  BE SURE NOT TO DELETE THE SEMI-COLONS! (OR ANY OF IT!).  SELECT THE VERY BEGINNING OF THE TEXT LINE AND TYPE:
   `C:\python;`   <----be sure to include the semi-colon (;).
   
   YOU SHOULD END UP WITH A TEXT LINE THAT STILL INCLUDES ALL THE PATHS THAT WE STARTED WITH, PLUS THE ONE WE ADDED:
   `e.i. C:\python;C:\Program Files (x86)\Intel\iCLS Client\;C:\Program Files (x86)\Microsoft SQL Server\140\Tools\Binn\;%SYSTEMROOT%\System32\OpenSSH\;`
   
   HIT OK, YOUR DONE!
   
   ##### IF OPTION B.:
   
   ---
   
   TO THE RIGHT, SELECT "NEW" AND TYPE IN `C:\python` <----NO need for a semi-colon (;) like the above example
   
   HIT OK, YOUR DONE!
   
#### CHECK IF YOU DID IT RIGHT
   
---
   
  OPEN *CMD* AND TYPE `python` INTO THE COMMAND LINE.  IF YOU GET SOMETHING LIKE:
  ```
  C:\Users\*YOUR-NAME-HERE*>python
  Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 21:26:53) [MSC v.1916 32 bit (Intel)] on win32
  Type "help", "copyright", "credits" or "license" for more information.
  >>>
  ```
  THEN YOU'VE GOT IT NOW!
  
  THE NEXT THING YOU'LL NEED IS *pip*.  PIP IS A PYTHON DATABASE ONLINE (SO YOU'LL NEED AN INTERNET CONNECTION TO GET IT AND USE IT)
  THAT YOU CAN USE TO **SECURELY** DOWNLOAD PYTHON MODULES AND LIBRARIES.  
  
## DOWNLOAD PIP

---

OPEN *CMD* AND TYPE PIP.  IF YOU DONT GET A BIG LONG LIST OF COMMANDS LIKE:
```
Commands:
  install                     Install packages.
  download                    Download packages.
  uninstall                   Uninstall packages.
  freeze                      Output installed packages in requirements format.
  list                        List installed packages.
  show                        Show information about installed packages.
  check                       Verify installed packages have compatible dependencies.
  config                      Manage local and global configuration.
  search                      Search PyPI for packages.
  wheel                       Build wheels from your requirements.
  hash                        Compute hashes of package archives.
  completion                  A helper command used for command completion.
  help                        Show help for commands.

General Options:
  -h, --help                  Show help.
  --isolated                  Run pip in an isolated mode, ignoring environment variables and user configuration.
  -v, --verbose               Give more output. Option is additive, and can be used up to 3 times.
  -V, --version               Show version and exit.
  -q, --quiet                 Give less output. Option is additive, and can be used up to 3 times (corresponding to
                              WARNING, ERROR, and CRITICAL logging levels).
  --log <path>                Path to a verbose appending log.
  --proxy <proxy>             Specify a proxy in the form [user:passwd@]proxy.server:port.
  --retries <retries>         Maximum number of retries each connection should attempt (default 5 times).
  --timeout <sec>             Set the socket timeout (default 15 seconds).
  --exists-action <action>    Default action when a path already exists: (s)witch, (i)gnore, (w)ipe, (b)ackup,
                              (a)bort.
  --trusted-host <hostname>   Mark this host as trusted, even though it does not have valid or any HTTPS.
  --cert <path>               Path to alternate CA bundle.
  --client-cert <path>        Path to SSL client certificate, a single file containing the private key and the
                              certificate in PEM format.
  --cache-dir <dir>           Store the cache data in <dir>.
  --no-cache-dir              Disable the cache.
  --disable-pip-version-check
                              Don't periodically check PyPI to determine whether a new version of pip is available for
                              download. Implied with --no-index.
  --no-color                  Suppress colored output

```

THEN YOU DONT HAVE PIP INSTALLED, HERE'S HOW:

YOU'LL NEED TO GO ONLINE AND EITHER DOWNLOAD A FILE CALLED 'get-pip.py' OR YOU CAN JUST FIND THE SCRIPT ONLINE, PRETTY EASILY, AND
COPY-PASTE IT TO YOU FAVORITE TEXT EDITOR (CODE EDITOR)(MINES notepad++) AND SAVE THE FILES AS `get-pip.py`.  TRY AND SAVE THE FILE
TO THE C:\ (HARD DRIVE ROOT) AS BEFORE OR JUST NAVIGATE WHERE YOU HAVE IT SAVED USING CMD.  FOR THOSE OF YOU WHO DONT KNOW HOW TO
DO THAT, SAVE THE FILE (OR COPY-PASTE IT), AS WE DID BEFORE, TO THE C:\.  

OPEN CMD AND TYPE `cd C:\` (OR cd TO WHERE YOU HAVE THE `get-pip.py` SAVED).  cd MEANS CHANGE DIRECTORY, IT'S THE COMMAND YOU USE
TO 'NAVIGATE' THROUGH YOUR COMPUTER.  NOW THAT WE ARE IN THE HARD DRIVE'S ROOT DIR TYPE THE FOLLOWING:
    `python get-pip.py`
THIS WILL RUN THE PYTHON APPLICATION WE DOWNLOADED AND READ THE .py (python) SCRIPT 'get-pip'.  YOU SHOULD SEE A STATUS BAR FILL UP
ON YOUR SCREEN.  WHEN THE INSTALL IS DONE (IT WONT TAKE VERY LONG AT ALL), TYPE `pip` into the command line again.

NOW YOU SHOULD BE GETTING THE BIG LIST OF COMMADS SHOWN ABOVE.  IF YOU STILL GET AN ERROR THEN YOU'LL NEED TO PUT IT INTO YOUR
ENVIRONMENT AS WE DID BEFORE.  THIS TIME, HOWEVER, YOUR LATEST VERSION OF PYTHON SHOULD ALREADY HAVE PIP IN IT'S LIBRARY.  GO
BACK TO YOUR ENVIRONMENTAL VARIABLES AND ADD THE LINE `C:\python\Scripts` into your Paths and you should get the Command Menu when
you type `pip` into CMD now.  

---

#### IF YOU AINT GOT THE ABOVE, THEN IM NOT SURE HOW TO HELP YOU

---

# INSTALL PYGAME

PYGAME IS A VERY COMMON, WELL KNOWN LIBRARY WE USE IN PYTHON TO MAKE GAMES.  TO INSTALL IT, OPEN 'CMD' AND TYPE:
`pip install pygame`

# INSTALL PYGLET

PYGLET IS ANOTHER VERY COMMON LIBRARY USED WITH openGL TO CREATE 3D GRAPHICS ONSCREEN.  openGL WAS INVENTED IN 1992 AND HAS BEEN
USED EVER SINCE TO CREATE A BED FOR THE DEVELOPMENT OF ONSCREEN GRAPHICS.  openGL IS SO COMMON, THAT ITS EMBEDDED IN MOST EVERY
GRAPHICS CARD YOU'LL FIND TODAY.  openGL STANDS FOR 'OPEN GRAPHICS LIBRARY', PYGLET IS ANOTHER LIBRARY THAT HELPS US USE OPENGL.  

---
---
---

# ALL DONE! GO PLAY!

