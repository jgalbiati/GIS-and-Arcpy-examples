# Code goals:
#   1.) Select all geometry with geometry status == 'EDITED'.
#   2.) Delete geometry *Created more than one day ago* with Null
#       ID field
#   3.) Change remaining selection's Geometry status to 'DONE'

import arcpy
from datetime import datetime


# The Layer path needs to be updated with the correct database to write to.
#   The goal is to have this script run daily, and updates reflected in
#       the main production table
layer_path = r'...'
fields = ["GEOMETRYSTATUS", "LEGALDESCRIPTIONID", "CREATED_DATE"]


# Given that the code is intended to work on a table in a versioned database,
#     will need to be executed from within an edit session:
edit = arcpy.da.Editor(layer_path)
edit.startEditing(False, True)
edit.startOperation()
with arcpy.da.UpdateCursor(layer_path, fields,
                            where_clause="GEOMETRYSTATUS = 'EDITED'") as cursor:
    for row in cursor:
        if (row[1] is None) & ((datetime.now() - row[2]).days > 1):
            cursor.deleteRow()
        else:
            row[0] = 'DONE'
            cursor.updateRow(row)

edit.stopOperation()
edit.stopEditing(True)
