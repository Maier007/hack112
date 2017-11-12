from noteClass import*

KEY = [WholeNote,HalfNote,QuarterNote,EighthNote,WholeRest,HalfRest,QuarterRest,EighthRest,'.','Sharp','Flat','Natural']
CELLSIZE = 30
NUMCELL = len(KEY)
COLS = 3
ROWS = NUMCELL//COLS+min(NUMCELL%COLS,1) #Round up

def drawPad(canvas,data):
    startX = data.px
    startY = data.py
    endX = data.px+COLS*CELLSIZE
    endY = data.py+ROWS*CELLSIZE
    canvas.create_rectangle(startX,startY,endX,endY,fill='cyan')
    for row in range(1,ROWS):
        canvas.create_line(startX,startY+row*CELLSIZE,endX,startY+row*CELLSIZE)
    for col in range(1,COLS):
        canvas.create_line(startX+col*CELLSIZE,startY,startX+col*CELLSIZE,endY)
    for i in range(NUMCELL):
        if ((isinstance(KEY[i],Note) and KEY[i] == data.currNote) or
           (data.isDot and KEY[i] == '.')):
           
            row = i//COLS
            col = i%COLS
            startX = data.px+col*CELLSIZE
            startY = data.py+row*CELLSIZE
            endX = data.px+(col+1)*CELLSIZE
            endY = data.py+(row+1)*CELLSIZE
            canvas.create_rectangle(startX,startY,endX,endY,fill='pink')


def clickPad(event,data):
    col = (event.x-data.px)//CELLSIZE
    row = (event.y-data.py)//CELLSIZE
    if col > COLS or row > ROWS:
        return
    index = row*COLS+col
    if index > NUMCELL:
        return
    if isinstance(KEY[index], Note):
        data.nextNote = KEY[index]
        return True
    else:
        if KEY[index] == '.':
            data.isDot = not data.isDot
        elif KEY[index] == 'Sharp':
            data.noteSign = 1
        elif KEY[index] == 'Flat':
            data.noteSign = -1
        elif KEY[index] == 'Natural':
            data.noteSign = 0
    print(KEY[index])
    return False
        
