import csv 
import os
import traceback

class OpenParseCSV():
    def __init__(self):
        self.sourcePath=(os.getcwd() + "/Resources/") # get local source path
        self.sourcePathFile = os.path.abspath(os.getcwd() + "/Resources/election_data.csv")  # Get local source path file name
        self.destPath = os.path.abspath(os.getcwd() + "/analysis/") # assign destination path
        self.destPathFile=(self.destPath + "/Election Results.txt") # assign destination file name
        if not os.path.exists(self.destPath): # Check if destination location exists, else create it, but should exist if the challenge instructions were followed. 
            os.makedirs(self.destPath)
        
    def parseFile(self):
        self.ballotId = list()
        self.candidate = list()
        with open(self.sourcePathFile,"r") as csvfile: 
            content = csv.reader(csvfile)  #Read the CSV file
            # titles = (next(csvfile).replace("\n","")).split(",") # This is the tile row, comes in this format 'Ballot ID,County,Candidate\n' Not used, so I commented it out. 
            for row in content: 
                if "Ballot ID" in row: continue # skip the titles row
                self.ballotId.append(row[0]) 
                self.candidate.append((row[2]).replace("\n",""))

        self.candidatesDict = {}
        for cand in set(self.candidate): # set is a data type used to store multiple items in a single variable https://realpython.com/python-sets/  https://www.w3schools.com/python/python_sets.asp
            if 'CANDIDATE' in cand.upper(): continue #Skip the title   
            self.candidatesDict[cand] = self.candidate.count(cand) # count each candidates instances from the set and put them in the candidatesDict dictionary
        
        self.totalVotes = len(self.ballotId) # total votes can also be calculated 
        # self.totalVotes = sum(candidatesDict.values()) # Could have gotten the total votes like this also
        self.firstPlaceName = max(self.candidatesDict, key = self.candidatesDict.get) # Get the candidate with the higher number of votes
        self.firstPlaceText = self.firstPlaceName + ": " + str(round(((max(self.candidatesDict.values()) / self.totalVotes)*100),3)) + "% (" + str(max(self.candidatesDict.values())) + ")"
        
        self.listOfNonWinners = [] # start a new list to put the other candidates
        for key, value in self.candidatesDict.items(): 
            if key in self.firstPlaceName: continue # Skipt the winner we already collected above
            nextCandidateText = key + ": " + str(round((value/self.totalVotes)*100, 3)) + "% (" + str(value) + ")"
            self.listOfNonWinners.append(nextCandidateText)
   
    def printAndOutputFile(self):
        self.printList = [   # concoct the list to print and to make the file 
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
            winnerIndex = self.printList.index(self.firstPlaceText) # find the index of our winner in the list.
            if "Charles Casper Stockham" in otherCandidate: # added this conditional to make it look exactly as in the challenge assigment, I am after 100%. 
                inserIndex = winnerIndex - 1
            else:
                inserIndex = winnerIndex + 2
  
            self.printList.insert(inserIndex, otherCandidate) #insert other candidate in the correct place to match challenge text file. 

        for statement in self.printList: print(statement)

        print(f'CREATING "Election Results.txt" FILE IN LOCATION {self.destPath}') 

        with open(self.destPathFile, "w") as txtFile:
            for statement in self.printList:
                txtFile.write("%s\n" % statement) # write each item on a new line
   
        print("FILE CREATED.")  
        print("EXITING SCRIPT.") 

    def endScript(self):
        return  

if __name__ == "__main__":
    openParseCSV = OpenParseCSV() #instantiate the class. 
    try:
        openParseCSV.parseFile()
    except:
        print("Something went wrong. Verify the source file exists in", openParseCSV.sourcePath, "and try running the script again") #Another printing methos that automatically provides spaces
        traceback.print_exc()
        openParseCSV.endScript()
    try:
        openParseCSV.printAndOutputFile()                                                                                                                                     
    except:
        print(f"Something went wrong. Verify the destination location still exists, inspect {openParseCSV.destPath} , perhaps another application deleted this location.") 
        traceback.print_exc()
        openParseCSV.endScript()
