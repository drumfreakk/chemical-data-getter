#!/usr/bin/env python3

from chembox import get_chembox
from hpphrases import parse_h, parse_p
from sys import argv
import re

def print_nicely(data):
#	print(data)
	out = ""
	for k,i in data.items():
		out += re.sub("\n\n", "\n", k + ": " + i + "\n")
	print(out)

box_full = get_chembox("Ethanol" if len(argv) == 1 else argv[1])

data = {}
needed = {"CAS Number":["CASNo"], "Molar Mass":["MolarMass"], "Density":["Density"], "Boiling Point": ["BoilingPt","BoilingPtC"], "Melting Point" : ["MeltingPt","MeltingPtC"], "Flash Point":["FlashPtC", "FlashPt"], "Hazards":["HPhrases"], "P&R":["PPhrases"]}

for k,i in needed.items():
	done = False
	for el in i: 
		try:
			data[k] = re.split("(\|?}*(<\D*)?)$", re.split("^[^\d−]*", box_full[el])[-1])[0]
			done = True
		except KeyError:
			pass
	if done:
		if k == "Boiling Point" or k == "Melting Point" or k == "Flash Point":
			data[k] += " °C"
		elif k == "Hazards":
			data[k] = parse_h(data[k])
		elif k == "P&R":
			pr = parse_p(data[k])
			data["Prevention"] = pr[0]
			data["Response"] = pr[1]
			del data["P&R"]
	else:
		data[k] = "N/A"
	
print_nicely(data)
