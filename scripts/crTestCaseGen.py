#!/usr/bin/env python

import re
import math
import crTemplate

def csvBooleanExpand(csvLineData):
    """Each line which contains 'X' is duplicated and the X replace with 0,1. Only one expansion per line is processed"""
    ExpandOccurred = 0
    newCsvLineData = []
    for line in csvLineData:
        #print(line)
        newCsvLine = []
        booleanExpand = 0
        csvLine = line.split(',')
        tempLine = ''
        for variable in csvLine:
            #search for an x,X included in alphanumeric string before it, if true don't expand
            if re.search('[\s]*[a-zA-Z0-9]+x[\s]*', variable) or re.search('[\s]*[a-zA-Z0-9]+X[\s]*', variable):
                tempLine = tempLine + variable + ','
            #search for an x,X included in alphanumeric string after it, if true don't expand
            elif re.search('[\s]*x[a-zA-Z0-9]+[\s]*', variable) or re.search('[\s]*X[a-zA-Z0-9]+[\s]*', variable):
                tempLine = tempLine + variable + ','
            #search for an x,X with only spaces before or after, if true EXPAND, 
            #replace x,X with special string to be used later. 
            #This is done to ensure other x,X in the line remain untouched
            elif booleanExpand is 0 and (re.search('[\s]*x[\s]*', variable) or re.search('[\s]*X[\s]*', variable)):
                booleanExpand = 1
                tempLine = tempLine + "abcdefghijklmnopqrstuvwxyz" + ','
            #anything else also don't expand
            else:
                tempLine = tempLine + variable + ','
        #print(tempLine)
        if booleanExpand is 0:
            newCsvLineData.append(line)
        else:
            #remove extra end ','
            tempLine = tempLine[0:-1]
            #put back the original line and create the extra one
            newCsvLine.append(tempLine)
            newCsvLine.append(tempLine)
            #remove the special string with 0 and 1
            newCsvLine[0] = newCsvLine[0].replace('abcdefghijklmnopqrstuvwxyz','0',1)
            newCsvLine[1] = newCsvLine[1].replace('abcdefghijklmnopqrstuvwxyz','1',1)
            #add the new line to the final processed csv data
            newCsvLineData.append(newCsvLine[0])
            newCsvLineData.append(newCsvLine[1])
            ExpandOccurred = 1

    return ExpandOccurred, newCsvLineData

def csvRangeExpand(csvLineData):
    """Each line which contains 'MIN..STEP..MAX' is duplicated with the (MAX-MIN)/STEP replacements. Only one expansion per line is processed"""
    ExpandOccurred = 0
    newCsvLineData = []
    minRange = 0
    stepSize = 0
    maxRange = 0
    direction = 'UP'
    newRangeValue = 0
    requiredExpandLine = 0
    tempString = ''
    for line in csvLineData:
        #print(line)
        newCsvLine = []
        booleanExpand = 0
        csvLine = line.split(',')
        tempLine = ''
        for variable in csvLine:
            #search for an x,X with only spaces before or after, if true EXPAND, 
            #replace x,X with special string to be used later. 
            #This is done to ensure other x,X in the line remain untouched
            if booleanExpand is 0 and re.search('[\s]*[0-9][0-9]*[\s]*\.\.[\s]*[0-9][0-9]*[\s]*\.\.[\s]*[0-9][0-9]*[\s]*', variable):
                booleanExpand = 1
                tempString = variable.split('..')
                minRange = int(tempString[0])
                stepSize = int(tempString[1])
                maxRange = int(tempString[2])
                if minRange < maxRange:
                    direction = 'UP'
                else:
                    direction = 'DOWN'
                    minRange = int(tempString[2])
                    maxRange = int(tempString[0])
                tempLine = tempLine + "abcdefghijklmnopqrstuvwxyz" + ','
            #anything else also don't expand
            else:
                tempLine = tempLine + variable + ','
        #print(tempLine)
        if booleanExpand is 0:
            newCsvLineData.append(line)
        else:
            #remove extra end ','
            tempLine = tempLine[0:-1]
            #pull back to orignial line
            newCsvLine.append(tempLine)
            if direction is 'UP':
                newCsvLine[0] = newCsvLine[0].replace('abcdefghijklmnopqrstuvwxyz',str(minRange),1)
                newRangeValue = minRange
            else:
                newCsvLine[0] = newCsvLine[0].replace('abcdefghijklmnopqrstuvwxyz',str(maxRange),1)
                newRangeValue = maxRange
            #add the new line to the final processed csv data
            newCsvLineData.append(newCsvLine[0])
            #add a new line for each value in the range (MAX-MIN)/STEP
            #print(minRange)
            #print(stepSize)
            #print(maxRange)
            requiredExpandLine = int(math.ceil((maxRange - minRange)/stepSize))
            #print(requiredExpandLine)
            #remove the special string and replace with ranges values (minRange + stepSize + stepSize + stepSize + stepSize + MaxRange)
            for i in range(0,requiredExpandLine,1):
                newCsvLine.append(tempLine)
                if direction is 'UP':
                    newRangeValue = newRangeValue + stepSize
                    if newRangeValue <= maxRange:
                        newCsvLine[i+1] = newCsvLine[i+1].replace('abcdefghijklmnopqrstuvwxyz',str(newRangeValue),1)
                        #add the new line to the final processed csv data
                        newCsvLineData.append(newCsvLine[i+1])
                    else:
                        newCsvLine[i+1] = newCsvLine[i+1].replace('abcdefghijklmnopqrstuvwxyz',str(maxRange),1)
                        #add the new line to the final processed csv data
                        newCsvLineData.append(newCsvLine[i+1])
                else:
                    newRangeValue = newRangeValue - stepSize
                    if newRangeValue >= minRange:
                        newCsvLine[i+1] = newCsvLine[i+1].replace('abcdefghijklmnopqrstuvwxyz',str(newRangeValue),1)
                        #add the new line to the final processed csv data
                        newCsvLineData.append(newCsvLine[i+1])
                    else:
                        newCsvLine[i+1] = newCsvLine[i+1].replace('abcdefghijklmnopqrstuvwxyz',str(minRange),1)
                        #add the new line to the final processed csv data
                        newCsvLineData.append(newCsvLine[i+1])
            ExpandOccurred = 1

    return ExpandOccurred, newCsvLineData


def testCaseCodeGen(sourceTemplate, headerTemplate, testCaseDirAndFile, testCaseFileOnlyNoExt):   
    """Takes the Test Case Data and generates C code to run with the Module under test"""

    #file handling
    fh = open(testCaseDirAndFile, 'r')
    raw_testCase_data = fh.read()
    fh.close()
    testCaseLineData = raw_testCase_data.split('\n')

    #open the c file template
    fh = open(sourceTemplate, 'r')
    raw_sourceFile = fh.read()
    fh.close()
    
    fh = open(headerTemplate, 'r')
    raw_headerFile = fh.read()
    fh.close()

    #Required sections
    variableTypes = []
    variableNames = []
    actualTestData = []
    csvLine = []
    rawRowStringArray = []
    rawRowString = ''
    valueArray = []
    controlArray = []
    valueMaxArray = []
    accummulatedTime = 0
    numberTestCases = 0
    numberVariables = 0
    numberRangeRows = 0
    finalVarStructType = ''
    finalCtrlStructType = ''
    finalValueArray = ''
    finalControlArray = ''
    finalValueMaxArray = ''
    reqRefString = ''
    commentString = ''
    tempNumberVariables = 0
    
    #************* TEST CASE *******************
    #***************************** Variable Types and Names ******************************
    #search for the line with the variable types 
    sectionfound = 0
    for line in testCaseLineData:
        #print(line)
        if re.search('CR_Test,Types', line):
            sectionfound = 1
            line = line.replace('CR_Test,','',1) #only replace the first as the string "Types" may occur else where in row 
            line = line.replace('Types,','',1) #only replace the first as the string "Types" may occur else where in row 
            variableTypes = line.split(',')
            break
    if sectionfound is 0:
        print("Warning: No Variable Types found. \n")
    
    #search for the Variable names 
    sectionfound = 0
    for line in testCaseLineData:
        #print(line)
        if re.search('Update_time,Check_time', line):
            sectionfound = 1
            line = line.replace('Update_time,','',1) #only replace the first as the string "Types" may occur else where in row 
            line = line.replace('Check_time,','',1) #only replace the first as the string "Types" may occur else where in row 
            variableNames = line.split(',')
            #print(variableNames)
            count = 0
            #determine the number of variable 
            for string in variableNames:
                if re.search('Req_Ref', string):
                    numberVariables = count
                count = count + 1
            break
    if sectionfound is 0:
        print("Warning: No Variable Types found. \n")
        
    #remove the Reg_Ref and Comments from variable name list
    variableNames = variableNames[0:-2]
    
    #check variable types list it could have extra cell on the end
    #print(variableTypes)
    if len(variableTypes) > numberVariables:
        extraCells = len(variableTypes) - numberVariables
        for x in range(0,extraCells,1):
            variableTypes = variableTypes[0:-1]
    #print(variableTypes)
    
    #print(numberVariables)
    #combine the variable type and names with standard C code formatting 
    count = 0
    for count in range(0,numberVariables,1):
        finalVarStructType = finalVarStructType + '    ' + variableTypes[count] + ' ' + variableNames[count] + ';\n'
        
    #print(finalVarStructType)

    #***************************** Actual Test Data ******************************
    #search for the line with the actual test data 
    #remove the variable type and names row to leave the actual test case

    sectionfound = 0
    
    #Also create a raw row string of the test case
    #add c code array sytax
    rawRowString = "\n{ \n"
    
    for line in testCaseLineData:
        #print(line)
        if re.search('CR_Test,Types', line):
            pass
        elif re.search('Update_time,Check_time', line):
            pass
        else:
            sectionfound = 1
            #Check if the row has any text
            if re.search('[a-zA-Z0-9][a-zA-Z0-9_,]*', line):
                actualTestData.append(line)
                #Add the row to the raw row string with c code sytax, after removing the Reg_Ref
                rawRowString = rawRowString + "    \"" + line + "\",\n"
            else:                
                break
    if sectionfound is 0:
        print("Warning: No Test Data found. \n")
    
    #print(*actualTestData)
    
    #remove extra end ',' and return
    rawRowString = rawRowString[0:-2]
    rawRowString = rawRowString + line + '\n}'
    #print(rawRowString)
    
#**************************************************************************
    #TestData = ['10, 20,FxED, X,x,56  =,34<','40,50,BXB,70, x,78=,12>','40,50..1..60,BXB,70, x,78=,12>']
    #print(*TestData)
    #for string in TestData:
        #print(string)
    #print('\n')
    #finished, newTestData = csvBooleanExpand(TestData)
    #for string in newTestData:
        #print(string)
    #print('\n')
    #finished, newTestData = csvBooleanExpand(newTestData)
    #finished, newTestData = csvRangeExpand(newTestData)
    #for string in newTestData:
    #    print(string)
    #print('\n')
#*****************************************************************************
    
    #find for boolean expansion (Xx means don't care and with be replaced with 0,1)
    temp = actualTestData[0].split(',')
    count = 0
    for variable in temp:
        count = count + 1
    #print(count)
    for i in range(0,count,1):
        itRan, actualTestData = csvBooleanExpand(actualTestData)
        #print(*actualTestData)
        if itRan is 0:
            break
    for i in range(0,count,1):
        itRan, actualTestData = csvRangeExpand(actualTestData)
        #print(*actualTestData)
        if itRan is 0:
            break
    #print(*actualTestData)
    
    #generate the control and Value arrays
    lineCount = 0
    sectionfound = 0
    tempArray = []
    for line in actualTestData:
        csvLine = line.split(',')
        #check for the end of the test case
        if csvLine[0] is '':
            break
        #added formatting for the c structure
        valueArray.append("    ")
        controlArray.append("    ")
        valueMaxString = ''
        numberTestCases = numberTestCases + 1
        count = 0
        rangeFound = 0
        for value in csvLine:
            if (( numberVariables + 2 ) > count ):
                #first value in the row is the updateTime 
                #(time between the end of the previous row and the stimulus of this one)
                if count == 0:
                    accummulatedTime = accummulatedTime + int(value)
                    controlArray[lineCount] = controlArray[lineCount] + "{ " + str(accummulatedTime) + ", "
                    count = 1
                #second value in the row is the checkTime - NOT IMPLIMENTED
                #(time between the stimulus and the expected of this one)
                elif count == 1:
                    controlArray[lineCount] = controlArray[lineCount] + value
                    valueArray[lineCount] = valueArray[lineCount] + "{ "
                    count = 2
                else:
                    #replace the evaluation symbols with the control enumerations
                    #must be in this order
                    if re.search('[\s]*[0-9][0-9]*[\s]*\.\.[\s]*[0-9][0-9]*[\s]*!=', value):
                        controlArray[lineCount] = controlArray[lineCount] + ", TC_RANGE_NOT_EQU"
                        tempValue = value.replace('!=','')
                        tempArray = tempValue.split('..')
                        value = tempArray[0]
                        valueMax = tempArray[1]
                        rangeFound = 1
                    elif re.search('[\s]*[0-9][0-9]*[\s]*\.\.[\s]*[0-9][0-9]*[\s]*=', value):
                        controlArray[lineCount] = controlArray[lineCount] + ", TC_RANGE_EQUAL"
                        tempValue = value.replace('=','')
                        tempArray = tempValue.split('..')
                        #check which way the range goes.
                        if int(tempArray[0]) < int(tempArray[1]):
                            value    = tempArray[0]
                            valueMax = tempArray[1]
                        else:
                            valueMax = tempArray[0]
                            value    = tempArray[1]
                        rangeFound = 1
                    elif re.search('[\s]*[a-zA-Z0-9][a-zA-Z0-9_]*[\s]*\<=', value):
                        controlArray[lineCount] = controlArray[lineCount] + ", TC_GREATER_EQU"
                        value = value.replace('<=','')
                        valueMax = '0'
                    elif re.search('[\s]*[a-zA-Z0-9][a-zA-Z0-9_]*[\s]*\>=', value):
                        controlArray[lineCount] = controlArray[lineCount] + ", TC_LESS_EQU"
                        value = value.replace('>=','')
                        valueMax = '0'
                    elif re.search('[\s]*[a-zA-Z0-9][a-zA-Z0-9_]*[\s]*!=', value):
                        controlArray[lineCount] = controlArray[lineCount] + ", TC_NOT_EQU"
                        value = value.replace('!=','')
                        valueMax = '0'
                    elif re.search('[\s]*[a-zA-Z0-9][a-zA-Z0-9_]*[\s]*\>', value):
                        controlArray[lineCount] = controlArray[lineCount] + ", TC_LESS"
                        value = value.replace('>','')
                        valueMax = '0'
                    elif re.search('[\s]*[a-zA-Z0-9][a-zA-Z0-9_]*[\s]*\<', value):
                        controlArray[lineCount] = controlArray[lineCount] + ", TC_GREATER"
                        value = value.replace('<','')
                        valueMax = '0'
                    elif re.search('[\s]*[a-zA-Z0-9][a-zA-Z0-9_]*[\s]*=', value):
                        controlArray[lineCount] = controlArray[lineCount] + ", TC_EQUAL"
                        value = value.replace('=','')
                        valueMax = '0'
                    #check if value only and if yes it is stimulus only
                    elif re.search('[\s]*[a-zA-Z0-9][a-zA-Z0-9_]*[\s]*',value):
                        controlArray[lineCount] = controlArray[lineCount] + ", TC_STIMULUS"
                        valueMax = '0'
                    #check for a blank field, if blank make value zero and mark control to do nothing
                    elif re.search('',value) or re.search('[\s]*',value):
                        controlArray[lineCount] = controlArray[lineCount] + ", TC_NOTHING"
                        value = '0'
                        valueMax = '0'
                    else:
                        pass
                    #remove the evaluation sybols from value array
                    #must be in this order
                    valueArray[lineCount] = valueArray[lineCount] + value  + " ,"
                    #build up the max values row string even if it is not required
                    valueMaxString = valueMaxString + valueMax  + " ,"
                    count = count + 1
            elif (( numberVariables + 2 ) == count ):
                if value is not '':
                    reqRefString = reqRefString + value + ','
                count = count + 1
            elif (( numberVariables + 3 ) == count ):
                if value is not '':
                    commentString = commentString + value + ','
                count = count + 1
            else:
                pass
        
        #remove extra end ','
        valueArray[lineCount] = valueArray[lineCount][0:-1]

        #check if max value row string actually contained a range
        if rangeFound:
            #add row to Max array and remove extra end ','
            valueMaxArray.append("    { " + valueMaxString[0:-1] + " },")
            numberRangeRows = numberRangeRows + 1
        
        #first time through record the number of variables (not counting the 2 time columns)
        if sectionfound == 0:
            #numberVariables = count - 2
            sectionfound = 1
        #finish formatting the line
        controlArray[lineCount] = controlArray[lineCount] + " },"
        valueArray[lineCount] = valueArray[lineCount] + " },"
        lineCount = lineCount + 1

    #Remove the extra ',' on the last row of the c array
    controlArray[lineCount-1] = controlArray[lineCount-1][0:-1]
    valueArray[lineCount-1]   = valueArray[lineCount-1][0:-1]
    #check if there were any range evaluation found
    if numberRangeRows is not 0:
        #remove extra end ','
        valueMaxArray[numberRangeRows-1] = valueMaxArray[numberRangeRows-1][0:-1]
        
    #combine the right number of Control type and names with standard C code formatting 
    count = 0
    for count in range(0,numberVariables,1):
        finalCtrlStructType = finalCtrlStructType + '    TestCase_Control_en ' + variableNames[count] + '_Control;\n'
    #print(finalCtrlStructType)

    #combine the lines of the actual test data into one long string 
    count = 0
    for string in valueArray:
        finalValueArray = finalValueArray + string + '\n'
        count = count + 1
    #print(finalValueArray)

    #combine the lines of the control data into one long string 
    count = 0
    for string in controlArray:
        finalControlArray = finalControlArray + string + '\n'
        count = count + 1
    #print(finalControlArray)

    #combine the lines of the actual test data into one long string 
    count = 0
    for string in valueMaxArray:
        finalValueMaxArray = finalValueMaxArray + string + '\n'
        count = count + 1
    #print(finalValueMaxArray)

    reqRefString = reqRefString[0:-1]
    commentString = commentString[0:-1]
    #print(reqRefString)
    #print(commentString)
    
    #***************************** Write Test C file *******************

    # SOURCE FILE GENERATOR
    #search for the key words to replace with c code
    raw_sourceFile = raw_sourceFile.replace('##TestCase_HeaderFile##', testCaseFileOnlyNoExt + "_testcase.h")
    raw_sourceFile = raw_sourceFile.replace('##TestCase_NoTests##', str(numberTestCases))
    raw_sourceFile = raw_sourceFile.replace('##TestCase_NoVariables##', str(numberVariables))
    raw_sourceFile = raw_sourceFile.replace('##TestCase_NoRangeRows##', str(numberRangeRows))
    raw_sourceFile = raw_sourceFile.replace('##TestCase_Name##', testCaseFileOnlyNoExt)
    raw_sourceFile = raw_sourceFile.replace('##TestCase_RawRowString##', rawRowString)
    raw_sourceFile = raw_sourceFile.replace('##TestCase_ReqString##', reqRefString)
    raw_sourceFile = raw_sourceFile.replace('##TestCase_ValueType##', finalVarStructType)
    raw_sourceFile = raw_sourceFile.replace('##TestCase_ControlType##', finalCtrlStructType)
    raw_sourceFile = raw_sourceFile.replace('##TestCase_Values##', finalValueArray)
    raw_sourceFile = raw_sourceFile.replace('##TestCase_Control##', finalControlArray)
    raw_sourceFile = raw_sourceFile.replace('##TestCase_ValuesMax##', finalValueMaxArray)

    #Generating test functions which contain the actual test variables 
    # Stimulate function
    raw_sourceFile = crTemplate.varMLTemplateGen(raw_sourceFile, '##TestCase_StimulateFn##', '##VarName##', '##NL##', variableNames)
    # Expected function
    raw_sourceFile = crTemplate.varMLTemplateGen(raw_sourceFile, '##TestCase_ExpectedFn##', '##VarName##', '##NL##', variableNames)
    raw_sourceFile = crTemplate.varMLTemplateGen(raw_sourceFile, '##TestCase_ExpectedV1##', '##VarName##', '##NL##', variableNames)
    raw_sourceFile = crTemplate.varMLTemplateGen(raw_sourceFile, '##TestCase_ExpectedV2##', '##VarName##', '##NL##', variableNames)
    raw_sourceFile = crTemplate.varMLTemplateGen(raw_sourceFile, '##TestCase_ExpectedV3##', '##VarName##', '##NL##', variableNames)
    raw_sourceFile = crTemplate.varMLTemplateGen(raw_sourceFile, '##TestCase_ExpectedV4##', '##VarName##', '##NL##', variableNames)
    raw_sourceFile = crTemplate.varMLTemplateGen(raw_sourceFile, '##TestCase_ExpectedV5##', '##VarName##', '##NL##', variableNames)
    # Variable Check function
    raw_sourceFile = crTemplate.varAndTypeMLTemplateGen(raw_sourceFile, '##TestCase_VarCheckFn1##', '##VarName##', '##VarType##', '##NL##', variableNames, variableTypes)
    raw_sourceFile = crTemplate.varAndTypeMLTemplateGen(raw_sourceFile, '##TestCase_VarCheckFn2##', '##VarName##', '##VarType##', '##NL##', variableNames, variableTypes)

    # HEADER FILE GENERATOR
    #search for the key words to replace with c code
    raw_headerFile = raw_headerFile.replace('##TestCase_Name##', str.upper(testCaseFileOnlyNoExt))

    return raw_sourceFile, raw_headerFile, reqRefString

