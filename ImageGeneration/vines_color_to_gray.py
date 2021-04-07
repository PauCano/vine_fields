import sys, getopt
import os
import matplotlib.pyplot as plt
from skimage import io

colors=[[255,0,0],#red 0
		[0,255,0],#green 1
		[0,0,255],#blue 2
		[255,255,0],#yellow 3
		[255,0,255],#Purple 4
		[0,255,255]#Cyan 5
] #colors: Red, Green, Blue, Yellow, Purple, Cyan

def getNearestColor(pixel): #return the nearest defined color to the pixel color
	if pixel[0] == colors[1][0] and pixel[1] == colors[1][1] and pixel[2] == colors[1][2]:
		return [0,0,0] #Green = 0
	elif pixel[0] == colors[0][0] and pixel[1] == colors[0][1] and pixel[2] == colors[0][2]:
		return [1,1,1] #Red = 1
	elif pixel[0] == colors[2][0] and pixel[1] == colors[2][1] and pixel[2] == colors[2][2]:
		return [2,2,2] #Blue = 2
	elif pixel[0] == colors[4][0] and pixel[1] == colors[4][1] and pixel[2] == colors[4][2]:
		return [2,2,2] #Purple = 3
	else:
		return [3,3,3] #Others = 4

def Process(name):
	fileName=name
	baseImage = io.imread(fileName) #open image file
	if baseImage.shape[2] > 3:
		baseImage = baseImage[:,:,:3]
	for x in range(baseImage.shape[0]):
		for y in range(baseImage.shape[1]):
			baseImage[x][y] = getNearestColor(baseImage[x][y])
	baseImage = baseImage[:,:,0]
	newName = fileName.split(".")[0]+"_color.png"
	os.rename(fileName,newName)
	plt.imsave(name, baseImage,vmin=0,vmax=255, cmap='gray')#save image

def main(argv):
	inputFile = ""
	try:
		opts, args = getopt.getopt(argv,"i:",["input="])
	except getopt.GetoptError:
		print('python vines_color_to_gray.py -i inputImage.png')
		sys.exit(2)
	for opt, arg in opts: #read and assign image file
		if opt in ("-i", "--input"):
			inputFile = arg
	Process(inputFile) #process the image file

if __name__ == "__main__":
	main(sys.argv[1:])