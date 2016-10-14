#Directory Merger Program
#Nicholas Ghobrial - P3

import sys
import os
import os.path as osp
import stat
import shutil

print ("This program will merge two source directories into a destination directory.")

def getInput () :
    if len(sys.argv) != 4:
        print("Must enter exactly 2 source directories and 1 destination.")
        sys.exit()
        
    for i in range(1,4) :
        sys.argv[i] = osp.abspath(sys.argv[i])
        if osp.isdir(sys.argv[i]) : 
            print("Input ", i, ": ", sys.argv[i])
        elif i == 3 :
            try :
                os.mkdir(sys.argv[i])
                print("Destination: ", sys.argv[i])
            except OSError :
                print("Destination already exists - cannot merge.")
                sys.exit()
        else :
            print("Input ", i, " is not a valid directory name.")
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

getInput()
mergeDirs(sys.argv[1], sys.argv[2], sys.argv[3])
