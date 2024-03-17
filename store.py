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

cursor = cnxn.cursor()

cursor.execute(''' 
    CREATE TABLE articles (
               article_id int primary key,
               article_title nvarchar(50)
    )

        ''')

cursor.commit()