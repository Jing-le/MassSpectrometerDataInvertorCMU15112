import math, decimal
from Classes import *

def roundHalfUp(d): #Taken from cmu112
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def numConvert(n): #Code to change values into actual numbers from strings
    num = 0
    L = n.split("E")
    num += float(L[0]) * 10**float(L[1][1:])
    if math.isclose(num, roundHalfUp(num)): #Get rid of weird float values
        num = roundHalfUp(num)
    return num

def timeConvert(L):
    #Takes the time values, which are set at hours, mins, and secs and changes
    #it into minutes
    newL = ['time']
    for n in L[0]:
        if n != 'time':
            splitT = n.split(':')
            secV = int(splitT[0]) * 60 + int(splitT[1]) + float(splitT[2]) / 60
            newL.append(secV)
    L.pop(0)
    L.insert(0, newL)
    return L

def loadData(filename): #Returns data in a 2d list
    #Data calling from hw8 code
    with open(filename, "r", encoding="utf-8") as f:
        fileString = f.read()
    L = []
    firstline = True
    for line in fileString.splitlines():
        if firstline:
            firstline = False
            continue
        if line == '': #Skips any empty lines
            continue
        addL = []
        for value in line.split(","):
            if "E" in value:
                value = numConvert(value)
            addL.append(value)
        L.append(addL)
    if len(L[1]) != len(L[-1]): #Get rid of incomplete tests
        L.pop()
    while len(L[0]) != len(L[1]): #Get rid of settings without data
        L[0].pop()
    return L

def timeTable(timeData): #Filter through uploaded time data
    with open(timeData, "r", encoding="utf-8") as f:
        fileString = f.read()
    L = []
    for line in fileString.splitlines():
        for times in line.split('-'):
            L.append(times)
    minL = []
    for n in L:
        splitT = n.split(':')
        secV = int(splitT[0]) * 60 + int(splitT[1]) + int(splitT[2]) / 60
        minL.append(secV)
    return minL

def filterDataAMU(app, data): #Filters data by AMU based on which ion
    newL = []
    for col in range(len(data[0])):
        addL = []
        if data[0][col] in app.criteria.amus or data[0][col] == 'time':
            for row in range(len(data)):
                addL.append(data[row][col])
            newL.append(addL)
    newT = ['time']
    for n in newL[0]: #Converts time values to minutes
        if n != 'time':
            splitT = n.split(':')
            secV = int(splitT[0]) * 60 + int(splitT[1]) + float(splitT[2]) / 60
            newT.append(secV)
    newL.pop(0) #Removes old list and puts in new one
    newL.insert(0, newT)
    for r in range(len(newL)): #To leave only numbers
        newL[r].pop(0)
    return newL

def filterTime(data): #Filter from whole data set
    timeList = []
    for row in range(1, len(data)):
        timeList.append(data[row][0])
    minL = []
    for n in timeList:
        splitT = n.split(':')
        secV = int(splitT[0]) * 60 + int(splitT[1]) + float(splitT[2]) / 60
        minL.append(secV)
    return minL

def timeRanges(data, timeFile):
    #This compares the time values that are inputted with the time values from 
    #the data set. It then gives you the numbers that are the closest to what
    #the desired times are
    inTime = timeTable(timeFile)
    times = filterTime(data)
    bestTimes = []
    bestD = math.inf
    bestT = 0
    for n1 in inTime:
        for n2 in times:
            value = abs(n2-n1)
            if value < bestD:
                bestD = value
                bestT = n2
        bestD = math.inf
        bestTimes.append(bestT)
    return bestTimes

def aveCol(L):
    #Code averages all the columns to use in the plotting data
    rows, cols = len(L), len(L[0])
    rL = []
    for col in range(1, cols):
        value = 0
        for row in range(rows):
            value += L[row][col]
        value /= rows
        rL.append(value)
    return sum(rL)

def timeAndMassData(AMUlist, ranges, sortL):
    #Code gives the inbetween of the time values plus the ends. I want to find 
    #the values in between two time ranges and this code separates the original
    #data list to do that
    if ranges == []:
        return sortL
    else:
        nList = []
        for i in range(len(AMUlist[0])):
            if ranges[0] <= AMUlist[0][i] <= ranges[1]:
                eList = []
                for r in range(len(AMUlist)):
                    eList.append(AMUlist[r][i])
                nList.append(eList)
        sortL.append(aveCol(nList))
        return timeAndMassData(AMUlist, ranges[2:], sortL)

def monomerVal(app, data): 
    #Finds the monomer value for the ion and sorts it based on their amus
    monomerL = []
    for col in range(len(data[0])):
        addL = []
        if data[0][col] in app.criteria.monomer or data[0][col] == 'time':
            for row in range(len(data)):
                addL.append(data[row][col])
            monomerL.append(addL)
    monomer = timeConvert(monomerL)
    for n in range(len(monomer)):
        monomer[n].pop(0)
    return monomer

def dimerVal(app, data):
    #Finds the dimer values for the ion and sorts it based on amus
    dimerL = []
    for col in range(len(data[0])):
        addL = []
        if data[0][col] in app.criteria.dimer or data[0][col] == 'time':
            for row in range(len(data)):
                addL.append(data[row][col])
            dimerL.append(addL)
    dimer = timeConvert(dimerL)
    for n in range(len(dimer)):
        dimer[n].pop(0)

    return dimer

def pointValues(app, z, averages, m, d):
    #Equations to find what the points are
    tcl = 5/(2.32*80)
    k = app.criteria.reagent
    L = []
    for i in range(len(averages)):
        monomer = (1/(z*k*tcl))*(m[i]/averages[i])
        dimer = (1/(z*k*tcl))*(d[i]/averages[i])
        L.append((monomer, dimer))
    return L

def bounds(data):#Code to find the min and max of each axis
    maxX = 0
    minX = math.inf
    maxY = 0
    minY = math.inf
    for point in data:
        #Need all if statements to check each individual one
        if point[0] > maxX:
            maxX = point[0]
        if point[0] < minX:
            minX = point[0]
        if point[1] > maxY:
            maxY = point[1]
        if point[1] < minY:
            minY = point[1]
    if math.isclose(minY, maxY): #If insufficient data
        return None
    return minX, maxX, minY, maxY

def xAxis(minX, maxX):
    #Creates the axis on the graph. Done by finding intervals
    stepVal = (maxX - minX)/5
    val = minX
    L = []
    for n in range(7):
        val += stepVal
        L.append(val)
    L.insert(0, minX)
    return L

def yAxis(minY, maxY):
    #Same thing as the one above
    stepVal = (maxY - minY)/4
    val = minY
    L = []
    for n in range(6):
        val += stepVal
        L.append(val)
    L.insert(0, minY)
    return L

def sciNot(n):
    #Converts numbers into scientific notation
    n = int(n)
    times = 0
    while len(str(n)) > 2:
        n//=10
        times += 1
    return f'{n}e+{times}'

def pointsLinex(app):
    #Find the correct axis points to display later
    newL = []
    minX, maxX, minY, maxY = bounds(app.plotpoints)
    L = xAxis(minX, maxX)
    for val in L:
        val = sciNot(val)
        newL.append(val)
    return newL

def pointsLiney(app):
    #Same thing as the one above
    newL = []
    minX, maxX, minY, maxY = bounds(app.plotpoints)
    L = yAxis(minY, maxY)
    for val in L:
        val = sciNot(val)
        newL.append(val)
    return newL

def leastSquare(app):
    #Code to solve the least square regression method
    points = app.positions
    n = len(points)
    sumxy = 0
    sumx = 0
    sumy = 0
    sumx2 = 0
    for p in points:
        sumxy += p[0] * p[1]
        sumx += p[0]
        sumy += p[1]
        sumx2 += p[0]**2
    m = ((n*sumxy)-(sumx*sumy))/((n*sumx2)-sumx**2)
    b = (sumy - (m*sumx))/n
    return m, b