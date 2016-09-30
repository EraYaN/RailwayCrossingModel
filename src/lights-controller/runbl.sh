rm -f lights-bell.lps
rm -f lights-bell.lts

mcrl22lps lights-bell.mcrl2 lights-bell.lps &&
lps2lts lights-bell.lps lights-bell.lts &&
ltsgraph lights-bell.lts
