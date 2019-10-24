import json
import re
from builtins import hasattr

from sendEmail import sendEmail
import urllib3
from bs4 import BeautifulSoup

# open file
f = open("links.json", "r")
contents = f.read()
parsedContent = json.loads(contents)



def scrape(page, courseCode):
    soup = BeautifulSoup(page.data, 'html.parser')
    regex = re.compile(".*{}.*".format(courseCode))
    rows = soup.find_all("tr");
    for row in rows:
        anchorTag = row.find("a", {"name": regex})
        if ((anchorTag) != None) :
            # twice because has white text
            sibling = row.next_sibling.next_sibling
            if ("Open" in str(sibling)):
                print("{} is Open".format(courseCode))
                sendEmail(courseCode)
                break

for link in parsedContent:
    http = urllib3.PoolManager()
    page = http.request("GET", link['link'])
    print("Scraping for {}".format(link['courseCode']))
    scrape(page, link['courseCode'])
