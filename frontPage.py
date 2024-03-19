#importing dateTime for file creating and storing informations into a file
import time as t
import datetime 
import sys
import os

#impporting selenium for webscraping 
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException



#functions used during scraping logic and storing data\
#function to create a directory of the data that needs to be stored. 
def createDataFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Warining: Creating directory. ' +  directory)

#the website sometimes has data images so sometimes you can't just check the src
#retruns the src 
def getImageSrc(image_element):
    check_src = str(image_element.get_attribute('src'))

    if(check_src == 'None'):
        return str(image_element.get_attribute('data-src'))
    else:
        return check_src

def get_all_links(xpath, driver):
    links = []
    aTags = driver.find_element(By.XPATH, xpath).find_elements(By.TAG_NAME, 'a')

    for link in aTags:
        links.append(link.get_attribute('href'))
    
    return links

def get_h3_links(xpath, driver):
    links = []
    h3Tags = driver.find_element(By.XPATH, xpath).find_elements(By.TAG_NAME, 'h3')

    for i in range(len(h3Tags)):
        links.append(h3Tags[i].find_element(By.TAG_NAME, 'a').get_attribute('href'))

    return links

def get_h5_links(xpath, driver):
    links = []


    if check_exists_by_tagName(driver, 'h5'):
        h5Tags = driver.find_element(By.XPATH, xpath).find_elements(By.TAG_NAME, 'h5')

    for i in range(len(h5Tags)):
        links.append(h5Tags[i].find_element(By.TAG_NAME, 'a').get_attribute('href'))

    return links

def get_first_aTag_updates(xpath, driver):
    articles = driver.find_element(By.XPATH, xpath).find_elements(By.TAG_NAME, 'article')

    link_to_article = []
    for article in articles:
        link_to_article.append(article.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        #link_to_article.append(article.text)

    return link_to_article



def check_exists_by_xpath(xpath, driver):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True 

def check_exists_by_tagName(driver, name):
    try:
        driver.find_element(By.TAG_NAME, name)
    except NoSuchElementException:
        return False
    return True



def article_scrape(driver, datafile):
    article_path = '/html/body/div[3]/main/div/div[2]/div[1]'
    author_path = '/html/body/div[3]/main/div/div[2]/div[1]/div/div/h5'

    '/html/body/div[3]/main/div[2]/div/div'

    if check_exists_by_xpath(article_path, driver) == False:
        visual_article(driver, datafile)
        return

    article_driver = driver.find_element(By.XPATH, article_path)
    author_driver = 0    

    if check_exists_by_xpath(author_path, driver):
        author_driver = driver.find_element(By.XPATH, author_path)

    section = ''
    title = ''
    title_sub = ''
    img_element = article_driver.find_element(By.CLASS_NAME, 'img-responsive')
    fig_caption = ''
    author = 'Anonymous'

    if check_exists_by_tagName(article_driver, 'h4'):
        section =  article_driver.find_element(By.TAG_NAME, 'h4').text

    if check_exists_by_tagName(article_driver, 'h1'):
        title =  article_driver.find_element(By.TAG_NAME, 'h1').text

    if check_exists_by_tagName(article_driver, 'span'):
        title_sub =  article_driver.find_element(By.TAG_NAME, 'span').text

    if check_exists_by_tagName(article_driver, 'figcaption'):
        fig_caption =  article_driver.find_element(By.TAG_NAME, 'figcaption').text

    if author_driver != 0:
        author = author_driver.text

    datafile.write("\n" +section + "\n" + title+ "\n" + title_sub+ "\n" + getImageSrc(img_element)+ "\n" + fig_caption + "\n" + author + "\n")

def visual_article(driver, datafile):
    article_path = '/html/body/div[3]/main/div[2]/div/div'
    author_path = '/html/body/div[3]/main/div[2]/div/div/div[2]/div/h5'

    article_driver = driver.find_element(By.XPATH, article_path)
    author_driver = 0    

    if check_exists_by_xpath(author_path, driver):
        author_driver = driver.find_element(By.XPATH, author_path)

    
    section = ''
    title = ''
    title_sub = ''
    img_element = article_driver.find_element(By.CLASS_NAME, 'img-responsive')
    fig_caption = ''
    author = 'Anonymous'


    if check_exists_by_tagName(article_driver, 'h4'):
        section =  article_driver.find_element(By.TAG_NAME, 'h4').text

    if check_exists_by_tagName(article_driver, 'h1'):
        title =  article_driver.find_element(By.TAG_NAME, 'h1').text

    if check_exists_by_tagName(article_driver, 'span'):
        title_sub =  article_driver.find_element(By.TAG_NAME, 'span').text

    if check_exists_by_tagName(article_driver, 'figcaption'):
        fig_caption =  article_driver.find_element(By.TAG_NAME, 'figcaption').text

    if author_driver != 0:
        author = author_driver.text

    datafile.write("\n" +section + "\n" + title+ "\n" + title_sub+ "\n" + getImageSrc(img_element)+ "\n" + fig_caption + "\n" + author + "\n")



#creating the directory 
time = datetime.datetime.now()
time_date_hour = time.strftime("%Y") + '-' + time.strftime("%m")+ '-' + time.strftime('%d')+ '-' +time.strftime('%H')
directory = "./" + time_date_hour + "_dir/"

createDataFolder(directory)
#we write to file while scraping the data

fileName = 'main'

dataFileLocation = directory + fileName + ".txt"

datafile = open(dataFileLocation, 'w', encoding='utf-8') #creates the file 

options = Options()
options.add_argument('--headless=new')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
 
# initialize an instance of the chrome driver (browser)
driver = webdriver.Chrome(
      options=options, 
    # other properties...
)

# visit your target site
site = 'https://kathmandupost.com/'
driver.get(site)

trending_topics_xpath = '/html/body/div[4]/main/div/div[1]/div/div'

#get all links in trending topics
trending_links = get_all_links(trending_topics_xpath, driver)

datafile.write("***TRENDING TOPICS***")
print('***TRENDING TOPICS***')

for link in trending_links:
    print(link)
    driver.get(link)
    article_scrape(driver, datafile)

driver.get(site)



datafile.write("***MAIN ARTICLES***")
print('***MAIN ARTICLES***')

main_articles_xpath = '/html/body/div[4]/main/div/div[2]'

article_links = get_h3_links(main_articles_xpath, driver)

for link in article_links:
    print(link)
    driver.get(link)
    article_scrape(driver, datafile)


driver.get(site)
datafile.write("***LATEST UPDATES***")
print('***LATEST UPDATES***')
updates_xpath = '/html/body/div[4]/main/div/div[6]/div/div[3]'

updates_links = get_first_aTag_updates(updates_xpath, driver)


for link in updates_links:
    print(link)
    driver.get(link)
    article_scrape(driver, datafile)

driver.get(site)



most_read_xpath = '/html/body/div[4]/main/div/div[6]/div/div[4]/div[1]/div'

datafile.write("***MOST READ***")
print('***MOST READ***')

most_read_links = get_h5_links(most_read_xpath, driver)

for link in most_read_links:
    print(link)
    driver.get(link)
    article_scrape(driver, datafile)

driver.get(site)

editors_picks_xpath = '/html/body/div[4]/main/div/div[6]/div/div[4]/div[3]/div'

editors_picks_links = get_h5_links(editors_picks_xpath, driver)

datafile.write("***Editor's Picks***")
print("***Editor's Picks***")

for link in editors_picks_links:
    print(link)
    driver.get(link)
    article_scrape(driver, datafile)

driver.get(site)



culture_arts_xpath = '/html/body/div[4]/main/div/div[9]/div[3]'

culture_arts_links = list(set(get_all_links(culture_arts_xpath, driver)))

datafile.write("***CULTURE & ARTS***")
print("***CULTURE & ARTS***")

for link in culture_arts_links:
    print(link)
    driver.get(link)
    article_scrape(driver, datafile)

driver.get(site)


all_news_xpath = '/html/body/div[4]/main/div/div[11]/div/div[1]/div/article/ul'

news_class_list = driver.find_elements(By.CLASS_NAME, 'block-newsCat--list')

ulElements = []

links = []

for newsList in news_class_list:
    ulElements.append(newsList.find_element(By.TAG_NAME, 'ul'))

for ulElement in ulElements:
   aTags_in_ul = ulElement.find_elements(By.TAG_NAME, 'a')
   

   for link in aTags_in_ul:
        links.append(link.get_attribute('href'))



datafile.write("***NEWS***")
print("***NEWS***")


for link in links:
    print(link)
    driver.get(link)
    article_scrape(driver, datafile)

driver.get(site)






datafile.close()
# release the resources allocated by Selenium and shut down the browser
driver.quit()
