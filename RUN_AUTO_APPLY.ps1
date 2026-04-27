# RUN_AUTO_APPLY.ps1 - Execute automatic lead assignment
# Downloads and runs AUTO_APPLY_ASSIGNMENTS.py from GitHub

$pythonUrl = "https://raw.githubusercontent.com/Ancient1ZION/ZYN-Empire/main/AUTO_APPLY_ASSIGNMENTS.py"
$tempFile = "$env:TEMP\AUTO_APPLY_ASSIGNMENTS.py"

Write-Host "Downloading AUTO_APPLY_ASSIGNMENTS.py..." -ForegroundColor Green

try {
    # Download the Python file
        Invoke-WebRequest -Uri $pythonUrl -OutFile $tempFile -ErrorAction Stop
            Write-Host "Download successful. Running auto-assignment engine..." -ForegroundColor Green

                    # Execute Python script
                        python $tempFile

                                # Clean up
                                    Remove-Item $tempFile -Force
                                        Write-Host "Complete!" -ForegroundColor Green
                                        }
                                        catch {
                                            Write-Host "Error: $_" -ForegroundColor Red
                                                exit 1
                                                }
