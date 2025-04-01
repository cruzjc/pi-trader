@echo off
setlocal enabledelayedexpansion

REM Configuration
set REMOTE_DIR=/home/JeanclydeCruz/pi-trader
set LOCAL_DIR=%~dp0

REM Create remote directory structure
echo Creating remote directory structure...
ssh -i .\RaspberryPi-Key JeanclydeCruz@raspberrypi "mkdir -p %REMOTE_DIR%/src %REMOTE_DIR%/config %REMOTE_DIR%/logs"

REM Copy files to Raspberry Pi
echo Copying files to Raspberry Pi...
scp -i .\RaspberryPi-Key "%LOCAL_DIR%requirements.txt" JeanclydeCruz@raspberrypi:%REMOTE_DIR%/
scp -i .\RaspberryPi-Key "%LOCAL_DIR%src\*.py" JeanclydeCruz@raspberrypi:%REMOTE_DIR%/src/
scp -i .\RaspberryPi-Key "%LOCAL_DIR%config\.env.example" JeanclydeCruz@raspberrypi:%REMOTE_DIR%/config/

REM Setup Python environment and install dependencies
echo Setting up Python environment...
ssh -i .\RaspberryPi-Key JeanclydeCruz@raspberrypi "cd %REMOTE_DIR% && python3 -m venv env && source env/bin/activate && pip install -r requirements.txt"

REM Create systemd service for auto-start
echo Creating systemd service...
ssh -i .\RaspberryPi-Key JeanclydeCruz@raspberrypi "echo '[Unit]
Description=Pi Trader Automated Trading System
After=network.target

[Service]
Type=simple
User=JeanclydeCruz
WorkingDirectory=%REMOTE_DIR%
Environment=PATH=%REMOTE_DIR%/env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=%REMOTE_DIR%/env/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target' | sudo tee /etc/systemd/system/pi-trader.service"

REM Reload systemd and enable service
echo Configuring service...
ssh -i .\RaspberryPi-Key JeanclydeCruz@raspberrypi "sudo systemctl daemon-reload && sudo systemctl enable pi-trader.service"

echo.
echo Deployment completed! To start the trading system:
echo 1. SSH into your Raspberry Pi using: ssh_pi.bat
echo 2. Configure your API keys: nano %REMOTE_DIR%/config/.env
echo 3. Start the service: sudo systemctl start pi-trader
echo.
echo To view logs:
echo - Trading logs: tail -f %REMOTE_DIR%/logs/trading.log
echo - Error logs: tail -f %REMOTE_DIR%/logs/error.log
echo - Service logs: sudo journalctl -u pi-trader -f 