from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import *
import re

baseurl = "https://apps.sd.gov/applications/rv23mflookup/default.aspx"
f = open('sd_fuel_license.txt', 'wb')
headers = ("license_type|license_no|owner|address|phone|record_date|\n")
f.write(headers)

now = strftime("%Y-%m-%d")
fp = webdriver.FirefoxProfile()
browser = webdriver.Firefox(firefox_profile=fp)
browser.implicitly_wait(10)
browser.get(baseurl)

try:
    owner = browser.find_element_by_id("txtOwnerName")    
    owner.send_keys("%")
except:
    print "Couldn't find the text field."
    
browser.find_element_by_id("btnSearch").click()

html = browser.page_source
soup = BeautifulSoup(html)

results = soup.find('table', {'id': 'tblResults'})

page = results.findAll('td')[67].string.strip()
lastie = re.search(r'Page 1 of (\d+)', page)
lastpage = lastie.group().replace('Page 1 of ','')

counter = 1

def scrape(x):
    for obj in x.findAll('tr')[1:11]:
        col = obj.findAll('td')
        license_type = col[0].get_text(strip=True)
        license_no = col[1].get_text(strip=True)
        owner = col[2].get_text(strip=True)
        print owner
        address1 = col[3].get_text(strip=True)
        address2 = col[4].get_text(strip=True)
        address = address1 + " " + address2
        phone = col[5].get_text(strip=True)
        rec = (license_type, license_no, owner, address, phone, now, "\n")
        f.write("|".join(rec))

while counter <= int(lastpage):
    browser.find_element_by_id("tblResults")
    html = browser.page_source
    soup = BeautifulSoup(html)
    results = soup.find('table', {'id': 'tblResults'})
    scrape(results)
    browser.find_elements_by_xpath('//*[@id="tblResults"]/tbody/tr[12]/td/font[3]/b/a')[0].click()
    counter += 1
    sleep(4)

f.flush()
f.close()
