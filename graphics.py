from tkinter import *
from PIL import ImageTk, Image
import math
from noteClass import *

def init(data):
    # drawing pad
    data.psize = 30
    data.px = data.width - data.psize
    data.py = 20
    
    #drawing staff
    data.staffStartHeight = 60
    data.staffSpaceLine = 20
    data.staffSpace = 200
    data.staffXStart = 10
    data.staffXEnd = data.width - data.psize - 10
    
    #data on notes
    data.staff = []     # regular 1D list
    data.pitches = pitchesSetup()
    data.noteMenu = noteMenuSetup()
    data.currNote = -1
    data.mode = "Compose"

def mousePressed(event, data): #make a new note
    if clickPad(event, data) == True:
        newNote = data.nextNote()
        data.staff.append(newNote)

def keyPressed(event, data):#change pitch or mode
    if data.mode == "Compose":
        note = data.staff[data.currNote[0]][data.currNote[1]]
        if event.keysym == "Up":
            pitch = data.pitches.index(note.getPitch()) + 1
            if pitch >= 88:   pitch -= 1  # 88: number of keys on a keyboard
            pitch = data.pitches[pitch]
            note.pitch(pitch)
        elif event.keysym == "Down":    
            pitch = data.pitches.index(note.getPitch()) - 1
            if pitch < 0:   pitch += 1
            pitch = data.pitches[pitch]
            note.pitch(pitch)
        elif event.keysym == "Left":
            data.currNote -= 1
        elif event.keysym == "Right":
            data.currNote += 1
        elif event.keysym == "Delete":
            dur = data.currNote.getDuration()
            pitch = 0
            # gets the rest image
            im = getNewImage(dur, pitch)
            data.currNote = Note(dur, im, pitch)
        elif event.keysym == "p":
            data.mode = "Play"
    elif data.mode == "Play":
        if event.keysym == "c":
            data.mode = "Compose"

def timerFired(data):
    if data.mode == "Play":
        for n in staff:
            pattern = midi.Pattern()
            track = midi.Track()
            pattern.append(track)
            eot = midi.EndOfTrackEvent(tick=1)
            track.append(eot)
            midi.write_midifile("testNoteClass.mid", pattern)
            
            n.playNote(track)


### DATA FUNCTIONS ###

def pitchesSetup():
    pitches = []
    letters, numbers = ['C','D','E','F','G','A','B'], [0,1,2,3,4,5,6,7,8]
    l,n = 5,0
    for i in range(88):
        # resetting after each octave
        if l >= len(letters):
            n += 1
            l = 0
        # checking for black keys: saving them as sharps(#)
        sharps = set(['C','D','F','G','A'])
        if len(pitches) > 0 and pitches[len(pitches)-1][0] in sharps and pitches[len(pitches)-1][1] != "#":
            l -= 1
            pitch = letters[l] + "#" + str(numbers[n])
        # checking for white keys
        else:
            pitch = letters[l] + str(numbers[n])
        l += 1
        pitches.append(pitch)
    return pitches


def noteMenuSetup():
    return []
    # list of the image files (whole note, half note, etc) to be shown


def getNextNote(data, d):
    note = data.currNote
    measure, innerNote = note[0], note[1]
    if measure == 0 and innerNote == 0:
        return note
    if d < 0:
        if measure > 0 and innerNote == 0:
            measure += 1*d
            innerNote = (len(data.staff[measure])-1)
        else:
            innerNote += 1*d
        return (measure, innerNote)
    if d > 0:
        if measure == len(staff)-1 and innerNote == len(staff[measure])-1:
            return note
        elif measure < len(staff)-1 and innerNote == len(staff[measure])-1:
            measure += 1
            innerNote = 0
        else:
            innerNote += 1*d
        return (measure, innerNote)
    return note


def getNewImage(dur, pitch):
    if pitch == 0:
        pass
        # get image of rest
    else:
        pass
        # get image of note with appropriate duration
    return 42

def isClicked(a,b,x,y,r):
    # a,b: mouse coordinates. x,y: center of the item. r: radius/size of item
    distX = (a,x)**2
    distY = (b,y)**2
    dist = (distX + distY)**0.5
    if dist <= radius:  return True
    else:   return False

### DRAW FUNCTIONS ###

def drawStaff(canvas, data, numStaff):
    treble = Image.open("Images/smallTreble.png")
    ph1 = ImageTk.PhotoImage(treble)
    data.im_tk = ImageTk.PhotoImage(treble)
    
    for j in range(numStaff):
        beginningLineYStart = data.staffStartHeight + j*data.staffSpace
        beginningLineYEnd = beginningLineYStart + 4*data.staffSpaceLine
        canvas.create_line(data.staffXStart, beginningLineYStart, data.staffXStart, beginningLineYEnd, width = 5)
        canvas.create_line(data.staffXEnd, beginningLineYStart, data.staffXEnd, beginningLineYEnd, width = 5)
        
        trebleX = treble.width/2 + data.staffXStart
        trebleY = data.staffStartHeight + j*data.staffSpace +\
                                    2.5 * data.staffSpaceLine
        canvas.create_image(trebleX, trebleY, im = data.im_tk)
        
        for i in range(5):
            y = data.staffStartHeight + (i*data.staffSpaceLine) + \
                                        (j*data.staffSpace)
            canvas.create_line(data.staffXStart, y, data.staffXEnd,y, width = 3)

def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height, fill = "white", width = 0)
    drawStaff(canvas, data, 2)



##########################################################
### STANDARD RUN FUNCTION ################################
##########################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 400)


