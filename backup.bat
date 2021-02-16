@echo off

echo %date%

echo Current time is %date%-%time%
echo "%~dp0"

set prename1=%date%-%time%
set prename2=%prename1::=%
set name=%prename2:.=%

echo %name%

if exist "%~dp0\World Backups" GOTO COPY

md "%~dp0\World Backups"

:COPY
md "%~dp0\World Backups\%name%"
Xcopy "%~dp0\world" "%~dp0\World Backups\%name%" /E /H /C /I
