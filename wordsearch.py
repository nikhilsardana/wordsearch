import numpy as np
import math

def forward(grid, startx, starty, wl, numr, numc):
  wend = startx+wl-1
  if(wend>=numr):
    return
  else:
    return ''.join(grid[starty][startx:wend+1])

def backward(grid, startx, starty, wl, numr, numc):
  wend = startx-wl+1
  if(wend<0):
    return
  else:
    return ''.join(grid[starty][wend:startx+1])[::-1]

def diag(grid, startx, starty, wl, numr, numc):
  lst = [""]*4
  leftx = startx-wl+1
  rightx = startx+wl-1
  upy = starty-wl+1
  downy = starty+wl-1
  if(leftx>=0 and upy>=0):
    for i in range(0, wl):
        lst[0]+=grid[startx-i][starty-i]

  if(leftx>=0 and downy<numc):
    for i in range(0, wl):
        lst[1]+=grid[startx-i][starty+i]

  if(rightx<numr and upy>=0):
    for i in range(0, wl):
        lst[2]+=grid[startx+i][starty-i]

  if(rightx<numr and downy<numc):
    for i in range(0, wl):
        lst[3]+=grid[startx+i][starty+i]

  return lst

def getwords(grid, minw, maxw, numr, numc):
  lst  = []
  coord = []
  for k in range(minw, maxw+1):
    for i in range(numcols):
      for j in range(numrows):

        out, c = forward(grid, i, j, k, numr, numc)
        if not (out==None):
          lst.append(out)
          coord.append(c)

        out, c = backward(grid, i, j, k, numr, numc)
        if not (out==None):
          lst.append(out)
          coord.append(c)
  return lst

def diagwords(grid, minw, maxw, numr, numc):
  lst = []
  for k in range(minw, maxw+1):
    for i in range(numcols):
      for j in range(numrows):
        out = diag(grid, i, j, k, numr, numc)
        for q in out:
          if not (q==""):
            lst.append(q)

  return lst

#############################
# Create Dictionary
#############################

d = {}
with open("english.txt") as f:
    for line in f:
       key = line.split()
       d[key[0].rstrip()] = 1 # all words set to value of 1

with open("addendum.txt") as f:
	for line in f:
		key = line.split()
		d[key[0].rstrip()] = 1


with open("formatted.txt") as f:
  letters = f.readlines()

letters = [x.rstrip() for x in letters]
grid = [list(x) for x in letters]
print(grid)
print("-----------------------------------")
gridT = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))] 
print(gridT)

minw = 4
maxw = 10
numrows = len(grid)
numcols = len(grid[0])

fb = getwords(grid, minw, maxw, numrows, numcols)
ud = getwords(gridT, minw, maxw, numcols, numrows)
di = diagwords(grid, minw, maxw, numrows, numcols)

full = fb+ud+di

found = []
for word in full:
  if word.lower() in d:
    found.append(word)

print(found)
