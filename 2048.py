import rhinoscriptsyntax as rs
from random import random as r
from time import sleep
from Rhino import RhinoApp

rs.AddRectangle(rs.WorldXYPlane(),4,4)

for i in range(1,4):
    line = rs.AddLine([i,0,0],[i,4,0])
    rs.ObjectLinetype(line, 'Hidden')
    line = rs.AddLine([0,i,0],[4,i,0])
    rs.ObjectLinetype(line, 'Hidden')
    
rs.AddTextDot('<',[1,6,0])
rs.AddTextDot('^',[2,7,0])
rs.AddTextDot('>',[3,6,0])
rs.AddTextDot('v',[2,5,0])
    
rs.ZoomExtents()
winText = 0
win = 0

pts = [[0 for j in range(4)] for i in range(4)]
c = 0
d = 0
recs = [[0 for j in range(4)] for i in range(4)]
tags = [[0 for j in range(4)] for i in range(4)]
            
def fill(pts):
        a = int(r()*4)
        b = int(r()*4)
        if pts[a][b] == 0:
            if r() > 0.2:
                pts[a][b] = 2
            else:
                pts[a][b] = 4
        else:
            fill(pts)

def draw(pts):
    rs.EnableRedraw(0)
    sleep(0.05)
    RhinoApp.Wait()
    for i in range(4):
        for j in range(4):
            if recs[i][j]:
                rs.DeleteObject(recs[i][j])
            if tags[i][j]:
                rs.DeleteObject(tags[i][j])
            if pts[i][j] :
                recs[i][j] = rs.AddRectangle(rs.PlaneFromNormal((i+0.1,j+0.1,0),(0,0,1)),0.8,0.8)
                tags[i][j] = rs.AddText( pts[i][j], (i+0.5, j+0.5,0) , 0.2+(0.1/len(str(pts[i][j]))) ,'Arial',0,131074)
                if pts[i][j] <= 4:
                    rs.ObjectColor(tags[i][j],(245,245,220))
                    rs.ObjectColor(recs[i][j],(245,245,220))
                if 8 <= pts[i][j] <= 16:
                    rs.ObjectColor(tags[i][j],(245,97,0))
                    rs.ObjectColor(recs[i][j],(245,97,0))
                if 32 <= pts[i][j] <= 64:
                    rs.ObjectColor(tags[i][j],(245,7,0))
                    rs.ObjectColor(recs[i][j],(245,9,0))
                if pts[i][j] > 64:
                    rs.ObjectColor(tags[i][j],(245,197,44))
                    rs.ObjectColor(recs[i][j],(245,197,44))
    rs.EnableRedraw(1)
    
def getdir():
    dot = rs.GetObject('dir?',8192)
    dotText = rs.TextDotText(dot)
    return(dotText)

def shiftLeft(pts):
    for i in range(4):
        for k in range(3):
            if pts[k][i] == 0:
                if k == 0:
                    if pts[1][i]:
                        pts[0][i] = pts[1][i]
                        pts[1][i] = 0
                    elif pts[2][i]:
                        pts[0][i] = pts[2][i]
                        pts[2][i] = 0
                    else:
                        pts[0][i] = pts[3][i]
                        pts[3][i] = 0
                if k == 1:
                    if pts[2][i]:
                        pts[1][i] = pts[2][i]
                        pts[2][i] = 0
                    else:
                        pts[1][i] = pts[3][i]
                        pts[3][i] = 0
                if k == 2:
                    if pts[3][i]:
                        pts[2][i] = pts[3][i]
                        pts[3][i] = 0

def addLeft(pts):
    for i in range(4):
        for k in range(3):
            if pts[k][i] == pts[k+1][i]:
                pts[k][i] *= 2
                pts[k+1][i] = 0

def shiftRight(pts):
    for i in range(4):
        for k in range(3):
            if pts[3-k][i] == 0:
                if k == 0:
                    if pts[2][i]:
                        pts[3][i] = pts[2][i]
                        pts[2][i] = 0
                    elif pts[1][i]:
                        pts[3][i] = pts[1][i]
                        pts[1][i] = 0
                    else:
                        pts[3][i] = pts[0][i]
                        pts[0][i] = 0
                if k == 1:
                    if pts[1][i]:
                        pts[2][i] = pts[1][i]
                        pts[1][i] = 0
                    else:
                        pts[2][i] = pts[0][i]
                        pts[0][i] = 0
                if k == 2:
                    if pts[0][i]:
                        pts[1][i] = pts[0][i]
                        pts[0][i] = 0

def addRight(pts):
    for i in range(4):
        for k in range(3):
            if pts[3-k][i] == pts[2-k][i]:
                pts[3-k][i] *= 2
                pts[2-k][i] = 0

def shiftDown(pts):
    for i in range(4):
        for k in range(3):
            if pts[i][k] == 0:
                if k == 0:
                    if pts[i][1]:
                        pts[i][0] = pts[i][1]
                        pts[i][1] = 0
                    elif pts[i][2]:
                        pts[i][0] = pts[i][2]
                        pts[i][2] = 0
                    else:
                        pts[i][0] = pts[i][3]
                        pts[i][3] = 0
                if k == 1:
                    if pts[i][2]:
                        pts[i][1] = pts[i][2]
                        pts[i][2] = 0
                    else:
                        pts[i][1] = pts[i][3]
                        pts[i][3] = 0
                if k == 2:
                    if pts[i][3]:
                        pts[i][2] = pts[i][3]
                        pts[i][3] = 0

def addDown(pts):
    for i in range(4):
        for k in range(3):
            if pts[i][k] == pts[i][k+1]:
                pts[i][k] *= 2
                pts[i][k+1] = 0

def shiftTop(pts):
    for i in range(4):
        for k in range(3):
            if pts[i][3-k] == 0:
                if k == 0:
                    if pts[i][2]:
                        pts[i][3] = pts[i][2]
                        pts[i][2] = 0
                    elif pts[i][1]:
                        pts[i][3] = pts[i][1]
                        pts[i][1] = 0
                    else:
                        pts[i][3] = pts[i][0]
                        pts[i][0] = 0
                if k == 1:
                    if pts[i][1]:
                        pts[i][2] = pts[i][1]
                        pts[i][1] = 0
                    else:
                        pts[i][2] = pts[i][0]
                        pts[i][0] = 0
                if k == 2:
                    if pts[i][0]:
                        pts[i][1] = pts[i][0]
                        pts[i][0] = 0

def addTop(pts):
    for i in range(4):
        for k in range(3):
            if pts[i][3-k] == pts[i][2-k]:
                pts[i][3-k] *= 2
                pts[i][2-k] = 0

def checkWin(pts,win):
    for i in range(4):
        for j in range(4):
            if pts[i][j] == 2048:
                winText = rs.AddText('You Won!', (2,2,0), 0.5, 'Arial', 1, 2)
                return winText

for i in range(3):
    fill(pts)

draw(pts)


for i in range(1000):
    if win == 0:
        winText = checkWin(pts,win)
        if winText:
            win = 1
    sleep(0.2)
    RhinoApp.Wait()
    dir = getdir()
    if winText:
        rs.DeleteObject(winText)
        winText = 0
    if dir == '<':
        shiftLeft(pts)
        draw(pts)
        addLeft(pts)
        draw(pts)
        shiftLeft(pts)
        draw(pts)
    if dir == '>':
        shiftRight(pts)
        draw(pts)
        addRight(pts)
        draw(pts)
        shiftRight(pts)
        draw(pts)
    if dir == 'v':
        shiftDown(pts)
        draw(pts)
        addDown(pts)
        draw(pts)
        shiftDown(pts)
        draw(pts)
    if dir == '^':
        shiftTop(pts)
        draw(pts)
        addTop(pts)
        draw(pts)
        shiftTop(pts)
        draw(pts)
    fill(pts)
    draw(pts)