@echo OFF
rem cls

rem Setup Enviroment Variables
SET PYTHONPATH=..\..\python;..\..\python\bin
SET WINGWPATH=..\..\..\Program Files (x86)\mingw-w64\i686-8.1.0-posix-dwarf-rt_v6-rev0\mingw32\bin;..\..\..\Program Files (x86)\mingw-w64\i686-8.1.0-posix-dwarf-rt_v6-rev0\mingw32\i686-w64-mingw32\include
SET CRTEST=.\scripts;.\templates

SET PATH=%PATH%;%PYTHONPATH%;%WINGWPATH%;%CRTEST%;

rem CRTest Example modules
python .\scripts\crTestMain.py -cfg crTestAndConfig.txt    

del *.gcno
del *.gcda

pause