from noteClass import*

KEY = [WholeNote,HalfNote,QuarterNote,EighthNote,WholeRest,HalfRest,QuarterRest,EighthRest,'.','Sharp','Flat','Natural']
CELLSIZE = 30
NUMCELL = len(KEY)
COLS = 1
ROWS = NUMCELL//COLS+min(NUMCELL%COLS,1) #Round up

def drawPad(canvas,data):
    startX = data.px
    startY = data.py
    endX = data.px+COLS*CELLSIZE
    endY = data.py+ROWS*CELLSIZE
    canvas.create_rectangle(startX,startY,endX,endY,fill='pale turquoise')
    for row in range(1,ROWS):
        canvas.create_line(startX,startY+row*CELLSIZE,endX,startY+row*CELLSIZE)
    for col in range(1,COLS):
        canvas.create_line(startX+col*CELLSIZE,startY,startX+col*CELLSIZE,endY)
    for i in range(NUMCELL):
        if ((KEY[i] == data.nextNote) or
           (data.isDot and KEY[i] == '.') or
           (data.noteSign == 1 and KEY[i] == 'Sharp') or
           (data.noteSign == 0 and KEY[i] == 'Natural') or
           (data.noteSign == -1 and KEY[i] == 'Flat')):
            row = i//COLS
            col = i%COLS
            startX = data.px+col*CELLSIZE
            startY = data.py+row*CELLSIZE
            endX = data.px+(col+1)*CELLSIZE
            endY = data.py+(row+1)*CELLSIZE
            canvas.create_rectangle(startX,startY,endX,endY,fill='gold')


def clickPad(event,data):
    col = (event.x-data.px)//CELLSIZE
    row = (event.y-data.py)//CELLSIZE
    if col > (COLS-1) or row > (ROWS-1):
        return None
    index = int(row*COLS+col)
    if index > (NUMCELL-1):
        return None
    if KEY[index] == '.':
        data.isDot = not data.isDot
    elif KEY[index] == 'Sharp':
        data.noteSign = 1
    elif KEY[index] == 'Flat':
        data.noteSign = -1
    elif KEY[index] == 'Natural':
        data.noteSign = 0
    elif issubclass(KEY[index], Note):
        data.nextNote = KEY[index]
        return True
    return False
