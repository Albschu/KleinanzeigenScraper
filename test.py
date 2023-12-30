import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data = {'year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
         'unemployment_rate': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
         }  
dataframe = pd.DataFrame(data)

main_window = tk.Tk()

# Creates a new figure - a container for the actual plot
# Figsize is width/height in inches
figure = plt.Figure(figsize=(5, 4), dpi=100)
# Adds an axes to the figure
# Input is number of rows, number of cols, index position
# Assumes a grid layout
figure_plot = figure.add_subplot(1, 1, 1)
figure_plot.set_ylabel('Unemployment Rate')
# Place figure on main window
line = FigureCanvasTkAgg(figure, main_window)
# get_tk_widget
line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
# Meant for actual dates - groups unemployment rates by year and adds them up
dataframe = dataframe[['year', 'unemployment_rate']].groupby('year').sum()
dataframe.plot(kind='line', legend=True, ax=figure_plot, color='r', marker='o', fontsize=10)
figure_plot.set_title('Year Vs. Unemployment Rate')

main_window.mainloop()