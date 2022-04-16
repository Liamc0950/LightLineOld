import urllib.request
from bs4 import BeautifulSoup as BS
import csv

URL = "https://us.rosco.com/en/products/catalog/roscolux?field_brand_target_id=41&field_type_target_id=All&sort_by=field_roscolux_sort_order_value&sort_order=ASC&items_per_page=20&search=&page="

page = 0
limit = 14

fullNames = []
codes = []
colorValues = []

def convert(lst):
	return ' '.join(lst) 


while(page <= limit):
	URLPAGE = URL + str(page)
	with urllib.request.urlopen(URLPAGE) as response:
		html = response.read()
		soup = BS(html, features="html.parser")

		colorNames = soup.findAll("div", {"class", "desc"})
		colors = soup.findAll("a", {"class", "info lightbox"})

		for name in colorNames:
			name = name.find("a").contents[0]
			splitName = str(name).split(" ")
			fullNames.append(convert(splitName[1:len(splitName)]))
			codes.append(splitName[0])

		for color in colors:
			#adds hex color value to list
			#first gets style attribute from the child tag of the <a> tag stored in color
			#then splits this, deliniated by space and selects second element, which is the hex
			#color.  Finally removed the last character, which is a semicolon
			colorValues.append((str(color.contents[1]["style"]).split(" ")[1])[:-1])



		page += 1

i = 0
while i < len(fullNames):
	print(codes[i], fullNames[i], colorValues[i])
	i += 1


with open('roscolux.csv', mode='w') as roscolux_file:
	roscolux_writer = csv.writer(roscolux_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	j = 0
	roscolux_writer.writerow(["COLOR CODE", "COLOR NAME", "HEX VALUE"])
	while j < len(fullNames):
		roscolux_writer.writerow([codes[j], fullNames[j], colorValues[j]])
		j += 1