from cmu_112_graphics import *
from SortDataCode import *
from Classes import *

def pointCoord(app, points):
    #Code to produce the sets of points that will be graphed initially
    minX, maxX, minY, maxY = bounds(points)
    x0, y0 = (app.width/app.ibx, app.height/app.iby)
    x1, y1 = (app.width - x0, app.height - y0)
    porp = []
    for p in points:
        #Code to scale points to fractional values
        newx = (p[0]-minX)/(maxX-minX)
        newy = (p[1]-minY)/(maxY-minY)
        porp.append((newx, newy))
    for np in porp:
        #Code to actually relate that to the graph in the center
        fx = np[0]*(x1-x0) + x0
        fy = np[1]*(y0-y1) + y1
        if (app.width//8 < fx < app.width - (app.width//8) and 
            app.height//8 < fy < app.height - (app.height//8)):
            app.positions.append((fx, fy))

def xCoord(app):
    #Scales point values onto the x axis
    minX, maxX, minY, maxY = bounds(app.plotpoints)
    x0, x1 = app.width/app.ibx, app.width - (app.width/app.ibx)
    places = xAxis(minX, maxX)
    L = []
    for p in places:
        np = ((p - minX) / (maxX-minX)) * (x1-x0) + x0
        if app.width//8 < np < app.width - (app.width//8):
            L.append(np)
    return L

def yCoord(app):
    #Does the same thing as one above
    minX, maxX, minY, maxY = bounds(app.plotpoints)
    y0, y1 = app.height/app.iby, app.height - (app.height/app.iby)
    places = yAxis(minY, maxY)
    L = []
    for p in places:
        np = ((p - minY) / (maxY-minY)) * (y0-y1) + y1
        if app.height//8 < np < app.height - (app.height//8):
            L.append(np)
    return L

def convert(app, p, points):
    #Takes in point values that lie on the graph and convert them back into the
    #values they were before graphing
    minX, maxX, minY, maxY = bounds(points)
    x0, y0 = (app.width/app.ibx,app.height/app.iby)
    x1, y1 = (app.width - x0, app.height - y0)
    newx = roundHalfUp(((p[0]-x0)/(x1-x0))*(maxX-minX)+minX)
    newy = roundHalfUp(((p[1]-y1)/(y0-y1))*(maxY-minY)+minY)
    return f'({newx}, {newy})'

def drawSquare(app, canvas):
    #Draws a square based on where you drag the mouse. Used to visualize the
    #zoom feature
    x0, y0 = (app.ix, app.iy)
    x1, y1 = (app.zx, app.zy)
    canvas.create_rectangle(x0, y0, x1, y1, fill = '')

def drawPoints(app, canvas, r, x, y):
    #Code to draw any kind of point onto the graph   
    canvas.create_oval(x-r, y-r, x+r, y+r, fill = 'blue', width = 0)

def zoom(app):
    #Graphs a new plot of points based on the bounds of the new drawn box
    zx0, zy0 = app.ix, app.iy
    zx1, zy1 = app.fx, app.fy
    zx0, zx1 = min(zx0, zx1), max(zx0, zx1)
    zy0, zy1 = max(zy0, zy1), min(zy0, zy1)
    cP = []
    for points in app.positions:
        #Finds the points that actually are in the box.
        if (zx0<=points[0]<=zx1 and zy1<=points[1]<=zy0):
            cP.append((points[0], points[1]))
    x0, x1, y0, y1 = app.x0, app.x1, app.y0, app.y1
    for p in cP:
        #Very similar to pointCoord, but just scales based on drawn box
        newX = ((p[0]-zx0)/(zx1-zx0))*(x1-x0) + x0
        newY = ((p[1]-zy0)/(zy1-zy0))*(y0-y1) + y1
        app.newP.append((newX, newY))

def drawZoomCoord(app, canvas):
    #Code is used to draw the bounds of the new zoomed in graph. Only shows the
    #endpoints of the graphs
    zx0, zy0 = app.ix, app.iy
    zx1, zy1 = app.fx, app.fy
    zx0, zx1 = min(zx0, zx1), max(zx0, zx1)
    zy0, zy1 = max(zy0, zy1), min(zy0, zy1)
    minX, maxX, minY, maxY = bounds(app.plotpoints)
    x0, y0 = (app.width/app.ibx,app.height/app.iby)
    x1, y1 = (app.width - x0, app.height - y0)
    L = [(zx0, zy0), (zx1, zy1)]
    newL = []
    for point in L:
        newx = sciNot(roundHalfUp(((point[0]-x0)/(x1-x0))*(maxX-minX)+minX))
        newy = sciNot(roundHalfUp(((point[1]-y1)/(y0-y1))*(maxY-minY)+minY))
        newL.append((newx, newy))
    canvas.create_text(app.width//8, app.height - (app.height//8) + app.r*2, 
                        text = newL[0][0])
    canvas.create_text(app.width//8 - app.r*5, app.height - (app.height//8)
                        -app.r, text = newL[0][1])
    canvas.create_text(app.width - (app.width//8), app.height - (app.height//8)
                        + app.r*2, text = newL[1][0])
    canvas.create_text(app.width//8 - app.r*4, app.height//8, text = newL[1][1])
    
def within(app, point, x, y):
    #Code to check if mouse is within the point value
    cx = point[0]
    cy = point[1]
    return (((cx - x)**2 + (cy - y)**2)**0.5 <= app.r)

def drawNotchx(app, canvas, x, text):
    #Draw the notches in the graph plus the number value there
    y = app.height
    canvas.create_line(x, y - (y//8), x, y-(y//8)-app.r*2, fill = 'black')
    canvas.create_text(x, y - (y//8) + 2*app.r, text = text)

def drawNotchy(app, canvas, y, text):
    #Same as the function above
    x = app.width//8
    canvas.create_line(x, y, x + app.r*2, y, fill = 'black')
    canvas.create_text(x-app.r*5, y, text = text)

def drawLOBF(app, canvas):
    #Code to draw line of best fit. Will remove the drawn line if out of bounds
    m, b = leastSquare(app)
    x0 = app.width//8
    y0 = m*(x0) + b
    if y0 > app.height - app.height//8:
        y0 = app.height - app.height//8
        x0 = (y0-b)/m
    x1 = app.width - app.width//8
    y1 = m*(x1) + b
    if y1 < app.height//8:
        y1 = app.height//8
        x1 = (y1-b)/m
    canvas.create_line(x0, y0, x1, y1)

def graph_keyPressed(app, event):
    if event.key == 'Space' and app.run == True: #Allows you to zoom in
        zoom(app)
        app.run = False
    elif event.key == 'Left':
        app.ibx -= 0.5
        if app.ibx == 2.5: #Needed so the graph doesn't reverse
            app.ibx += 0.5
        app.positions = []
        pointCoord(app, app.plotpoints)
        app.xpos = xCoord(app)
    elif event.key == 'Right':
        app.ibx += 0.5
        app.positions = []
        pointCoord(app, app.plotpoints)
        app.xpos = xCoord(app)
    elif event.key == 'Up':
        app.iby -= 0.5
        if app.iby == 2: #Needed so graph doesn't reverse
            app.iby += 0.5
        app.positions = []
        pointCoord(app, app.plotpoints)
        app.ypos = yCoord(app)
    elif event.key == 'Down':
        app.iby += 0.5
        app.positions = []
        pointCoord(app, app.plotpoints)   
        app.ypos = yCoord(app)
    elif event.key == 'n': #Code to turn the line of best fit on and off
        if app.lobf == True:
            app.lobf = False
        else:
            app.lobf = True
    elif event.key == 'r': #Resets positions back to original
        app.positions = []
        app.iby = 6
        app.ibx = 6
        pointCoord(app, app.plotpoints)
        app.xpos = xCoord(app)
        app.ypos = yCoord(app)

def graph_mousePressed(app, event):
    #Sets initial coordinates for drawing the box
    if app.x0<=event.x<=app.x1 and app.y0 <=event.y<=app.y1:
        app.ix = event.x
        app.iy = event.y
        app.zx = event.x
        app.zy = event.y
    #The code block here is just for button pressing
    elif app.homeButton.inBounds(event.x, event.y):
        app.homeButton.doFunction(app)
        app.positions = []
    elif app.backZoom.inBounds(event.x, event.y):
        app.backZoom.doFunction(app)
    elif app.instrB.inBounds(event.x, event.y):
        app.instrB.doFunction(app)

def graph_mouseReleased(app, event):
    #Used for the bounds of the zoomed box
    if app.x0<=event.x<=app.x1 and app.y0 <=event.y<=app.y1:
        app.fx = event.x
        app.fy = event.y

def graph_mouseDragged(app, event):
    #Need the zx value to draw the box at each interval
    if app.x0<=event.x<=app.x1 and app.y0 <=event.y<=app.y1:
        app.zx = event.x
        app.zy = event.y 

def graph_mouseMoved(app, event):
    #All this code is just to check if mouse is within so it can display the pts
    for p in app.positions:
        if within(app, p, event.x, event.y):
            app.pPrint = p
            return
        elif not within(app, p, event.x, event.y):
            app.pPrint = None
    for pz in app.newP:
        if within(app, pz, event.x, event.y):
            app.pPrint = pz
            return
        elif not within(app, pz, event.x, event.y):
            app.pPrint = None

def graph_sizeChanged(app):
    #If the screen gets dragged in any way, the graph will still look right
    app.positions = []
    pointCoord(app, app.plotpoints)
    app.setSize(800, 600)

def graph_redrawAll(app, canvas):
    x, y = (app.width, app.height)
    #Creates intial page look. Also remains like that the entire time
    canvas.create_rectangle(0, 0, x, y, fill = 'cornsilk2')
    canvas.create_rectangle(x//8, y//8, x-(x//8), y-(y//8), fill = 'white', 
                            outline = 'black', width = app.r//2)
    canvas.create_text(x//2, y - y//20, 
    text = 'Sulfuric acid monomer concentration, [N1](cm3)', font = 'Times 15',)
    canvas.create_text(x//25, y//2, 
    text = 'Sulfuric acid dimer concentration, [N2](cm3)', font = 'Times 15', 
    angle = 90)
    if app.run:
        #Code draws the original graph onto the screen
        #Also allow the user to draw boxes
        app.homeButton.createGraphButton(canvas)
        app.instrB.createGraphButton(canvas)
        canvas.create_text(app.width//6, app.height//20, 
            text = f'Settings: {app.criteria.ion} with {app.criteria.typeSpec}'
            , font = 'Times 15 bold')
        for points in app.positions:
            x = points[0]
            y = points[1]
            drawPoints(app, canvas, app.r, x, y)
        for px in range(len(app.xpos)):
            drawNotchx(app, canvas, app.xpos[px], pointsLinex(app)[px])
        for py in range(len(app.ypos)):
            drawNotchy(app, canvas, app.ypos[py], pointsLiney(app)[py])
        drawSquare(app, canvas)
        if app.lobf:
            drawLOBF(app, canvas)
        if app.pPrint != None: #Displays the point value
            canvas.create_rectangle(app.pPrint[0]-13*app.r, 
                                    app.pPrint[1]+0.5*app.r,
                                    app.pPrint[0]+17*app.r, 
                                    app.pPrint[1]+4*app.r,
                                    fill = 'white')
            canvas.create_text(app.pPrint[0]+2*app.r, app.pPrint[1]+2*app.r, 
                                text = convert(app,app.pPrint,app.plotpoints),
                                font = 'Times 10 bold')
    
    else:
        #Displays the zoomed graph
        app.instrB.createGraphButton(canvas)
        app.backZoom.createGraphButton(canvas)
        for point in app.newP:
            x = point[0]
            y = point[1]
            drawPoints(app, canvas, app.r, x, y)
        drawZoomCoord(app, canvas)
        if app.pPrint != None:
            canvas.create_rectangle(app.pPrint[0]-13*app.r, 
                                    app.pPrint[1]+0.5*app.r,
                                    app.pPrint[0]+17*app.r, 
                                    app.pPrint[1]+4*app.r,
                                    fill = 'white')
            canvas.create_text(app.pPrint[0]+2*app.r, app.pPrint[1]+2*app.r, 
                                text = convert(app,app.pPrint,app.plotpoints),
                                font = 'Times 10 bold')  

    if app.instr: #Code for the instructions
        canvas.create_rectangle(app.width//2 - app.width//4, 
                                app.height//2 - app.width//6,
                                app.width//2 + app.width//4, 
                                app.height//2 + app.width//6,
                                fill = 'sandy brown')
        canvas.create_text(app.width//2, app.height//2-app.width//7,
                text = "Use the arrow keys to stretch and compress the graph")
        canvas.create_text(app.width//2, app.height//2+app.width//7,
                        text = 'Click on button again to remove instructions')
        canvas.create_text(app.width//2, 
                            app.height//2-app.width//7+app.width//25, 
            text = 'Drag the cursor over a section of the graph to zoom into.')
        canvas.create_text(app.width//2, 
                        app.height//2-app.width//7+app.width//18, 
                        text = 
            '''Once satisfied with your selection, press 'space' to zoom in''')
        canvas.create_text(app.width//2, 
                            app.height//2-app.width//7+app.width//12,
                            text = 'Hover over points to see their values')
        canvas.create_text(app.width//2,app.height//2-app.width//7+app.width//9,
                            text = 'Press "n" to show Line of Best Fit')
        canvas.create_text(app.width//2,app.height//2, text =
                        'Press "r" to reset to original coordinate positions')