#special files to get the other stuff on the website thats not as important


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

def createFile(directoryName, fileName):
    location = directoryName + fileName

    return open(location, 'w', encoding='utf-8')





options = Options()
options.add_argument('--headless=new')
 
# initialize an instance of the chrome driver (browser)
driver = webdriver.Chrome(
      options=options, 
    # other properties...
)

# visit your target site

sites = [
    'https://kathmandupost.com/travel', 
    'https://kathmandupost.com/investigations', 
    'https://kathmandupost.com/climate-environment',  
    'https://kathmandupost.com/world',
    'https://kathmandupost.com/science-technology'
]

fileNames = [
    'travel.txt',
    'investigation.txt',
    'climate-environment.txt',
    'world.txt',
    'science-technology.txt'
]
#'travel.txt' -> TRAVEL
names = [sub[: -4].upper() for sub in fileNames]

date_hour = time.strftime("%Y") + '-' + time.strftime("%m")+ '-' + time.strftime('%d')+ '-' +time.strftime('%H')
directoryName = "./" + date_hour + "_dir/"

xpath = '/html/body/div[3]/main/div/div[2]/div[1]/div/div'


for i in range(len(sites)):
    datafile = createFile(directoryName, fileNames[i])
    datafile.write(names[i] + "\n\n")
    driver.get(sites[i])
    pageScrape(xpath, datafile, driver)


