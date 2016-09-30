# mCRL2 Compile script by EraYaN
# 2016-09-23
# v0.1
param (
    [string]$project = "test",
    [string]$trace_action = "",
    [switch]$show_graph = $false
)

$mCRL2RegData = Get-Item -Path Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\mCRL2
$mCRL2Path = Join-Path -Path $mCRL2RegData.GetValue('DisplayIcon') -ChildPath "bin"
Write-Host "mCRL2 installed in: " $mCRL2Path -ForegroundColor Yellow
$env:Path += ";$mCRL2Path"

Write-Host "Cleaning Up" -ForegroundColor Green
Remove-Item "${project}.lps*"
Remove-Item "${project}.lts"
Write-Host "Compiling" -ForegroundColor Green
cmd /C mcrl22lps.exe "${project}.mcrl2" "${project}.lps" --lin-method=regular --rewriter=jitty
cmd /C lps2lts.exe "${project}.lps" "${project}.lts" --rewriter=jitty --strategy=breadth

if($trace_action){
	Write-Host "Generating Traces" -ForegroundColor Green
	cmd /C lps2lts.exe  "${project}.lps" "${project}_trace_${trace_action}.lts" --action=$trace_action --rewriter=jitty --strategy=breadth --trace
	$traces = Get-ChildItem "${project}.lps*.trc"
	ForEach ($trace In $traces) {
		cmd /C tracepp "$trace" "${trace}.txt" --format=plain
	}
	$traces_results = Get-ChildItem "${project}.lps*.trc.txt"
	$i = 0;
	ForEach ($trace_result In $traces_results) {
		Write-Host "Trace ${i}:"
		Get-Content "$trace_result"
		$i++;
	}
}

if($show_graph){
	Write-Host "Launching LTSGraph" -ForegroundColor Green
	cmd /C START ltsgraph.exe "${project}.lts"
}
