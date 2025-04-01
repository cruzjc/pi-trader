@echo off
setlocal enabledelayedexpansion

REM Configuration
set REMOTE_DIR=/home/JeanclydeCruz/pi-trader

REM Copy files to Raspberry Pi
echo Copying files to Raspberry Pi...
scp -i .\RaspberryPi-Key requirements.txt JeanclydeCruz@raspberrypi:%REMOTE_DIR%/
scp -i .\RaspberryPi-Key src\*.py JeanclydeCruz@raspberrypi:%REMOTE_DIR%/src/
scp -i .\RaspberryPi-Key config\.env.example JeanclydeCruz@raspberrypi:%REMOTE_DIR%/config/

echo Files transferred successfully! 