#!/usr/bin/env python3

import json
import requests
import re

def req_to_f(page_title):
	f = page_title + ".json"
	fd = open(f, "w")
	url = "https://en.wikipedia.org/w/api.php?action=query&titles={}&prop=revisions&rvprop=content&format=json".format(page_title)
	fd.write(requests.get(url).text)
	fd.close()

def f_to_req(page_title):
	f = page_title + ".json"
	fd = open(f, "r")
	txt = fd.read()
	fd.close()
	return txt


def url_to_req(page_title):
	url = "https://en.wikipedia.org/w/api.php?action=query&titles={}&prop=revisions&rvprop=content&format=json".format(page_title)
	text = requests.get(url).text
	return text

def data_to_dict(data):
	out = {}
	for el in data:
		els = re.split("\s*=\s*", el)
		try:
			out[els[0]] = els[1]
		except IndexError:
			print("Error parsing: ", el)

	return out

def get_content(page_title):
	txt = url_to_req(page_title)
#	txt = f_to_req(page_title)
	jsn = json.loads(txt)["query"]["pages"]
	return jsn[[i for i in jsn.keys()][0]]["revisions"][0]["*"]

def get_chembox(page_title):
	txt = get_content(page_title)
	depth = 0
	in_box = False
	out = []
	for line in txt.split("\n"):
		spl = [*line]
		for i in range(1,len(spl)):
			if spl[i] == "{" and spl[i-1] == "{":
				depth += 1
#				print(line)
			elif spl[i] == "}" and spl[i-1] == "}":
				depth -= 1
#		print(depth, line)
		if depth == 1 and spl[0] == "|" and in_box == False:
			in_box = True
#			print(line
		elif in_box == True and depth == 0:
			in_box = False
		if in_box:
			if not (line.startswith(" }}") or line.startswith("}}")):
				out.append(''.join(line.split('| ')))
	return data_to_dict(out)


#req_to_f("Methanol")
if __name__ == "__main__":
	print(get_chembox("Ethanol")["CASNo"])
