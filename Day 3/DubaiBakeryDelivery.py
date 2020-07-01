import arcpy

myPath = "C:\\Users\\ahme8608\\Documents\\Etisalat\\Python Workshop\\Python Workshop\\Day 3\\"
arcpy.env.workspace = myPath + "01 - Data.gdb"

arcpy.CopyFeatures_management("Restaurants_UAE", "memory/BakeryRestaurants")
arcpy.CopyFeatures_management("UAE_Emirates", "memory/Dubai")

with arcpy.da.UpdateCursor("memory/BakeryRestaurants", "*", "lower(NAME_LAT) not like '%baker%'") as cursor:
    for row in cursor:
        cursor.deleteRow()

with arcpy.da.UpdateCursor("memory/Dubai", "*") as cursor:
    for row in cursor:
        if row[cursor.fields.index("EMIRATE_DS")] != "DUBAI":
            cursor.deleteRow()

arcpy.Buffer_analysis("memory/BakeryRestaurants", "memory/All_Bakery_Delivery_Zones", "5 Kilometers", dissolve_option="ALL")

arcpy.Clip_analysis("memory/All_Bakery_Delivery_Zones", "memory/Dubai", arcpy.env.workspace + "//BakeryDeliveryZones")

print("Completed Execution")