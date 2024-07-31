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

main_page_dataFile_exists = os.path.exists(os.path.join(os.getcwd(), directoryName, "main.txt"))


main_scaper_done = dir_exists and main_page_dataFile_exists


#checking if the main page files are already there
if(not main_scaper_done):
    print("running frontPage.py")
    os.system("python frontPage.py")
   
#this is for checking if a visual-stories exists. if it doesnt then run other.py
other_page_datafile_exists = os.path.exists(os.path.join(os.getcwd(), directoryName,  "visual-stories.txt"))
if (not other_page_datafile_exists):
    print("running other.py")
    os.system("python other.py")

#ask user if they want to store data into a ssms databse
store_yes = input("do you want to store data? (yes/no)")
#if yes then run python store.py
if store_yes == 'yes':
    os.system("python store.py")
