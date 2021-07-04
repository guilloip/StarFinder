'''
Find brighter Star
using some CV functions

'''
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

''''
SOME SHOWING IMAGE TOOLS
'''

def plotGrayHisto(img,text=""):
	imax,jmax = img.shape
	dep=1
	vals = range(256*dep)
	histo = {i:0 for i in vals}

	for i in range(imax):
		for j in range(jmax):
			px=img[i,j]
			v = int(px)
			histo[v] += 1

	for v in vals:
		print(f"{v} -> {histo[v]}")

	print('total of pixels adquired in histogram:',sum(histo.values()))
	print('total of pixels calculated from resolution:',imax*jmax)
	# hysto
	plt.bar(vals,histo.values(),log=True)
	fontTit = {'family':'sans','color':'purple','size':20}
	fontLab = {'family':'sans','color':'gray','size':15}
	plt.title("Histogram: "+text,fontdict=fontTit)
	plt.xlabel("Level",fontdict=fontLab)
	plt.ylabel("Number Of Pixels",fontdict=fontLab)

	plt.show()

def showImage(img,text="",w=800,h=600) :
	win = "ImageWin"
	cv.namedWindow(win,flags=cv.WINDOW_NORMAL) 
	cv.setWindowTitle(win,text)
	cv.imshow(win,img)
	cv.resizeWindow(win,w,h)
	cv.waitKey(0)

'''
READ & PREPROCESS IMAGE ***********************************
'''
#ORIGINAL
filename = 'field.jpg'
imgRGB = cv.imread(filename)

imax,jmax,dep = imgRGB.shape
print(f"Resolution = {jmax}x{imax} Channels = {dep}")

showImage(imgRGB,"Original Color")

#GRAY CONVERTED IMAGE FOR BETTER PROCESSING
img = cv.cvtColor(imgRGB, cv.COLOR_RGB2GRAY)

imax,jmax = img.shape
dep=1
print(f"Resolution = {jmax}x{imax} Channels = {dep}")

showImage(img,"gray scale of:field.jpg")

plotGrayHisto(img,"gray version")

cv.imwrite('gray_'+filename, img)

#CREATE A BINARY THRES HOLD VERSION OF img 0 or 255 for Star detection
#	0 if its lower than 220
#	255 otherwise

ret,imgt = cv.threshold(img,thresh=220.0,maxval=255.0,type=cv.THRESH_BINARY)

plotGrayHisto(imgt,"THRESH(gray version)")
showImage(imgt,"THRESH(gray version)")
cv.imwrite('threshold_'+filename, imgt)

'''
FINDING STARS **************************************

Definition: Star: a set of nonzero points of imgt closer each other than a defined Radius (R)
	We will run over all pixels, once it find a HI pixel in imgt, we will
	check if its near to any already existing star.
		If it is, joint to that star, else create a new star

	When finish, the middle point will be used to define the center of star
	but using real img values instead of the threshold to give some weight (or maybe not)
	
	Once defined de center, the britgh will be calculated ass the sum of the bight of the
	nearests points to that center
'''
class StarType():
	def __init__(s,R=8):
		s.pix=[]
		s.R =R
		s.hasCM = False
		s.x=-1
		s.y=-1

	def count(s):
		return len(s.pix)
		
	def getMaxDist(s,p):
		return max([(s.pix[i][0]-p[0])**2+(s.pix[i][1]-p[1])**2 for i in range(s.count())])
	
	def isNear(s,p):
		m = s.getMaxDist(p)
		return True if m <= 4*s.R*s.R else False
		
	def append(s,p):
		s.pix.append(p)
		s.hasCM=False
		
	def setBright(s,b):
		s.birght=b
		
	def calcCenter(s):
		s.x=0
		s.y=0
		n=s.count()
		for i in range(n):
			s.x += s.pix[i][0]
			s.y += s.pix[i][1]
		s.x/=n
		s.y/=n
		s.hasCM=True
		
	def getCenter(s):
		if not s.hasCM :
			s.calcCenter()
		return (int(s.x),int(s.y))


R = int(input("Enter Star Radious (10):"))
if R<1 : R = 10

stars = []

#LOOKING FOR STARS:
for i in range(imax):
	for j in range(jmax):
		if imgt[i,j] != 0 :
			added = False
			for s in stars :
				if s.isNear([i,j]):
					s.append([i,j])
					added=True
			if not added :
				ns = StarType(R)
				ns.append([i,j])
				stars.append(ns)

print("*** STAR FINDING PROCESS ENDED ***")
print("found stars:",len(stars))

for i in range(len(stars)):
	(x,y) = stars[i].getCenter()
	n = stars[i].count()
	print(f"Star#{i} : {n} HI pixels detected @ [{y},{x}]")


'''
EVALUATING STARS BRIGHT  ************************ 
'''

#calculate the brigths as sum of values in square 2Rx2R and store in a dict
brigths = {}
for k in range(len(stars)):
	(x,y) = stars[k].getCenter()
	n=0
	b=float(0)
	for i in range(max((x-R,0)),min((imax,x+R+1))) :
		for j in range(max((y-R,0)),min((jmax,y+R+1))) :
			b+=img[i,j]
			n+=1
	if n>0 :
		brigths[k]=b/n
	else:
		print(f"star {k} : range error!!!")

#ordering by brigth

topStars = sorted(brigths.items(),key = lambda item : item[1], reverse=True)

'''
PRINTING RESULTS *************************************
'''

topN = min(4,len(topStars))

print("********* THE {} BRIGTHERS STARS ARE: **********".format(topN))
for s in topStars[:topN]:
	x,y = stars[s[0]].getCenter()
	print(f"ORDER: {topStars.index(s)+1} for Star#{s[0]} @({y},{x}) with bright of {s[1]:5f} arb.units")
if len(topStars) > topN:
	print("------------- Rest of stars --------------") 
for s in topStars[topN:]:
	x,y = stars[s[0]].getCenter()
	print(f"ORDER: {topStars.index(s)+1} for Star#{s[0]} @({y},{x}) with bright of {s[1]:5f} arb.units")





