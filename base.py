class MyExcept(Exception):
	pass

def getYear():
	import os
	dirname = os.path.basename(os.path.abspath('.'))
	if "MICRODADOS_ENEM_" in dirname:
		year = int(dirname[16:])
		return year
	else:
		raise NameError("Program not in a default INEP directory")


raise MyExcept("OI")
getYear()
os.path
