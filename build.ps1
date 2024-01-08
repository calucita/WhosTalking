# Powershell script to keep the pyinstaller created files and making the release versions
param([int]$ver=0)

$dir = Get-Location
$plainRun = Join-Path $dir "dist\Run.exe"

$dirRun = Join-Path $dir "dist\Run_*.exe"
$dirWho = Join-Path $dir "dist\Who*.exe"

$latest = Get-ChildItem -Path $dirRun | Sort-Object LastWriteTime -Descending | Select-Object -First 1
# Write-Host $latest.Name

$last_Rmiv = $latest.Name.Split(".")[-2]
$last_Rmiv = [int]$last_Rmiv + 1
$last_Rmav = $latest.Name.Split(".")[-3]

# Handle case where we're on the 1st minor version of the development
$latestW = Get-ChildItem -Path $dirWho | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$mainversion = $latestW.Name.Split(".")[-2]

if ([int]$mainversion -gt [int]$last_Rmav)
{
    $last_Rmav = $mainversion
    $last_Rmiv = "1"
}

if (Test-Path $plainRun)
{
    $bk_run = -join($latest.Name.Split(".")[0],".",$last_Rmav,".", $last_Rmiv,".exe")

    Rename-Item -Path $plainRun -NewName $bk_run
}

pyinstaller.exe Run.spec --upx-dir "..\..\..\Downloads\upx-4.0.2-win64\upx-4.0.2-win64"

if ($ver -eq 0)
{
    Exit
}

if ($ver -le [int]$last_Rmav)
{
    throw "Version specified older than the latest local version"
    Exit
}

if (Test-Path $plainRun)
{
    $bk_run = -join($latestW.Name.Split(".")[0],".",$ver,".exe")
    
    Rename-Item -Path $plainRun -NewName $bk_run
}
