import csv 
import os
import traceback

class OpenParseCSV():
    def __init__(self):
        self.sourcePath=(os.getcwd() + "/Resources/") # get local source path
        self.sourcePathFile = os.path.abspath(os.getcwd() + "/Resources/budget_data.csv") # Get local source path file name
        self.destPath = os.path.abspath(os.getcwd() + "/analysis/") # assign destination path
        self.destPathFile=(self.destPath + "/Financial Analysis.txt") # assign destination file name
        if not os.path.exists(self.destPath): # Check if destination location exists, else create it, but should exist if the challenge instructions were followed. 
            os.makedirs(self.destPath)
    
        if not os.path.isfile(self.sourcePathFile): # if the sourcepath does not exist end the script, path should exist if instructions were followed. 
            print("SOURCE FILE DOES NOT EXIST. MAKE SURE THIS PATH EXISTS: {self.sourcePathFile}")
            self.endScript()

    def analizeFile(self):
        self.dictOfChanges = dict()  # create a dictionary, 2 lists and a counter for the total number of months
        self.listOfProfitLoses = list()
        self.changeList = list()
        self.totalNumberOfMonths = 0
        with open(self.sourcePathFile,"r") as csvfile: 
            contents = csv.reader(csvfile)  # Read the CSV file
            next(csvfile) # This is the tile row, skipping it.
            fRow = next(csvfile).split(",") # Extract the first Row to get value for change calculation
            oldValue = int((fRow[1]).replace("\n","")) # remove unwanted escape, new row characters "\n" 
            fValue = oldValue # keeping the first value to add it to the total value at the end since the next function removes the first row
            for row in contents:  #iterate through hte CSV file to collect data and make calculations, content is now is missing the title and the first value.
                profitLoses = int(row[1])
                changeCalc = profitLoses - oldValue
                self.changeList.append(changeCalc)
                self.dictOfChanges.update({changeCalc : row[0]})  #build a dictionary to get the highest and lowest change in profit at the end. 
                self.totalNumberOfMonths += 1
                self.listOfProfitLoses.append(int(profitLoses))
                oldValue = profitLoses

        self.totalNumberOfMonths = str(self.totalNumberOfMonths  + 1) # total months plus one since the first row was removed at the begining by the next function.  
        self.totalAmountText = "$" + str(sum(self.listOfProfitLoses) + fValue) # sum of values plus the first value that was also removed by the next function
        self.averageChangeText = "$" + str(round(sum(self.changeList) / len(self.changeList), 2))
        self.greatestIncrease = max(self.changeList) #extracting the greatest increase and decrease values and dates from the dictionary built in the for loop. 
        self.greatestDecrease = min(self.changeList)
        self.gIncreaseDate = self.dictOfChanges[self.greatestIncrease] 
        self.gDecreaseDate = self.dictOfChanges[self.greatestDecrease]
        self.greatestIncreaseText = self.gIncreaseDate + " ($" + str(max(self.changeList)) + ")"
        self.greatestDecreaseText = self.gDecreaseDate + " ($" + str(min(self.changeList)) + ")"

    def printAndOutputFile(self):
        self.printList = [   # concoct the list to print and to make the file 
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

        for statement in self.printList: print(statement)

        print(f'CREATING FILE "Financial Analysis.txt" IN LOCATION {self.destPath}') 

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
        openParseCSV.analizeFile()
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