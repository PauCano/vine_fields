import sys, getopt
import os
import xml.etree.ElementTree as ET

def main(argv):
	folder = ""
	outputFolder = ""
	try:
		opts, args = getopt.getopt(argv,"s:o:",["simulation=", "output="])
	except getopt.GetoptError:
		print('linesDataset.py -s simulationFolder -o outputFolder')
		sys.exit(2)
	for opt, arg in opts: #read and assign command parameters
		if opt in ("-s", "--simulation"):
			folder = arg
		elif opt in ("-o", "--output"):
			outputFolder = arg
	
	outputPath = folder+"\\output" #general output folder of the simulation
	print("Setting up Simulation "+folder.split("\\")[-1]) #printing process settings
	print("Folder: "+folder)
	GT=False
	groundMaterials=["loam_sandy_brown_fine","loam_gravelly_brown","sandy_loam_brown","soil_vegetation"]
	weedMaterials=["grass_rye","grass_dry","hemlock_low"]
	leavesMaterials=["tilia_cordata_leaf","populus_nigra_leaf","citrus_sinensis1_leaf"]
	modulesToRender = [1]
	imagesToSkip = 89
	iteration = 0
	
	ImagesAlreadyDone = 14014
	currentImage = 0
	
	
	dartMainFolder = "\\".join(folder.split('\\')[:-3])
	fieldsXML = folder+"\\input\\object_3d.xml"
	sunXML = folder+"\\input\\directions.xml"
	dartToolFolder = dartMainFolder+"\\tools\\windows\\" #select dart's tools folder
	fieldsTree = ET.parse(fieldsXML) #open, parse, and get root of phase xml file containing camera values
	fieldsRoot = fieldsTree.getroot()
	field_def = fieldsRoot[0][2][0]
	weeds_def = fieldsRoot[0][2][1]
	sunTree = ET.parse(sunXML) #open, parse, and get root of phase xml file containing camera values
	sunRoot = sunTree.getroot()
	sunOrientation = sunRoot[0][0]
	materialsXML = folder+"\\input\\coeff_diff.xml"
	materialsTree = ET.parse(materialsXML)
	materialsRoot = materialsTree.getroot()
	weedMaterialAttribute = materialsRoot[0][0][6]
	groundMaterialAttribute = materialsRoot[0][0][0]
	leavesMaterialAttribute = materialsRoot[0][0][1]

	fieldList = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
	#print(fieldList)
	weedsList = [f for f in os.listdir("C:\\Users\\pcano\\Desktop\\weedFields\\")]
	#print(weedsList)
	for groundMaterial in range(4 if not GT else 1):
		groundMaterialAttribute.set("ModelName", groundMaterials[groundMaterial])
		for weedMaterial in range(3 if not GT else 1):
			weedMaterialAttribute.set("ModelName", weedMaterials[weedMaterial])
			for leavesMaterial in range(3 if not GT else 1):
				leavesMaterialAttribute.set("ModelName", leavesMaterials[leavesMaterial])
				if not GT:
					materialsTree.write(materialsXML)
				sunList = [0] if GT else [30,40,50,60,70,20,10,0]
				for sun in sunList:
					sunOrientation.set("sunViewingZenithAngle", str(sun))
					sunTree.write(sunXML)
					latList = [225] if GT else [225,165,105,45,285,345]
					if sun == 0:
						latList = [225]
					for sunLatitude in latList:
						sunOrientation.set("sunViewingAzimuthAngle", str(sunLatitude))
						sunTree.write(sunXML)
						for weed in weedsList:
							weeds_def.set("fieldDescriptionFileName", "C:\\Users\\pcano\\Desktop\\weedFields\\" + weed)
							for field in fieldList:
								output = outputFolder+"\\"+str(groundMaterial)+str(weedMaterial)+str(leavesMaterial)+"_"+field.split('.')[0]+"_"+weed.split('.')[0]+"_"+str(sun)+"_"+str(sunLatitude)+".png"
								field_def.set("fieldDescriptionFileName", "C:\\Users\\pcano\\DART\\user_data\\simulations\\dataset_lines\\"+field)
								fieldsTree.write(fieldsXML)
								
								if (iteration % imagesToSkip) in modulesToRender or GT:
									if currentImage >=  ImagesAlreadyDone:
										os.system(dartToolFolder+"dart-full.bat "+folder.split("\\")[-1])# "" simulation_name="+folder.split("\\")[-1]
										print("\nCompositing images...")
										bandFolders = [f.path for f in os.scandir(outputPath) if f.is_dir()][:3]
										for i in range(3):#get each of the rendered images' path
											bandFolders[i] = '"'+bandFolders[i]+"\\BRF\\ITERX\\IMAGES_DART\\ima01_VZ=000_0_VA=000_0.mp#"+'"'
										R = bandFolders[2]
										G = bandFolders[1]
										B = bandFolders[0]
										os.system(dartToolFolder+"dart-colorComposite.bat "+R+" "+G+" "+B+" "+output)#execute color composition
										print("Color image composited for field "+field+", weeds "+weed+" and sun orientations ("+str(sun)+","+str(sunLatitude)+").")
									currentImage += 1
									print(currentImage)
								iteration += 1
				
if __name__ == "__main__":
	main(sys.argv[1:])