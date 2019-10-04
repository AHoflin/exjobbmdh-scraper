from bs4 import BeautifulSoup
import requests


# Running the scraper
site = requests.post('http://www.exjobbmdh.se/jobb_lista.asp', data={'omradesid': 2})
content = site.text
scraper = BeautifulSoup(content, 'html.parser')
t_body = scraper.find('table')
t_body = t_body.findAll('tr')

# Appending the results to list (titles)
titles = []
for index, tr in enumerate(t_body):
    if index != 0:
        titles.append(tr.find('a').text)

for title in titles:
    print(title)
