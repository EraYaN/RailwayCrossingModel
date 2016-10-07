# mCRL2 Compile script by EraYaN
# 2016-09-23
# v0.1
param (
    [string]$Project = "test",
    [string]$TraceAction = "",
    [switch]$ShowGraph = $false,
	[switch]$CleanupOnly = $false,
	[switch]$Verbose = $false
)

$mCRL2RegData = Get-Item -Path Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\mCRL2
$mCRL2Path = Join-Path -Path $mCRL2RegData.GetValue('DisplayIcon') -ChildPath "bin"
Write-Host "mCRL2 installed in: " $mCRL2Path -ForegroundColor Yellow
$env:Path += ";$mCRL2Path"

$ToolArguments = "";

if($Verbose){
$ToolArguments += "--verbose";
}

Write-Host "Cleaning Up" -ForegroundColor Green
Remove-Item "${Project}*.lps*"
if ( Test-Path "${Project}.lts" ){
	Remove-Item "${Project}.lts"
}
if ( Test-Path "${Project}.pbes" ){
	Remove-Item "${Project}.pbes"
}
Remove-Item "${Project}_trace_*.lts"
if(!$CleanupOnly){
	if(Test-Path "${Project}.mcrl2"){
		Write-Host "Compiling to LPS" -ForegroundColor Green
		cmd /C mcrl22lps.exe "${Project}.mcrl2" "${Project}.lps" --lin-method=regular --rewriter=jitty $ToolArguments
	} else {
		Write-Host "Did not compile to LPS, ${Project}.mcrl2 not found." -ForegroundColor Yellow
	}
	if(Test-Path "${Project}.lps"){
		Write-Host "Compiling to LTS" -ForegroundColor Green
		cmd /C lps2lts.exe "${Project}.lps" "${Project}.lts" --rewriter=jitty --strategy=breadth $ToolArguments
	} else {
		Write-Host "Did not compile to LTS, ${Project}.lps not found." -ForegroundColor Yellow
	}
	if((Test-Path "${Project}.mcf") -And (Test-Path "${Project}.lps")){
		Write-Host "Compiling to PBES" -ForegroundColor Green
		cmd /C lps2pbes.exe "${Project}.lps" "${Project}.pbes" --formula="${Project}.mcf" --out=pbes $ToolArguments
	} else {
		Write-Host "Did not compile to PBES, ${Project}.mcf or ${Project}.lps not found." -ForegroundColor Yellow
	}
	if(Test-Path "${Project}.pbes"){
		Write-Host "Processing PBES" -ForegroundColor Green
		cmd /C pbes2bool.exe "${Project}.pbes" --erase=none --rewriter=jitty --search=breadth-first --strategy=0 $ToolArguments
	} else {
		Write-Host "Did not process PBES, ${Project}.pbes not found." -ForegroundColor Yellow
	}

	if($TraceAction){
		Write-Host "Generating Traces" -ForegroundColor Green
		cmd /C lps2lts.exe  "${Project}.lps" "${Project}_trace_${TraceAction}.lts" --action=$TraceAction --rewriter=jitty --strategy=breadth --trace
		$traces = Get-ChildItem "${Project}.lps*.trc"
		ForEach ($trace In $traces) {
			cmd /C tracepp "$trace" "${trace}.txt" --format=plain
		}
		$traces_results = Get-ChildItem "${Project}.lps*.trc.txt"
		$i = 0;
		ForEach ($trace_result In $traces_results) {
			Write-Host "Trace ${i}:"
			Get-Content "$trace_result"
			$i++;
		}
	}
	Write-Host "Generation Done." -ForegroundColor Green
	if($ShowGraph){
		Write-Host "Launching LTSGraph" -ForegroundColor Green
		cmd /C START ltsgraph.exe "${Project}.lts"
	}
}
Write-Host "Done." -ForegroundColor Green
