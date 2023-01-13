from tkinter import *
from tkinter import ttk
from SortDataCode import *
from GraphDrawing import *
from DataInput import *
from Classes import *
import string

#Main screen for project

def appStarted(app): 
    #All these are for the starting page. Some interact with other pages too       
    app.mode = 'intro'
    app.dropDownI = False
    app.dropDownS = False
    app.selectI = False
    app.selectS = False
    app.graphb = Buttons('Graph', 'cadet blue', 'white', 'next', 
                app.width//2, app.height*(3/4), app.width//8, app.height//18)
    app.b = Buttons('Select Ion', 'dim gray', 'white', 'dropDownI', 
                app.width//4, app.height//3, app.width//8, app.height//18)
    app.specB = Buttons('Select Mass Spec', 'dim gray', 'white', 'dropDownS', 
                app.width*(3/4), app.height//3, app.width//8, app.height//18)
    app.homeButton = Buttons('Home', 'OrangeRed2', 'black', 'returnHome', 
                            app.width//22, app.height*(24/25), 
                            app.width//25, app.height//30)
    app.backZoom = Buttons('Back', 'tomato2', 'black', 'backGraph', 
                            app.width//12, app.height//15, 
                            app.width//25, app.height//30)
    app.instrB = Buttons('Features', 'sandy brown', 'black', 'reveal',
                        app.width*(17/18), app.height//18,
                        app.width//25, app.height//30)
    app.input = Buttons('Input Data', 'dim gray', 'white', 'input',
                        app.width-(app.width//12), app.height-(app.height//15),
                        app.width//15, app.height//25)
    app.timeInput = Buttons('Input Time', 'dim gray', 'white', 'input',
                        app.width-(app.width//4), app.height-
                        (app.height//15), app.width//15, app.height//25)
    app.delayB = Buttons('Input Time Delay', 'dim gray', 'white', 'input',
                        app.width-(app.width//2), app.height-
                        (app.height//15), app.width//10, app.height//25)
    app.dropDownI = False
    app.dropDownS = False
    app.selectI = False
    app.selectS = False
    app.ionb = []
    app.specb = []
    app.b.doFunction(app)
    app.specB.doFunction(app)       
    app.dataT = ''
    app.timeT = ''
    app.delayT = ''
    app.letters = letterL(string.ascii_lowercase)       
    app.NEdata = True
    app.reselect = False
    app.criteria = SpecSettings(None, None)
    #Group of app variables for the graphing
    app.x0, app.y0 = app.width//8, app.height//8
    app.x1, app.y1 = app.width - app.x0, app.height - app.y0
    app.positions = []
    app.r = min(app.width, app.height)//120
    app.ix, app.iy, app.zx, app.zy = (0, 0, 0, 0)
    app.newP = []
    app.run = False
    app.pPrint = None
    app.ibx = 6
    app.iby = 6
    app.instr = False
    app.lobf = False

def intro_mousePressed(app, event):
    #Chunk of code to test if mouse is in bounds of the button
    if app.b.inBounds(event.x, event.y):
        app.dropDownI = True
        app.reselect = False
    elif app.specB.inBounds(event.x, event.y):
        app.dropDownS = True
    elif (app.graphb.inBounds(event.x, event.y) and app.NEdata == False and 
        app.reselect == False):
        app.mode = 'graph'
        app.run = True
    elif app.input.inBounds(event.x, event.y):
        app.mode = 'text'
    elif app.timeInput.inBounds(event.x, event.y):
        app.mode = 'times'
    elif app.delayB.inBounds(event.x, event.y):
        app.mode = 'delay'
    for bi in app.ionb:
        if bi.inBounds(event.x, event.y) and app.dropDownI == True:
            app.dropDownI = False
            app.selectI = True
            app.selectI = Buttons(bi.select(), 'dim gray', 'SpringGreen2', 
                        'dropDownI', app.b.x, app.b.y, app.b.w, app.b.h)
            app.criteria.ion = bi.select()
            app.positions = []
    for bs in app.specb:
        if bs.inBounds(event.x, event.y) and app.dropDownS == True:
            app.dropDownS = False
            app.selectS = True
            app.selectS = Buttons(bs.select(), 'dim gray', 'SpringGreen2',
                        'dropDownS', app.specB.x, app.specB.y, app.specB.w, 
                        app.specB.h)
            app.criteria.typeSpec = bs.select()
            app.positions = []

    #Code chunk to start graphing. Initally creates all the points needed
    if app.criteria.ion != None and app.criteria.typeSpec != None:
        app.criteria.addAMUs()
        if app.criteria.monomer == None:
            app.NEdata = True
            return
        try: #If the file isn't found, then it doesn't let you graph
            allData = loadData('./' + app.dataT)
            allTimes = timeRanges(allData, './' + app.timeT)
        except:
            app.NEdata = True
            return    
        allData = loadData('./' + app.dataT)
        allTimes = timeRanges(allData, './' + app.timeT)
        averages = timeAndMassData(filterDataAMU(app, allData), allTimes, [])
        monomerAvg = timeAndMassData(monomerVal(app, allData), allTimes, [])
        dimerAvg = timeAndMassData(dimerVal(app, allData), allTimes, [])
        app.plotpoints = pointValues(app, app.criteria.getTypeSpec(), 
                                    averages, monomerAvg, dimerAvg)
        if bounds(app.plotpoints) == None or app.criteria.monomer == None:
            #Checks to see if all points are found, if not, it won't run
            app.NEdata = True
        else:
            #Plots the points
            app.NEdata = False
            app.xpos = xCoord(app)
            app.ypos = yCoord(app)
            app.positions = []
            pointCoord(app, app.plotpoints)
        
def intro_sizeChanged(app): #Makes it so you can't change the size of the screen
    app.setSize(800, 600) 

def intro_redrawAll(app, canvas):
    #Just creates the screen and all the buttons on the intro page
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'peach puff')
    canvas.create_text(app.width//2, app.height//8, 
                        text = "Mass Spectrometer Data Invertor", 
                        fill = 'black', font = 'Times 28 bold')
    app.graphb.createHomeButton(canvas)
    app.input.createHomeButton(canvas)  
    app.timeInput.createHomeButton(canvas)
    app.delayB.createHomeButton(canvas)

    #Code tells you if not enough data through testing some conditionals
    if not app.NEdata and app.reselect and app.dataT != '' and app.timeT != '':
        canvas.create_text(app.width//2, app.height//2, 
                            text = 'Select criterias to graph by', 
                            font = 'Times 20 bold', fill = 'red')
    if app.NEdata and app.criteria.ion!=None and app.criteria.typeSpec!=None:
        canvas.create_text(app.width//2, app.height//2, 
                text = "Warning!!! Not enough data to proceed with graphing",
                font = 'Times 20 bold', fill = 'red')
    #Code for creating the drop down boxes
    if not app.selectI:
        app.b.createHomeButton(canvas)
    else:
        app.selectI.createHomeButton(canvas)
    if app.dropDownI == True:
        for n in app.ionb:
            n.createHomeButton(canvas)
    if not app.selectS:
        app.specB.createHomeButton(canvas)
    else:
        app.selectS.createHomeButton(canvas)
    if app.dropDownS == True:
        for s in app.specb:
            s.createHomeButton(canvas)

def startScreen():
    runApp(width = 800, height = 600)

def main():
    startScreen()

if __name__ == '__main__':
    main()