#!/usr/bin/env python

import re

def varMLTemplateGen(fileData, varTag, varNameTag, returnTag, variableList):   
    """Returns the file Data with the Multi line Variable templates populated and repeated for each variable name"""
    fileLineData = fileData.split('\n')
    temp = ''
    variableString = ''
    variableTempory = ''
    variableTemplate = ''
    sectionfound = 0
    count = 0
    for line in fileLineData:
        #Find the line with the var template
        if re.search(varTag, line):
            #remove the searchable key word
            line = line.replace(varTag, '')
            #store the fn template
            variableTemplate = variableTemplate + line + '\n'
            #restore the line with the key word only
            if count is 0:
                temp = temp + varTag + '\n'
                count = 1
            sectionfound = 1
        else:
            #store the lines
            temp = temp + line + '\n'
    if sectionfound is 0:
        print("Warning: Variable template not found \n")
    #restore the file but with the var template removed but the key word left
    fileData = temp

    #Create a string containing as many fn's as there are variables
    for name in variableList:
        variableTempory = variableTemplate.replace(varNameTag, name )
        variableString = variableString + variableTempory.replace(returnTag, '\n' )

    fileData = fileData.replace(varTag, variableString)
    return fileData
#*******************************************************************************************************
def varAndTypeMLTemplateGen(fileData, varTag, varNameTag, varTypeTag, returnTag, variableList, typeList):   
    """Returns the file Data with the Multi line Variable templates populated (variable names and types) and repeated for each variable name"""
    fileLineData = fileData.split('\n')
    temp = ''
    variableString = ''
    variableTempory = ''
    variableTemplate = ''
    sectionfound = 0
    count = 0
    for line in fileLineData:
        #Find the line with the var template
        if re.search(varTag, line):
            #remove the searchable key word
            line = line.replace(varTag, '')
            #store the fn template
            variableTemplate = variableTemplate + line + '\n'
            #restore the line with the key word only
            if count is 0:
                temp = temp + varTag + '\n'
                count = 1
            sectionfound = 1
        else:
            #store the lines
            temp = temp + line + '\n'
    if sectionfound is 0:
        print("Warning: Variable and Type template not found \n")
    #restore the file but with the var template removed but the key word left
    fileData = temp

    #Create a string containing as many fn's as there are variables
    count = 0
    for name in variableList:
        variableTempory = variableTemplate.replace(varNameTag, name )
        variableTempory = variableTempory.replace(varTypeTag, typeList[count] )
        count = count + 1
        variableString = variableString + variableTempory.replace(returnTag, '\n' )

    fileData = fileData.replace(varTag, variableString)
    return fileData
#***************************************************************************************

