from svgfig.svg import SVG
from svgfig.defaults import defaults_svg

#constants

packages = {"0603": (1.6, .8),
"0805": (2, 1.3),
"1206": (3.2, 1.6),
"QFN-12": (5, 5),
"TQFP-44": (11.75, 11.75),
"SOT23-3": (3, 2.5),
"SOIC-8": (5, 6),
"SOIC-14": (8.65, 6),
"SOT23-6": (3, 3),
"CONN_USB_MINI-B": (7.7, 6)} 

replace = {"RN8P-4R-CRA06S": "1206", "SO-08": "SOIC-8", "SO-14": "SOIC-14"}

labels = ("name", "x", "y", "angle", "package")

#build a list of dictionaries from the .mnt file produced via EAGLE
parts = [dict(zip(labels, part)) for part in [line.split() for line in open("v3.brd.mnt")]]

#clean up the generated list of dictionaries
for part in parts:
	try:
		if part["package"] in replace.keys():
			part["package"] = replace[part["package"]]
		if (int(part["angle"]) % 180):
			part["width"] = packages[part["package"]][1]
			part["height"] = packages[part["package"]][0]
		else:
			part["width"] = packages[part["package"]][0]
			part["height"] = packages[part["package"]][1]
		part["y"] = float(part["y"])
		part["x"] = float(part["x"])
	except:
		print "part %s not in library" % part["name"]
		print len(parts)
		parts.remove(part)
		print len(parts)

#set one "user defined point" to be one mm
defaults_svg['width'] = "12cm"
defaults_svg['height'] = "12cm"
defaults_svg['viewBox'] = (0, 0, 120, 120)
defaults_svg['style'] = {"stroke-width": ".1"}


#flip Y axis to keep in line with EAGLE
partHolder = SVG("g", transform = "translate(0, 120) scale(1, -1)")
pcbHolder = SVG("g", transform = "translate(0, 120) scale(1, -1)")
buildPlatformMate = SVG("g", transform = "translate(0, 120) scale(1, -1)")

#draw outlines on each layer for cutting and reference
buildPlatformMate.append(SVG("rect", x = 0, y = 0, height = 120, width = 120)) 
pcbHolder.append(SVG("rect", x = 0, y = 0, height = 120, width = 120)) 
partHolder.append(SVG("rect", x = 0, y = 0, height = 120, width = 120)) 

topSheet = SVG("g")
topSheet.append(pcbHolder)
topSheet.append(partHolder)

#the ToM build plate has holes at (4,4) through (116,116)
ToMCoords = [4, 60, 116]

for x in ToMCoords:
	for y in ToMCoords:
		buildPlatformMate.append(SVG("circle", r = 3.6/2, cx = x, cy = y))

#draw rectangles for each part
for part in parts:
	try:
		partHolder.append(SVG("rect", x = part['x']-part['width']/2, y = part['y']-part['height']/2, width = part['width'], height = part['height']))
	except:
		print part

pcbHolder.append(SVG("rect", x = 0, y = 0, height = 80, width = 50, rx = 5, ry = 5))

topSheet.save("tS.svg")

#/Applications/EAGLE/EAGLE.app/Contents/MacOS/EAGLE -C "run loctab;quit" ../v3/v3.brd
