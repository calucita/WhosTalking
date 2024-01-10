# Powershell script to keep the pyinstaller created files and making the release versions
param([int]$ver=0)

function renameDevRun {
    param (
        [string]$path,
        [string]$mainname,
        [string]$version,
        [string]$devversion
    )
    if (Test-Path $path)
    {
        $bk_run = -join($mainname,".",$version,".", $devversion,".exe")
        Rename-Item -Path $path -NewName $bk_run
    }
}

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
    renameDevRun -path $plainRun -mainname $latest.Name.Split(".")[0] -version $last_Rmav -devversion $last_Rmiv
    $last_Rmiv = [int]$last_Rmiv + 1
}

pyinstaller.exe Run.spec --upx-dir "..\..\..\Downloads\upx-4.0.2-win64\upx-4.0.2-win64"

if ($ver -eq 0)
{
    renameDevRun -path $plainRun -mainname $latest.Name.Split(".")[0] -version $last_Rmav -devversion $last_Rmiv
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
