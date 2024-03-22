#this file is for stroing the information on the files. 

import pyodbc
import time
import sys
import os

from dotenv import load_dotenv

load_dotenv()

server = os.getenv('server')
database = os.getenv('database')
username =  os.getenv('username1')
password =  os.getenv('password')


# Establishing a connection to the SQL Server
#connecting to database
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                      SERVER='+server+';\
                      DATABASE='+database+';\
                      UID='+username+';\
                      PWD='+ password)

"""
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf8')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf8')
cnxn.setencoding(encoding='utf8')
"""


cursor = cnxn.cursor()

new_tables_check = input("Is this your time saving to ssms? (yes/no)")

if (new_tables_check == 'yes'):
    try:
        cursor.execute(''' 
            CREATE TABLE main_articles (
                page_section nvarchar(50),
                section nvarchar(100),
                title nvarchar(500),
                subtitle nvarchar(500),
                title_img_src nvarchar(2083),
                title_img_caption nvarchar(500),
                author nvarchar(500)   
            )
            ''')

        cursor.commit()

        cursor.execute(''' 
            CREATE TABLE articles (
                section nvarchar(100),
                title nvarchar(500),
                subtitle nvarchar(500),
                title_img_src nvarchar(2083),
                author nvarchar(500)   
            )
            ''')

        cursor.commit()
    except:
        print("ERROR: Failed creating tables. The tables may already exist.")
        sys.exit() 


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
    'travel.txt',
    'investigation.txt',
    'climate-environment.txt',
    'world.txt',
    'science-technology.txt',
    'interviews.txt',
    'visual-stories.txt'
]

main_page_sections = [
    '***TRENDING TOPICS***',
    '***MAIN ARTICLES***',
    '***LATEST UPDATES***',
    '***MOST READ***',
    "***Editor's Picks***",
    "***CULTURE & ARTS***",
    "***NEWS***"
]



page_section = ""
section = ""
title = ""
sub_title = ""
title_img_src = ""
title_img_caption = ""
author = ""

date_hour = time.strftime("%Y") + '-' + time.strftime("%m")+ '-' + time.strftime('%d')+ '-' +time.strftime('%H')
directoryName = "./" + date_hour + "_dir"

#file_location = directoryName + chr(92) + "main.txt"
#datafile = open(file_location, 'r', encoding='utf-8')
article_count = 0
for file in fileNames:
    file_location = directoryName + chr(92) + file
    datafile = open(file_location, 'r', encoding='utf-8')
    lines = datafile.readlines()
    count = 0

    for line in lines:
        line_stripped = line.strip()

        skip = 0

        if line[0] == '*':
            #print(line_stripped)
            section = line_stripped[1:]
            #reset count 
            count = 0
            skip = 1

        if skip != 1:
            if count == 0:
                title = line_stripped
            elif count == 1:
                author = line_stripped
            elif count == 2:
                sub_title = line_stripped
            elif count == 3:
                title_img_src = line_stripped
            elif (count == 4):
                cursor.execute(''' 
                    INSERT INTO articles values 
                    (
                        ?,
                        ?,
                        ?,
                        ?,
                        ?     
                    )
                    ''', section, title, sub_title, title_img_src, author)
                cursor.commit()
                #print(section, title, author, sub_title, title_img_src)
                

            count = count + 1

            if count > 4:
                count = 0
                

file_location = directoryName + chr(92) + "main.txt"
datafile = open(file_location, 'r', encoding='utf-8')
lines = datafile.readlines()
count = 0
article_count = 0
for line in lines:
    line_stripped = line.strip()
    
    #its possible for the line to be a section change or an empty line

    if count == 0:
        for page_section_item in main_page_sections:
            if(line_stripped == page_section_item):
                page_section = line_stripped
                break
    #section line
    elif count == 1:
        section = line_stripped 
    elif count == 2:
        title = line_stripped 
    elif count == 3:
        sub_title = line_stripped 
    elif count == 4:
        title_img_src = line_stripped 
    elif count == 5:
        title_img_caption = line_stripped 
    elif (count == 6):
        author = line_stripped
        article_count = article_count + 1
        cursor.execute(''' 
        INSERT INTO main_articles values 
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?      
        )
        ''', page_section, section, title, sub_title, title_img_src, title_img_caption, author)
        cursor.commit()
        

    
    count = count + 1

    if (count > 6):
        count = 0
    

