#!/usr/bin/env python

#*****************************************************************************
def gcovOutputGen(gcovFileLineData):   
    """Returns the string of the results of .gcov text file"""
    import re
    
    functionData = []
    callData = []
    branchData = []
    outputString = ''
    
    for line in gcovFileLineData:
        if re.search('function', line):
            functionData.append(line)
            #print(line)
        elif re.search('call', line):
            callData.append(line)
            #print(line)
        elif re.search('branch', line):
            branchData.append(line)    
            #print(line)
    
    #functions called
    total = 0
    noneZero = 0
    temp = []
    for line in functionData:
        total = total + 1
        temp = line.split(' ')
        #print(temp[3])
        if int(temp[3]) is not 0:
            noneZero = noneZero + 1
    if total is not 0:
        percent = (noneZero / total ) * 100
        outputString = outputString + 'Functions called:    %3.2f' % (round(percent,2)) + '% of ' + str(total) + '\n'
    
    #branches taken and taken at least once 
    count = 0
    total = 0
    noneZero = 0
    temp = []
    for line in branchData:
        total = total + 1
        if re.search('never executed', line):
            count = count + 1
        else:
            temp = line.split(' ')
            temp[4] = temp[4].replace('%','')
            #print(temp[4])
            if int(temp[4]) is not 0:
                noneZero = noneZero + 1
    if total is not 0:
        percent = ((total - count)/total) * 100
        outputString = outputString + 'Branches executed:   %3.2f' % (round(percent,2)) + '% of ' + str(total) + '\n'
        percent = (noneZero / total ) * 100
        outputString = outputString + 'Taken at least once: %3.2f' % (round(percent,2)) + '% of ' + str(total) + '\n'

    #calls taken
    count = 0
    total = 0
    for line in callData:
        total = total + 1
        if re.search('never executed', line):
            count = count + 1
    
    if total is not 0:
        percent = ((total - count)/total) * 100
        outputString = outputString + 'Calls executed:      %3.2f' % (round(percent,2)) + '% of ' + str(total) + '\n'
    return outputString

#******************************************************************************
def gcovMasterMerge(gcovFileLineData, gcovMasterFileLineData):   
    """Returns the string of the new master merged file"""
    import re
    
    newMaster = []
    
    count = 0
    tempGcovLine = []
    tempMasterGcovLine = []
    for line in gcovFileLineData: 
        if re.search('branch', line) and re.search('branch', gcovMasterFileLineData[count]):
            tempGcovLine = line.split(' ')
            tempGcovLine[4] = tempGcovLine[4].replace('%','')
            tempMasterGcovLine = gcovMasterFileLineData[count].split(' ')
            tempMasterGcovLine[4] = tempMasterGcovLine[4].replace('%','')
            #print(tempGcovLine[4] + "  " + tempMasterGcovLine[4])
            if tempGcovLine[4].isdigit():
                if tempMasterGcovLine[4].isdigit():
                    if int(tempGcovLine[4]) < int(tempMasterGcovLine[4]):
                        newMaster.append(gcovMasterFileLineData[count])
                        #print(gcovMasterFileLineData[count])
                    else:
                        newMaster.append(line)
                        #print(line)
                else:
                    newMaster.append(line)
                    #print(line)
            else:
                if tempMasterGcovLine[4].isdigit():
                    newMaster.append(gcovMasterFileLineData[count])
                    #print(gcovMasterFileLineData[count])
                else:
                    newMaster.append(gcovMasterFileLineData[count])
        else:
            newMaster.append(gcovMasterFileLineData[count])
        count = count + 1
    return newMaster

if __name__ == '__main__':
    import argparse
    import re
    
    # Parser command-line parameters
    parser = argparse.ArgumentParser(description="Gcov Accumulation: Used to accumulate GCOV result")

    parser.add_argument(
        '--gcovData', '-gd', dest='newGcovData', default='', type=str,
        help="Name of the template c file",
    )
    parser.add_argument(
        '--masterGcov', '-mgd', dest='masterGcovDataFile', default='', type=str,
        help="Name of the user test case file",
    )

    args = parser.parse_args()

    if args.newGcovData:
        fh = open(args.newGcovData, 'r')
        raw_gcov_data = fh.read()
        fh.close()
        gcovDataLineData =raw_gcov_data.split('\n')
    else:
        print("Error no gcov data file specified")

    if args.masterGcovDataFile:
        fh = open(args.masterGcovDataFile, 'r')
        raw_gcov_data = fh.read()
        fh.close()
        masterGcovDataLineData =raw_gcov_data.split('\n')
    else:
        print("Error no gcov data file specified")
    
    print('File \'.\\gcov\\1_vmon.c.gcov\'')
    print(gcovOutputGen(gcovDataLineData))

    print('File \'.\\gcov\\3_vmon.c.gcov\'')
    print(gcovOutputGen(masterGcovDataLineData))

    newMasterLines = gcovMasterMerge(gcovDataLineData,masterGcovDataLineData)
    print(gcovOutputGen(newMasterLines))

    newMasterString = ''
    for line in newMasterLines:
        newMasterString = newMasterString + line + '\n'

    #print(newMasterString)
