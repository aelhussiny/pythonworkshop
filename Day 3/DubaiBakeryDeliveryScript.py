import arcpy

all_restaurants = arcpy.GetParameter(0)
emirates_fc = arcpy.GetParameter(1)
output_fc = arcpy.GetParameter(2)

arcpy.CopyFeatures_management(all_restaurants, "memory/BakeryRestaurants")
arcpy.CopyFeatures_management(emirates_fc, "memory/Dubai")

with arcpy.da.UpdateCursor("memory/BakeryRestaurants", "*", "lower(NAME_LAT) not like '%baker%'") as cursor:
    for row in cursor:
        cursor.deleteRow()

with arcpy.da.UpdateCursor("memory/Dubai", "*") as cursor:
    for row in cursor:
        if row[cursor.fields.index("EMIRATE_DS")] != "DUBAI":
            cursor.deleteRow()

arcpy.Buffer_analysis("memory/BakeryRestaurants", "memory/All_Bakery_Delivery_Zones", "5 Kilometers", dissolve_option="ALL")

arcpy.Clip_analysis("memory/All_Bakery_Delivery_Zones", "memory/Dubai", output_fc)

print("Completed Execution")