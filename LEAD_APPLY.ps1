Write-Host "================================================================================" -ForegroundColor Green
Write-Host "AUTOMATED LEAD ASSIGNMENT ENGINE" -ForegroundColor Green  
Write-Host "================================================================================" -ForegroundColor Green

$leads = @(
    @{id=1; company="DoD Division 7"; value=250000; stage="PROPOSAL"; industry="Government"}
        @{id=2; company="CBP Procurement"; value=180000; stage="NEW"; industry="Government"}
            @{id=3; company="Price Capital Group"; value=35000; stage="CONTACTED"; industry="Finance"}
                @{id=4; company="Johnson Roofing LLC"; value=6000; stage="NEW"; industry="Construction"}
                    @{id=5; company="Chen Tech Logistics"; value=25000; stage="PROPOSAL"; industry="Tech"}
                        @{id=6; company="Thompson Industries"; value=8000; stage="WON"; industry="Manufacturing"}
                            @{id=7; company="Walsh HVAC Solutions"; value=5000; stage="WON"; industry="Services"}
                                @{id=8; company="Rivera Medical Supplies"; value=9000; stage="CONTACTED"; industry="Healthcare"}
                                    @{id=9; company="Williams Auto Group"; value=8000; stage="NEW"; industry="Automotive"}
                                        @{id=10; company="Guzman Electrical"; value=12000; stage="CONTACTED"; industry="Construction"}
                                            @{id=11; company="Park & Associates"; value=15000; stage="NEW"; industry="Consulting"}
                                                @{id=12; company="Tech Admin SBR"; value=17000; stage="PROPOSAL"; industry="Tech"}
                                                )

                                                $assigned = @()
                                                $totalValue = 0
                                                $skipped = 0

                                                foreach ($lead in $leads) {
                                                    if ($lead.stage -eq 'WON') {
                                                            Write-Host "SKIP: $($lead.company) (already WON)"
                                                                    $skipped++
                                                                            continue
                                                                                }

                                                                                        if ($lead.value -ge 250000) {
                                                                                                $agent = "Noah"
                                                                                                    }
                                                                                                        elseif ($lead.industry -match 'government') {
                                                                                                                $agent = "Adam"
                                                                                                                    }
                                                                                                                        elseif ($lead.value -ge 50000) {
                                                                                                                                $agent = "Malik"
                                                                                                                                    }
                                                                                                                                        elseif ($lead.stage -eq 'CONTACTED') {
                                                                                                                                                $agent = "Sara"
                                                                                                                                                    }
                                                                                                                                                        elseif ($lead.stage -in 'PROPOSAL', 'NEGOTIATING') {
                                                                                                                                                                $agent = "Malik"
                                                                                                                                                                    }
                                                                                                                                                                        elseif ($lead.stage -eq 'NEW') {
                                                                                                                                                                                $agent = "Zara"
                                                                                                                                                                                    }
                                                                                                                                                                                        else {
                                                                                                                                                                                                $agent = "Samson"
                                                                                                                                                                                                    }
                                                                                                                                                                                                        
                                                                                                                                                                                                            $assigned += @{lead=$lead.company; agent=$agent; value=$lead.value}
                                                                                                                                                                                                                $totalValue += $lead.value
                                                                                                                                                                                                                    
                                                                                                                                                                                                                        Write-Host "ASSIGN: $($lead.id.ToString().PadLeft(2)) | $($lead.company.PadRight(30)) | `$$($lead.value.ToString().PadLeft(9)) -> $($agent.PadRight(15)) | $($lead.stage)"
                                                                                                                                                                                                                        }
                                                                                                                                                                                                                        
                                                                                                                                                                                                                        Write-Host ""
                                                                                                                                                                                                                        Write-Host "SUMMARY"
                                                                                                                                                                                                                        Write-Host "================================================================================" -ForegroundColor Green
                                                                                                                                                                                                                        Write-Host "Total Leads:       $($leads.Count)"
                                                                                                                                                                                                                        Write-Host "Assigned:          $($assigned.Count)"
                                                                                                                                                                                                                        Write-Host "Skipped (WON):     $skipped"
                                                                                                                                                                                                                        Write-Host "Total Value:       `$$totalValue"
                                                                                                                                                                                                                        
                                                                                                                                                                                                                        Write-Host ""
                                                                                                                                                                                                                        Write-Host "AGENT DISTRIBUTION:"
                                                                                                                                                                                                                        $agentCounts = @{}
                                                                                                                                                                                                                        foreach ($a in $assigned) {
                                                                                                                                                                                                                            if ($agentCounts.ContainsKey($a.agent)) {
                                                                                                                                                                                                                                    $agentCounts[$a.agent]++
                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                $agentCounts[$a.agent] = 1
                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                    foreach ($agent in ($agentCounts.Keys | Sort-Object)) {
                                                                                                                                                                                                                                                        Write-Host "  $($agent.PadRight(15)): $($agentCounts[$agent].ToString().PadLeft(2)) leads"
                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                        Write-Host "================================================================================" -ForegroundColor Green
                                                                                                                                                                                                                                                        Write-Host "COMPLETE: All leads automatically assigned!" -ForegroundColor Green
                                                                                                                                                                                                                                                        Write-Host "================================================================================" -ForegroundColor Green
