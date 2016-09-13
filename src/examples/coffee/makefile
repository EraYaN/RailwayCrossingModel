
FILES = \
	coffee.mcrl2


all: $(FILES)

coffee: coffee.graph

%.lps: %.mcrl2
	mcrl22lps $< $@

%.lts: %.lps
	lps2lts $< $@

%.graph: %.lts
	ltsgraph $<