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



#functions used during scraping logic and storing data\
#function to create a directory of the data that needs to be stored. 
def createDataFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Warining: Creating directory. ' +  directory)





time = datetime.datetime.now()



#the file that will be created after the scraping will be this. this is so that we only scrape every hour and save it everyHour
fileName = time.strftime("%Y") + '-' + time.strftime("%m")+ '-' + time.strftime('%d')+ '-' +time.strftime('%H')


#directory will just be the file name 
directory = "./" + fileName + "_dir/"


createDataFolder(directory)
#we write to file while scraping the data

dataFileLocation = directory + fileName + ".txt"

datafile = open(dataFileLocation, 'w') #creates the file 

options = Options()
options.add_argument('--headless=new')
 
# initialize an instance of the chrome driver (browser)
driver = webdriver.Chrome(
      options=options, 
    # other properties...
)

# visit your target site
site = 'https://kathmandupost.com/'
driver.get(site)


# scraping logic...

#getting all responsive images in front page
responsiveImages = driver.find_elements(By.XPATH,"//img[contains(@class,'img-responsive')]")

#where all the images will go
imgsrc = []

for img in responsiveImages:
    imgsrc.append(str(img.get_attribute('src')))

#for now we write all the img src to the file
datafile.write("ALL IMG SRCS\n\n")
datafile.writelines(imgsrc)
datafile.write("\n")


#here i tried to download the images but the server doesn't let us get these images. 403: Forbiden. :(
"""
#downloading images
    
#filepath of where the img data should go
img_data_path = directory + "img{}.jpg" 
    

print(img_data_path)

for i in range(5):
    if(str(imgsrc[i]) != "None"):
        urllib.request.urlretrieve(str(imgsrc[i]), img_data_path.format(i))

"""



#getting the trending topics the top of the page
trending_topics = driver.find_elements(By.CSS_SELECTOR, ".trending-topics-list li")

#writing it to file 
datafile.write('TRENDING TOPICS\n')

trending_topics.pop(0)

for e in trending_topics:
    datafile.write(e.text + '\n')

datafile.write('\n')

#this part will be getting all the information on the main page that is divided into 3 columns

#these are the paths to the each column. the driver will get this 
LeftCol_XPATH = "/html/body/div[4]/main/div/div[2]/div[1]" 
MiddleCol_XPATH = "/html/body/div[4]/main/div/div[2]/div[2]"
RightCol_XPATH = "/html/body/div[4]/main/div/div[2]/div[3]"

LeftCol = driver.find_element(By.XPATH, LeftCol_XPATH)
MiddleCol = driver.find_element(By.XPATH, MiddleCol_XPATH)
RightCol = driver.find_element(By.XPATH, RightCol_XPATH)


#each cols has articles that have the information of each

#getting the titles of the aritcles by getting the h3
#getting the Authors by reading the span 
#getting the subtitles by reading the p 

#left Col scraping logic
LeftCol_Titles = LeftCol.find_elements(By.TAG_NAME, 'h3')
LeftCol_Authors = LeftCol.find_elements(By.TAG_NAME, 'span')
LeftCol_Subtitles = LeftCol.find_elements(By.TAG_NAME,  'p')


datafile.write("Main Articles\n")

for i in range(len(LeftCol_Titles)):
    title = LeftCol_Titles[i].text + " "
    author = LeftCol_Authors[i].text + " "
    subTitle = LeftCol_Subtitles[i].text + "\n"
    if(len(title) != 0):
        info = [title, author, subTitle]
        datafile.writelines(info)
        
        


#middle_col is a bit weird cause it also has the main article which is an h2 element
Main_Article = MiddleCol.find_element(By.TAG_NAME, 'h2')

#the other articles  
MiddleCol_Titles = MiddleCol.find_elements(By.TAG_NAME, 'h3')
MiddleCol_Authors = MiddleCol.find_elements(By.TAG_NAME, 'span')
MiddleCol_Subtitles = MiddleCol.find_elements(By.TAG_NAME,  'p')

datafile.write(Main_Article.text + " " +MiddleCol_Authors[0].text + " " + MiddleCol_Subtitles[0].text)

MiddleCol_Authors.pop(0)
MiddleCol_Subtitles.pop(0)

datafile.write('\n')

for i in range(len(MiddleCol_Titles)):
    title = MiddleCol_Titles[i].text + " "
    author = MiddleCol_Authors[i].text + " "
    subTitle = MiddleCol_Subtitles[i].text + "\n"
    if(len(title) != 0):
        info = [title, author, subTitle]
        datafile.writelines(info)

datafile.write('\nOPINION SECTION\n')

#RightCol is the opinions column. Technically not news but it follows the same stucture as the left columns
RightCol_Titles = RightCol.find_elements(By.TAG_NAME, 'h3')
RightCol_Authors = RightCol.find_elements(By.TAG_NAME, 'span')
RightCol_Subtitles = RightCol.find_elements(By.TAG_NAME,  'p')

for i in range(len(RightCol_Titles)):
    title = RightCol_Titles[i].text + " "
    author = RightCol_Authors[i].text + " "
    if(len(RightCol_Authors[i].text) == 0):
        author = "By Anonymous "
    subTitle = RightCol_Subtitles[i].text + "\n"
    if(len(title) != 0):
        info = [title, author, subTitle]
        datafile.writelines(info)

#next up is getting the visual stories 
visualStories_XPATH = "/html/body/div[4]/main/div/div[5]/div"
#this will get us the text of the titles. we can worry abou the image and other stuff later

#TODO: get the images and other stuff of the articles 
visualStories = driver.find_element(By.XPATH, visualStories_XPATH)

#this section has 4 different links that needs to be clicked then saved to its own file

#TODO:FIX THIS CAUSE IDK WHY IT WON'T LET ME CLICK right after i referecne it damn thing
#visualStories_links = visualStories.find_element(By.TAG_NAME, 'figure').click()
#creating the visual story
visual_Datafile_Location_name = directory + "visual_Stories" + ".txt"

visual_Datafile = open(visual_Datafile_Location_name, 'w')

visual_Datafile.write("VISUAL STOREIS")

#both the text and images will take the diver to the 

visualStories_a = driver.find_element(By.XPATH, visualStories_XPATH).find_elements(By.TAG_NAME, 'a')
visualStories_links = []

for a in visualStories_a:
    visualStories_links.append(a.get_attribute("href"))

visualStories_links.pop(0)
visualStories_links.pop(1)
visualStories_links.pop(2)
visualStories_links.pop(3)

for page in visualStories_links:
    driver.get(page)
    page_row_XPATH = '/html/body/div[3]/main/div[2]/div'
    page_row = driver.find_element(By.XPATH, '/html/body/div[3]/main/div[2]/div')
    page_title = page_row.find_element(By.TAG_NAME, 'h1')
    page_subTitle = page_row.find_element(By.TAG_NAME, 'span')
    image_srcs = page_row.find_elements(By.TAG_NAME, 'img')
    figCaptionTitle = page_row.find_element(By.TAG_NAME, 'figcaption')
    articleAuthor = page_row.find_element(By.TAG_NAME, 'h5')
    published_updated_time = page_row.find_elements(By.CLASS_NAME, "updated-time")

    print()
    print(page_title.text)
    print(page_subTitle.text)
    print("TITLE IMAGE")
    print(image_srcs[0].get_attribute('src'))
    print(figCaptionTitle.text)
    print()
    print("By " + articleAuthor.text)
    print(published_updated_time[0].text)
    print(published_updated_time[1].text)
    
    page_images_xpath = "/html/body/div[3]/main/div[2]/div/div/div[2]/div/div[6]"
    page_article = page_row.find_element(By.XPATH, page_images_xpath)

    page_article_imgs = page_article.find_elements(By.TAG_NAME, 'img')
    page_article_figcaptions = page_article.find_elements(By.TAG_NAME, 'figcaption')


    print("\nARTICLE IMAGES AND CAPTIONS")

    
    for i in range(len(page_article_figcaptions)):
        check_src = str(page_article_imgs[i].get_attribute('src'))


        if(check_src == 'None'):
            print(page_article_imgs[i].get_attribute('data-src'))
        else:
            print(check_src)        

        print(page_article_figcaptions[i].text)
        

    
    
    

    







driver.get(site)


#print(visualStories_links)




    #

datafile.write('\nVisual Stories\n')
visualStories = driver.find_element(By.XPATH, visualStories_XPATH)
datafile.writelines(visualStories.text)


#gett all the articles under "More News"
moreNews_XPATH = "/html/body/div[4]/main/div/div[6]/div/div[3]/div"
moreNews = driver.find_element(By.XPATH, moreNews_XPATH)

moreNews_Titles = moreNews.find_elements(By.TAG_NAME,  'h3')
moreNews_Authors = moreNews.find_elements(By.TAG_NAME,  'span')
moreNews_subTitles = moreNews.find_elements(By.TAG_NAME,  'p')

#within moreNews_Authors "SPONSORED" comes up twice in pos 1 and 2, so we need to remove it 
moreNews_Authors.pop(1)
moreNews_Authors.pop(1)



#within the articles there is a "Latest News" and "Sponsored Section"
#we should seperate them 

LatestNews_Title = moreNews_Titles[0].text
LatestNews_Author = moreNews_Authors[0].text
LatestNews_subTitles = moreNews_subTitles[0].text

datafile.writelines(["\n\nLATEST NEWS\n" + LatestNews_Title + " ", LatestNews_Author + " ", LatestNews_subTitles + "\n"])


Sponsored_Title = moreNews_Titles[1].text
Sponsored_Author = moreNews_Authors[1].text
Sponsored_subTitles = moreNews_subTitles[1].text

#print(LatestNews_Title, LatestNews_Author, LatestNews_subTitles)
#print(Sponsored_Title, Sponsored_Author, Sponsored_subTitles)
datafile.writelines(["\nSPONSORED\n" + Sponsored_Title + " ", Sponsored_Author + " ", Sponsored_subTitles + "\n"])





#poping those two titles so that they aren't repeated

moreNews_Titles.pop(0)
moreNews_Titles.pop(0)

moreNews_Authors.pop(0)
moreNews_Authors.pop(0)

moreNews_subTitles.pop(0)
moreNews_subTitles.pop(0)

datafile.write("\nMORE NEWS\n")


for i in range(len(moreNews_Titles)):
    title = moreNews_Titles[i].text + " "
    author = moreNews_Authors[i].text + " "
    if(len(moreNews_Authors[i].text) == 0):
        author = "By Anonymous "
    subTitle = moreNews_subTitles[i].text + "\n"
    if(len(title) != 0):
        info = [title, author, subTitle]
        datafile.writelines(info)


#getting the most read section 
#TODO:need to have the driver click on each element and get the author and subtitles as well
mostRead_XPATH = "/html/body/div[4]/main/div/div[6]/div/div[4]/div[1]/div"
mostRead = driver.find_element(By.XPATH, mostRead_XPATH)
mostRead_Tiltes = mostRead.find_elements(By.TAG_NAME, 'h5')

datafile.write("\nMost Read\n")

for i in range(len(mostRead_Tiltes)):
    title = moreNews_Titles[i].text + "\n"
    if(len(title) != 0):
        datafile.write(title)

#getting the Editors picks of the day
editorsPicks_XPATH = "/html/body/div[4]/main/div/div[6]/div/div[4]/div[3]/div"
editorsPicks = driver.find_element(By.XPATH, editorsPicks_XPATH)
editorsPicks_Tiltes = editorsPicks.find_elements(By.TAG_NAME, 'h5')

datafile.write("\nEditor's Picks\n")

for i in range(len(editorsPicks_Tiltes)):
    title = editorsPicks_Tiltes[i].text + "\n"
    if(len(title) != 0):
        datafile.write(title)


#getting the videos of the days
#TODO:click on videos and more information
videos_XPATH = "/html/body/div[4]/main/div/div[9]/div[1]/div"
videos = driver.find_element(By.XPATH, videos_XPATH)
videos_Titles = videos.find_elements(By.TAG_NAME, 'h5')

datafile.write("\nVideos\n")

for i in range(len(videos_Titles)):
    title = videos_Titles[i].text + "\n"
    if(len(title) != 0):
        datafile.write(title)

#Culture and arts sections 
cultureArts_XPATH = "/html/body/div[4]/main/div/div[9]/div[3]"
#the main artilce is h1 and the other articles are h3 
#TODO:get the authors of the article
cultureArts = driver.find_element(By.XPATH, cultureArts_XPATH)
cultureArts_Titles_main = cultureArts.find_element(By.TAG_NAME, 'h1')
cultureArts_Titles_other = cultureArts.find_elements(By.TAG_NAME, 'h3')

#getting all the subtiles 
cultureArts_Titles_subTitles = cultureArts.find_elements(By.TAG_NAME, 'p')


datafile.writelines(["\nCulture & Arts\n" + cultureArts_Titles_main.text + " ", cultureArts_Titles_subTitles[0].text + "\n"])

cultureArts_Titles_subTitles.pop(0)

for i in range(len(cultureArts_Titles_other)):
    title = cultureArts_Titles_other[i].text + "\n"
    subTitle = cultureArts_Titles_subTitles[i].text + "\n"
    if(len(title) != 0):
        datafile.write(title)
        
        datafile.write(subTitle)


#this section gets the last part of the articles featued on the front page 
#i spereated it inot different secations so that the data will be ordered when scrapeing
#each section has ul tag and those ul tags have the link and titles of the aritlces that are featured

nationalNews_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[1]'
politics_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[2]'
valley_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[3]'
money_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[4]'

climateEnv_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[5]'
health_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[6]'
food_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[7]'
travel_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[8]'

scienceTech_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[9]'
sports_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[10]'
world_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[11]'
features_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[12]'

columns_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[13]'
editorial_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[14]'
interviews_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[15]'
letters_XPATH = '/html/body/div[4]/main/div/div[11]/div/div[16]'

#now to loop though and get each ul 

nationalNews = driver.find_element(By.XPATH, nationalNews_XPATH)
politics = driver.find_element(By.XPATH, politics_XPATH)
valley = driver.find_element(By.XPATH, valley_XPATH)
money = driver.find_element(By.XPATH, money_XPATH)

climateEnv = driver.find_element(By.XPATH, climateEnv_XPATH)
health = driver.find_element(By.XPATH, health_XPATH)
food = driver.find_element(By.XPATH, food_XPATH)
travel = driver.find_element(By.XPATH, travel_XPATH)

scienceTech = driver.find_element(By.XPATH, scienceTech_XPATH)
sports = driver.find_element(By.XPATH, sports_XPATH)
world = driver.find_element(By.XPATH, world_XPATH)
features = driver.find_element(By.XPATH, features_XPATH)

columns = driver.find_element(By.XPATH, columns_XPATH)
editorial = driver.find_element(By.XPATH, editorial_XPATH)
interviews = driver.find_element(By.XPATH, interviews_XPATH)
letters = driver.find_element(By.XPATH, letters_XPATH)

#now we can get all the titles for now
#TODO:GET MORE Suff from each of these articles 

nationalNews_ul = nationalNews.find_elements(By.TAG_NAME, 'ul')
politics_ul = politics.find_elements(By.TAG_NAME, 'ul')
valley_ul = valley.find_elements(By.TAG_NAME, 'ul')
money_ul = money.find_elements(By.TAG_NAME, 'ul')

climateEnv_ul = climateEnv.find_elements(By.TAG_NAME, 'ul')
health_ul = health.find_elements(By.TAG_NAME, 'ul')
food_ul = food.find_elements(By.TAG_NAME, 'ul')
travel_ul = travel.find_elements(By.TAG_NAME, 'ul')

scienceTech_ul = scienceTech.find_elements(By.TAG_NAME, 'ul')
sports_ul = sports.find_elements(By.TAG_NAME, 'ul')
world_ul = world.find_elements(By.TAG_NAME, 'ul')
features_ul = features.find_elements(By.TAG_NAME, 'ul')

columns_ul = columns.find_elements(By.TAG_NAME, 'ul')
editorial_ul = editorial.find_elements(By.TAG_NAME, 'ul')
interviews_ul = interviews.find_elements(By.TAG_NAME, 'ul')
letters_ul = letters.find_elements(By.TAG_NAME, 'ul')

listOfUls = [nationalNews_ul, politics_ul, valley_ul, money_ul, climateEnv_ul, health_ul, food_ul, travel_ul, scienceTech_ul, sports_ul, world_ul, features_ul, columns_ul, editorial_ul, interviews_ul, letters_ul]



temp = 1 #this will help with what section its on
#printing each section
for section in listOfUls:
    match temp:
        case 1: 
            datafile.write("\nNATIONAL\n")
        case 2: 
            datafile.write("\nPOLITICS\n")
        case 3: 
            datafile.write("\nVALLEY\n")
        case 4: 
            datafile.write("\nMONEY\n")
        case 5: 
            datafile.write("\nCLIMATE & ENVIRONMENT\n")
        case 6: 
            datafile.write("\nHEALTH\n")
        case 7: 
            datafile.write("\nFOOD\n")
        case 8: 
            datafile.write("\nTRAVEL\n")
        case 9: 
            datafile.write("\nSCIENCE & TECHNOLOGY\n")
        case 10: 
            datafile.write("\nSPORTS\n")
        case 11: 
            datafile.write("\nWORLD\n")
        case 12: 
            datafile.write("\nFEATURES\n")
        case 13: 
            datafile.write("\nCOLUMNS\n")
        case 14: 
            datafile.write("\nEDITORIAL\n")
        case 15: 
            datafile.write("\nINTERVIEWS\n")
        case 16: 
            datafile.write("\nLETTERS\n")
    for ul in section:
        datafile.write(ul.text + "\n")
    temp = temp + 1



datafile.close()

"""
dataFileRead = open(dataFileLocation, 'r')
print(dataFileRead.read())
dataFileRead.close()

"""

# release the resources allocated by Selenium and shut down the browser
driver.quit()
