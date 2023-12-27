
from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime


# create a connection to the database
connection = sqlite3.connect("data.db")
db = connection.cursor()

# this is the search term that the user will enter
# searchText = input("Enter search term: ").replace(" ", "-")

# this is the search term used for testing
searchText = "super mario bros wonder".replace(" ", "-")

url = f"https://www.kleinanzeigen.de/s-{searchText}/k0"

# sets Headers for the request (User-Agent), so the request is not blocked. (from https://github.com/tax0r/Ebay-Kleinanzeigen-Scraper/blob/master/Ebay-Kleinanzeigen%20Scraper/main.py)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
}

# save the HTML in a variable.
html_text = requests.get(url=url, headers=headers).text  # this returns the whole html from the website

soup = BeautifulSoup(html_text, 'lxml')           # create soup object (allows us to parse through html file and grab data)

postingData = soup.find('div', class_='position-relative')   # find all the postings on the page and only save the HTML related to the postings

postings = postingData.find_all("li", class_="ad-listitem")  # a posting has the class "ad-listitem"; save the HTML of a single posting in a List-entry (better exessability)

# Loop through all the postings on the page
for posting in postings:
    negotiable = False                                        # set the default value for negotiable to False
    img = "No Image"                                          # set the default value for img to "No Image"


    # if the posting is shorter than 130 (111 + buffer) characters, it is not a posting, but a visual divider (Postings are ~60k characters long)
    if len(str(posting)) < 130:  
        continue  # Skip this element as it doesn't contain valid data


    # get the data from the posting
    location = posting.find("div", class_="aditem-main--top--left").text.strip()
    date = posting.find("div", class_="aditem-main--top--right").text.strip()
    name = posting.find("div", class_="aditem-main--middle").h2.a.text.strip()
    description = posting.find("div", class_="aditem-main--middle").p.text.strip()
    price = posting.find("div", class_="aditem-main--middle--price-shipping").p.text.strip().replace(" €", "")

    url = "https://www.kleinanzeigen.de/" + posting.find("div", class_="aditem-main--middle").h2.a.get("href")


    # if imagebox srpimagebox does not exist, the posting does not have an image
    if posting.find("div", class_="imagebox srpimagebox") is not None:
        img = posting.find("div", class_="imagebox srpimagebox").img.get("src")


    # Price can have nagotiable in it, so we need to check for that
    if "VB" in price:
        negotiable = True   
        price = price.replace("VB","") #

    # If the price is "Zu verschenken", set it to 0
    if "Zu verschenken" in price:
        price = 0.0
    else:
        # If the price is not "Zu verschenken", cast the String into a double
        price = float(price)

    db.execute("INSERT INTO ScrapedData (SearchText, name, img, url, postDate, description, price, negotiable, datetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (searchText, name, img, url, date, description, price, negotiable, datetime.now()))


# Commit the changes and close the connection
connection.commit() # finalize the changes
connection.close()

