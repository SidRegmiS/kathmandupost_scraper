# Web scraper for THE KATHMANDU POST

to run the program do: **python .\main.py**

the program will create a directory in the current directory. 
there will be files in the new directory that has all of the information that was scraped.

in the .env file replace the information so that it stores the data into your server:
    server = ''
    database = ''
    username1 = ''
    password = ''

store.py will ask "Is this your time saving to ssms? (yes/no)". 
    if its your first time storing data say type "yes" then enter key
        this will create the database tables. 
    else say "no" then enter key

WARNING: 

You might get an error message saying:

"ERROR: Couldn't read tbsCertificate as SEQUENCE
ERROR: Failed parsing Certificate"

This error does not break the scraper. This might be because your webdriver is not updated and it is warning the scraper that the site it is visting is unsafe.  

It will take a long time for the scraper to run. there are print statements to show what link the scraper is visiting