#Directory Merger Program
#Nicholas Ghobrial - P3

import sys
import os
import os.path as osp
import stat
import shutil

print ("This program will merge two source directories into a destination directory.")
inputString = input ("Enter the two sources to be merged and the destination: ")
inputList = inputString.split()

if len(inputList) != 3:
    print("Please enter exactly 2 source directories and one destination directory.")
    
for i in range(0,3) :
    inputList[i] = osp.abspath(inputList[i])
    if osp.isdir(inputList[i]) : 
        print("Input ", i+1, ": ", inputList[i])
    elif i == 2 :
        os.mkdir(inputList[i])
        print("Destination: ", inputList[i])
    else :
        print("Input ", i+1, " is not a valid directory name.")
        sys.exit()
    

def myCopy(source, dest):
    if not osp.exists(dest) :
        os.mkdir(dest)
        
    destList = os.listdir(dest)
    try :
        contents = os.listdir(source)
        print (source, "contains: ", contents)
    except PermissionError :
        print("Permission error - can't get contents of", source)
        os.chdir(osp.dirname(source))
        return
    
    for item in contents :
        newSrc = osp.join(source, item)
        newDest = osp.join(dest, item)
        filestats = os.stat(newSrc, follow_symlinks = True)
        
        if osp.isdir(newSrc) :
            print(newSrc, " is a directory. Copying to ", newDest)
            myCopy(newSrc, newDest)
            
        elif stat.S_ISLNK(filestats.st_mode) :
            print(newSrc, " is a symbolic link.")
            print("Copying ", newSrc, " to ", newDest)
            shutil.copy2(newSrc, newDest)
            
        elif osp.isfile(newSrc)  :
            
            print(newSrc, " is a file.")
            print("Copying ", newSrc, " to ", newDest)
            if osp.exists(newDest):
                os.chdir(osp.dirname(newDest))
                print("Found identical files! Copying newer version.")
                time1 = osp.getmtime(osp.abspath(newSrc))
                for file in destList :
                    print (file, " found in ", osp.abspath(file))
                    if osp.basename(file) == osp.basename(newSrc) :
                        time2 = osp.getmtime(osp.abspath(file))
                        newSrc2 = osp.join(source, file)
                    if time1 < time2 :
                        print("The existing file is newer. Not copying anything")
                    else :
                        print("Copying ", newSrc2, " to ", newDest)
                        shutil.copy2(newSrc2, newDest)
            else :
                shutil.copy2(newSrc, newDest)
            
def mergeDirs(source1, source2, dest) :
    myCopy(source1, dest)
    myCopy(source2, dest)
    
mergeDirs(inputList[0], inputList[1], inputList[2])
    
