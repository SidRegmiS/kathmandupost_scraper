#importing dateTime for file creating and storing informations into a file
import time
import datetime 
import sys
import os


#we need to check if a file exists so that we don't rerun the scraper too many times for the same data
#files are stored in a directory named "year-month-day-hour" of when the scraper ran
#then check the files in that direcotry. 

#the file that will be created after the scraping will be this. this is so that we only scrape every hour and save it everyHour
date_hour = time.strftime("%Y") + '-' + time.strftime("%m")+ '-' + time.strftime('%d')+ '-' +time.strftime('%H')
directoryName = "./" + date_hour + "_dir"

dir_exists = os.path.isdir(directoryName)

main_page_dataFile_exists = os.path.exists(os.path.join(os.getcwd(), directoryName, date_hour + ".txt"))
main_page_dataFile_visualStories_exists = os.path.exists(os.path.join(os.getcwd(), directoryName,  "visual_Stories.txt"))

main_scaper_done = dir_exists and main_page_dataFile_exists and main_page_dataFile_visualStories_exists

#checking if the main page files are already there
if(not main_scaper_done):
    print("main scraper needs to be ran agian")
    os.system("python frontPage.py")
   



national_page_datafile_exists = os.path.exists(os.path.join(os.getcwd(), directoryName,  "national.txt"))


if(not national_page_datafile_exists):
    print("national scaper needs to be run")
    os.system("python national.py")


poilitcs_page_datafile_exists = os.path.exists(os.path.join(os.getcwd(), directoryName,  "politics.txt"))

if(not poilitcs_page_datafile_exists):
    print("politics page needs to be scraped")
    os.system("python politics.py")

    
valley_page_datafile_exists = os.path.exists(os.path.join(os.getcwd(), directoryName,  "valley.txt"))


if(not valley_page_datafile_exists):
    print("Valley page needs to be scraped")
    os.system("python valley.py")



opinion_page_datafile_exists = os.path.exists(os.path.join(os.getcwd(), directoryName,  "opinion.txt"))

#scrapes both all opinion articles 
if(not opinion_page_datafile_exists):
    print("opinion page needs to be scraped")
    os.system("python opinion.py")


sports_page_datafile_exists = os.path.exists(os.path.join(os.getcwd(), directoryName,  "sports.txt"))

if(not sports_page_datafile_exists):
    print("sports page needs to be scraped")
    os.system("python sports.py")


    
culture_n_arts_page_datafile_exists = os.path.exists(os.path.join(os.getcwd(), directoryName,  "cul_life.txt"))

if(not culture_n_arts_page_datafile_exists):
    print("culture page needs to be scraped")
    os.system("python culture.py")


health_page_datafile_exists = os.path.exists(os.path.join(os.getcwd(), directoryName,  "health.txt"))

if(not culture_n_arts_page_datafile_exists):
    print("health page needs to be scraped")
    os.system("python health.py")




