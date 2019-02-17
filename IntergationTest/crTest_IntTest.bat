@echo OFF
rem cls

SET DRIVE=F

rem Setup Enviroment Variables
SET PYTHONPATH=..\..\..\python;..\..\..\python\bin
SET MINGWPATH=..\..\..\..\Program Files (x86)\mingw-w64\i686-8.1.0-posix-dwarf-rt_v6-rev0\mingw32\bin;..\..\..\..\Program Files (x86)\mingw-w64\i686-8.1.0-posix-dwarf-rt_v6-rev0\mingw32\i686-w64-mingw32\include
SET CRTEST=..\scripts;..\templates

SET PATH=%PATH%;%PYTHONPATH%;%MINGWPATH%;%CRTEST%;

rem CRTest Example modules (Part of Integration Test as well)
python ..\scripts\crTestMain.py -cfg crTestAndConfig.txt    

python ..\scripts\crTestMain.py -cfg crTestAndConfig2.txt

python ..\scripts\crTestMain.py -cfg crTestCorrectConfig.txt

rem CRTest Integration Test
python ..\scripts\crTestMain.py -cfg crTestIntTestConfig.txt

del *.gcno
del *.gcda

pause