from cmu_112_graphics import *

class SpecSettings:
    #A class to set certain variables based on the selected settings
    def __init__(self, ion, typeSpec):
        self.ion = ion
        self.typeSpec = typeSpec
        self.amus = None
        self.reagent = None

    def addAMUs(self):
        #All preset values when someone chooses a setting
        if self.ion == "Nitrate":
            self.amus = {'160.0 amu', '195.0 amu', '62.0 amu', '80.0 amu', '125.0 amu'}
            self.monomer = {'97.0 amu', '160.0 amu'}
            self.dimer = {'195.0 amu'}
            self.reagent = 1.9e-9
        elif self.ion == "Acetate":
            self.amus = {'97.0 amu', '195.0 amu', '59.0 amu', '77.0 amu', '119.0 amu'}
            self.monomer = {'97.0 amu'}
            self.dimer = {'195.0 amu'}
            self.reagent = 1.9e-9
    
    def getTypeSpec(self):
        if self.typeSpec == 'MCC':
            return 1
        elif self.typeSpec == 'PCC':
            return 2

'''Button class to allow for creation of all types of buttons for use in project
The input requires what you want to display for the button, color/textcolor, 
what you want it to do, and its position.'''

class Buttons:
    def __init__(self, text, color, tColor, function, x, y, w, h):
        self.text = text
        self.color = color
        self.function = function
        self.tColor = tColor
        self.bounds = []
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def createHomeButton(self, canvas):
        #Specific for the buttons I want on the intro screen
        w = self.w
        h = self.h
        x, y = self.x, self.y
        canvas.create_rectangle(x-w, y-h, x+w, y+h, fill = self.color)
        canvas.create_text(x, y, text = self.text, fill = self.tColor, 
                            font = 'Times 15')

    def createGraphButton(self, canvas):
        w = self.w
        h = self.h
        x, y = self.x, self.y
        canvas.create_rectangle(x-w, y-h, x+w, y+h, fill=self.color, width=2)
        canvas.create_text(x, y, text = self.text, fill = self.tColor, 
                            font = 'Times 12')

    def inBounds(self, x, y):
        #To check if you click within the button
        w, h, = self.w, self.h
        return self.x-w<x<self.x+w and self.y-h<y<self.y+h

    def doFunction(self, app):
        #An easy way to keep adding functions into this function so it does
        #what you want
        if self.function == 'dropDownI':
            self.dropDownI(app)
        elif self.function == 'dropDownS':
            self.dropDownS(app)
        elif self.function == 'returnHome':
            self.returnHome(app)
        elif self.function == 'backGraph':
            self.backGraph(app)
        elif self.function == 'reveal':
            self.reveal(app)

    def dropDownI(self, app):
        #Code to specifically create dropdown menu for ions. Easy to add more
        b1 = Buttons('Nitrate', 'dim gray', 'white', 'selectI', 
                    self.x, self.y+app.height//9, self.w, self.h)
        b2 = Buttons('Acetate', 'dim gray', 'white', 'selectI', 
                    self.x, self.y+2*app.height//9, self.w, self.h)
        app.ionb.append(b1)
        app.ionb.append(b2)
    
    def dropDownS(self, app):
        #Like code above
        spec1 = Buttons('MCC', 'dim gray', 'white', 'selectS', 
                    self.x, self.y+app.height//9, self.w, self.h)
        spec2 = Buttons('PCC', 'dim gray', 'white', 'selectS', 
                    self.x, self.y+2*app.height//9, self.w, self.h)
        app.specb.append(spec1)
        app.specb.append(spec2)

    def returnHome(self, app): #Changes screens back to home
        app.mode = 'intro'
        app.positions = []

    def backGraph(self, app): #Returns from the zoom graph to normal graph
        app.run = True
        app.newP = []
        app.ix, app.iy, app.zx, app.zy = (0, 0, 0, 0)
    
    def reveal(self, app): #Shows instructions/features
        if app.instr == True:
            app.instr = False
        else:
            app.instr = True

    def select(self): #Selects the button variable
        return self.text