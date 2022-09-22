@echo off
python transpiler.py %1 %~n1.c
gcc %~n1.c -o %~n1.exe
%~n1.exe