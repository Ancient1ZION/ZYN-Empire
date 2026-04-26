# ZYN EMPIRE - INSTANT EXECUTION SCRIPT FOR WINDOWS
# Run this in PowerShell to instantly download and execute AGENTS.py
# NO file management required

Write-Host "============================================================"
Write-Host "ZYN EMPIRE - INSTANT STARTUP"
Write-Host "============================================================"
Write-Host ""
Write-Host "Downloading AGENTS.py from GitHub..."
Write-Host ""

# Download AGENTS.py
$url = "https://raw.githubusercontent.com/Ancient1ZION/ZYN-Empire/main/AGENTS.py"
$output = "AGENTS.py"

try {
    # Use .NET to download the file
        (New-Object Net.WebClient).DownloadFile($url, $output)
            Write-Host "Successfully downloaded AGENTS.py!"
                Write-Host ""
                    Write-Host "Downloading agents_config.json..."

                            # Download config
                                $configUrl = "https://raw.githubusercontent.com/Ancient1ZION/ZYN-Empire/main/agents_config.json"
                                    $configOutput = "agents_config.json"
                                        (New-Object Net.WebClient).DownloadFile($configUrl, $configOutput)
                                            Write-Host "Successfully downloaded agents_config.json!"
                                                Write-Host ""
                                                    Write-Host "============================================================"
                                                        Write-Host "STARTING ZYN EMPIRE AUTONOMOUS AGENTS ENGINE"
                                                            Write-Host "============================================================"
                                                                Write-Host ""

                                                                        # Execute AGENTS.py
                                                                            py AGENTS.py

                                                                                    Write-Host ""
                                                                                        Write-Host "============================================================"
                                                                                            Write-Host "System execution complete!"
                                                                                                Write-Host "============================================================"
                                                                                                }
                                                                                                catch {
                                                                                                    Write-Host "ERROR: Failed to download or execute AGENTS.py"
                                                                                                        Write-Host "Error details: $_"
                                                                                                            Write-Host ""
                                                                                                                Write-Host "Please ensure:"
                                                                                                                    Write-Host "1. You have an internet connection"
                                                                                                                        Write-Host "2. Python 3.14+ is installed"
                                                                                                                            Write-Host "3. You're running this script from your home directory"
                                                                                                                            }
