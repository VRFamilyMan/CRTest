# CRTest

The CR Test is a python based module tester for use with C code. The test cases are in csv format and the contents is automatically generated in the c code arrays. The test case defines stimulus and evaluation critria.


## Getting Started

For instructions on how to use see the "CR Test user manual" under the \doc dorectory

### Prerequisites

This tool requires Python and your choice of C compiler. To access the test coverage features which use GCOV you will need to use MinGW as your C compiler. All all verification of this tool have been performed on Windows 7 and 10.

### Installing and Running example module test

Download CRTest, install python and MinGW (or your own choice of compiler) on your PC.

The only other thing required to run the example project is to update the tool paths in the crTestAnd.bat file.

```
@echo OFF
rem cls

rem Setup Enviroment Variables
SET PYTHONPATH=..\..\python;..\..\python\bin
SET MINGWPATH=..\..\..\Program Files (x86)\mingw-w64\i686-8.1.0-posix-dwarf-rt_v6-rev0\mingw32\bin;..\..\..\Program Files (x86)\mingw-w64\i686-8.1.0-posix-dwarf-rt_v6-rev0\mingw32\i686-w64-mingw32\include
SET CRTEST=.\scripts;.\templates

SET PATH=%PATH%;%PYTHONPATH%;%MINGWPATH%;%CRTEST%;

rem CRTest Example modules
python .\scripts\crTestMain.py -cfg crTestAndConfig.txt    

del *.gcno
del *.gcda

pause
```

Once the paths are correct, simply run the bat file and see the "And Module" test cases execute.

## Versions

v1.04

```
Initial working version
```

v1.05

```
Features of this release:
Fixed GCOV processing for multiple source locations
- CrTest configuration now requires all user source files to be specified
- CrTest no longer support auto source file searching
- Detection of user C file inclusion into the crtest_stubs.c is no longer case sensitive  
Fixed test case file processing bug where test variable type definitions which containing the word "Types" would crash.
```

## Authors

* **Chris Roberts** - *Initial work* - [VRFamilyMan](https://github.com/VRFamilyMan)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Peter Boin for his ideas and encouragement
