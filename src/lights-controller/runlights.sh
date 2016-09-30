rm -f lights-controller.lps
rm -f lights-controller.lts

mcrl22lps lights-controller.mcrl2 lights-controller.lps &&
lps2lts lights-controller.lps lights-controller.lts &&
ltsgraph lights-controller.lts