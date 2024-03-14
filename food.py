#importing dateTime for file creating and storing informations into a file
import time
import datetime 
import sys
import os

#impporting selenium for webscraping 
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


#the website sometimes has data images so sometimes you can't just check the src
#retruns the src 
def getImageSrc(image_element):
    check_src = str(image_element.get_attribute('src'))
    if(check_src == 'None'):
        return str(image_element.get_attribute('data-src'))
    else:
        return check_src

#all national articles have the same structure
#need to pass in the xpath as a string 
#need to pass data file for writing
def pageScrape(xpath, datafile, driver):
    articles = driver.find_element(By.XPATH, xpath).find_elements(By.TAG_NAME, 'article')
    imgs_Of_Article = driver.find_element(By.XPATH, xpath).find_elements(By.CLASS_NAME, 'img-responsive')

    
    for i in range(len(articles)):
        datafile.write(articles[i].text)
        datafile.write("\nImage: " + getImageSrc(imgs_Of_Article[i]) + "\n\n")


options = Options()
options.add_argument('--headless=new')
 
# initialize an instance of the chrome driver (browser)
driver = webdriver.Chrome(
      options=options, 
    # other properties...
)

# visit your target site
site = 'https://kathmandupost.com/food'
driver.get(site)

date_hour = time.strftime("%Y") + '-' + time.strftime("%m")+ '-' + time.strftime('%d')+ '-' +time.strftime('%H')
directoryName = "./" + date_hour + "_dir/"
dataFileLocation = directoryName + "food.txt"

datafile = open(dataFileLocation, 'w', encoding='utf-8') #creates the file 

ul_xpath = '/html/body/div[3]/main/div/ul'

valley_title = driver.find_element(By.XPATH, ul_xpath).find_elements(By.TAG_NAME, 'li')
valley_sites = driver.find_element(By.XPATH, ul_xpath).find_elements(By.TAG_NAME, 'a')

datafile.write("Food\n\n")

siteTitles = []
sites_links = []

for title in valley_title:
    siteTitles.append(title.text)

#print(siteTitles)

for site in valley_sites:
    sites_links.append(site.get_attribute('href'))

#print(sites_links)

artilces_xpath = '/html/body/div[3]/main/div/div[2]/div[1]/div/div'

pageScrape(artilces_xpath, datafile, driver)

for i in range(len(sites_links)):
    datafile.write(siteTitles[i] + "\n\n")
    driver.get(sites_links[i])
    pageScrape(artilces_xpath, datafile, driver)
