import argparse
import os.path

from pyx import *

__author__ = "Christopher O'Neill"
__version__ = "$0.1a $"
__date__ = "$Date: 2018/06/18 14:00:00 $"
__copyright__ = "Copyright (c) 2018 Christopher O'Neill"
__license__ = "GPLv2"

#######################################
########## Class definitions ##########
#######################################

class Vector(object):
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
		
	def __add__(self, v):
		if (type(v) == Vector):
			return Vector(self.x + v.x, self.y + v.y)
		else:
			return self.arr() + v
	
	def __sub__(self, v):
		return Vector(self.x - v.x, self.y - v.y)
	
	def __mul__(self, d):
		return Vector(self.x * d, self.y * d)
	
	def arr(self):
		return [self.x, self.y]
	
	def __repr__(self):
		return str(self.x) + ',' + str(self.y)


####################################
########## Global defines ##########
####################################

# block size
# this assumes '--zaxis out', program will 
# change these automatically for '--zaxis up'
(dx, dy, dz) = (Vector(2,0), Vector(0,2), Vector(-1,-1))

# radius of marker circles
dr = 0.2

# face colors
# (xcol, ycol, zcol) = ('#8e8e8e', '#efefef', '#bebebe')

# extension of axis labels, in block units
axesextra = 0

# width of the edges of the buchberger graph
buchwidth = 0.10


######################################
################ Code ################
######################################

xlabelbump = Vector(0,-12)
ylabelbump = Vector(2,-12)
zlabelbump = Vector(2,12)

UPPERLEFT = 1
UPPERRIGHT = 2
LOWERLEFT = 3
LOWERRIGHT = 4
CENTER = 9

parser = argparse.ArgumentParser(description='Draw the staircase diagram for a given monomial ideal')
parser.add_argument('filenames', metavar='filename', type=str, nargs='+', help='file containing the monomial generators of an ideal')

parser.add_argument('-b', '--buchberger', action='store_true', help='draw the buchberger graph')
parser.add_argument('-v', '--verbose', action='count')
parser.add_argument('-z', '--zaxis', choices=['up', 'out', 'right'], default='out', help='direction for the z-axis')

parser.add_argument('-cf', '--front-color', action='store', default='#bebebe', help='color of front faces')
parser.add_argument('-cs', '--side-color', action='store', default='#8e8e8e', help='color of side faces')
parser.add_argument('-ct', '--top-color', action='store', default='#efefef', help='color of top faces')

parser.add_argument('--nolabels', action='store_true', help='don\'t draw generator labels')

args = parser.parse_args()


(xcol, ycol, zcol) = (args.side_color, args.top_color, args.front_color)

if (args.zaxis == 'up'):
	(dx,dy,dz) = (dz,dx,dy)
	(xcol,ycol,zcol) = (zcol,xcol,ycol)
	(xlabelbump, ylabelbump, zlabelbump) = (zlabelbump, xlabelbump, ylabelbump)
elif (args.zaxis == 'right'):
	(dx,dy,dz) = (dy,dz,dx)
	(xcol,ycol,zcol) = (ycol,zcol,xcol)
	(xlabelbump, ylabelbump, zlabelbump) = (ylabelbump, zlabelbump, xlabelbump)

xcolr = int(xcol[1:3],16)/255.0
xcolg = int(xcol[3:5],16)/255.0
xcolb = int(xcol[5:7],16)/255.0

ycolr = int(ycol[1:3],16)/255.0
ycolg = int(ycol[3:5],16)/255.0
ycolb = int(ycol[5:7],16)/255.0

zcolr = int(zcol[1:3],16)/255.0
zcolg = int(zcol[3:5],16)/255.0
zcolb = int(zcol[5:7],16)/255.0

for filename in args.filenames:
	# read file
	f = open(filename, 'r')
	lines = f.readlines()
	f.close()
	
	(outfile, ext) = os.path.splitext(filename)
	svgfile = outfile + '.svg'
	pdffile = outfile + '.pdf'
	
	# parse file contents
	gens = []
	try:
		for line in lines:
			line = line.rstrip()
			if (len(line) == 0):
				continue
			g = [int(elem) for elem in line.split(' ')]
			if (len(g) != 3 or g[0] < 0 or g[1] < 0 or g[2] < 0):
				raise
			gens.append(g)
	except:
		print 'Error in file %s: %s' % (filename, line)
		continue
	
	if (args.verbose > 0):
		print 'Current ideal: ' + str(gens)
	
	# find bounds
	isartinian = [0, 0, 0]
	maxdeg = [0, 0, 0]
	
	for g in gens:
		maxdeg[0] = max(maxdeg[0], g[0])
		maxdeg[1] = max(maxdeg[1], g[1])
		maxdeg[2] = max(maxdeg[2], g[2])
		
		if (g[0] == 0 and g[1] == 0):
			isartinian[2] = 1;
		if (g[0] == 0 and g[2] == 0):
			isartinian[1] = 1;
		if (g[1] == 0 and g[2] == 0):
			isartinian[0] = 1;

	maxdeg[0] += ((not isartinian[0]) * 3) + 1
	maxdeg[1] += ((not isartinian[1]) * 3) + 1
	maxdeg[2] += ((not isartinian[2]) * 3) + 1
	
	# init grid
	grid = []
	for x in range(maxdeg[0] + 1):
		grid.append([])
		for y in range(maxdeg[1] + 1):
			grid[-1].append([])
			for z in range(maxdeg[2] + 1):
				grid[-1][-1].append(1)
	
#	grid = [[[1] * maxdeg[2]] * maxdeg[1]] * maxdeg[0]
	
	if (args.verbose > 1):
		print grid
	
#	for g in gens:
#		print g
	
	# build grid
	for x in range(maxdeg[0]):
		for y in range(maxdeg[1]):
			for z in range(maxdeg[2]):
				for g in gens:
					if (g[0] <= x and g[1] <= y and g[2] <= z):
						grid[x][y][z] = 0
						break
	
	if (args.verbose > 1):
		print grid
	
	# draw boxes
	def blockfrombase(x,y,z):
		return dx*x + dy*y + dz*z
	
	stairlowerleft = Vector(0,0)
	stairupperright = Vector(0,0)
	for x in (0, maxdeg[0] + axesextra):
		for y in (0, maxdeg[1] + axesextra):
			for z in (0, maxdeg[2] + axesextra):
				cur = blockfrombase(x,y,z)
				stairlowerleft.x = min(stairlowerleft.x, cur.x)
				stairlowerleft.y = min(stairlowerleft.y, cur.y)
				stairupperright.x = max(stairupperright.x, cur.x)
				stairupperright.y = max(stairupperright.y, cur.y)
	
#	origin = Vector(0, 0) #Vector(1, 1) - stairlowerleft
	
	c = canvas.canvas()
	# text.preamble('\\parindent=0pt')
	
	if (args.verbose > 1):
		print 'Staircase lower left: ' + str(stairlowerleft)
	
	# the lower left back corner
	def cubestart(x, y, z):
		return blockfrombase(x,y,z)
	
	def drawline(p1, p2):
		c.stroke(path.line(p1.x, p1.y, p2.x, p2.y), [color.rgb.black])
	
	def drawtext(st, p):
		hal = text.halign.boxleft
		val = text.valign.bottom
	#	if (loc == UPPERLEFT):
	#		val = text.valigh.top
	#	elif (loc == LOWERRIGHT):
	#		hal = text.halign.boxright
	#	elif  (loc == UPPERRIGHT):
	#		hal = text.halign.boxright
	#		val = text.valign.top
		
		c.text(p.x, p.y, st, [hal, val, color.rgb.black])
	
	def drawaxislabel(axis, p):
		c.text(p.x, p.y, axis, [text.halign.boxcenter, text.valign.middle, text.mathmode, color.rgb.black])
	
	def markgenerator(x, y, z):
		p = cubestart(x, y, z)
		c.stroke(path.circle(p.x, p.y, dr), [color.rgb.black, deco.filled([color.rgb(0.65, 0.65, 0.65)])])
		
		if (not args.nolabels):
			drawtext(str(x) + str(y) + str(z), p + Vector(dr, -0.3))
		
	def markirreducible(x, y, z):
		p = cubestart(x, y, z)
		c.stroke(path.circle(p.x, p.y, dr), [color.rgb.black, deco.filled([color.rgb(1.0, 1.0, 1.0)])])
		
		if (not args.nolabels):
			drawtext(str(x) + str(y) + str(z), p + Vector(dr, -0.3))
	
	def drawxside(x, y, z):
		start = cubestart(x, y, z)
		
		p1 = start + dx
		p2 = p1 + dz
		p3 = p1 + dz + dy
		p4 = p1 + dy
		
		p = path.line(p1.x, p1.y, p2.x, p2.y) << path.line(p2.x, p2.y, p3.x, p3.y) << path.line(p3.x, p3.y, p4.x, p4.y)
		p.append(path.closepath())
		c.stroke(p, [color.rgb.black, deco.filled([color.rgb(xcolr, xcolg, xcolb)])])
	
	def drawyside(x, y, z):
		start = cubestart(x, y, z)
		
		p1 = start + dy
		p2 = p1 + dz
		p3 = p1 + dz + dx
		p4 = p1 + dx
		
		p = path.line(p1.x, p1.y, p2.x, p2.y) << path.line(p2.x, p2.y, p3.x, p3.y) << path.line(p3.x, p3.y, p4.x, p4.y)
		p.append(path.closepath())
		c.stroke(p, [color.rgb.black, deco.filled([color.rgb(ycolr, ycolg, ycolb)])])
	
	def drawzside(x, y, z):
		start = cubestart(x, y, z)
		
		p1 = start + dz
		p2 = p1 + dx
		p3 = p1 + dx + dy
		p4 = p1 + dy
		
		p = path.line(p1.x, p1.y, p2.x, p2.y) << path.line(p2.x, p2.y, p3.x, p3.y) << path.line(p3.x, p3.y, p4.x, p4.y)
		p.append(path.closepath())
		c.stroke(p, [color.rgb.black, deco.filled([color.rgb(zcolr, zcolg, zcolb)])])
	
	def drawbuchedge(g1, g2):
		p1 = cubestart(g1[0], g1[1], g1[2])
		p2 = cubestart(g2[0], g2[1], g2[2])
		p12 = cubestart(max(g1[0],g2[0]), max(g1[1],g2[1]), max(g1[2],g2[2]))
		
		p = path.line(p1.x, p1.y, p12.x, p12.y) << path.line(p12.x, p12.y, p2.x, p2.y)
		c.stroke(p, [style.linewidth(buchwidth), color.rgb.black])
	
	# draw axes
	axisx = dx*(maxdeg[0] + axesextra)
	axisy = dy*(maxdeg[1] + axesextra)
	axisz = dz*(maxdeg[2] + axesextra)
	
	axisxy = dx*(maxdeg[0] + axesextra) + dy*(maxdeg[1] + axesextra)
	axisyz = dy*(maxdeg[1] + axesextra) + dz*(maxdeg[2] + axesextra)
	axisxz = dx*(maxdeg[0] + axesextra) + dz*(maxdeg[2] + axesextra)
	
	drawline(Vector(0, 0), axisx)
	drawline(Vector(0, 0), axisy)
	drawline(Vector(0, 0), axisz)
	
	drawline(axisx, axisxy)
	drawline(axisy, axisxy)
	drawline(axisy, axisyz)
	drawline(axisz, axisyz)
	drawline(axisx, axisxz)
	drawline(axisz, axisxz)
	
	drawaxislabel('x', axisx + dx*0.1)
	drawaxislabel('y', axisy + dy*0.1)
	drawaxislabel('z', axisz + dz*0.1)
	
	# draw staircase
	for x in range(maxdeg[0]):
		for y in range(maxdeg[1]):
			for z in range(maxdeg[2]):
				if (grid[x][y][z] > 0):
					if (x == maxdeg[0] - 1 or grid[x+1][y][z] == 0):
						drawxside(x,y,z)
					if (y == maxdeg[1] - 1 or grid[x][y+1][z] == 0):
						drawyside(x,y,z)
					if (z == maxdeg[2] - 1 or grid[x][y][z+1] == 0):
						drawzside(x,y,z)
					
					if (grid[x+1][y][z] == 0 and grid[x][y+1][z] == 0 and grid[x][y][z+1] == 0):
						markirreducible(x + 1, y + 1, z + 1)
	
	# draw buchberger graph
	if (args.buchberger):
		for g1 in gens:
			for g2 in gens:
				if (g1 == g2):
					continue
				
				g12 = [max(g1[0],g2[0]), max(g1[1],g2[1]), max(g1[2],g2[2])]
				
				# determine if this is an edge
				isedge = True
				for g3 in gens:
					if (g3 == g1 or g3 == g2):
						continue
						
					if (g3[0] <= g12[0] and g3[1] <= g12[1] and g3[2] <= g12[2] and 
						(g12[0] == 0 or g3[0] < g12[0]) and 
						(g12[1] == 0 or g3[1] < g12[1]) and 
						(g12[2] == 0 or g3[2] < g12[2])):
						isedge = False
				
				# draw the edge
				if (isedge):
					drawbuchedge(g1, g2)
	
	for g in gens:
		markgenerator(g[0],g[1],g[2])
	
	c.writePDFfile(pdffile)

"""
parser = argparse.ArgumentParser(description='Find the factorial of a number.')
parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer to find the factorial of')
args = parser.parse_args();

for i in args.integers:
	print "%d factorial is %d" % (i,fact(i))


oh=ShapeBuilder()
s=svg('test')

s.addElement(oh.createRect(0,0,400,200,12,12, strokewidth=2, stroke='navy'))
s.addElement(oh.createRect(100,50,200,100, strokewidth=2, stroke='navy', fill='yellow'))
s.addElement(oh.createCircle(700,500,50, strokewidth=5, stroke='red'))
s.addElement(oh.createCircle(810,500,50, strokewidth=5, stroke='yellow', fill='#AAAAAA'))
s.addElement(oh.createEllipse(600,50,50,30,strokewidth=5, stroke='red'))
s.addElement(oh.createEllipse(700,50,50,30,strokewidth=5, stroke='yellow', fill='#00AABB'))
s.addElement(oh.createLine(0,0,300,300,strokewidth=2,stroke='black'))
s.save('Shapes.svg')
"""

