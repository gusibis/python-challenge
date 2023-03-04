import csv 
import os
import traceback

class OpenAnalizeCSV():
    def __init__(self, sourcePathFile = None, destPathFile = None, sourcePath = None):
        self.sourcePathFile = sourcePathFile 
        self.destPathFile = destPathFile
        self.sourcePath = sourcePath
        try:
            self.analizeFile()
        except:
            print("Something went wrong. Verify the source file exists in", self.sourcePath, "and try running the script again") #Nother printing methos that provides padding and is also easy
            traceback.print_exc()
            return
        try:
            self.printAndOutputFile()                                                                                                                                     
        except:
            print(f"Something went wrong. Verify the source file exists in {self.sourcePath}, also verify you do not have the file {self.destPathFile} open if already exists and try running the script again") 
            traceback.print_exc()
            return

    def analizeFile(self):
        ballotId = list()
        candidate = list()
        with open(self.sourcePathFile,"r") as csvfile: 
            contents = csv.reader(csvfile)  #Read the CSV file
            # titles = (next(csvfile).replace("\n","")).split(",") # This is the tile row, comes in this format 'Ballot ID,County,Candidate\n' Not used, so I commented it out. 
            for row in contents: 
                ballotId.append(row[0]) 
                candidate.append((row[2]).replace("\n",""))

        candidatesDict = {}
        for cand in set(candidate): # set is a data type used to store multiple items in a single variable
            if 'CANDIDATE' in cand.upper(): #Skip the title
                continue
            candidatesDict[cand] = candidate.count(cand) # count each candidates instances and add them to the duplicatesDict dictionary

        self.totalVotes = len(ballotId) # total votes 
        self.firstPlaceName = max(candidatesDict, key = candidatesDict.get)
        self.firstPlaceText = max(candidatesDict, key = candidatesDict.get) + ": " + str(round(((max(candidatesDict.values()) / self.totalVotes)*100),3)) + "% (" + str(max(candidatesDict.values())) +")"
        self.lastPlaceName = min(candidatesDict, key = candidatesDict.get)
        self.lastPlaceText = min(candidatesDict, key = candidatesDict.get) + ": " + str(round(((min(candidatesDict.values()) / self.totalVotes)*100),3)) + "% (" + str(min(candidatesDict.values())) +")"
        del candidatesDict[self.firstPlaceName] #remove winner and last place to get the middle one. 
        del candidatesDict[self.lastPlaceName]
        self.middlePlaceText = list(candidatesDict.keys())[0] +": "+str(round(((int(list(candidatesDict.values())[0]) / self.totalVotes)*100),3)) + "% (" + str(int(list(candidatesDict.values())[0])) +")"

    def printAndOutputFile(self):
        printList = [   # concoct the list to print and to make the file 
            "Election Results",
            "",
            "-------------------------",
            "",
            "Total Votes: " + str(self.totalVotes),
            "",
            "-------------------------",
            "",
            self.middlePlaceText,
            self.firstPlaceText,
            self.lastPlaceText,
            "",
            "-------------------------",
            "",
            "Winner: " + self.firstPlaceName,
            "",
            "-------------------------",
        ]

        for statement in printList:
            print(statement)

        print(f"CREATING FILE IN LOCATION {self.destPathFile}") 

        with open(self.destPathFile, "w") as txtFile:
            for statement in printList:
                txtFile.write("%s\n" % statement) # write each item on a new line
   
        print("FILE CREATED.")  
        print("EXITING SCRIPT.") 

    def endScript():
        return  

if __name__ == "__main__":
    sourcePathFile = os.path.abspath(os.getcwd() + "/Resources/election_data.csv") # get source path 
    
    if not os.path.isfile(sourcePathFile):
        print("SOURCE FILE DOES NOT EXIST. CORRECT THIS AND TRY AGAIN")
        OpenAnalizeCSV.endScript()

    destPath = os.path.abspath(os.getcwd() + "/analysis/")
    if not os.path.exists(destPath): # Check if destination location exists, else create it, but should exist. 
        os.makedirs(destPath)

    createTextFile = OpenAnalizeCSV(sourcePathFile, destPathFile=(destPath + "/Election Results.txt"), sourcePath=(os.getcwd() + "/Resources/"))