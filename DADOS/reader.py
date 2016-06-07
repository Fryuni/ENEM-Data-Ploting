#!/usr/bin/env python3

class ModeError(NameError):
    def __init__(self, message):
        self.message = message

class Reader():
    def __init__(self, rawFile, values=None, dlimit=',', include='all', verbose=False):
        self._file = rawFile
        self.mode = rawFile.mode
        self.delimiter = dlimit
        self.verb = verbose
        if values == None:
            if self.mode == 'r':
                line = self._file.readline()
            elif self.mode == 'rb':
                line = ''.join([chr(x) for x in self._file.readline()])
            else:
                raise ModeError("Wrong file mode... Passed with '"+self.mode+"' mode")
            self.values = line.strip('\r\n').split(self.delimiter)
            self.pp(str(self.values))
        else:
            self.values = values
        self.include = include
        self.lh = len(self.values)

    def pp(self, message):
        if self.verb:
            print(" {+} "+str(message))

    def __iter__(self):
        return self

    def __next__(self):
        if self.mode == 'r':
            row = next(self._file).strip('\r\n').split(self.delimiter)
            while row == []:
                row = next(self._file).strip('\r\n').split(self.delimiter)
        elif self.mode == 'rb':
            try:
                row = ''.join([chr(x) for x in next(self._file)]).strip('\r\n').split(self.delimiter)
            except UnicodeDecodeError:
                row = []
            except:
                raise
            finally:
                while row == []:
                    try:
                        row = ''.join([chr(x) for x in next(self._file)]).strip('\r\n').split(self.delimiter)
                    except UnicodeDecodeError:
                        row = []
                    except:
                        raise
        d = dict(zip(self.values, row))
        return d

    def __int__(self):
        len(self.values)



def odReader(rawFile, dlimit=','):
    import csv
    print(" [+] Opening CSV file")
    try:
        reader = csv.DictReader(rawFile, delimiter=dlimit)
        return reader
    except:
        print(" [!] Unable to read file "+rawFile)
        raise NameError("Unable to read file "+rawFile)


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
