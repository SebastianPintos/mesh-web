import os

class FileWritter:

    def __init__(self, fileName):
        self.fileName = fileName

    def write(self, string):
        file = open(self.fileName, 'a')
        file.write(string + "\n")
        file.close()

class FileReader:
    def __init__(self, fileName):
        self.fileName = fileName

    def read():
        file = open(self.fileName, 'r')
        toRet = file.read()
        file.close()
        return toRet

class FileLineReader: #TODO Al recuperar las lineas del arhivo, hay que filtrar el \n

    def __init__(self, fileName):
        self.fileName = fileName
        with open(self.fileName) as f:
            self.lines = f.readlines()
        self.index = 0

    def is_end_of_file(self):
        return len(self.lines) == self.index

    def getLine(self):
        line = self.lines[self.index]
        print("El index es", self.index , "y la longitud del array es ", len(self.lines) -1 )
        if self.is_end_of_file():
            return None
        self.index = self.index + 1
        return line

class FileDeletor:

    def __init__(self, fileName):
        self.file = fileName

    def delete(self):
        os.remove(self.file)
