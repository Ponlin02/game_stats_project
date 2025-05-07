import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime

# Your database connection
import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gamestatsdb"
)
cursor = db.cursor()

# Main window setup
root = tk.Tk()
root.title("Spelar Databas Program")
root.geometry("400x400")

def show_players():
    cursor.execute("SELECT * FROM Players")
    players = cursor.fetchall()
    output = "\n".join([f"{p[0]} - {p[1]}" for p in players])
    messagebox.showinfo("Spelare", output)

def create_team():
    team_name = simpledialog.askstring("Input", "Ange namn på laget:")
    if not team_name:
        return

    cursor.execute("INSERT INTO Teams (TeamName) VALUES (%s)", (team_name,))
    team_id = cursor.lastrowid

    cursor.execute("SELECT * FROM Players")
    players = cursor.fetchall()
    player_text = "\n".join([f"{p[0]} - {p[1]}" for p in players])
    messagebox.showinfo("Tillgängliga spelare", player_text)

    player_ids = []
    for i in range(5):
        pid = simpledialog.askinteger("Input", f"Välj spelare {i+1} (ID):")
        if pid:
            player_ids.append(pid)

    for pid in player_ids:
        cursor.execute("INSERT INTO TeamMembers (TeamID, PlayerID) VALUES (%s, %s)", (team_id, pid))

    db.commit()
    messagebox.showinfo("Klar", "Laget har skapats!")

def show_teams():
    cursor.execute("SELECT * FROM Teams")
    teams = cursor.fetchall()
    output = "\n".join([f"{t[0]} - {t[1]}" for t in teams])
    messagebox.showinfo("Lagen", output)

def winrate_between_two_players():
    cursor.execute("SELECT * FROM Players")
    players = cursor.fetchall()
    player_text = "\n".join([f"{p[0]} - {p[1]}" for p in players])
    messagebox.showinfo("Spelare", player_text)

    p1 = simpledialog.askinteger("Input", "Ange första spelare ID:")
    p2 = simpledialog.askinteger("Input", "Ange andra spelare ID:")

    query = """
    SELECT COUNT(*) AS GamesTogether 
    FROM Matches m
    JOIN TeamMembers t1 ON m.Team1ID = t1.TeamID OR m.Team2ID = t1.TeamID
    JOIN TeamMembers t2 ON t1.TeamID = t2.TeamID
    WHERE t1.PlayerID = %s AND t2.PlayerID = %s;
    """
    cursor.execute(query, (p1, p2))
    games = cursor.fetchone()[0]

    win_query = """
    SELECT COUNT(*) AS WinsTogether
    FROM Matches m
    JOIN TeamMembers t1 ON m.WinningTeamID = t1.TeamID
    JOIN TeamMembers t2 ON t1.TeamID = t2.TeamID
    WHERE t1.PlayerID = %s AND t2.PlayerID = %s;
    """
    cursor.execute(win_query, (p1, p2))
    wins = cursor.fetchone()[0]

    if games > 0:
        winrate = (wins / games) * 100
        message = f"{wins} vinster av {games} matcher ({winrate:.1f}% winrate)"
    else:
        message = "Inga matcher tillsammans"
    
    messagebox.showinfo("Resultat", message)

def create_match():
    try:
        team1_id = simpledialog.askinteger("Input", "Enter Team 1 ID:")
        team2_id = simpledialog.askinteger("Input", "Enter Team 2 ID:")
        winner_id = simpledialog.askinteger("Input", "Enter winning team ID:")

        if None in (team1_id, team2_id, winner_id):
            messagebox.showwarning("Cancelled", "Match creation cancelled!")
            return
        
        # Get the current date for the matches
        match_date = datetime.date.today()

        insert_query = """
        INSERT INTO Matches (Team1ID, Team2ID, WinningTeamID, MatchDate)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(insert_query, (team1_id, team2_id, winner_id, match_date))
        db.commit()
        insert_player_gamestats(team1_id, team2_id)
        messagebox.showinfo("Success", "Match created successfully!")
    
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", f"An error occured: {error}")

def insert_player_gamestats(team1, team2):
    cursor.execute("SELECT * FROM Matches")
    matches = cursor.fetchall()
    output = "\n".join([f"{m[0]} - {m[1]} - {m[2]} - {m[3]} - {m[4]}" for m in matches])
    messagebox.showinfo("Matcher", output)

    matchid = simpledialog.askinteger("Input", "MatchID:")
    #cursor.execute("SELECT Team1ID, Team2ID FROM Matches WHERE MatchID = %s", (matchid,))
    #teams = cursor.fetchall()
        
    cursor.execute("SELECT playerID FROM TeamMembers WHERE TeamID = %s OR TeamID = %s", (team1, team2))
    count = 0
    for players in cursor.fetchall():  
          
        kills = simpledialog.askinteger("Input", "Kills:")
        deaths = simpledialog.askinteger("Input", "Deaths:")
        assists = simpledialog.askinteger("Input", "Assists:")
        
        query = """
        INSERT INTO PlayerMatchStats (MatchID, PlayerID, TeamID, Kills, Deaths, Assists)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        if count < 5:
            cursor.execute(query, (matchid, players[0], team1, kills, deaths, assists))
        else:
            cursor.execute(query, (matchid, players[0], team2, kills, deaths, assists))
            
        count += 1
        db.commit()

def get_player_kda():
    try:
        cursor.execute("SELECT * FROM Players")
        players = cursor.fetchall()
        player_text = "\n".join([f"{p[0]} - {p[1]}" for p in players])
        messagebox.showinfo("Spelare", player_text)

        player_id = simpledialog.askinteger("Input", "Ange spelar ID:")

        kda_query = """
        SELECT GetPlayerKDA(%s)
        """
        cursor.execute(kda_query, (player_id,))
        result = cursor.fetchone()

        if result and result[0]:
            messagebox.showinfo("Player KDA", result[0])
        else:
            messagebox.showinfo("Player KDA", "No data found for this player")

    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", f"An error occured: {error}")


def exit_program():
    cursor.close()
    root.destroy()
    db.close()

# Buttons
tk.Button(root, text="Visa Spelare", command=show_players).pack(pady=5)
tk.Button(root, text="Skapa Lag", command=create_team).pack(pady=5)
tk.Button(root, text="Visa Lag", command=show_teams).pack(pady=5)
tk.Button(root, text="Visa Winrate Mellan Två Spelare", command=winrate_between_two_players).pack(pady=5)
tk.Button(root, text="Create match", command=create_match).pack(pady=5)
tk.Button(root, text="Spelar KDA", command=get_player_kda).pack(pady=5)
tk.Button(root, text="Avsluta", command=exit_program).pack(pady=5)

# Start GUI loop
root.mainloop()