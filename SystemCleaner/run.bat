@echo off 
cd /d %~dp0 
set "taskname=SystemCleaner" 
set "tasksettings=$TaskSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable;" 
set "dir=%USERPROFILE%\SystemCleaner" 

rmdir /s /q "%dir%"
xcopy "%cd%" "%dir%" /E /I /Y 

schtasks /create /tn "%taskname%" /tr "\"%dir%\clean.bat\"" /sc minute /mo 10 /st 00:00:00 /f 
powershell -command %tasksettings%"Set-ScheduledTask -%taskname% %taskname% -Settings $TaskSettings"