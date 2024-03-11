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
    time.sleep(5)



national_page_datafile_exists = os.path.exists(os.path.join(os.getcwd(), directoryName,  "national.txt"))


if(not national_page_datafile_exists):
    print("national scaper needs to be run")
    os.system("python national.py")
else:
    print("national scaper needs to be run for debugging")
    os.system("python national.py")




