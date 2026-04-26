@echo off
REM ZYN EMPIRE AUTOMATIC SETUP FOR WINDOWS
REM This script downloads AGENTS.py and runs it automatically
REM NO MANUAL FILE MOVEMENT REQUIRED

echo ============================================================
echo ZYN EMPIRE - AUTOMATIC SETUP
echo ============================================================
echo.
echo This script will:
echo 1. Download AGENTS.py from GitHub
echo 2. Download agents_config.json
echo 3. Run the autonomous agents engine
echo.
echo ============================================================
echo.

REM Create a temp folder for downloads
if not exist "temp" mkdir temp
cd temp

echo Downloading AGENTS.py from GitHub...
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/Ancient1ZION/ZYN-Empire/main/AGENTS.py', 'AGENTS.py')"

if exist AGENTS.py (
    echo Successfully downloaded AGENTS.py!
        echo.
            echo Downloading agents_config.json...
                powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/Ancient1ZION/ZYN-Empire/main/agents_config.json', 'agents_config.json')"
                    echo.
                        echo ============================================================
                            echo STARTING ZYN EMPIRE AUTONOMOUS AGENTS ENGINE
                                echo ============================================================
                                    echo.

                                            REM Run the Python script
                                                py AGENTS.py

                                                        echo.
                                                            echo ============================================================
                                                                echo System execution complete!
                                                                    echo ============================================================
                                                                        pause
                                                                        ) else (
                                                                            echo ERROR: Failed to download AGENTS.py
                                                                                echo Please check your internet connection and try again.
                                                                                    echo.
                                                                                        echo Alternative: Visit https://github.com/Ancient1ZION/ZYN-Empire
                                                                                            pause
                                                                                            )

                                                                                            cd ..
                                                                                            exit /b 0
