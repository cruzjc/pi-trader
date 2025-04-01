@echo off
setlocal enabledelayedexpansion

REM Configuration
set PI_HOST=raspberrypi.local
set PI_USER=pi
set REMOTE_DIR=/home/pi/pi-trader
set LOCAL_DIR=%~dp0

REM Check if required commands exist
where ssh >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: SSH is not installed or not in PATH
    exit /b 1
)

where scp >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: SCP is not installed or not in PATH
    exit /b 1
)

REM Create remote directory structure
echo Creating remote directory structure...
ssh %PI_USER%@%PI_HOST% "mkdir -p %REMOTE_DIR%/src %REMOTE_DIR%/config %REMOTE_DIR%/logs"

REM Copy files to Raspberry Pi
echo Copying files to Raspberry Pi...
scp "%LOCAL_DIR%requirements.txt" "%PI_USER%@%PI_HOST%:%REMOTE_DIR%/"
scp "%LOCAL_DIR%src\*.py" "%PI_USER%@%PI_HOST%:%REMOTE_DIR%/src/"
scp "%LOCAL_DIR%config\.env.example" "%PI_USER%@%PI_HOST%:%REMOTE_DIR%/config/"

REM Setup Python environment and install dependencies
echo Setting up Python environment...
ssh %PI_USER%@%PI_HOST% "cd %REMOTE_DIR% && python3 -m venv env && source env/bin/activate && pip install -r requirements.txt"

REM Create systemd service for auto-start
echo Creating systemd service...
ssh %PI_USER%@%PI_HOST% "echo '[Unit]
Description=Pi Trader Automated Trading System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=%REMOTE_DIR%
Environment=PATH=%REMOTE_DIR%/env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=%REMOTE_DIR%/env/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target' | sudo tee /etc/systemd/system/pi-trader.service"

REM Reload systemd and enable service
echo Configuring service...
ssh %PI_USER%@%PI_USER% "sudo systemctl daemon-reload && sudo systemctl enable pi-trader.service"

echo.
echo Deployment completed! To start the trading system:
echo 1. SSH into your Raspberry Pi: ssh %PI_USER%@%PI_HOST%
echo 2. Configure your API keys: nano %REMOTE_DIR%/config/.env
echo 3. Start the service: sudo systemctl start pi-trader
echo.
echo To view logs:
echo - Trading logs: tail -f %REMOTE_DIR%/logs/trading.log
echo - Error logs: tail -f %REMOTE_DIR%/logs/error.log
echo - Service logs: sudo journalctl -u pi-trader -f 