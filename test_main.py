import mysql.connector
import tkinter as tk

# Establish the connection
connection = mysql.connector.connect(
    host = "localhost",      # Or the IP address of your DB server
    user = "root",  # The MySQL username (often 'root')
    password = "",  # The password for that user
    database = "gamestatsdb"  # The name of your schema/database
)

# Create the root window
root = tk.Tk()
root.title("GameStatsWindow")

# Add a label to test
label = tk.Label(root, text = "This is a test label")
label.pack()

# Start the GUI event loop
# root.mainloop()

# Create a cursos to execute queries
cursor = connection.cursor()

#Example query
cursor.execute("SELECT * FROM Matches")

# Fetch and print results
for row in cursor.fetchall():
    print(row)

#clean up
cursor.close()
connection.close()