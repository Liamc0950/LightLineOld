import urllib.request
from bs4 import BeautifulSoup as BS
import csv, os
import shutil
URL = "https://us.rosco.com/en/products/catalog/gobos?field_type_target_id=All&sort_order=ASC&items_per_page=24&search=&page="

IMAGE_ULR = "https://us.rosco.com/"

page = 0
limit = 141

goboNames = []
goboCodes = []
imageFileNames = []
imageURLs = []


while(page <= limit):
    URLPAGE = URL + str(page)
    with urllib.request.urlopen(URLPAGE) as response:
        html = response.read()
        soup = BS(html, features="html.parser")

        goboProductsSoup = soup.find("div", {"class", "product-holder"})
        goboNamesSoup = soup.findAll("span", {"class", "text-box"})
        goboCodesSoup = soup.findAll("span", {"class", "name"})
        goboImagesSoup = goboProductsSoup.findAll("img")

        # for product in goboProductsSoup:
        #     goboImagesSoup.append(product.find("img"))
    
        for goboCode in goboCodesSoup:
            rawCode = goboCode.find("a").text
            if list(rawCode)[0] !="G" and list(rawCode)[0] != "P":
                code = "R" + rawCode
            else:
                code = rawCode
            
            goboCodes.append(code)
            imageFileNames.append(code + ".jpg")

        for goboName in goboNamesSoup:
            name = goboName.contents[0]
            name.replace('\n', '')
            name.replace('"', '')
            print(name)
            goboNames.append(name)

        for goboImage in goboImagesSoup:
            url = IMAGE_ULR + goboImage.attrs['src']
            imageURLs.append(url)




        #Increment the page number, to move to the next page of results on the Rosco website
        print("PAGE: " + str(page))
        page += 1




# for i in range(len(imageURLs)):
#     full_url = imageURLs[i]
#     urllib.request.urlretrieve(imageURLs[i], "images/" + imageFileNames[i])
#     print("IMAGE " + str(imageFileNames[i]) + " SAVED " + str(i) + "/" + str(len(imageURLs)))



with open('roscoGobos.csv', mode='w') as roscoGobos_file:
	roscoGobos_writer = csv.writer(roscoGobos_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	j = 0
	roscoGobos_writer.writerow(["GOBO CODE", "GOBO NAME", "IMAGE FILENAME"])
	while j < len(goboNames):
		roscoGobos_writer.writerow([goboCodes[j], goboNames[j], imageFileNames[j]])
		j += 1
