from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urlparse, parse_qs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# loading environment variables
load_dotenv()

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


# Writing list to temporary json-file
with open('data/temp_jobs.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json.dumps(jobs, indent=4, sort_keys=True, ensure_ascii=False))


old_data = json.load(open("data/jobs.json"))
new_data = json.load(open("data/temp_jobs.json"))

if old_data == new_data:
    print("No changes made...")
    exit(0)

with open('data/jobs.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json.dumps(jobs, indent=4, sort_keys=True, ensure_ascii=False))

# Send email
my_email = os.getenv("email")
my_password = os.getenv("password")
receiver_email = my_email  # EHM... Fix this maybe?

msg = MIMEMultipart('alternative')
msg['Subject'] = 'Test mail'
msg['From'] = my_email
msg['To'] = receiver_email

html = '<html><body><p>Hi,<br>http://www.exjobbmdh.se has been updated. Here are the current jobs available:</p><br>'

for job in jobs:
    html += "<a href=\"http://www.exjobbmdh.se/" + jobs[job]['link'] + "\">" + jobs[job]['title'] + "</a><br><br>"

html += '</body></html>'

message = MIMEText(html, 'html')
msg.attach(message)

s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login(my_email, my_password)
s.sendmail(my_email, receiver_email, msg.as_string())
s.quit()




