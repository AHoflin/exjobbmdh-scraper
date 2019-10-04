from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urlparse, parse_qs


# Running the scraper
site = requests.post('http://www.exjobbmdh.se/jobb_lista.asp', data={'omradesid': 2})
content = site.text
scraper = BeautifulSoup(content, 'html.parser')
t_body = scraper.find('table')
t_body = t_body.findAll('tr')

# Appending the results to list (titles)
jobs = {}
for index, tr in enumerate(t_body):
    if index != 0:
        title = tr.find('a').text
        link = tr.find('a')['href']
        url = urlparse(link)
        job_id = parse_qs(url.query)['jobbid']
        jobs[job_id[0]] = {'title': title, 'link': link}

# Writing list to json-file
with open('data/jobs.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json.dumps(jobs, indent=4, sort_keys=True, ensure_ascii=False))


