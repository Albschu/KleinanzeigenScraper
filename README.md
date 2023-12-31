# YOUR PROJECT TITLE
#### Video Demo:  <URL HERE>
#### Description: This project comprises two components: 
####              a web scraper and a visualization tool.  
####                  Web Scraper(file: "KleinanzeigenScraper.py"):
####                  The web scraper extracts information from Kleinanzeigen 
####                  (Germany's Craigslist equivalent) and stores the data in an 
####                  SQLite3 database.  
####
####                  Visualization Tool(file: "forntend.py"):
####                  The visualization tool is a Tkinter-based 
####                  interface designed to display the cheapest, newest, and most 
####                  expensive listings. The scraper cannot be initiated from the
####                  interface, but users can add new search terms.
####            usage:
####                  Start interface (Fontend.py) and add a Searchterm you want Scraped, close the Interface.  
####                  Start the Scraper and let it run for how long you want to.
####                  Start the Interface back up and see the Data. 
####                  If It ran Multiple Days, you can see the Price Progression.



#### Ideas to expand on:
####    - filter out deleted posts
####    - try to incorparate categorys, to filter out "repair posts"
####    - filter out "I search for ..." posts
