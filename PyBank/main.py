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
            self.analizeFile()
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

    def analizeFile(self):
        dictOfChanges = dict()  # create a dictionary, 2 lists and a counter for the total number of months
        listOfProfitLoses = list()
        changeList = list()
        totalNumberOfMonths = 0
        with open(self.sourcePathFile,"r") as csvfile: 
            contents = csv.reader(csvfile)  # Read the CSV file
            next(csvfile) # This is the tile row, skipping it.
            fRow = next(csvfile).split(",") # Extract the first Row to get value for change calculation
            oldValue = int((fRow[1]).replace("\n","")) # remove unwanted escape, new row characters "\n" 
            fValue = oldValue # keeping the first value to add it to the total value at the end since the next function removes the first row
            for row in contents:  #iterate through hte CSV file to collect data and make calculations, content is now is missing the title and the first value.
                profitLoses = int(row[1])
                changeCalc = profitLoses - oldValue
                changeList.append(changeCalc)
                dictOfChanges.update({changeCalc : row[0]})  #build a dictionary to get the highest and lowest change in profit at the end. 
                totalNumberOfMonths += 1
                listOfProfitLoses.append(int(profitLoses))
                oldValue = profitLoses

        self.totalNumberOfMonths = str(totalNumberOfMonths  + 1) # total months plus one since the first row was removed at the begining by the next function.  
        self.totalAmountText = "$" + str(sum(listOfProfitLoses) + fValue) # sum of values plus the first value that was also removed by the next function
        self.averageChangeText = "$" + str(round(sum(changeList) / len(changeList), 2))
        self.greatestIncrease = max(changeList) #extracting the greatest increase and decrease values and dates from the dictionary built in the for loop. 
        self.greatestDecrease = min(changeList)
        self.gIncreaseDate = dictOfChanges[self.greatestIncrease] 
        self.gDecreaseDate = dictOfChanges[self.greatestDecrease]
        self.greatestIncreaseText = self.gIncreaseDate + " ($" + str(max(changeList)) + ")"
        self.greatestDecreaseText = self.gDecreaseDate + " ($" + str(min(changeList)) + ")"

    def printAndOutputFile(self):
        printList = [   # concoct the list to print and to make the file 
            "Financial Analysis",
            "",
            "----------------------------",
            "",
            "Total Months: " + self.totalNumberOfMonths,
            "",
            "Total: " + self.totalAmountText,
            "",
            "Average Change: " + self.averageChangeText,
            "",
            "Greatest Increase in Profits: " + self.greatestIncreaseText,
            "",
            "Greatest Decrease in Profits: " + self.greatestDecreaseText,
            "",
        ]

        for statement in printList: print(statement)

        print(f'CREATING FILE "Financial Analysis.txt" IN LOCATION {self.destPath}') 

        with open(self.destPathFile, "w") as txtFile:
            for statement in printList:
                txtFile.write("%s\n" % statement) # write each item on a new line
   
        print("FILE CREATED.")  
        print("EXITING SCRIPT.") 

    def endScript():
        return  


if __name__ == "__main__":
    sourcePathFile = os.path.abspath(os.getcwd() + "/Resources/budget_data.csv") # get source path 
    
    if not os.path.isfile(sourcePathFile):
        print("SOURCE FILE DOES NOT EXIST. MAKE SURE THIS PATH EXISTS: {sourcePathFile}")
        OpenParseCSV.endScript()

    destPath = os.path.abspath(os.getcwd() + "/analysis/")
    if not os.path.exists(destPath): # Check if destination location exists, else create it, but if the challenge documentation was followed it should already exist. 
        os.makedirs(destPath)

    OpenParseCSV(sourcePathFile, destPathFile=(destPath + "/Financial Analysis.txt"), sourcePath=(os.getcwd() + "/Resources/"), destPath = destPath)