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

#Menu logic
MENU_OFF = False
while not MENU_OFF:
    print("Spelar datarbas program")
    print("-" * 20)
    print("1. Visa Spelare")
    print("2. Skapa Lag")
    print("3. Registrera match")
    print("-" * 20)

    try:
        choice = int(input(""))
        if choice < 1 or choice > 3:
            raise ValueError
    except ValueError:
        print("mata in ett tal mellan 1 och 3")
    else:
        if choice == 1:
            cursor.execute("SELECT * FROM Players")
        
        # Fetch and print results
        for row in cursor.fetchall():
            print(row)

#clean up
cursor.close()
connection.close()