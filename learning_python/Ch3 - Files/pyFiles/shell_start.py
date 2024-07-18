#
# Example file for working with filesystem shell methods
# LinkedIn Learning Python course by Joe Marini
#

import os
from os import path
import shutil
from shutil import make_archive
from zipfile import ZipFile

fileName = "new_textfile.txt"

def main():
    arr = os.listdir()
    
    fileSize = 0
    
    for file in arr:
        if file.endswith(".txt"):
            fileSize += os.path.getsize(file)
            print(fileSize)
            
            
        
    # make a duplicate of an existing file
    # if path.exists(fileName):
        # get the path to the file in the current directory
        # scr = path.realpath(fileName)
        
        # let's make a backup copy by appending "bak" to the name
        # destination = scr + ".bak"
        # shutil.copy(scr, destination)
        
        # rename the original file
        # os.rename(fileName, "new_" + fileName)
        
        # now put things into a ZIP archive
        # root_dir, tail = path.split(scr)
        
        # print(root_dir)
        # print(tail)
        
        # shutil.make_archive("archive", "zip", root_dir)
        
        # more fine-grained control over ZIP files
        # with ZipFile("testzip.zip", "w") as newzip:
        #     newzip.write(fileName)
        #     newzip.write("textfile.txt.bak")
      
if __name__ == "__main__":
    main()
