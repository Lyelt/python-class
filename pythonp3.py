#Directory Merger Program
#Nicholas Ghobrial - P3

import sys
import os
import os.path as osp
import stat
import shutil
import time

print ("This program will merge two source dirs into a destination directory.")
# -----------------------------------------------------------------------------
def getInput () :   # Reads command line args and validates
    # Make sure there are 3 directories entered
    if len(sys.argv) != 4:
        print("Must enter exactly 2 source directories and 1 destination.")
        sys.exit()
        
    for i in range(1,4) :
        sys.argv[i] = osp.abspath(sys.argv[i])  # Convert to absolute pathname
        if osp.isdir(sys.argv[i]) : 
            print("Input ", i, ": ", sys.argv[i]) # Proper input
        elif i == 3 :
            # Make the destination directory if it doesn't exist
            try :
                os.mkdir(sys.argv[i])
                print("Destination: ", sys.argv[i])
            except OSError :
                print("Destination already exists - cannot merge.")
                sys.exit()
        else :
            print("Input ", i, " is not a valid directory name.")
            sys.exit()  

# -----------------------------------------------------------------------------
def myCopy(source, dest):
    if not osp.exists(dest) :
        os.mkdir(dest) # Make the destination if it doesn't exist
        
    destList = os.listdir(dest) # List of contents of dest folder
    try :
        contents = os.listdir(source) # List of contents of source
        #print (source, "contains: ", contents)
    except PermissionError :
        print("Permission error - can't get contents of", source)
        os.chdir(osp.dirname(source))
        return
    
    for item in contents :
        newSrc = osp.join(source, item) # Get full pathname of source and dest
        newDest = osp.join(dest, item)
        filestats = os.stat(newSrc, follow_symlinks = True) # For symlinks
        
        if osp.isdir(newSrc) :
            # If the found item is a directory, recursively copy its contents
            #print(newSrc, " is a directory. Copying to ", newDest)
            myCopy(newSrc, newDest)
            
        elif stat.S_ISLNK(filestats.st_mode) :
            # If the item is a link, follow the link and copy it
            #print(newSrc, " is a symbolic link.")
            #print("Copying ", newSrc, " to ", newDest)
            shutil.copy2(newSrc, newDest)
            
        elif osp.isfile(newSrc)  :
            # If item is a file, check if it matches an existing file
            #print(newSrc, " is a file.")
            #print("Copying ", newSrc, " to ", newDest)
            if osp.exists(newDest):
                os.chdir(osp.dirname(newDest))
                #print("Found identical files! Copying newer version.")
                time1 = osp.getmtime(osp.abspath(newSrc))
                # Compare file modification times, copy the newer version
                for file in destList :
                    #print (file, " found in ", osp.abspath(file))
                    if osp.basename(file) == osp.basename(newSrc) :
                        time2 = osp.getmtime(osp.abspath(file))
                        newSrc2 = osp.join(source, file)
                    if time1 < time2 :
                        #print("The existing file is newer. No file copied")
                        continue
                    else :
                        #print("Copying ", newSrc2, " to ", newDest)
                        shutil.copy2(newSrc2, newDest)
            else :
                shutil.copy2(newSrc, newDest)
                
# -----------------------------------------------------------------------------
def printResults() :
    # Neatly print results of the merge
    print("\n------Source Folder 1------------------")
    printDirectory(sys.argv[1])
    print("\n------Source Folder 2------------------")
    printDirectory(sys.argv[2])
    print("\n------Merged Destination------------------")
    printDirectory(sys.argv[3])
            
# -----------------------------------------------------------------------------
def printDirectory(direc) :
    # Print detailed information about each file in the sources + dest
    contents = os.listdir(direc)
    for item in contents :
        dest = osp.join(direc, item)
        if osp.isdir(dest) :
            printDirectory(dest)
        else :
            print("{:.<70}{:.>25}".format(dest, time.ctime(osp.getmtime(dest))))
            
# -----------------------------------------------------------------------------
def mergeDirs(source1, source2, dest) :
    # Copy the two source directories to the destination
    myCopy(source1, dest)
    myCopy(source2, dest)
  
getInput()
mergeDirs(sys.argv[1], sys.argv[2], sys.argv[3])
printResults()
