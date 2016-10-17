#!/bin/bash 
 
Project="full-system" 
ToolArguments="" 
 
rm -f ${Project}.lps 
rm -f ${Project}.lts 
rm -f ${Project}.pbes 
rm -f ${Project}_trace_*.pbes 
 
mcrl22lps "${Project}.mcrl2" "${Project}.lps" --lin-method=regular --rewriter=jitty && 
lps2lts "${Project}.lps" "${Project}.lts" --rewriter=jitty --strategy=breadth && 
 
lps2pbes "${Project}.lps" "${Project}.pbes" --formula="${Project}.mcf" --out=pbes $ToolArguments 
pbes2bool "${Project}.pbes" --erase=none --rewriter=jitty --search=breadth-first --strategy=0 $ToolArguments 
 
ltsgraph ${Project}.lts