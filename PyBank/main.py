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
            print(f"Something went wrong. Verify the source file exists in {self.sourcePath}, also verify you do not have the file {self.destPathFile} open if it already exists and try running the script again") 
            traceback.print_exc()
            return

    def analizeFile(self):
        dictOfChanges = dict()
        listOfProfitLoses = list()
        changeList = list()
        totalNumberOMonths = 0
        with open(self.sourcePathFile,"r") as csvfile: 
            contents = csv.reader(csvfile)  #Read the CSV file
            next(csvfile) # This is the tile row, skipping it. S
            fRow = next(csvfile).split(",") # Extract the first Row to get value and date. 
            # fDate = fRow[0] #Not needed, so I commented it out. 
            oldValue = int((fRow[1]).replace("\n",""))
            fValue = oldValue # this is to add it to the total value at the end since the next function removes the first row
            for row in contents:  #iterate through hte CSV file to collect data and make calculations, contents now is missing the title and the first value.
                profitLoses = int(row[1])
                changeCalc = profitLoses - oldValue
                changeList.append(changeCalc)
                dictOfChanges.update({changeCalc : row[0]})  #build a dictionary to get the highest and lowest change in profit at the end. 
                totalNumberOMonths += 1
                listOfProfitLoses.append(int(profitLoses))
                oldValue = profitLoses

        self.totalNumberOMonths = str(totalNumberOMonths  + 1) # total months variable plus one since the first row was removed at the begining.  
        self.totalAmount = "$" + str(sum(listOfProfitLoses) + fValue) # sum of values plus the first value that again was removed by the next function
        self.averageChange = "$" + str(round(sum(changeList) / len(changeList), 2))
        self.greatestIncrease = max(changeList)
        self.greatestDecrease = min(changeList)
        self.gIncreaseDate = dictOfChanges[self.greatestIncrease] #extracting the greatest inc and dec from the dictionary built in the loop. 
        self.gDecreaseDate = dictOfChanges[self.greatestDecrease]
        self.greatestIncreaseText = self.gIncreaseDate + " ($" + str(max(changeList)) + ")"
        self.greatestDecreaseText = self.gDecreaseDate + " ($" + str(min(changeList)) + ")"

    def printAndOutputFile(self):
        printList = [   # concoct the list to print and to make the file 
            "Financial Analysis",
            "----------------------------",
            "Total Months: " + self.totalNumberOMonths,
            "Total: " + self.totalAmount,
            "Average Change: " + self.averageChange,
            "Greatest Increase in Profits: " + self.greatestIncreaseText,
            "Greatest Decrease in Profits: " + self.greatestDecreaseText,
            "```",
        ]

        for statement in printList:
            print(statement)

        print(f"CREATING FILE IN LOCATION {self.destPathFile}" ) 

        with open(self.destPathFile, "w") as txtFile:
            for statement in printList:
                txtFile.write("%s\n" % statement) # write each item on a new line
   
        print("FILE CREATED.")  
        print("EXITING SCRIPT.") 

    def endScript():
        return  


if __name__ == "__main__":
    currentDirectory = os.getcwd() # Obtain current directory
    sourcePath = currentDirectory + "/Resources/" 
    sourcePathFile = sourcePath + "budget_data.csv"
    
    if not os.path.isfile(sourcePathFile):
        print("SOURCE FILE DOES NOT EXIST. CORRECT THIS AND TRY AGAIN")
        OpenAnalizeCSV.endScript()

    destPath = currentDirectory + "/analysis/"
    if not os.path.exists(destPath): # Check if destination location exists, else create it
        os.makedirs(destPath)

    destPathFile = destPath + "Financial Analysis.txt"
    createTextFile = OpenAnalizeCSV(sourcePathFile, destPathFile, sourcePath)