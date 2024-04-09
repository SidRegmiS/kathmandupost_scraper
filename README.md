Product Owner: Nishcal (nish)
Data Engineer: Siddhartha (Fragrance)
Data Scientist:  
# Web scraper for THE KATHMANDU POST

to run the program do: **python .\main.py**

the program will create a directory in the current directory. 
there will be files in the new directory that has all of the information that was scraped. 

WARNING: 

You might get an error message saying:

"ERROR: Couldn't read tbsCertificate as SEQUENCE
ERROR: Failed parsing Certificate"

This error does not break the scraper. This might be because your webdriver is not updated and it is warning the scraper that the site it is visting is unsafe.  

It will take a long time for the scraper to run. there are print statements to show what link the scraper is visiting
