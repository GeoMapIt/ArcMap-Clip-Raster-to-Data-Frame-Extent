"""
Clips user specified raster data to user specified data frame within mxd document.
Run as tool in Arcmap.
Made by Nathan R
Script will fail if input raster has a different CS than df
"""

import arcpy
from arcpy import env
from arcpy import mapping

#Script Parameters
data_to_clip = arcpy.GetParameterAsText(0)
data_frame = arcpy.GetParameterAsText(1) 
export_location = arcpy.GetParameterAsText(2)
add_to_toc = arcpy.GetParameterAsText(3)

#Creates DF_Extent feature class in default arcgis workspace
mxd = mapping.MapDocument("CURRENT")
df = mapping.ListDataFrames(mxd, "*")[int(data_frame)-1]
coord_sys = df.spatialReference
frameExtent = df.extent

array = arcpy.Array()
array.add(arcpy.Point(frameExtent.XMin, frameExtent.YMin))
array.add(arcpy.Point(frameExtent.XMin, frameExtent.YMax))
array.add(arcpy.Point(frameExtent.XMax, frameExtent.YMax))
array.add(arcpy.Point(frameExtent.XMax, frameExtent.YMin))
array.add(arcpy.Point(frameExtent.XMin, frameExtent.YMin))
polygon = arcpy.Polygon(array)

#Creates temporary feature class in default arcgis workspace to be used as clip boundary
arcpy.CopyFeatures_management(polygon, "DF_Extent_TODELETE")

#Defines temporary feature class to data frame coordinate system
arcpy.DefineProjection_management("DF_Extent_TODELETE", coord_sys)

#Clips raster to temporary feature class
arcpy.Clip_management(data_to_clip, (str(frameExtent.XMin) + " " + str(frameExtent.YMin) + " " + str(frameExtent.XMax) + " " + str(frameExtent.YMax)), export_location, "DF_Extent_TODELETE", "0", "ClippingGeometry", "MAINTAIN_EXTENT")

#Deletes temporary feature class
arcpy.Delete_management("DF_Extent_TODELETE")

#Adds result into TOC
if add_to_toc == "true":
    addlayer = arcpy.mapping.Layer(export_location)
    arcpy.mapping.AddLayer(df, addlayer, "TOP")
