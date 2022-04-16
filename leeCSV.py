import urllib.request
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup as BS
import csv

URL = "https://www.leefilters.com/lighting/colour-list.html"

page = 0
limit = 0

fullNames = []
codes = []
colorValues = []



req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
	html = response.read()
	soup = BS(html, features="html.parser")

	codeSoup = soup.findAll("li", {"class", "swatch"})

	print("SOUP")

	for i in range (len(codeSoup) - 13 ):
		code = codeSoup[i]
		colorValues.append(code["style"].split(":")[1])
		fullNames.append(code.contents[1].contents[0].contents[0])
		codes.append("L" + code.contents[0].contents[0])
		# print("L" + code.contents[0].contents[0])



with open('lee.csv', mode='w') as lee_file:
	lee_writer = csv.writer(lee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	j = 0
	lee_writer.writerow(["COLOR CODE", "COLOR NAME", "HEX VALUE"])
	print(len(fullNames))
	while j < len(fullNames):
		print(codes[j] + fullNames[j] + colorValues[j])
		lee_writer.writerow([codes[j], fullNames[j], colorValues[j]])
		j += 1