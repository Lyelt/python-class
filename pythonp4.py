#Nicholas Ghobrial - Python Program 4 - Transactions

import re
import sys
from operator import itemgetter

dataLines = []      # List for storing original file input
amexList = []       # Store specifically American Express, Visa, and MasterCard
visaList = []
mcList = []

#----------------------------------------------------------------------------
#---Read in the data file and store it in dataLines
def getInput() :
    if len(sys.argv) != 3 :
        print ("Please enter input and output file names.")
    
    print ("Input: "+sys.argv[1])
    fileObj = open(sys.argv[1], "r")
    for line in fileObj :
        dataLines.append(line.strip("\n"))
        
    fileObj.close()
    
#---------------------------------------------------------------------------- 
#---Use the actual regular expressions and parse each line
def parseLines() :
    for line in dataLines :
        nameMatcher = re.compile(r"([A-Za-z]+)\s([A-Z][\.\s])?\s?([A-Za-z]+)(\sIII|\sIV|\sSr|\sJr|\sSr\.|\sJr\.)?")
        # Default is number format
        dateMatcher = re.compile(r"((?:0?[1-9])|(?:1[0-2]))[-/]((?:[012]?[0-9])|(?:3[01]))[-/]((?:(?:19)|(?:20))?[0-9]{2})")
        amountMatcher = re.compile(r"[\$]?([0-9]{1,6}(\.[0-9][0-9])?)")
        # Default is Visa
        cardMatcher = re.compile(r"([4][0-9]{15})|([4][0-9]{3}( [0-9]{4}){3})") 
        
        items = line.split(":") # List of each item on the line
        # Search for matches in each piece
        name = nameMatcher.search(items[0])
        date = dateMatcher.search(items[1])
        amount = amountMatcher.search(items[2])
        card = cardMatcher.search(items[3])
        #----Check for errors-------------------------------------------
        if not name :
            print ("Name not found on line: "+ line)
            continue
        if not date :
            # Try date text format
            dateMatcher = re.compile(r"([A-Za-z]+)\s((?:[012]?[0-9])|(?:3[01])),\s((?:(19)|(20))[0-9]{2})")
            date = dateMatcher.search(items[1])
            if not date :
                print ("Invalid date format on line: "+ line)
                continue
        if not amount :
            print ("Invalid amount on line: "+ line)
            continue
        
        amex = False
        visa = True
        mc = False
        if not card :
            # Not a Visa, trying MasterCard
            cardMatcher = re.compile(r"(5[1-5][0-9]{14})|(5[1-5][0-9]{2}( [0-9]{4}){3})")
            card = cardMatcher.search(items[3])
            amex = False
            visa = False
            mc = True
            if not card :
                # Not a MasterCard. Trying American Express
                cardMatcher = re.compile(r"((34|37[0-9]{2})|([2221-2720]) [0-9]{6} [0-9]{5})|(34|37[0-9]{13})|([2221-2720][0-9]{11})")
                card = cardMatcher.search(items[3])
                amex = True
                visa = False
                mc = False
                if not card :
                    print("No valid card number on line: "+ line)
                    amex = False
                    visa = False
                    mc = False
                    continue
        # Store line in appropriate list
        if amex :
            amexList.append([name, date, amount, card])
        elif visa :
            visaList.append([name, date, amount, card])
        elif mc :
            mcList.append([name, date, amount, card])
            
#----------------------------------------------------------------------------  
#---Allows converting of month name to number
def getMonth (month) :
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return months.index(month) + 1
    
#----------------------------------------------------------------------------  
#---Turns a line of data into a standard format. Returns a list of the
#---normalized data: [fname, mi, lname, ext, day, month, year, amount, card]
def normalizeData (dataList, cardType) :
    #----Day = DD
    day = int(dataList[1].group(2))
    #----If month is text, get its number. Otherwise, Month = MM
    if str(dataList[1].group(1)).isdigit() :
        month = dataList[1].group(1)
    else :
        month = getMonth(dataList[1].group(1))
    #----Turn year into YYYY format. 0-16 is assumed 2000s. 17-99 is 1900s
    year = int(dataList[1].group(3))
    if year > 16 and year < 100 :
        year += 1900
    elif year <= 16 :
        year += 2000
    
    #----Default = no middle initial or suffix
    ext = ""
    mi = ""
    lname = dataList[0].group(3)
    fname = dataList[0].group(1)
    if dataList[0].group(4) :
        ext = dataList[0].group(4)
        if ext.strip() == "Jr" or ext.strip() == "Sr" :
            ext = " "+ext.strip()+"."   # Make sure Jr/Sr end with period
        else :
            ext = dataList[0].group(4)  # III, IV
    if dataList[0].group(2) :
        mi = dataList[0].group(2)
        if not mi.endswith(".") :       # Make sure MI ends with a period
            mi = mi.strip()+"."
        
    #----Amount: add $ and decimal point if necessary
    amount = dataList[2].string
    if not str(amount).startswith("$") :
        amount = "$"+amount
    if str(amount).find(".") == -1 :
        amount = amount+".00"
        
    #----Card Number: add appropriate spacing if necessary
    card = dataList[3].string
    if card.find(" ") == -1 :
        if cardType == 'visa' or cardType == 'mc' :
            card = card[0:4] + " " + card[4:8] + " " + card[8:12] + " " + card[12:]
        elif cardType == 'amex' :
            card = card[0:4] + " " + card[4:10] + " " + card[10:]
            
    #----Returns a new list containing the normalized data
    return ([fname, mi, lname, ext, day, month, year, amount, card])

#----------------------------------------------------------------------------  
#---Returns sorted list, sorted in order of data, last name, and then amount
def sortList (dataList) :
    return sorted(dataList, key=itemgetter(6,5,4,2,7))

#----------------------------------------------------------------------------
#---Format the given list and print it neatly.
def doPrint (dataList, out) :
    print("---------------------------")
    for i in range(0, len(dataList)):
        card = str(dataList[i][8]).ljust(20)
        date = str(dataList[i][5]).zfill(2) + "/" + str(dataList[i][4]).zfill(2) + "/" + str(dataList[i][6])
        name = str(dataList[i][2] + dataList[i][3] + ", " + dataList[i][0] + " " + dataList[i][1]).ljust(20)
        amount = str(dataList[i][7])
        print(card + " : " + date + " : " + name + " : " + amount)
        out.write(card + " : " + date + " : " + name + " : " + amount + "\n")
        
#----------------------------------------------------------------------------
#---Normalize the data, sort each list, and then call print on each list.
#---Separated by American Express users, then MasterCard, and finally Visa.
def output () :
    for i in range(0, len(amexList)):
        amexList[i] = normalizeData(amexList[i], "amex")
    for i in range(0, len(mcList)):
        mcList[i] = normalizeData(mcList[i], "mc")
    for i in range(0, len(visaList)):
        visaList[i] = normalizeData(visaList[i], "visa")
        
    sortedAmex = sortList(amexList)
    sortedMc = sortList(mcList)
    sortedVisa = sortList(visaList)
    
    try :
        outFile = open(sys.argv[2], "w")
    except Exception as e : 
        print("Could not open specified output file.", e)
        sys.exit()
         
    doPrint(sortedAmex, outFile)
    doPrint(sortedMc, outFile)
    doPrint(sortedVisa, outFile)
    
    outFile.close()
    
#----------------------------------------------------------------------------             
getInput()
parseLines()
output()