#!/usr/bin/env python3

def Reader(rawFile, dlimit=','):
	import csv
	print(" [+] Importing data")
	try:
		with open(rawFile) as csvfile:
			reader = csv.DictReader(csvfile, delimiter=dlimit)
			return reader
	except:
		print(" [!] Unable to read file "+rawFile)
		raise NameError("Unable to read file "+rawFile)

def splitAns(ansRaw, org):
	r = []
	for ans in ansRaw[:]:
		r.append(ans)


'''def Main():
	parser = argparse.ArgumentParser(prog="CLEANER")
	parser.add_argument('-f', '--file', type='string', dest='filename', \
			help="CSV file to import data from.\nIf not parsed program will be prompted at start.")
	parser.add_argument('-r', '--lines', type='int', dest='read', help="Number of lines to read.\nOptional. DEFAULT: Read all file", \
			default=False)
	parser.add_argument('-s', '--skip', type='int', dest='skip', help="Number of lines to skip from first line.\nOptional. DEFAULT: None", \
			default=False)
	args = parser.parse_args()

	print(" [-] Starting program...")
	if not args.filename:
		args.filename = input(" [!] Insert name of the CSV file to read\n==>")

	csvR = Reader(args.filename)


if __name__=="__main__":
	Main()'''
