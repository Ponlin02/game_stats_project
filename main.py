import mysql.connector

# Establish the connection
connection = mysql.connector.connect(
    host = "localhost",      # Or the IP address of your DB server
    user = "root",  # The MySQL username (often 'root')
    password = "",  # The password for that user
    database = "gamestatsdb"  # The name of your schema/database
)

# Create a cursos to execute queries
cursor = connection.cursor()

#Example query
cursor.execute("SELECT * FROM Players")

# Fetch and print results
for row in cursor.fetchall():
    print(row)

#clean up
cursor.close()
connection.close()