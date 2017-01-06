#Nicholas Ghobrial Program 2

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
seenWordDict = {} #key = word, value = number of times seen
maxWordLength = 0 #Length of the longest word seen so far

#Open the file
fileName = input("Please enter the name of text file to analyze: ")
fileObj = open(fileName, "r")

#Build the dictionary of words and their frequencies
for line in fileObj:
    wordList = line.split()
    for index in range(0, len(wordList)):
        wordList[index] = wordList[index].strip(",.?!'\/:;@#$%^&*()-_+=\"<>{}[]0123456789`~|")
        wordList[index] = wordList[index].lower()
    
    for word in wordList:
        if len(word) > maxWordLength:   #Store the max word length
            maxWordLength = len(word)
        if word in seenWordDict:        #If the word's already in it, increment count
            seenWordDict[word] += 1
        else:
            seenWordDict[word] = 1      #Otherwise, add it
            
fileObj.close()

#--------------------------------------------------------------------------------------------------------
#Now set up the data structure
mainList = [] #Main list, length of the longest word seen so far
for i in range(0, maxWordLength):
    mainList.append({})                     #Each slot is a dictionary
    for k in range(0, 26):
        mainList[i][alphabet[k]] = set()    #Key = letter in alphabet, Value = set of words
   
for word in seenWordDict:
    for j in range(0, len(word)):           #Process each letter of each word
        if (word[j] in alphabet):
            mainList[j][word[j]].add(word)  #Add the word to every set it corresponds to

#--------------------------------------------------------------------------------------------------------
#Now process user input
answer = "y"

while answer.lower() == "y":
    #Reset and initialize all data structures
    totalOccur = 0  #Total occurrences of words in answer
    answerDict = {} 
    answerList = []
    answerSet = set()
    end = False
    
    #Make sure input is at least two letters long
    while(True):
        inputWord = input("Enter beginning of a word to autocomplete: ")
        if len(inputWord) <= 1:
            print ("Please enter at least two letters to autocomplete.")
        else:
            break
        
    #Intersect all answer sets, two at a time
    for i in range(0, len(inputWord)-1):
        if i == 0:
            #Intersect the first two sets of words
            answerSet = mainList[i][inputWord[i]] & mainList[i+1][inputWord[i+1]]
        else:
            #Then intersect the result with the remaining sets
            answerSet = answerSet & mainList[i+1][inputWord[i+1]]
        if answerSet == set():
            print ("There are no words that begin with that input.")
            end = True
            break
        
    #Put the answer set into a dictionary    
    if (end != True):
        for word in answerSet:
            answerDict[word] = seenWordDict[word]
            totalOccur += seenWordDict[word]    #Sum up the total occurrences
        answerList = sorted(answerDict, key=answerDict.get, reverse=True) #Convert to a sorted list
        
        count = 0
        #Calculate percentage of each word. Print top 5 results
        for word in answerList:
            percent = (answerDict[word] / totalOccur) * 100
            print("The word ", word, " occurs ", answerDict[word], " times, or ", "%.2f" % percent, "% of the time.")
            count += 1;
            if count == 5:
                break
    
    answer = input("Would you like to enter another word? (y/n)")    

print("Program terminating. Thank you for using autocomplete.")