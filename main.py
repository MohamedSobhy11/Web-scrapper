import requests , os
from bs4 import BeautifulSoup
import pandas as pd


def linkextraction(soup):
    quote = []
    table = soup.find('div', attrs={'class': 'col-xs-12 col-md-5 col-lg-4'})
    for row in table.find_all(('li')):
        quote.append(row.a['href'])
    quote = list(set(quote))
    quote.remove('#heading')
    return quote

def tableextractor(soup):
    table1 = soup.find('table')
    headers = []
    for i in table1.find_all('th'):
        title = i.text
        headers.append(title)
    mydata = pd.DataFrame(columns=headers)
    for j in table1.find_all('tr')[1:]:
      row_data = j.find_all('td')
      row = [i.text for i in row_data]
      length = len(mydata)
      mydata.loc[length] = row
    return mydata



if __name__ == '__main__':
    URL = "https://oceanexplorer.noaa.gov/okeanos/animal_guide/animal_guide.html"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html5lib')
    mainDir = "data"
    os.makedirs(mainDir, exist_ok=True)
    for link in linkextraction(soup):
        imgLinks = []
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html5lib')
        cat = soup.find('h2').text.replace(' ', '_')
        dirs = mainDir + '/' + cat
        os.makedirs(dirs, exist_ok=True)
        table = soup.find('table')
        for row in table.find_all('td'):
            imgLinks.append(row.a['href'])

        for count, i in enumerate(imgLinks):
            #print(i)
            url = 'https://www.ncei.noaa.gov/waf/okeanos-animal-guide/images/' + i.removesuffix('.html') + '.jpg'
            url1 = 'https://www.ncei.noaa.gov/waf/okeanos-animal-guide/' + i
            r = requests.get(url)
            i = requests.get(url1)
            soup1 = BeautifulSoup(i.content, 'html5lib')

            with open(dirs+'/'+str(count+1)+'.jpg', 'wb') as f:
                f.write(r.content)
            table = tableextractor(soup1)
            with open('table.txt', 'w') as f:
                for line in table:
                    f.write(line)
                    f.write('\n')

