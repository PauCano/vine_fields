import os
import subprocess
import sys, getopt
def main(argv):
	folder = ""
	try:
		opts, args = getopt.getopt(argv,"f:",["folder="])
	except getopt.GetoptError:
		print('python proces_vines_folder.py -f folder')
		sys.exit(2)
	for opt, arg in opts: #read and assign image file
		if opt in ("-f", "--folder"):
			folder = arg
	images = os.listdir(folder)
	length =  len(images)
	for i in range(length):
		image = images[i]
		path=os.path.join(folder,image)
		print(path, str(i)+"/"+str(length))
		output = subprocess.check_output("python labeled_process.py -i "+path,shell=True)
		print(output)
		output = subprocess.check_output("python vines_color_to_gray.py -i "+path,shell=True)
		print(output)
		print()
	#for i in range(length):
		#image = images[i]
		#print(image)
		#baseName=image.split(".")[0]
		#if(baseName[-1]=='5'):
			#os.remove(os.path.join(folder,image))
			#print("delete")
		#else:
			#newName = "_".join(baseName.split("_")[:-1])
			
			#os.rename(os.path.join(folder,image),os.path.join(folder,newName+".png"))
			#print("rename")
		#print()

if __name__ == "__main__":
	main(sys.argv[1:])