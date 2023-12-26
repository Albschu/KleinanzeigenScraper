
from bs4 import BeautifulSoup
import requests

# this is the search term that the user will enter
# search = input("Enter search term: ").replace(" ", "-")

# this is the search term used for testing
search = "super mario bros wonder".replace(" ", "-")

url = f"https://www.kleinanzeigen.de/s-{search}/k0"

# sets Headers for the request (User-Agent), so the request is not blocked. (from https://github.com/tax0r/Ebay-Kleinanzeigen-Scraper/blob/master/Ebay-Kleinanzeigen%20Scraper/main.py)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
}

# save the HTML in a variable.
html_text = requests.get(url=url, headers=headers).text  # this returns the whole html from the website

soup = BeautifulSoup(html_text, 'lxml')           # create soup object (allows us to parse through html file and grab data)

postingData = soup.find('div', class_='position-relative')   # find all the postings on the page and only save the HTML related to the postings

postings = postingData.find_all("li", class_="ad-listitem")  # a posting has the class "ad-listitem"; save the HTML of a single posting in a List-entry (better exessability)


# Test: get the data for the first posting
posting = postings[2]                                       # save the first posting in a variable
negotiable = False                                        # set the default value for negotiable to False


# if len(str(posting)) < 130:  # if the posting is shorter than 130 (111 + buffer) characters, it is not a posting, but a visual divider (Postings are ~60k characters long)
#     continue  # Skip this element as it doesn't contain valid data


# get the data from the posting
location = posting.find("div", class_="aditem-main--top--left").text.strip()
date = posting.find("div", class_="aditem-main--top--right").text.strip()
name = posting.find("div", class_="aditem-main--middle").h2.a.text.strip()
description = posting.find("div", class_="aditem-main--middle").p.text.strip()
price = posting.find("div", class_="aditem-main--middle--price-shipping").p.text.strip().replace(" €", "")

url = "https://www.kleinanzeigen.de/" + posting.find("div", class_="aditem-main--middle").h2.a.get("href")
img = posting.find("div", class_="imagebox srpimagebox").img.get("src")


# Price can have nagotiable in it, so we need to check for that
if "VB" in price:
    negotiable = True   # set negotiable to True if it is named
    price = price.replace("VB","") # remove the "VB" from the price

# If the price is "Zu verschenken", set it to 0
if "Zu verschenken" in price:
    price = 0.0
else:
    # If the price is not "Zu verschenken", cast the String into a double
    price = float(price)




# print the data (for testing)
# print(img)
# print(url)
# print(location)
# print(date)
# print(name)
# print(description)
# print(price)
# print(negotiable)






# Loop through all the postings on the page
# for posting in postings: