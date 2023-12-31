import tkinter as tk 
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import sqlite3
import webbrowser

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from datetime import datetime


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


        # create a text entry box, with a dropdown menu
        self.SearchText = StringVar()
        self.combobox = ttk.Combobox(self.grid, textvariable=self.SearchText, font=("Helvetica", 20), values = self.getCurrentWatchlist())
        self.combobox.grid(row=0, column=0, columnspan=3, sticky="ew")




        # create a button
        self.btn2 = tk.Button(self.grid, text="Add to Watchlist", command=self.addToWatchlist)
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






        self.grid.pack(fill = "x", padx=10)  # This adds the grid to the window (we add the widgets to the grid and then add the grid to the window)


        self.root.mainloop()     # This call makes sure the window stays open until the user closes it.


    def getCurrentWatchlist(self):
        list = db.execute("SELECT searchterm FROM watchlist WHERE active = 1").fetchall()
        data = []
        for row in list:
            data.append(row[0])
        return data

    def addToWatchlist(self, *args):
        Searchterm = self.SearchText.get()
        x = db.execute("INSERT INTO watchlist (searchterm, active) VALUES (?, ?)", (Searchterm, 1))          # 1 represents true        

    def showScrapedData(self, *args):

        self.ScrapedData.getData(self.combobox.get(), self.OptionSelect.get())
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

        rawData = db.execute("SELECT AVG(Price), datetime FROM ScrapedData WHERE searchText = ? GROUP BY datetime", [self.combobox.get()]).fetchall()
        data = {'Date': [], 'MedianPrice': [], 'Time': []}
        for row in rawData:
            data["MedianPrice"].append(row[0])
            # Convert the string to a datetime object
            datetime_obj = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')

            # Extract the date and time
            date = datetime_obj.date()
            time = datetime_obj.time().strftime('%H:%M:%S')

            data["Date"].append(date)
            data["Time"].append(time)
  

        dataframe = pd.DataFrame(data)
        # Creates a new figure - a container for the actual plot
        # Figsize is width/height in inches
        figure = plt.Figure(figsize=(5, 4), dpi=100)
        # Adds an axes to the figure
        # Input is number of rows, number of cols, index position
        # Assumes a grid layout
        figure_plot = figure.add_subplot(1, 1, 1)
        figure_plot.set_ylabel('Unemployment Rate')
        # Place figure on main window
        line = FigureCanvasTkAgg(figure, self.root)
        # get_tk_widget
        line.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH)
        dataframe = dataframe[['Date', 'MedianPrice']].groupby('Date').sum()
        dataframe.plot(kind='line', legend=True, ax=figure_plot, color='r', marker='o', fontsize=10)
        figure_plot.set_title(f'Median Price')



        



if __name__ == "__main__":
    connection = sqlite3.connect("data.db")
    db = connection.cursor()
    MyGUI()
    connection.commit()
    connection.close()
