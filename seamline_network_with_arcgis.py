# -*- coding: utf-8 -*-
"""
Script Name: Seamline netwrok construction with ArcGIS
Description: 1. Create a mosaic dataset
             2. Add orthoimages to the dataset
             3. Build seamline network
               
Created Time: 2017-10-20 09:13:03

@author: Chaoer

Note that, this script is supposed to be executed from coustomly added "script tool".

	-The guide of "Adding a script tool" can be found at:
	-http://desktop.arcgis.com/en/arcmap/10.3/analyze/creating-tools/adding-a-script-tool.htm
	
Five param should be added:	
	
DisplayName            Data Type
WorkSpace              Workspace
Geodatabase Name       String
Mosaic Dataset Name    String
Projection Type        Coordinate System
Orthoimages Directory  Folder
	
	-The guide of "Setting script tool parameters" can be found at:
	-http://desktop.arcgis.com/en/arcmap/10.3/analyze/creating-tools/setting-script-tool-parameters.htm	
	
"""

"""*****************************************************************"""
import arcpy # Import ArcPy site-package
import time
import os

"""*****************************************************************"""
# workspace of your arcgis, on my computer, it is --- "C:\Users\A\Documents\ArcGIS"
workspace = arcpy.GetParameterAsText(0)
# filedatabase used to save the mosaic datasets, I set it to be --- "Seamline_ArcPy.gdb" 
gdbname = arcpy.GetParameterAsText(1) 
# name of the mosaic datasets, for example, for dataset2 in this arctile --- "SanFrancisco"
mdname = arcpy.GetParameterAsText(2) 
# projection of the dataset. It is selected from gui of ArcGIS. For dataset2 in this arctile,  --- WGS_1984_UTM_Zone_10N
prjfile = arcpy.GetParameterAsText(3)
# dir contains the orthoimages. (orthoimages please in *.tif format)
orthoimage_path = arcpy.GetParameterAsText(4)

# set the workspace
arcpy.env.workspace = workspace 
# Use 8 processes (This setting is used for efficiency comparison in our experiments).
arcpy.env.parallelProcessingFactor = "8"

# If gdb is not exist, then create it
if not arcpy.Exists(gdbname):
    try:
        arcpy.CreateFileGDB_management(workspace, gdbname)
    except Exception as err:
        arcpy.AddError(err)
        print (err)

"""*****************************************************************"""
# Create mosaic dataset
if arcpy.Exists(mdname):
    arcpy.AddMessage("Dataset is already exists, then exit.")
    exit(-1)

noband = "3"
pixtype = "8_BIT_UNSIGNED"

arcpy.AddMessage("\nCreate mosaic dataset...\n")
try:
    arcpy.CreateMosaicDataset_management(gdbname, mdname, prjfile, noband, 
                                     pixtype)
except Exception as err:
    arcpy.AddError(err)
    print (err)

"""*****************************************************************"""
# Change workspace to the gdb
arcpy.env.workspace = os.path.join(workspace, gdbname);

# Add orthoimages to the dataset 
rastype = "Raster Dataset"
updatecs = "UPDATE_CELL_SIZES"
updatebnd = "UPDATE_BOUNDARY"
updateovr = "#"
maxlevel = "#"
maxcs = "#"
maxdim = "#"
spatialref = "#"
inputdatafilter = "*.tif"
subfolder = "NO_SUBFOLDERS"
duplicate = "EXCLUDE_DUPLICATES"

arcpy.AddMessage("Add orthoimages to the dataset...\n")
try:
    arcpy.AddRastersToMosaicDataset_management(mdname, rastype, orthoimage_path,
		updatecs, updatebnd, updateovr,
		maxlevel, maxcs, maxdim, spatialref, inputdatafilter,
		subfolder, duplicate)
		
except Exception as err:
    arcpy.AddError(err)
    print (err)

"""*****************************************************************"""
# Before the seamline selection, we must calculate the footprint of 
# orthoimages since there are black regions on orthoimages.
query = "#"
method = "RADIOMETRY"

arcpy.AddMessage("Build Footprint...\n")
try:
	start_1 = time.clock()
	arcpy.BuildFootprints_management(mdname, query, method)
	elapsed_1 = (time.clock() - start_1)
	arcpy.AddMessage("Build Footprint used: %.3f second. \n" % elapsed_1)
	
except Exception as err:
    arcpy.AddError(err)
    print (err)

 	
"""*****************************************************************"""
# Build seamline network
cellsize = "#"
sortmethod = "NORTH_WEST"
sortorder = "ASCENDING"
orderattribute = "#"
orderbase = "#"
viewpnt = "#"
computemethod = "RADIOMETRY" # Generate seamlines using the default param in ArcGIS GUI.
                             # other selectable param can be found at:
							 # https://desktop.arcgis.com/en/arcmap/latest/tools/data-management-toolbox/build-seamlines.htm

arcpy.AddMessage("Build seamline network...\n")
try:
	start = time.clock()
	arcpy.BuildSeamlines_management(mdname, cellsize, sortmethod,
	sortorder, orderattribute, orderbase, viewpnt,
	computemethod)
	
	elapsed = (time.clock() - start)
	arcpy.AddMessage("Build seamline network used: %.3f second. \n" % elapsed)
    
	elapsed = (time.clock() - start_1)
	arcpy.AddMessage("Total time: %.3f second. \n" % elapsed)
	
except Exception as err:
    arcpy.AddError(err)
    print (err)

arcpy.AddMessage("Finish!\n")