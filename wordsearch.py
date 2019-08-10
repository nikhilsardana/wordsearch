import numpy as np
import math
import argparse

#####################################
# Argument Parser
#####################################

parser = argparse.ArgumentParser(description='Optional app description')
# Optional arguments
parser.add_argument('--min', type=int, default=4,
                    help='Minimum word length')

parser.add_argument('--max', type=int, default=50,
                    help='Maximum word length')

# Switch
parser.add_argument('--addonly', action='store_true',
                    help='Only use addendum text file as dictionary')

parser.add_argument('--common', action='store_true',
                    help='Use dictionary of common English words only.')

parser.add_argument('--useall', action='store_true',
                    help='Show all found words. May be helpful when paired with --addonly.')

parser.add_argument('--fontsize', type=int, default=-1,
                    help='Font size for displaying word search letters.')

args = parser.parse_args()

####################################
# Find all possible wordsearch words
####################################

def forward(grid, startx, starty, wl, nr, nc):
  wend = startx+wl-1
  if(wend>=nc):
    return None, None
  else:
    return ''.join(grid[starty][startx:wend+1]), [[starty, i] for i in range(startx, wend+1)]

def backward(grid, startx, starty, wl, nr, nc):
  wend = startx-wl+1
  if(wend<0):
    return None, None
  else:
    return ''.join(grid[starty][wend:startx+1])[::-1], [[starty, i] for i in range(wend, startx+1)]

def diag(grid, startx, starty, wl, nr, nc):
  lst = [""]*4
  clist = [[],[],[],[]]
  leftx = startx-wl+1
  rightx = startx+wl-1
  upy = starty-wl+1
  downy = starty+wl-1
  if(leftx>=0 and upy>=0):
    for i in range(0, wl):
        lst[0]+=grid[starty-i][startx-i]
        clist[0].append([starty-i, startx-i])

  if(leftx>=0 and downy<nr):
    for i in range(0, wl):
        lst[1]+=grid[starty+i][startx-i]
        clist[1].append([starty+i, startx-i])

  if(rightx<nc and upy>=0):
    for i in range(0, wl):
        lst[2]+=grid[starty-i][startx+i]
        clist[2].append([starty-i, startx+i])

  if(rightx<nc and downy<nr):
    for i in range(0, wl):
        lst[3]+=grid[starty+i][startx+i]
        clist[3].append([starty+i, startx+i])

  return lst, clist

def getwords(grid, minw, maxw, nr, nc):
  lst  = []
  coords = []
  for k in range(minw, maxw+1):
    for i in range(nc):
      for j in range(nr):

        out, c = forward(grid, i, j, k, nr, nc)
        if not (out==None):
          lst.append(out)
          coords.append(c)

        out, c = backward(grid, i, j, k, nr, nc)
        if not (out==None):
          lst.append(out)
          coords.append(c)
  return lst, coords

def diagwords(grid, minw, maxw, nr, nc):
  lst = []
  coords = []
  for k in range(minw, maxw+1):
    for i in range(nc):
      for j in range(nr):
        out, c = diag(grid, i, j, k, nr, nc)
        for q in range(len(out)):
          if not (out[q]==""):
            lst.append(out[q])
            coords.append(c[q])

  return lst, coords

#############################
# Create Dictionary
#############################

d = {}
if not args.addonly:
  if args.common:
      with open("common.txt") as f:
        for line in f:
            key = line.split()
            d[key[0].rstrip().lower()] = 1 # all words set to value of 1
  else:
    with open("english.txt") as f:
        for line in f:
            key = line.split()
            d[key[0].rstrip().lower()] = 1 # all words set to value of 1

with open("addendum.txt") as f:
    for line in f:
        key = line.split()
        if(len(key)>0):
            d[key[0].rstrip().lower()] = 1

with open("formatted.txt") as f:
  letters = f.readlines()

letters = [x.rstrip() for x in letters]
letters = [x for x in letters if len(x)>0]
grid = [list(x) for x in letters]
gridT = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

minw = args.min
maxw = max(len(grid), len(grid[0]))
maxw = args.max
numrows = len(grid)
numcols = len(grid[0])

################################################
# Create list of all possible wordsearch strings
# of length between min and max, inclusive
#################################################
fb, coordfb = getwords(grid, minw, maxw, numrows, numcols)
ud, coordud = getwords(gridT, minw, maxw, numcols, numrows)
di, coorddi = diagwords(grid, minw, maxw, numrows, numcols)

#Flip coordinates because of transposed grid
#After flip, max = 20 19
for x in coordud:
    for k in range(len(x)):
        tmp0 = x[k][0] 
        tmp1 = x[k][1]
        x[k][0] = tmp1
        x[k][1] = tmp0

full = fb+ud+di
fullcoord = coordfb+coordud+coorddi

found = []
foundcoord = []
for w in range(len(full)):
  if full[w].lower() in d:
    found.append(full[w])
    foundcoord.append(fullcoord[w])

found = [f.upper() for f in found]

Z = [x for _,x in sorted(zip(found,foundcoord))]
found = sorted(found)
unique = set()
ucoords = []

######################################
# Write intermediate outputs to files
######################################

f = open("intermediate/found.txt", "w")
#print("Found the following words:")
for i in range(len(found)):
  word = found[i]
  if not word in unique:
    unique.add(word)
    ucoords.append(Z[i])
    f.write(word)
    f.write("\n")
    #print(word) 
f.close()

f = open("intermediate/coord.txt", "w")
for c in ucoords:
  f.write(str(c))
  f.write("\n")
f.close()

########################
# Gui and Visualization
#########################
from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import ast


with open("intermediate/found.txt") as f:
  mywords = f.readlines()

with open("intermediate/coord.txt") as f:
  coords = f.readlines()

coords = [x.rstrip() for x in coords]
mywords = [x.rstrip() for x in mywords]

indices = []
if not args.useall:
  main = Tk()
  main.title("Multiple Choice Listbox")
  main.geometry("+50+150")
  frame = ttk.Frame(main, padding=(3, 3, 12, 12))
  frame.grid(column=0, row=0, sticky=(N, S, E, W))

  tot = ""
  for x in mywords:
    tot+=x
    tot+=" "
  options = StringVar()
  options.set(tot)

  lstbox = Listbox(frame, listvariable=options, selectmode=MULTIPLE, width=40, height=20)
  lstbox.grid(column=0, row=0, columnspan=2)

  print("Showing:")
  def select():
      reslist = list()
      selection = lstbox.curselection()
      for i in selection:
          enter = lstbox.get(i)
          reslist.append(enter)
      for val in reslist:
          print(val)
          indices.append(mywords.index(val))

  btn = ttk.Button(frame, text="Choose", command=select)
  btn.grid(column=1, row=1)
  main.mainloop()


###################################
# Visualize selected words on
# matplotlib version of wordsearch.
###################################
if args.useall:
  indices = np.arange(0, len(mywords))
  print("Looking for:")
  for k in mywords:
    print(k)

with open("formatted.txt") as f:
  wordsearch = f.readlines()

wordsearch = [x.rstrip() for x in wordsearch]
wordsearch = [x for x in letters if len(x)>0]
grid = [list(x) for x in wordsearch]
gmap = np.zeros((len(grid), len(grid[0])))

for i in indices:
  coo = ast.literal_eval(coords[i])
  xr = max(np.random.random(),0.2)
  for c in coo:
    gmap[c[0]][c[1]] += xr

fig, ax = plt.subplots()
min_val = 0
max_valx = len(grid[0])
max_valy = len(grid)

ax.matshow(gmap, cmap=plt.cm.Set3)
for i in range(max_valx):
    for j in range(max_valy):
        if(args.fontsize>0):
            ax.text(i, j, grid[j][i], va='center', ha='center', fontsize=args.fontsize)
        else:
            ax.text(i, j, grid[j][i], va='center', ha='center')


plt.show()
