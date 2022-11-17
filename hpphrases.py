#!/usr/bin/env python3

def get_sentences(f):
	fd = open(f, "r")
	src = fd.readlines()
	fd.close()
	out = {}
	for l in src:
		spl = l.split('\t')
	#	k = "".join("".join(spl[0].split("H")).split("P"))
		out[spl[0]] = spl[1]
	return out	

def parse_h(inp):
	src = get_sentences("hphrases.tsv")
	out = "\n"
	for el in inp.split("|"):
		if el in src.keys():
			out += src[el]
		else:
			out += el + " NOT FOUND\n"
	return out
	

def parse_p(inp):
	psrc = get_sentences("pphrases.tsv")
	rsrc = get_sentences("rphrases.tsv")
	p = "\n"
	r = "\n"
	for el in inp.split("|"):
		if el in psrc.keys():
#			print(el)
			p += psrc[el]
		elif el in rsrc.keys():
			r += rsrc[el]
		else:
			p += el + " NOT FOUND\n"
	return (p,r)

if __name__ == "__main__":
	print(parse_p("210|280|305+351+338"))
