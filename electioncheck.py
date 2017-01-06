import sys

voterList = []
electionLines = []

def getInput() :
    if len(sys.argv) != 3 :
        print("Please enter the two files to be searched.")
        sys.exit()
    
    voteFileName = sys.argv[1]
    voterFileName = sys.argv[2]
    try :
        voteFileObj = open(voteFileName, "r")
        voterFileObj = open(voterFileName, "r")
    except FileNotFoundError :
        print("Please enter valid file names.")
        sys.exit()
    except PermissionError :
        print("You do not have the permissions to access the files.")
        sys.exit()
    
    for line in voterFileObj :
        voterList.append(line.strip('\n'))
        
    for line in voteFileObj :
        electionLines.append(line)
        
    voteFileObj.close()
    voterFileObj.close()
    
def validateInput() :
    voted = []
    name = ""
    votedFor = ""
    clinton = trump = 0
    for vote in electionLines :
        voteList = vote.split(":")
        name = voteList[1] + " " + voteList[0]
        voted.append(name)
        
    for vote in electionLines :
        votedFor = voteList[2]
        voteList = vote.split(":")
        name = voteList[1] + " " + voteList[0]
        
        if not name in voterList :
            print(name, " is not a registered voter. Vote doesn't count!")
        elif voted.count(name) > 1 :
            print(name, " voted more than once! Vote disqualified.")
        else :
            print(name, " voted for ", votedFor.strip())
            if votedFor.lower().strip() == "clinton" :
                clinton += 1
            elif votedFor.lower().strip() == "trump" :
                trump += 1
            else :
                print(name, " did not vote for a valid candidate.")
                
    return ((clinton, trump))
        
getInput()
votes = validateInput()
print("-------------------------------")
print("The total votes are as follows:")
print("Clinton has won ", votes[0], " votes.")
print("Trump has won ", votes[1], " votes.")