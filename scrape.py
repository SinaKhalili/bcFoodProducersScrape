import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import os
from selenium import webdriver

wd = webdriver.Chrome()

filename = "stores.csv"
f = open(filename, "w")

headers = "shop_name, email, owner_name, telephone, link\n"

f.write(headers)

print("Compiling list of all store links...")
num = 0 #The way this website works is by incrementing a counter in the url
links = []
for i in range(11): #There are 11 pages of store lists
#This is how you open connections and grab pages
    print("On page "+str(i+1) + "of 11")
    url_pg1 = 'https://www.contactcanada.com/database/companies.php?portal=7&s=' + str(num) + '&l=90'
    uClient = uReq(url_pg1)
    page = uClient.read()
    uClient.close() #remember to close connections
    page_soup = soup(page, "html.parser")
    listOfLinks = page_soup.findAll("li",{"class":["rowOdd","rowEven"]})
    for item in listOfLinks:
        link = 'https://www.contactcanada.com/database/' + item.a['href']
        links.append(link)
        print("added " + link)
    num += 90
cont = input('Press enter to continue...')

#Now I have a list of all the links!
#Ok now to open the links and get the data I want
print("Ok I have the list. There are " + str(len(links)) + " stores")
print("Now going into each store page and saving info...")

for link in links:
    uClient = uReq(link)
    page = uClient.read()
    uClient.close()
    page_soup = soup(page, "html.parser")
    info_container = page_soup.findAll("div",{"class":"profileWrapper"})
    shop_name = info_container[0].h2.text
    ownerPart = page_soup.findAll("ul", {"class":"profileSectionWrapper"})
    owner_name = ownerPart[1].li.text
    telephone = info_container[0].ul.li.text
    #address
    wd.get(link)
    #For whatever reason, the email field is loaded dynamically
    #So I'm using Selenium to fetch them
    email = ""
    mailerElement = wd.find_elements_by_class_name("linkEmail")
    for el in mailerElement:
        email = el.text
    f.write(shop_name + "," + owner_name + "," + telephone + "," + email + "," + link + "\n")

f.close()
wd.close()

print("Done. CSV file can be found as " + filename)
