#this file is for stroing the information on the files. 

import pyodbc
import time
import sys
import os 

server = 'DESKTOP-PLGKKL1'
database = 'KTP'
username = 'nish'
password = '1'

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

cursor.execute("""DROP TABLE main_articles""")
cursor.execute("""DROP TABLE articles""")


cursor.execute(''' 
    CREATE TABLE main_articles (
        page_section nvarchar(50),
        section nvarchar(100),
        title nvarchar(100),
        subtitle nvarchar(500),
        title_img_src nvarchar(2083),
        title_img_caption nvarchar(500),
        author nvarchar(100)   
    )
    ''')

cursor.commit()


cursor.execute(''' 
    CREATE TABLE articles (
        section nvarchar(100),
        title nvarchar(100),
        subtitle nvarchar(500),
        title_img_src nvarchar(2083),
        title_img_caption nvarchar(500),
        author nvarchar(100)   
    )
    ''')

cursor.commit()


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
directoryName = './2024-03-19-18_dir'
#datafile = open(file_location, 'r', encoding='utf-8')
article_count = 0
for file in fileNames:
    file_location = directoryName + chr(92) + file
    datafile = open(file_location, 'r', encoding='utf-8')
    print(file_location)
    lines = datafile.readlines()
    count = 0

   

    for line in lines:
        line_stripped = line.strip()


        if line[0] == '*':
            print(line_stripped)
            #reset count 
            count = 0
            continue

        
        

        if (count == 4):
            article_count = article_count + 1
            count = 0
        
        count = count + 1
        
        if article_count == 30:
            break
        


    break




sys.exit()

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
    

print(article_count)


    
    


"""
cursor.execute(''' 
    INSERT INTO articles values 
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
"""
