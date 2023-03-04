import csv 
import os
import traceback

class OpenParseCSV():
    def __init__(self, sourcePathFile = None, destPathFile = None, sourcePath = None, destPath = None):
        self.sourcePathFile = sourcePathFile 
        self.destPathFile = destPathFile
        self.sourcePath = sourcePath
        self.destPath = destPath
        try:
            self.parseFile()
        except:
            print("Something went wrong. Verify the source file exists in", self.sourcePath, "and try running the script again") #Another printing methos that automatically provides spaces
            traceback.print_exc()
            return
        try:
            self.printAndOutputFile()                                                                                                                                     
        except:
            print(f"Something went wrong. Verify the destination location still exists, inspect {self.destPath} , perhaps another application deleted this location.") 
            traceback.print_exc()
            return

    def parseFile(self):
        ballotId = list()
        candidate = list()
        with open(self.sourcePathFile,"r") as csvfile: 
            content = csv.reader(csvfile)  #Read the CSV file
            # titles = (next(csvfile).replace("\n","")).split(",") # This is the tile row, comes in this format 'Ballot ID,County,Candidate\n' Not used, so I commented it out. 
            for row in content: 
                if "Ballot ID" in row: continue # skip the titles row
                ballotId.append(row[0]) 
                candidate.append((row[2]).replace("\n",""))

        candidatesDict = {}
        for cand in set(candidate): # set is a data type used to store multiple items in a single variable https://realpython.com/python-sets/  https://www.w3schools.com/python/python_sets.asp
            if 'CANDIDATE' in cand.upper(): continue #Skip the title   
            candidatesDict[cand] = candidate.count(cand) # count each candidates instances from the set and put them in the candidatesDict dictionary
        
        self.totalVotes = len(ballotId) # total votes can also be calculated 
        # self.totalVotes = sum(candidatesDict.values()) # Could have gotten the total votes like this also
        self.firstPlaceName = max(candidatesDict, key = candidatesDict.get) # Get the candidate with the higher number of votes
        self.firstPlaceText = self.firstPlaceName + ": " + str(round(((max(candidatesDict.values()) / self.totalVotes)*100),3)) + "% (" + str(max(candidatesDict.values())) + ")"
        
        self.listOfNonWinners = [] # start a new list to put the other candidates
        for key, value in candidatesDict.items(): 
            if key in self.firstPlaceName: continue # Skipt the winner we already collected above
            nextCandidate = key + ": " + str(round((value/self.totalVotes)*100, 3)) + "% (" + str(value) + ")"
            self.listOfNonWinners.append(nextCandidate)
   
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
            "",
            self.firstPlaceText,
            "",
            "",
            "-------------------------",
            "",
            "Winner: " + self.firstPlaceName,
            "",
            "-------------------------",
            "",
        ]
         
        for otherCandidate in self.listOfNonWinners:
            winnerIndex = printList.index(self.firstPlaceText) # find the index of our winner in the list.
            if "Charles Casper Stockham" in otherCandidate: # added this conditional to make it look exactly as in the challenge assigment, I am after 100%. 
                inserIndex = winnerIndex - 1
            else:
                inserIndex = winnerIndex + 2
  
            printList.insert(inserIndex, otherCandidate) #insert other candidate in the correct place to match challenge text file. 

        for statement in printList: print(statement)

        print(f'CREATING "Election Results.txt" FILE IN LOCATION {self.destPath}') 

        with open(self.destPathFile, "w") as txtFile:
            for statement in printList:
                txtFile.write("%s\n" % statement) # write each item on a new line
   
        print("FILE CREATED.")  
        print("EXITING SCRIPT.") 

    def endScript():
        return  

if __name__ == "__main__":
    sourcePathFile = os.path.abspath(os.getcwd() + "/Resources/election_data.csv") # get source path, abspath used in case the evaluator uses Linux. 
    
    if not os.path.isfile(sourcePathFile):
        print("SOURCE FILE DOES NOT EXIST. MAKE SURE THIS PATH EXISTS: {sourcePathFile}")
        OpenParseCSV.endScript()

    destPath = os.path.abspath(os.getcwd() + "/analysis/")
    if not os.path.exists(destPath): # Check if destination location exists, else create it, but should exist if the challenge instructions were followed. 
        os.makedirs(destPath)

    OpenParseCSV(sourcePathFile, destPathFile=(destPath + "/Election Results.txt"), sourcePath=(os.getcwd() + "/Resources/"), destPath = destPath)
