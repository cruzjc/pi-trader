@echo off
setlocal enabledelayedexpansion

REM Configuration
set PI_HOST=raspberrypi.local
set PI_USER=pi

REM Check if SSH is available
where ssh >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: SSH is not installed or not in PATH
    exit /b 1
)

REM Connect to Raspberry Pi
echo Connecting to Raspberry Pi...
ssh -i .\RaspberryPi-Key JeanclydeCruz@raspberrypi

REM Connect to Raspberry Pi
echo Connecting to Raspberry Pi...
ssh %PI_USER%@%PI_HOST% 