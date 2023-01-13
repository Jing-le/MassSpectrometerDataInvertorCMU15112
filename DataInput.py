from cmu_112_graphics import *

def letterL(L): #Code puts all the letters into a set
    newS = set()
    for n in L:
        newS.add(n)
    return newS

def text_keyPressed(app, event): #Code to type things on the screen
    if event.key == 'Backspace':
        app.dataT = app.dataT[:-1]
    elif event.key in app.letters:
        app.dataT += event.key
    elif event.key == '.':
        app.dataT += '.'
    elif event.key == 'Enter':
        app.mode = 'intro'
        app.NEdata = False
        app.reselect = True
    elif event.key in {'1','2','3','4','5','6','7','8','9','0'}:
        app.dataT += event.key

def text_redrawAll(app, canvas): #Draws the box and text when you type
    x, y = app.width, app.height
    canvas.create_rectangle(x//2-x//4, y//2-y//10, x//2+x//4, y//2+y//10, 
                        width = x//100)
    canvas.create_text(x//2, y//2, text = app.dataT, font = 'Times 20')
    canvas.create_text(x//2, y//2-y//6, text = 'Type in data file', 
                        font = 'Times 30')

#Code is the same as above but just for another page
def times_keyPressed(app, event):
    if event.key == 'Backspace':
        app.timeT = app.timeT[:-1]
    elif event.key in app.letters:
        app.timeT += event.key
    elif event.key == '.':
        app.timeT += '.'
    elif event.key == 'Enter':
        app.mode = 'intro'
        app.NEdata = False
        app.reselect = True
    elif event.key in {'1','2','3','4','5','6','7','8','9','0'}:
        app.timeT += event.key

def times_redrawAll(app, canvas):
    x, y = app.width, app.height
    canvas.create_rectangle(x//2-x//4, y//2-y//10, x//2+x//4, y//2+y//10, 
                        width = x//100)
    canvas.create_text(x//2, y//2, text = app.timeT, font = 'Times 20')
    canvas.create_text(x//2, y//2-y//6, text = 'Type in time file', 
                        font = 'Times 30')

def delay_keyPressed(app, event):
    if event.key == 'Backspace':
        app.delayT = app.delayT[:-1]
    elif event.key == 'Enter':
        app.mode = 'intro'
        app.NEdata = False
        app.reselect = True
    elif event.key in {'1','2','3','4','5','6','7','8','9','0'}:
        app.delayT += event.key
    elif event.key == ':':
        app.delayT += event.key

def delay_redrawAll(app, canvas):
    x, y = app.width, app.height
    canvas.create_rectangle(x//2-x//4, y//2-y//10, x//2+x//4, y//2+y//10, 
                        width = x//100)
    canvas.create_text(x//2, y//2, text = app.delayT, font = 'Times 20')
    canvas.create_text(x//2, y//2-y//6, text = 'Type in time delay value (min:sec)', 
                        font = 'Times 30')    