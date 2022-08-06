# Code meant to be included as a code block within ArcMap's Field Calculator tool.
#     Run using expression 'incID()'. Code will run once for each selected geometry,
#     incrementing the global ind to iterate through the idList

ind = -1
idList = [...] # paste in ID list to be captured

def incID():
	global ind
	ind +=1
	if ind >= len(idList):
		return None
	else:
		return idList[ind]
