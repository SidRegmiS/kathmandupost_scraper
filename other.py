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

def pageScrape2(xpath, datafile, driver):
    title = driver.find_element(By.XPATH, xpath).find_element(By.TAG_NAME, 'h4')
    articles = driver.find_element(By.XPATH, xpath).find_elements(By.TAG_NAME, 'article')
    imgs_Of_Article = driver.find_element(By.XPATH, xpath).find_elements(By.CLASS_NAME, 'img-responsive')

    datafile.write(title.text + "\n")
    for i in range(len(articles)):
        datafile.write(articles[i].text)
        datafile.write("\nImage: " + getImageSrc(imgs_Of_Article[i]) + "\n\n")


def check_exists_by_xpath(xpath, driver):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True 

def get_all_links(xpath, driver):
    links = []
    aTags = driver.find_element(By.XPATH, xpath).find_elements(By.TAG_NAME, 'a')

    for link in aTags:
        links.append(link.get_attribute('href'))
    
    return links


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
    'https://kathmandupost.com/national',
    'https://kathmandupost.com/politics',
    'https://kathmandupost.com/valley',
    'https://kathmandupost.com/opinion',
    'https://kathmandupost.com/money',
    'https://kathmandupost.com/sports',
    'https://kathmandupost.com/art-culture',
    'https://kathmandupost.com/health',
    'https://kathmandupost.com/food',
    'https://kathmandupost.com/corrections',
    'https://kathmandupost.com/travel', 
    'https://kathmandupost.com/investigations', 
    'https://kathmandupost.com/climate-environment',  
    'https://kathmandupost.com/world',
    'https://kathmandupost.com/science-technology'
]

fileNames = [
    'national.txt',
    'politcs.txt',
    'valley.txt',
    'opinion.txt',
    'money.txt',
    'sports.txt',
    'art-culture.txt',
    'health.txt',
    'food.txt',
    'corrections.txt',
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

#special for 'correnctions' page
xpath2 = '/html/body/div[4]/main/div[2]/div/div/div[1]'

ul_xpath = '/html/body/div[3]/main/div/ul'


for i in range(len(sites)):
    
    name = names[i]
    datafile = createFile(directoryName, fileNames[i])
    driver.get(sites[i])
    print(name)
    if(name == 'CORRECTIONS'):
        pageScrape2(xpath2, datafile, driver)
    else:
        pageScrape2(xpath, datafile, driver)

        #check if the ul_xpath exists
        if check_exists_by_xpath(ul_xpath, driver):
            #get all links in ul
            links_in_ul = get_all_links(ul_xpath, driver)
            
            for link in links_in_ul:
                driver.get(link)
                pageScrape2(xpath, datafile, driver)

        




