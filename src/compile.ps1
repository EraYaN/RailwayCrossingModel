# mCRL2 Compile script by EraYaN
# 2016-09-23
# v0.1
param (
    [string]$Project = "test",
    [string]$TraceAction = "",
    [switch]$ShowGraph = $false,
	[switch]$CleanupOnly = $false
)

$mCRL2RegData = Get-Item -Path Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\mCRL2
$mCRL2Path = Join-Path -Path $mCRL2RegData.GetValue('DisplayIcon') -ChildPath "bin"
Write-Host "mCRL2 installed in: " $mCRL2Path -ForegroundColor Yellow
$env:Path += ";$mCRL2Path"

Write-Host "Cleaning Up" -ForegroundColor Green
Remove-Item "${Project}.lps*"
Remove-Item "${Project}.lts"
if(!$CleanupOnly){
	Write-Host "Compiling LPS" -ForegroundColor Green
	cmd /C mcrl22lps.exe "${Project}.mcrl2" "${Project}.lps" --lin-method=regular --rewriter=jitty
	Write-Host "Compiling LTS" -ForegroundColor Green
	cmd /C lps2lts.exe "${Project}.lps" "${Project}.lts" --rewriter=jitty --strategy=breadth

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
