#!/usr/bin/env python

import re

def configSingleEntry (lineData, configSection):
    """ Searches for section and returns single entry lines after section heading """
    sectionContentsString = ""
    error='NONE'
    sectionfound = 0
    for line in lineData:
        #print(line)
        if sectionfound is 0:
            if re.match(configSection, line):
                sectionfound = 1
                #print(line + "\n")
        # section found get single line data
        else:
            sectionContentsString = line
            #print(line)
            break
    if sectionfound is 0:
        error = "Section " + configSection + " not found"
    return error, sectionContentsString 
    
def configMultiEntry (lineData, configSection):
    """ Search for section and return list of strings of the multiply entry lines after section heading """ 
    sectionContentsStringList = []
    error='NONE'
    sectionfound = 0
    for line in lineData:
        #print(line)
        if sectionfound is 0:
            if re.match(configSection, line):
                sectionfound = 1
                #print(line2 + "\n")
        # section found get data until empty line
        else:
            if line is '':
                break
            else:
                sectionContentsStringList.append(line)
                #print(line2)
    if sectionfound is 0:
        error = "Section " + configSection + " not found"
    return error, sectionContentsStringList
    


