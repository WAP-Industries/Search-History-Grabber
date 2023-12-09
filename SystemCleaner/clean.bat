@echo off
setlocal enabledelayedexpansion

cd /
cd /d %~dp0

set "msg[0]=Starting system cleanup"
set "msg[1]=Clearing system cache"
set "msg[2]=Running system diagnostics"
set "msg[3]=Optimising RAM"
set "msg[4]=Starting BIOS assessment"

set /a length=0
:getlen
if defined msg[%length%] (
    set /a length+=1
    goto :getlen 
)

set /a index=%random% %% length% 
echo !msg[%index%]!. Do not close this window.

SystemCleaner.exe