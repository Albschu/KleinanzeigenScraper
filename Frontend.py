from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import requests
import sqlite3
import webbrowser


class ScrapedData:
    def __init__(self):
        self.name = ""
        self.price = ""
        self.location = ""
        self.date = ""
        self.description = ""
        self.imgUrl = ""
        self.Link = ""

    def getData(self, searchText, sort):
        # connect and link to the database
        connection = sqlite3.connect("data.db")
        db = connection.cursor()

        print(sort)
        if sort == "Show cheapest entry":
            que = db.execute(
                "SELECT * FROM ScrapedData WHERE SearchText = ? AND Price > 0.0 ORDER BY price ASC", [searchText]
                ).fetchone()
        elif sort == "Show newest entry":
            que = db.execute(
                "SELECT * FROM ScrapedData WHERE SearchText = ? ORDER BY Datetime DESC", [searchText]
                ).fetchone()
        elif sort == "Show most expensive entry":
            que = db.execute(
                "SELECT * FROM ScrapedData WHERE SearchText = ? ORDER BY price DESC", [searchText]
                ).fetchone()    
        else:
            que = None

        if que != None:
            self.name = que[2]
            self.price = que[7]
            self.date = que[5]
            self.description = que[6]
            self.imgUrl = que[3]
            self.Link = que[4]
        connection.close()


class MyGUI:
    def __init__(self):
        # create a window
        self.root = tk.Tk()                          # This creates the window
        self.root.geometry("1000x800")               # This resizes the window
        self.root.title("Kleinanzeigen Scraper")     # This gives the window a title
        self.ScrapedData = ScrapedData()            # This creates an instance of the ScrapedData class

        # Title the window 
        self.label = tk.Label(self.root, text="Kleinanzeigen Scraper", font=("Helvetica", 30))    # This is the label that will be displayed
        self.label.pack(pady=10)     # This is the label padding

        # add a grid 
        self.grid = tk.Frame(self.root)
        self.grid.columnconfigure(0, weight=1)
        self.grid.columnconfigure(1, weight=1)
        self.grid.columnconfigure(2, weight=1)
        self.grid.columnconfigure(3, weight=1)
        self.grid.columnconfigure(4, weight=1)


        # create a text entry box
        self.Search = tk.Entry(self.grid, text="Search", font=("Helvetica", 20))
        self.Search.grid(row=0, column=0, columnspan=3, sticky="ew")


        # create a button
        self.btn2 = tk.Button(self.grid, text="Add to Watchlist")
        self.btn2.grid(row=0, column=3, sticky="ewns", padx=10, pady=1)


        # Create a Dropdown menu
        self.options = [
            "Show cheapest entry",
            "Show newest entry",
            "Show most expensive entry"
        ]

        self.OptionSelect = StringVar()
        self.drop = OptionMenu(self.grid, self.OptionSelect, *self.options, command = self.showScrapedData)
        # self.OptionSelect.trace_add("write", self.dropdownEvent)
        self.OptionSelect.set(self.options[0])  # default value
        self.drop.grid(row=0, column=4, sticky="ewns", padx=10)


        # self.ScrapedData.getData("super-mario-bros-wonder", "cheapest")

        self.showScrapedData()



        self.grid.pack(fill = "x", padx=10)  # This adds the grid to the window (we add the widgets to the grid and then add the grid to the window)
        self.root.mainloop()     # This call makes sure the window stays open until the user closes it.

    def addToWatchlist(self, *args):
        print("Add to Watchlist")
        

    def showScrapedData(self, *args):

        self.ScrapedData.getData("super-mario-bros-wonder", self.OptionSelect.get())
        # add a picture
        self.imageUrl = self.ScrapedData.imgUrl        # This is the image url
        self.original = Image.open(requests.get(self.imageUrl, stream=True).raw)
        self.image = ImageTk.PhotoImage(self.original.resize((300, 300)))
        self.label = tk.Label(self.grid, image=self.image)
        self.label.image = self.image
        self.label.grid(row = 1, rowspan=2, columnspan=2, sticky="ewns", padx=10, pady=10)

        # add text with variable Data
        self.name = self.ScrapedData.name
        self.price = self.ScrapedData.price
        self.medianPrice = "Median Price"
        self.date = self.ScrapedData.date
        self.description = self.ScrapedData.description


        self.text = f"Name: {self.name}\nPrice: {self.price: .2f}€\nMedian Price: {self.medianPrice}\nPosted on: {self.date}\nDescription: {self.description}"

        self.nameLabel = tk.Label(self.grid, text=self.text, font=("Helvetica", 16), justify="left", wrap=650, anchor="nw")
        self.nameLabel.grid(row=1, column = 2, columnspan=3, sticky="nw", padx=10, pady=10)

        # add a button to open the link
        self.Linkbtn = tk.Button(self.grid, text="Open in Browser", command=lambda: webbrowser.open(self.ScrapedData.Link))     # lambda, because commdand normally only passes a function name, not a function call
        self.Linkbtn.grid(row=2, column=2, sticky="ewns", padx=10, pady=10)




        



if __name__ == "__main__":
    MyGUI()

