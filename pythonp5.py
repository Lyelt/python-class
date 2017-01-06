import tkinter
from tkinter.constants import LEFT
from tkinter.constants import TOP
from tkinter.constants import RIGHT
from tkinter.constants import ALL

#------------
deltax = 2  #Initial speed values
deltay = -2
down = True #To detect movement of obstacle
obsHit = 0  #Keep track of number of times obstacle was hit
#-----------

#-------------------------------------------------------------------------------
#-------------Control movement of balls/paddles---------------------------------
def moveit () :
    global  deltax, deltay, scoreText1, scoreText2, obsHit
    moveObs() # Begin movement of obstacle
    circlecanvas.move(imageid, deltax, deltay) # Begin movement of circle
    rBound = circlecanvas.winfo_width()
    uBound = circlecanvas.winfo_height()
    
    #----Coords of each object. Represented as a list:
    #----[UpperLeftX, UpperLeftY, BottomRightX, BottomRightY]
    balllocation = circlecanvas.coords(imageid)
    paddlelocation = circlecanvas.coords(paddleid)
    paddle2location = circlecanvas.coords(paddleid2)
    obslocation = circlecanvas.coords(obstacleid)

    # If ball collides with paddle, reverse x-direction
    if balllocation[2] >= paddlelocation[0] and balllocation[2] <= paddlelocation[2] and balllocation[3] >= paddlelocation[1] and balllocation[1] <= paddlelocation[3] :
        deltax = -deltax
    if balllocation[0] <= paddle2location[2] and balllocation[0] >= paddle2location[0] and balllocation[3] >= paddle2location[1] and balllocation[1] <= paddle2location[3] :  
        deltax = -deltax
    
    # If ball collides with obstacle, reverse x-direction and record object hit
    if ((balllocation[0] <= obslocation[2] and balllocation[0] >= obslocation[0] and balllocation[3] >= obslocation[1] and balllocation[1] <= obslocation[3]) or 
        (balllocation[2] >= obslocation[0] and balllocation[2] <= obslocation[2] and balllocation[3] >= obslocation[1] and balllocation[1] <= obslocation[3])) :
        deltax = -deltax
        if obsHit < 20 :
            obsHit += 1
        # Redraw a larger net
        circlecanvas.coords(obstacleid, 340, 8, 348, 80 - diff.get() + (10*obsHit))
    
    # If ball hits right side, update P2's score, reset ball
    if balllocation[2] >= rBound :
        circlecanvas.delete(scoreText1)
        circlecanvas.delete(scoreText2)
        p2score.set(p2score.get()+1)
        scoreText1 = circlecanvas.create_text(630, 10, text = p1score.get(), fill="white")
        scoreText2 = circlecanvas.create_text(70, 10, text = p2score.get(), fill="white")   
        circlecanvas.coords(imageid, (rBound / 2, uBound / 2, rBound / 2 + diff.get(), uBound / 2 + diff.get())) 
    # If ball hits left side, update P1's score, reset ball
    if balllocation[0] <= 0 :
        circlecanvas.delete(scoreText1)
        circlecanvas.delete(scoreText2)
        p1score.set(p1score.get()+1)
        scoreText1 = circlecanvas.create_text(630, 10, text = p1score.get(), fill="white")
        scoreText2 = circlecanvas.create_text(70, 10, text = p2score.get(), fill="white")
        circlecanvas.coords(imageid, (rBound / 2, uBound / 2, rBound / 2 + diff.get(), uBound / 2 + diff.get())) 
    # If ball hits top or bottom, reverse y-direction
    if balllocation[3] >= uBound :
        deltay = -deltay
    if balllocation[1] <= 0 :
        deltay = -deltay
    # If a player won, show victory screen
    if p1score.get() == scoreGoal.get() or p2score.get() == scoreGoal.get() :
        showVictory()
    # If playing against an AI, move its paddle accordingly
    if player.get() == "AI" :
      moveAI()
        
    rootwindow.after(10, moveit) # Keep repeating
    
#-------------------------------------------------------------------------------
#-------------Move the moving obstacle------------------------------------------
def moveObs () :
    obslocation = circlecanvas.coords(obstacleid)
    global down
    # If the obstacle is at the bottom, move up
    if obslocation[3] >= 497 :
        down = False
    # If the obstacle is at the top, move down
    if obslocation[1] <= 3 :
        down = True
    if down:
        circlecanvas.move(obstacleid, 0, 3)
    else :
        circlecanvas.move(obstacleid, 0, -3)

#-------------------------------------------------------------------------------
#-------------Show Victory Screen-----------------------------------------------
def showVictory () :
    circlecanvas.delete(ALL)
    obsHit = 0
    if p1score.get() == scoreGoal.get() :
        victoryText = circlecanvas.create_text(350, 100, text = "Player 1 Wins", fill="white")
    elif p2score.get() == scoreGoal.get() :
        victoryText = circlecanvas.create_text(350, 100, text = "Player 2 Wins", fill="white")

#-------------------------------------------------------------------------------
#-------------Controls the movement of the AI paddle----------------------------
def moveAI () :
    balllocation = circlecanvas.coords(imageid)
    paddle2location = circlecanvas.coords(paddleid2)
    if diff.get() == 20 :   #medium
        AImove = 2
    elif diff.get() == 30 : #easy
        AImove = 1
    elif diff.get() == 10 : #hard
        AImove = 3
    
    # AI moves toward the paddle
    if balllocation[0] < 350 :
        if balllocation[1] < paddle2location[1] :
            circlecanvas.move(paddleid2, 0, -AImove)
        elif balllocation[3] > paddle2location[3] :
            circlecanvas.move(paddleid2, 0, AImove)

#-------------------------------------------------------------------------------
#-------------Begin the game----------------------------------------------------
def startGame () :
    global imageid, paddleid, paddleid2, deltax, deltay, obstacleid
    
    #---Bind all key events (use W and S for a second player)
    circlecanvas.bind("<Up>", hitkeyup)
    circlecanvas.bind("<Down>", hitkeydown)
    if player.get() == "Human" :
        circlecanvas.bind("w", hitkeyw)
        circlecanvas.bind("s", hitkeys)
    circlecanvas.focus_set()
    
    #---Redraw all of the objects based on user choices
    circlecanvas.delete(ALL)
    imageid = circlecanvas.create_oval(340, 240, 340 + diff.get(), 240 + diff.get(), fill = "white", width = 1)
    paddleid = circlecanvas.create_rectangle(650, 250, 660, 250 + size.get(), fill = "white", width = 1)
    paddleid2 = circlecanvas.create_rectangle(50, 250, 60, 250 + size.get(), fill = "white", width = 1)
    obstacleid = circlecanvas.create_rectangle(340, 8, 348, 80 - diff.get(), fill= "white", width = 1)
    
    deltax = speed.get()    #Use user-chosen value of speed
    deltay = -(speed.get())
    
    moveit() #Move the ball and net
    
#-------------------------------------------------------------------------------
#-------------Handle Key events to move paddles---------------------------------
def hitkeyup (ev) :
    paddlelocation = circlecanvas.coords(paddleid)
    # Don't move further than top/bottom of screen
    if paddlelocation[1] >= 0 :
        circlecanvas.move(paddleid, 0, -(sens.get()))

def hitkeydown (ev) :
    paddlelocation = circlecanvas.coords(paddleid)
    if paddlelocation[3] <= 500:
        circlecanvas.move(paddleid, 0, sens.get())

def hitkeyw (ev) :
    paddle2location = circlecanvas.coords(paddleid2)
    if paddle2location[1] >= 0 :
        circlecanvas.move(paddleid2, 0, -(sens.get()))
    
def hitkeys (ev) :
    paddle2location = circlecanvas.coords(paddleid2)
    if paddle2location[3] <= 500 :
        circlecanvas.move(paddleid2, 0, sens.get())

#-------------------------------------------------------------------------------
#-------------Sets up the UI of the Pong Game-----------------------------------

#-------------------------------------------------------------------------------
#---Create the root window
rootwindow = tkinter.Tk()
rootwindow.title("Pong")
rootwindow.lift()
rootwindow.resizable(width=False, height=False)

#---A frame to pack all of the selection widgets
bigFrame = tkinter.Frame(rootwindow, bg = "white", width = 700, height = 150)
bigFrame.grid(row = 0, column = 0)
bigFrame.pack_propagate(0)

#-------------------------------------------------------------------------------
#---Radio Buttons for the size of the paddle
sizeFrame = tkinter.Frame(bigFrame, bg = "white")
sizeFrame.pack(side=LEFT)
label4 = tkinter.Label(sizeFrame, text = "Choose Paddle Size", bg = "white")
size = tkinter.IntVar()
smallButton = tkinter.Radiobutton(sizeFrame, text = "Small", variable = size, value = 60, bg = "white")
midButton = tkinter.Radiobutton(sizeFrame, text = "Medium", variable = size, value = 80, bg = "white")
largeButton = tkinter.Radiobutton(sizeFrame, text = "Large", variable = size, value = 100, bg = "white")
midButton.select()
label4.pack(side=TOP)
smallButton.pack()
midButton.pack()
largeButton.pack()

#-------------------------------------------------------------------------------
#---Radio Buttons for difficulty of the game
#---This includes ball size, obstacle size at start, and AI difficulty
diffFrame = tkinter.Frame(bigFrame, bg = "white")
diffFrame.pack(side=LEFT)
label = tkinter.Label(diffFrame, text = "Choose Difficulty", bg = "white")
diff = tkinter.IntVar()
easyButton = tkinter.Radiobutton(diffFrame, text = "Easy", variable = diff, value = 30, bg = "white")
medButton = tkinter.Radiobutton(diffFrame, text = "Medium", variable = diff, value = 20, bg = "white")
hardButton = tkinter.Radiobutton(diffFrame, text = "Hard", variable = diff, value = 10, bg = "white")
medButton.select()
label.pack(side=TOP)
easyButton.pack()
medButton.pack()
hardButton.pack()

#-------------------------------------------------------------------------------
#---Radio Buttons for speed of the ball
speedFrame = tkinter.Frame(bigFrame, bg = "white")
speedFrame.pack(side=LEFT)
label = tkinter.Label(speedFrame, text = "Choose Ball Speed", bg = "white")
speed = tkinter.IntVar()
slowButton = tkinter.Radiobutton(speedFrame, text = "Slow", variable = speed, value = 2, bg = "white")
mediumButton = tkinter.Radiobutton(speedFrame, text = "Medium", variable = speed, value = 3, bg = "white")
fastButton = tkinter.Radiobutton(speedFrame, text = "Fast", variable = speed, value = 4, bg = "white")
mediumButton.select()
label.pack(side=TOP)
slowButton.pack()
mediumButton.pack()
fastButton.pack()

#-------------------------------------------------------------------------------
#---Radio Buttons for length of game
scoreGoal = tkinter.IntVar()
scoreFrame = tkinter.Frame(bigFrame, bg = "white")
scoreFrame.pack(side=LEFT)
label3 = tkinter.Label(scoreFrame, text = "Play to score:", bg = "white")
button7 = tkinter.Radiobutton(scoreFrame, text = "7", variable = scoreGoal, value = 7, bg = "white")
button15 = tkinter.Radiobutton(scoreFrame, text = "15", variable = scoreGoal, value = 15, bg = "white")
button21 = tkinter.Radiobutton(scoreFrame, text = "21", variable = scoreGoal, value = 21, bg = "white")
button15.select()
label3.pack(side=TOP)
button7.pack()
button15.pack()
button21.pack()

#-------------------------------------------------------------------------------
#---Play against AI or Human
player = tkinter.StringVar()
playerFrame = tkinter.Frame(bigFrame, bg = "white")
playerFrame.pack(side=LEFT)
label2 = tkinter.Label(playerFrame, text = "Play Against", bg = "white")
AIButton = tkinter.Radiobutton(playerFrame, text = "AI", variable = player, value = "AI", bg = "white")
P2Button = tkinter.Radiobutton(playerFrame, text = "Human", variable = player, value = "Human", bg = "white")
AIButton.select()
label2.pack(side=TOP)
AIButton.pack()
P2Button.pack()

#-------------------------------------------------------------------------------
#---Slider for paddle sensitivity
sliderFrame = tkinter.Frame(bigFrame, bg = "white")
sliderFrame.pack(side=LEFT)
sensLabel = tkinter.Label(sliderFrame, bg = "white", text = "Paddle Sensitivity")
sens = tkinter.IntVar()
sensSlider = tkinter.Scale(sliderFrame, from_ = 10, to = 30, variable = sens, bg = "white", orient = tkinter.HORIZONTAL)
sensSlider.set(20)
sensLabel.pack(side=TOP)
sensSlider.pack()

#-------------------------------------------------------------------------------
#---Play and Quit buttons
buttonFrame = tkinter.Frame(bigFrame, bg = "white")
buttonFrame.pack(side=RIGHT)
#Start the game
startButton = tkinter.Button(buttonFrame, text = "Play", command = startGame, bg = "white")
quitButton = tkinter.Button(buttonFrame, text = "Quit", command = exit, bg = "white")
startButton.pack()
quitButton.pack()

#-------------------------------------------------------------------------------
#---Draw the canvas
circlecanvas = tkinter.Canvas(rootwindow, height = 500, width = 700, bg = "black")
circlecanvas.grid(row = 1, column = 0, columnspan = 2, sticky = "wens")
rootwindow.rowconfigure(1, weight = 4)
rootwindow.columnconfigure(0, weight = 1)

#-------------------------------------------------------------------------------
#---Draw a preliminary image of the objects
imageid = circlecanvas.create_oval(340, 240, 340 + diff.get(), 240 + diff.get(), fill = "white", width = 1)
paddleid = circlecanvas.create_rectangle(650, 250, 660, 250 + size.get(), fill = "white", width = 1)
paddleid2 = circlecanvas.create_rectangle(50, 250, 60, 250 + size.get(), fill = "white", width = 1)
obstacleid = circlecanvas.create_rectangle(340, 8, 348, 80 - diff.get(), fill= "white", width = 1)

#-------------------------------------------------------------------------------
#---Keep track of the scores of each player
p1score = tkinter.IntVar()
p2score = tkinter.IntVar()
p1score.set(0)
p2score.set(0)
scoreText1 = circlecanvas.create_text(630, 10, text = p1score.get(), fill="white")
scoreText2 = circlecanvas.create_text(70, 10, text = p2score.get(), fill="white")

rootwindow.mainloop()