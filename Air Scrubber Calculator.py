class airScrubber:
    # Constructor method (initializer)
    def __init__(self, scrubberType, cfmValue):
        self.scrubberType = scrubberType
        self.cfmValue = cfmValue
        

    def setFlag(self, flag):
        self.flag = flag

    def __str__(self):
        return f"({self.scrubberType})"


#------------------------function defs--------------------------------------
#returns list of all combinations of airscrubber that cfms sum to the target cfm or less
def findScrubberCombos(scrubbersCfms, cfmTar):
    def backtrack(start, path, total):
        if total <= cfmTar:
            result.append(path)
        for i in range(start, len(scrubbersCfms)):
            if total + scrubbersCfms[i] <= cfmTar:
                backtrack(i, path + [scrubbersCfms[i]], total + scrubbersCfms[i])
    
    result = []
    scrubbersCfms.sort()  # Ensure scrubbersCfms is sorted
    backtrack(0, [], 0)
    return result

#filter out undesired combos
def filterAirScrubbers(scrubberCombos, cfmTarget, original):
    finalArray = []
    toRemove = []
    
    for scrubberCombo in scrubberCombos:
        #add combo from original array that have a cfm sum equal to the target cfm to a removal list and a final list
        if sum(scrubberCombo) == cfmTarget:
            finalArray.append(scrubberCombo)
            toRemove.append(scrubberCombo)
        #add combo thats more than one AS away from target to removal list
        if cfmTarget - sum(scrubberCombo) >= max(original):
            toRemove.append(scrubberCombo)
    
    #remove undesired combos
    for items in toRemove:
        scrubberCombos.remove(items)

    toRemove = list(filter(None, toRemove))
    scrubberCombos = list(filter(None, scrubberCombos))
    
    #return array with cfm sums equal to target cfm
    return finalArray

#encode overflow scrubbers into combos
def addOverflowScrubber(scrubberCombos, original, scrubbers, cfmTarget):
    i = 1
    for scrubberCombo in scrubberCombos:
        scrubberCombo.append("")
        integers = [x for x in scrubberCombo if isinstance(x, int)]

        #represent overflow scrubbers as strings in the final slot of combo array in a (AS1/AS2) format
        for cfm in original:
            for scrubber in scrubbers:
                if cfm == scrubber.cfmValue:
                    tempCfm = scrubber.scrubberType
            
            if (sum(integers) + cfm > cfmTarget) and (i < len(original)):
                scrubberCombo[-1] = scrubberCombo[-1] + str(tempCfm) + '/'
            elif (sum(integers) + cfm > cfmTarget):
                scrubberCombo[-1] = scrubberCombo[-1] + str(tempCfm)
            i += 1
        i = 1 

#convert 2D list of cmf values to list of air scrubber name strings
def cmfToName2D(arr2D, scrubbers):
    for i in range(len(arr2D)):
        for j in range(len(arr2D[i])):
            for scrubber in scrubbers:
                if arr2D[i][j] == scrubber.cfmValue:
                    arr2D[i][j] = scrubber.scrubberType

#convert list from name to cmf values
def nameToCmf1D(arr1D, scrubbers):
        for scrubber in scrubbers:
            for j in range(len(arr1D)):
                if scrubber.scrubberType == arr1D[j]:
                    arr1D[j] = scrubber.cfmValue

#seperate A1/A2 element into individual componenets [A1,A2] and organise lists
def splitOrString(comboList, finalString, split, totalList, index, final):
    toRemove = []

    if '/' in comboList[index][-1]:
        finalString = comboList[index][-1]
        split = finalString.split("/")
        totalList = comboList[index] + split
    #if no A1/A2 component then split equals whole combo
    else:
        split = final[index]
        totalList  = split
    
    #remove original A1/A2 component from list
    for element in totalList:
        if '/' in element:
            toRemove.append(element)
    for item in toRemove:
        totalList.remove(item)
        toRemove = []

    return finalString, split, totalList

#sum all cmf values (for [A1, A2/A3] sumAllCmfs returns A1+A2+A3)
def sumAllCmfs(totalList, scrubbers):
    total = 0
    for scrubber in scrubbers:
        for scrubberName in totalList:
            if scrubberName == scrubber.scrubberType:
                total = total + scrubber.cfmValue
    return total

#calculate the sum for each combination
def sumRequiredCmfs(split, tempFinal, tempPrintValues, total, finalPrintValues, index, final, scrubbers):
    #handle cases without A1/A2 components
    if split == final[index]:
                nameToCmf1D(tempFinal, scrubbers)
                finalPrintValues.append(sum(tempFinal))
    #handle cases with A1/A2 component
    else: 
        #calculate total cmf of each combo within one list as oposed to A1+A2+A3 we have A1+A2 and A1+A3 for [A1, A2/A3] 
        for k in range(len(split)):
            for scrubber in scrubbers:
                #pick specific cmf value from A1/A2 and calculate total for that combo 
                #for [A1, A2/A3] seperate into A1 A3 and A1 A2 then calculate totals and add to list for printing later
                if split[k] == scrubber.scrubberType:
                    newArray = split[:k] + split[k + 1:]
                    for z in range(len(newArray)):
                        for scrubber in scrubbers:
                            if newArray[z] == scrubber.scrubberType:
                                newArray[z] = scrubber.cfmValue
                    tempPrintValues.append(total - sum(newArray))
                    #print(split, split[k], newArray, "split----------", tempPrintValues, k, len(split))
                    if k == len(split) - 1:
                        finalPrintValues.append(tempPrintValues)

#find sums of cfms for each combo to output
def getCmfSums(finalPrintValues, final, scrubbers):
    for i in range(len(final)):
        split = []
        finalString = []
        tempPrintValues = []
        totalList = []
        
        finalString, split, totalList = splitOrString(final, finalString, split, totalList, i, final)
        total = sumAllCmfs(totalList, scrubbers)
        tempFinal = final[i][:]
        sumRequiredCmfs(split, tempFinal, tempPrintValues, total, finalPrintValues, i, final, scrubbers)

#check if a value is a number or not
def isNumber(s):
    try:
        float(s)
        #return true if value is a number
        return True
    except ValueError:
        #return false if value is not a number
        return False
    
#check if a value is an int or not
def isInt(s):
    try:
        int(s)
        #return true if value is an int
        return True
    except ValueError:
        #return false if value is not an int
        return False
    
#function to get a valid input from user
def getValidInput(prompt, isInt = False):
    while True:
        try:
            value = input(prompt)
            if isInt:
                value = int(value)
            else:
                value = float(value)
            return value
        
        except ValueError:
            if isInt:
                print("Invalid input. Please enter a valid integer.")
            else:
                print("Invalid input. Please enter a valid number.")

#assign validated inputs to respective variables
def getInputs():
    #check and assign valid user unit inputs
    while True:
        units = input("Enter m for meters or f for feet: ").lower()
        if units == 'm' or units == 'f':
            print("valid")
            break
        else:
            print("invalid")
    
    while True:
        try:
            roomLength = getValidInput("Enter the length: ")
            roomWidth = getValidInput("Enter the width: ")
            roomHeight = getValidInput("Enter the height: ")
            airChanges = getValidInput("Enter the count:", isInt)
            print(f"Length: {roomLength}, Width: {roomWidth}, Height: {roomHeight}, Air Changes: {airChanges}")
            break  # Exit the loop if all inputs are valid
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    return units, roomLength, roomWidth, roomHeight, airChanges 
    
def meterToFeet(roomLength, roomWidth, roomHeight, units):
    #convert from meters to feet
    if units == "m":
        roomLength = roomLength*3.28084
        roomWidth = roomWidth*3.28084
        roomHeight = roomHeight*3.28084
    return roomLength, roomWidth, roomHeight

#calculate the required cfm for desired air changes
def calculateTargetCfm(roomLength, roomWidth, roomHeight, airChanges):
    #calculate volumes
    roomVolume = roomLength*roomWidth*roomHeight
    totalVolume = roomVolume*float(airChanges)
    #return target cfm
    return totalVolume/60

def main():
    finalPrintValues = []
    scrubbersCfms = []
    #list to store all scrubbers the user has at their facility
    scrubbers = [airScrubber("pheonix", 485), airScrubber("xPower", 650), airScrubber("thor", 1000)]

    #list that stores all the users air scrubbers cfm values 
    for scrubber in scrubbers:
        scrubbersCfms.append(scrubber.cfmValue)

    units, roomLength, roomWidth, roomHeight, airChanges = getInputs()
    
    roomLength, roomWidth, roomHeight = meterToFeet(roomLength, roomWidth, roomHeight, units)
    
    cfmTarget = calculateTargetCfm(roomLength, roomWidth, roomHeight, airChanges)

    #perform combination finding, cfm total calculations and combination filtering
    scrubberCombos = findScrubberCombos(scrubbersCfms, cfmTarget)
    final = filterAirScrubbers(scrubberCombos, cfmTarget, scrubbersCfms)
    addOverflowScrubber(scrubberCombos, scrubbersCfms, scrubbers, cfmTarget)
    final = final + scrubberCombos
    cmfToName2D(final, scrubbers)
    
    #sort output from least elements to most elements
    final = sorted(final, key=len)
    
    getCmfSums(finalPrintValues, final, scrubbers)

    #output air scrubber combinations and cmf total
    i = 0
    print("\n -----FINAL OUTPUT-----")
    for combo in final:
        if isinstance(finalPrintValues[i], int):
            print(combo, f"[{finalPrintValues[i]}]")
            i += 1
        else:
            print(combo, finalPrintValues[i])
            i += 1
    print(f"Length: {roomLength}, Width: {roomWidth}, Height: {roomHeight}, Air Changes: {airChanges}, Units: {units}, CFM: {cfmTarget}")
#------------------------function defs--------------------------------------^

if __name__ == "__main__":
    main()
    


#to-do
#add dynamic air scrubber adding from user

#testing
#print("final        ", final)
#print( "original     ", scrubberCombos)
#print("removed      ", toRemove)
#print("after removal", scrubberCombos)