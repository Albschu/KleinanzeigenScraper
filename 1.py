import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Define your test data
test_data = ('Test Search', 'Test Name', 'Test Img', 'Test URL', '2022-01-01', 'Test Description', 100.0, 1, '2022-01-01 00:00:00')

# Insert the test data into the ScrapedData table
c.execute("INSERT INTO ScrapedData (SearchText, name, img, url, postDate, description, price, negotiable, datetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", test_data)

# Commit the changes and close the connection
conn.commit()
conn.close()