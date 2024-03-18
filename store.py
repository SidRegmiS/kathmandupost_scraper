#this file is for stroing the information on the files. 

import pyodbc 

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

cnxn.setencoding(encoding='utf-8')

cursor = cnxn.cursor()

cursor.execute("""DROP TABLE articles""")

cursor.execute(''' 
    CREATE TABLE articles (
        page_section nvarchar(50),
        section nvarchar(50),
        title nvarchar(100),
        subtitle nvarchar(500),
        title_img_src nvarchar(2083),
        title_img_caption nvarchar(500),
        author nvarchar(50)   
    )
    ''')

cursor.commit()

page_section = 'TRENDING TOPICS'
section = 'NATIONAL'
title = 'No let-up to infant mortality in Salyan'
sub_title = "While the infant mortality rate has been on a decline for the past two years, it's projected to rise this year."
title_img_src = 'https://assets-api.kathmandupost.com/thumb.php?src=https://assets-cdn.kathmandupost.com/uploads/source/news/2024/news/Untitled2-1710642657.jpg&w=900&height=601'
title_img_caption = 'A health worker inspects a pregnant woman in Salyan District Hospital recently. BIPLAB MAHARJAN'
author = 'Biplab Maharjan'

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