# CODE GOAL:
# USING INFORMATION FROM DAILY ACTIVITY WITHIN A VERSIONED DATABASE,
#   GENERATE AN EXCEL-READABLE REPORT.


import arcpy

# Set paths for the data tables we're going to be pulling from:
#   Tables include: oil/gas well unit boundaries; oil/gas wells (represented by "uwi" numbers);
#       and a table tracking user activity within a versioned database

unitPath = r'filePath\file' # Paths to be set to where the DB and DB tables are stored
uwiPath = r'filePath2\file'
trackingPath = r'filePath3\file'


fields_uwi = ['County', 'Unit_ID', 'UnitName', 'UWI']
fields_unit = ['LAST_QC_USER', 'LAST_QC_DATE']


# Prepare parameters for selecting the UWIs we want:
mapper_id = arcpy.GetParameterAsText(0)
mapper_name = arcpy.GetParameterAsText(1)
date = arcpy.GetParameterAsText(2)


# Grab UWIs from QC2 UWITracking based on user ID and starting date:
uwis = []
uwis_Where = "UserName = '{}' AND ModifiedAt >= '{}' AND FromTask = 'QC2'".format(mapper_id, date)
with arcpy.da.SearchCursor(trackingPath, ['UWI'], where_clause=uwis_Where) as getUwis:
    for row in getUwis:
        uwis.append(str(row[0]))

# Format for use in other queries:
uwis = tuple(uwis)


# Designate the .csv for storing the query results. Because of how arcmap's geoprocessing
# overwriting works, this parameter will be an *input*, rather than an output, meaning a
# file should already exist prior to running this script.
out_path = arcpy.GetParameterAsText(3)
f = open(r'{}'.format(out_path), 'w')


# The main query: takes in UWIs list, and writes the fields from UWIQueue and
# UnitBoundaries layers to the .csv specified.
with arcpy.da.SearchCursor(uwiPath, fields_uwi, where_clause="UWI IN {}".format(uwis)) \
        as cursor:
    for row in cursor:
        with arcpy.da.SearchCursor(unitPath, fields_unit,
                                   where_clause="UNIT_ID={}".format(row[1])) as rel:
            for el in rel:
                f.write('{0}, {1}, {2}, {3}, {4}, {5}, {6} \n'.format(mapper_name, row[0],
                                                                      row[1], row[2],
                                                                      (row[3]), el[0],
                                                                      el[1]))
del row, cursor, el, rel
f.close()
