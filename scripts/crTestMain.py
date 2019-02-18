#!/usr/bin/env python

import re
import os
#import os.path
import sys
import inspect
import argparse
import subprocess
import glob
import shutil
import time
import crTestGcovAccum
import configHandler
import crTestCaseGen

#************CR UNIT TEST VERSION STRING **********************

crTestVersion = '00.01.05'

#*********** CR UNIT TESTER SPECIAL FILES *********************
crTest_sourceTemplateFile = 'crtest_tp.c'
crTest_headerTemplateFile = 'crtest_tp.h'
crTest_mainFile       = 'main.c'
crTest_stubFile       = 'crtest_stubs.c'    
#This unit test file is included in the crTest_sourceTemplate file
crTest_CaseCFile       = 'common_crtest.c' 
crTest_CaseHFile       = 'common_crtest.h' 
crTest_GcovExe         = 'gcov -b -a ' 
#****************************************************************

startTime = time.time()

# Argument Parser
parser = argparse.ArgumentParser(description="TestCase Generator: Used to take user test case and update a template c file")

parser.add_argument(
    '--config', '-cfg', dest='configFile', type=str,
    help="Build Manager configuration (or instruction) file. If not defined then manager will use config.txt.",
)

args = parser.parse_args()

# Argument file handling
if args.configFile:
    try:
        fh = open(args.configFile, 'r')
    except OSError:
        print('\n')
        print('Could not open ' + args.configFile + ' configuration File')
        print('CRTest aborted')
        print('\n')
        sys.exit()
    else:
        raw_file_data = fh.read()
        fh.close()
        configLineData = raw_file_data.split('\n')
        #configLineData = ''
        ##remove comments
        #for line in tempconfigLineData:
        #    if re.search('^#',line):
        #        pass
        #    else:
        #        configLineData = configLineData + line
        ##configLineData = tempFile
else:
    try:
        fh = open('crTestConfig.txt', 'r')
    except OSError:
        print('\n')
        print('Could not open crTestConfig.txt the default configuration File')
        print('CRTest aborted')
        print('\n')
        sys.exit()
    else:
        raw_file_data = fh.read()
        fh.close()
        configLineData = raw_file_data.split('\n')


# ************** Configuration File Parser *******************************************
configError = []
temp = ''
separateCompileReq = 'NO'

#search for section (single entry lines after section heading) 
temp, projectName = configHandler.configSingleEntry (configLineData, 'ProjectName:')
configError.append(temp)

#search for section (single entry lines after section heading) 
temp, compilerExe = configHandler.configSingleEntry (configLineData, 'CompilerExe:')
configError.append(temp)

#search for section (single entry lines after section heading) 
temp, linkerExe = configHandler.configSingleEntry (configLineData, 'LinkerExe:')
#check if linker is blank, if yes ignore linker options and object output directory
if linkerExe is '':
    objectFileDir = ''
    pass
else:
    separateCompileReq = 'YES'
    #search for section (multiply entry lines after section heading) 
    temp, linkerOptionList = configHandler.configMultiEntry (configLineData, 'LinkerOptions:')
    configError.append(temp)
    #combine linker option list into a continuous string for execution
    linkerOptionStr = ""
    if temp is 'NONE':
        for entry in linkerOptionList:
            linkerOptionStr = linkerOptionStr + entry + ' '
    #print(linkerOptionStr)
    
    #search for section (single entry lines after section heading) 
    temp, objectFileDir = configHandler.configSingleEntry (configLineData, 'ObjectFileDir:')
    configError.append(temp)

#search for section (multiply entry lines after section heading) 
temp, compilerOptionList = configHandler.configMultiEntry (configLineData, 'CompilerOptions:')
configError.append(temp)
#combine compiler option list into a continuous string for execution
compilerOptionStr = ""
if temp is 'NONE':
    for entry in compilerOptionList:
        compilerOptionStr = compilerOptionStr + entry + ' '
#print(compilerOptionStr)

#search for section (single entry lines after section heading) 
temp, outputDir = configHandler.configSingleEntry (configLineData, 'OutputDir:')
configError.append(temp)

#search for section (multiply entry lines after section heading) 
temp, sourceDirAndFileList = configHandler.configMultiEntry (configLineData, 'SourceFiles:')
configError.append(temp)

#search for section (single entry lines after section heading) 
temp, sourceFileDir = configHandler.configSingleEntry (configLineData, 'SourceFileDir:')
configError.append(temp)

#search for section (multiply entry lines after section heading) 
temp, includeDirList = configHandler.configMultiEntry (configLineData, 'IncludeDirectories:')
configError.append(temp)
includeDirStr = ""
if temp is 'NONE':
    for entry in includeDirList:
        includeDirStr = includeDirStr + entry + ' '

#search for section (single entry lines after section heading) 
temp, gcovEnabled = configHandler.configSingleEntry (configLineData, 'GcovEnabled:')
configError.append(temp)

#skip the other GCOV config parameters if not enabled
if re.search('(yes|YES|Yes)', gcovEnabled):
    #search for section (multiply entry lines after section heading) 
    temp, gcovSourceFileList = configHandler.configMultiEntry (configLineData, 'GcovFiles:')
    configError.append(temp)
    gcovSourceFileControl = []
    for file in gcovSourceFileList:
        gcovSourceFileControl.append('FILE_EXISTS')
    #print(gcovSourceFileList)

    #search for section (single entry lines after section heading) 
    temp, gcovOutputDir = configHandler.configSingleEntry (configLineData, 'GcovOutputDir:')
    configError.append(temp)
    #print(gcovOutputDir)

#search for section (single entry lines after section heading) 
temp, testCaseDir = configHandler.configSingleEntry (configLineData, 'TestCaseDir:')
configError.append(temp)

#search for section (single entry lines after section heading) 
temp, resultsDir = configHandler.configSingleEntry (configLineData, 'ResultsDir:')
configError.append(temp)

#search for section (single entry lines after section heading) 
temp, templateDir = configHandler.configSingleEntry (configLineData, 'TemplateDir:')
configError.append(temp)
#includeDirStr = ""
#Check if template directory specified and if yes update default location string
if templateDir is not '':
    crTest_sourceTplAndDir = templateDir + '\\' + crTest_sourceTemplateFile
    crTest_headerTplAndDir = templateDir + '\\' + crTest_headerTemplateFile
    crTest_mainFileAndDir  = templateDir + '\\' + crTest_mainFile

#check for config file errors
errorCount = 0
for line in configError:
    if line is 'NONE':
        pass
    else:
        print(line)
        errorCount = errorCount + 1
if (errorCount > 0):
    print('Invalid Configuration File')
    print('CRTest Aborted')
    sys.exit()
# *************************************************************************************
# **************** Test Cases*************************
# Find all the test cases
# and make lists with and without extentions
testCaseDirAndFileList = glob.glob(testCaseDir + '\*.csv')
testCaseFileOnlyWithExtList = []
testCaseFileOnlyNoExtList = []
temp = []
fileOnly = []
count = 0
for file in testCaseDirAndFileList:
    temp = file.split('\\')
    testCaseFileOnlyWithExtList.append(temp[-1]) 
    fileOnly = temp[-1].split('.')
    testCaseFileOnlyNoExtList.append(fileOnly[0])
    count = count + 1
# **********************************************************
testCaseResults = ''
testCase_Log = ''
tempString = ''
# Start constructing Results Output with housekeep information

tempString = '*************************************\n'
testCaseResults = testCaseResults + tempString

tempString = 'CR Test Version: ' + crTestVersion + '\n'
testCaseResults = testCaseResults + tempString

tempString = '*************************************\n'
testCaseResults = testCaseResults + tempString

os.system('gcc --version > capture.txt')
fh = open('capture.txt', 'r')
tempString = fh.read()
fh.close()
testCaseResults = testCaseResults + 'Compiler Version:\n' + tempString

#skip the GCOV version if not enabled
if re.search('(yes|YES|Yes)', gcovEnabled):
    os.system('gcov --version > capture.txt')
    fh = open('capture.txt', 'r')
    tempString = fh.read()
    fh.close()
    testCaseResults = testCaseResults + 'Gcov Version:\n' + tempString

testCase_Log = testCaseResults

#Screen display, test results and log file are the same up until this point
print(testCaseResults)
testCaseResults = testCaseResults + 'TEST RESULTS FOR ' + projectName + '\n\n'

# Start The actual Testing
print(projectName + " test in progress, please wait.....\n")

# Source File Handling
sourceString = ''

# Files must be included in the sourcefiles config
# Will exclude any of the files if they are included in the crtest_stubs.c file
if sourceDirAndFileList:

    sourceFileOnlyList = []
    sourceFileControl = []
    dirFilesplit = []
    temp = []

    #remove the directory struct and initialise the control block for each source file
    for file in sourceDirAndFileList:
        sourceFileControl.append('REQUIRED')
        dirFilesplit = file.split('\\')
        #file = file.replace(sourceFileDir + '\\','')
        temp.append(dirFilesplit[-1])
    sourceFileOnlyList = temp

    # open the provided cr test stubs file
    try:
        fh = open(sourceFileDir + '\\' + crTest_stubFile, 'r')
    except OSError:
        print('\n')
        print('Could not open ' + crTest_stubFile + ' File')
        print('CRTest aborted')
        print('\n')
        sys.exit()
    else:
        rawStubsData = fh.read()
        fh.close()
        stubsLineData = rawStubsData.split('\n')


    #search the stubs file to see in c files have been directly included
    #if yes these files don't need to be built
    #print(*sourceFileOnlyList)
    srcFileCount = 0
    for file in sourceFileOnlyList:
        #check each line in the stubs c file for included c files
        for line in stubsLineData:
            tempLine = line.lower()
            tempFile = file.lower()
            if re.search(tempFile, tempLine):
                sourceFileControl[srcFileCount] = 'NOT_REQUIRED'
                if re.search('(yes|YES|Yes)', gcovEnabled):
                    # Updating gcov control, example
                    count = 0
                    for gcovfile in gcovSourceFileList:
                        if gcovfile.lower() == file.lower():
                            # mark gcov control as file "NOT EXIST" as it is included in test Case
                            gcovSourceFileControl[count] = 'NOT_EXIST'
                        count = count + 1
        srcFileCount = srcFileCount + 1
    
    #Stubs file NOT added to source list as it is always included in generated test case file
    #Add the crtest generated c file to the directory and file list
    sourceDirAndFileList.append(sourceFileDir + '\\' + crTest_CaseCFile)
    sourceFileOnlyList.append(crTest_CaseCFile)
    sourceFileControl.append('REQUIRED')
    srcFileCount = srcFileCount + 1
        
    srcFileCtrlCount = 0
    for sourceFile in sourceDirAndFileList:
        if sourceFileControl[srcFileCtrlCount] == "REQUIRED":
            sourceString = sourceString + sourceFile + ' '
            #sourceDirAndFileList.append(sourceFile)
        srcFileCtrlCount = srcFileCtrlCount + 1
    
else:
    print('\n')
    print('No Source files found')
    print('CRTest aborted')
    print('\n')
    sys.exit()



#print(sourceFileOnlyList)
#print(sourceFileControl)
#print(gcovSourceFileList)
#print(gcovSourceFileControl)

#print(sourceString)

# Gcov File handling
gcovOutputFile = []
gcovMasterLineData = []

# Clear out the output temp files
os.system('del ' + outputDir + '\\*.c > junk.txt' )
os.system('del ' + outputDir + '\\*.txt > junk.txt' )
os.system('del ' + outputDir + '\\*.exe > junk.txt' )
#skip the GCOV file clear if not enabled
if re.search('(yes|YES|Yes)', gcovEnabled):
    os.system('del ' + gcovOutputDir + '\\*.gcov > junk.txt' )

# run through each test case
testcount = 0
gcovFileIndex = 0
raw_sourceFile = ''
requirementsString = ''

for testCaseFile in testCaseDirAndFileList:
    #generate the test case c files
    raw_sourceFile = ''
    raw_headerFile = ''
    requirementsString = ''
    raw_sourceFile, raw_headerFile, requirementsString = crTestCaseGen.testCaseCodeGen(crTest_sourceTplAndDir, crTest_headerTplAndDir, testCaseDirAndFileList[testcount], testCaseFileOnlyNoExtList[testcount])

    #********************** C CODE FILE HANDLING *************************
    #write the new testcase file in the format testcase_crtest.c
    fh = open(outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_crtest.c', 'w')
    fh.write(raw_sourceFile)
    fh.close
    
    #write the new testcase file in the format common_crtest.c and common_crtest.h
    fh = open(sourceFileDir + '\\' + crTest_CaseCFile, 'w')
    fh.write(raw_sourceFile)
    fh.close
    
    fh = open(sourceFileDir + '\\' + crTest_CaseHFile, 'w')
    fh.write(raw_headerFile)
    fh.close
    
    #********************** LOG FILE HANDLING *************************
    #Write a log file for each test case with the general info (versions) at the top
    fh = open(outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_log.txt', 'w')
    fh.write(testCase_Log + 'Test Case File: ' + testCaseFileOnlyWithExtList[testcount] + '\n\n')
    fh.close()
    #***************************************************************************
    logTemp = ''
    #compile test code and module under test
    if separateCompileReq is 'NO':
        #Run compiler and linker all-in-one goes. No object files are generated
        cmd = (compilerExe + ' ' + crTest_mainFileAndDir + ' ' + sourceString + ' ' + compilerOptionStr +' ' + includeDirStr + ' -o ' + outputDir + '\\' + testCaseFileOnlyNoExtList[testcount] + '_main.exe')
        #print(cmd)
        logTemp = logTemp + cmd + '\n'
        os.system(cmd)
    else:
        objectFileStr = ''
        #temp = crTest_mainFile.split('\\')
        objFile = crTest_mainFile.replace('.c','.o')
        #combine source file list into a continuous string for linker execution
        objectFileStr = objectFileStr  + objectFileDir +'\\' + objFile + ' '
        cmd = (compilerExe + ' -c ' + compilerOptionStr + ' ' + crTest_mainFileAndDir + ' ' + includeDirStr + ' -o ' + objectFileDir + '\\' + objFile )
        #print(cmd)
        logTemp = logTemp + cmd + '\n'
        os.system(cmd)
        #loop through the list of source file and compile
        for sourceFile in sourceDirAndFileList:
            temp = sourceFile.split('\\')
            objFile = temp[-1].replace('.c','.o')
            #combine source file list into a continuous string for linker execution
            objectFileStr = objectFileStr  + objectFileDir +'\\' + objFile + ' '
            cmd = (compilerExe + ' -c ' + compilerOptionStr + ' ' + sourceFile + ' ' + includeDirStr + ' -o ' + objectFileDir +'\\' + objFile )
            #print(cmd)
            logTemp = logTemp + cmd + '\n'
            os.system(cmd)
            
        cmd = (compilerExe + ' ' + objectFileStr + ' ' + linkerOptionStr + ' ' + includeDirStr + ' -o ' + outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_main.exe ')
        #print(cmd)
        logTemp = logTemp + cmd + '\n'
        os.system(cmd)
    
    if os.path.isfile(outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_main.exe'):
        pass
    else:
        cmd = '\nCompilation Error, ' + testCaseFileOnlyNoExtList[testcount] + '_main.exe could not be found\nCRTest aborted\n\n'
        print(cmd)
        logTemp = logTemp + cmd 
        #update log file with the compiler/linker commands and the reason for the error
        fh = open(outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_log.txt', 'a')
        fh.write(logTemp + '\n')
        fh.close
        sys.exit()
    
    #update log file with the compiler/linker commands
    #fh = open(outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_log.txt', 'a')
    #fh.write(logTemp + '\n')
    #fh.close
    
    #execute test exe file 
    os.system(outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_main.exe >> ' + outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_log.txt' )
    
    #open log file which contains the output of the test case exe file.
    fh = open(outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_log.txt', 'r')
    tempString = fh.read()
    fh.close
    tempLineData = tempString.split('\n')
    #search through the Test case log for the results line
    for line in tempLineData:
        if re.search('Test Complete:',line):
            print('Test Case File: ' + testCaseFileOnlyWithExtList[testcount] + '\n' + line)
            testCaseResults = testCaseResults + 'Test Case File: ' + testCaseFileOnlyWithExtList[testcount] + '\n' + line + '\n'
            #if requirementsString is not '':
            #    testCaseResults = testCaseResults + 'Requirements covered by this Test Case:\n' + requirementsString + '\n'
            break
    
    #skip the GCOV data file processing if not enabled
    if re.search('(yes|YES|Yes)', gcovEnabled):
        #add a new list of output files for each test case (gcovOutputFile[testcount][gcovFileIndex])
        gcovOutputFile.append([])
        gcovFileIndex = 0
        #print(gcovSourceFileList)
        count = 0
        for file in gcovSourceFileList: 
            #generate gcov output files
            #collect all the gcov generated file connected with the 
            #current c file
            tempFile = file.replace('.c','')
            commonTestFile = crTest_CaseCFile.replace('.c','')
            #print(tempFile)
            if objectFileDir is '':
                #if no obj directory specificed then the files will be in current directory
                #check if gcov data file exists
                if os.path.isfile(tempFile + '.gcda'):
                    fileList = glob.glob(tempFile + '.gcda')
                    gcovSearchDir = ''
                #check for c file which are included in test case file 
                elif (gcovSourceFileControl[count] == 'NOT_EXIST'):
                    fileList = ''
                    gcovSearchDir = ''
                    pass
                else:
                    #gcov files missing disable gcov
                    print('\nMissing GCOV Files, GCOV Aborted\n')
                    testCaseResults = testCaseResults + '\nMissing GCOV Files, GCOV Aborted\n'
                    #open log file which contains the output of the test case exe file.
                    fh = open(outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_log.txt', 'a')
                    fh.write('\nMissing GCOV Files, GCOV Aborted\n')
                    fh.close
                    gcovEnabled = 'NO'
                    #print('All In One')

            else:
                #gcov file will have been created in the object directory
                #check if gcov data file exists
                if os.path.isfile(objectFileDir + '\\' + tempFile + '.gcda'):
                    fileList = glob.glob(objectFileDir + '\\' + tempFile + '.gcda')
                    gcovSearchDir = ' -o' + objectFileDir
                #check for c file which are included in test case file 
                elif (gcovSourceFileControl[count] == 'NOT_EXIST'):
                    fileList = ''
                    gcovSearchDir = ' -o' + objectFileDir
                    pass
                else:
                    #gcov files missing disable gcov
                    print('\nMissing GCOV Files, GCOV Aborted\n')
                    testCaseResults = testCaseResults + '\nMissing GCOV Files, GCOV Aborted\n'
                    gcovEnabled = 'NO'
                    #print('Separate Compile')
            #print(*fileList)
            
            #check if gcov config has been forced to disable above due to missing files
            if re.search('(yes|YES|Yes)', gcovEnabled):
                #check if any gcov data files exist
                if fileList:
                    #files exist so run gcov for c file
                    os.system(crTest_GcovExe + ' ' + file + gcovSearchDir + ' >> ' + outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_log.txt')
                else:
                    #files DON"T exist so must be included in test stubs file
                    os.system(crTest_GcovExe + ' ' + crTest_CaseCFile + gcovSearchDir + ' >> ' + outputDir +'\\' + testCaseFileOnlyNoExtList[testcount] + '_log.txt')
                
                #rename the gcov files with the test case as a prefix and move
                gcovOutputFile[testcount].append(testCaseFileOnlyNoExtList[testcount] + '_' + gcovSourceFileList[gcovFileIndex] + '.gcov')
                #print(gcovOutputFile[testcount][gcovFileIndex])
                #Rename, move and delete the gcov output files
                os.system('rename ' + gcovSourceFileList[gcovFileIndex] + '.gcov  ' + gcovOutputFile[testcount][gcovFileIndex] )
                os.system('move ' + gcovOutputFile[testcount][gcovFileIndex] + '  ' + gcovOutputDir + ' > junk.txt')
            gcovFileIndex = gcovFileIndex + 1
    
    # delete the generated test case c file
    testcount = testcount + 1

#skip the GCOV accumulation processing if not enabled
if re.search('(yes|YES|Yes)', gcovEnabled):
    # Process all gcov output files to produce a accumulated master file
    # open the first test case gcov output file
    gcovMasterString = []
    tempString = '\nAccumulated Gcov Output:\n\n'
    for srcFileIndex in range(gcovFileIndex):
        for testIndex in range(testcount):
            fh = open(gcovOutputDir + '\\' + gcovOutputFile[testIndex][srcFileIndex], 'r')
            rawFileData = fh.read()
            fh.close()
            tempGcovLineData = rawFileData.split('\n')
            if testIndex is 0:
                #this is the first file so no data to accumulate
                gcovMasterLineData = tempGcovLineData
            else:
                # merge the new file and the previous accumulated files
                gcovMasterLineData = crTestGcovAccum.gcovMasterMerge(tempGcovLineData, gcovMasterLineData)
        
        # Output the master file test summary
        tempString = tempString + 'Source File: ' + gcovSourceFileList[srcFileIndex] + '\n'
        tempString = tempString + crTestGcovAccum.gcovOutputGen(gcovMasterLineData) + '\n'
        # Create Gcov master file string ready for storing as a file in the format master_<sourcefilename>.c.gcov
        gcovMasterString = ''
        for line in gcovMasterLineData:
                gcovMasterString = gcovMasterString + line + '\n'

        gcovMasterFileName = gcovOutputDir + '\\master_' + gcovSourceFileList[srcFileIndex] + '.gcov'
        #write the new master gcov output file
        fh = open(gcovMasterFileName, 'w')
        fh.write(gcovMasterString)
        fh.close

    #******************** CLEARUP THE TEMP FILES ******************************************
    if objectFileDir is '':
        #if no obj directory specificed then the gcov data files will be in current directory
        os.system('del *.gcda')
        os.system('del *.gcno')
    else:
        #gcov data file will have been created in the object directory
        FileList = glob.glob(objectFileDir + '\\' + tempFile + '.gcda')
        gcovSearchDir = ' -o' + objectFileDir
        os.system('del ' + objectFileDir + '\\*.gcda')
        os.system('del ' + objectFileDir + '\\*.gcno')
    os.system('del *.gcov')
else:
    #clear tempString
    tempString = '\n'
    
os.system('del junk.txt')
os.system('del capture.txt')
#os.system('del .\\src\\common_crtest.c')

#******************* END OF TEST HOUSE KEEPING ***************************************
stopTime = time.time()
totalTime = stopTime - startTime

tempString = tempString + 'Total Test duration ' + str(int(totalTime)) + 'sec.\n'
print(tempString)

testCaseResults = testCaseResults + tempString
fh = open(resultsDir + '\\' + projectName + '_TestResult.txt', 'w')
fh.write(testCaseResults)
fh.close


