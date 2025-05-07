-- Create that database if it doesnt already exist!
CREATE DATABASE IF NOT EXISTS gamestatsdb;

-- Select the database so that we use it
USE gamestatsdb;

-- ###############
-- Table "Players"
-- ###############
CREATE TABLE Players (
	PLayerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Wins INT DEFAULT 0,
    GamesPlayed INT DEFAULT 0
    -- not containing kills and stuff because we can calculate it later. :D
);

-- #############
-- Table "Teams"
-- #############
CREATE TABLE Teams (
	TeamID INT AUTO_INCREMENT PRIMARY KEY,
    TeamName VARCHAR(100) NOT NULL
);

-- ##########################################################
-- Table "TeamMembers"
-- Many-to-many relationship between Teams and Players
-- Each team has 5 members (5v5 games) not less unfortunatley
-- ##########################################################
CREATE TABLE TeamMembers (
	TeamID int,
    PlayerID int,
    PRIMARY KEY (TeamID, PlayerID),
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID) ON DELETE CASCADE,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID) ON DELETE CASCADE
    -- "Cascade" means that the row will be deleted to avoid "ghost" references!
);

-- ##########################
-- Table "Matches"
-- Match info between 2 teams
-- ##########################
CREATE TABLE Matches (
	MatchID INT AUTO_INCREMENT PRIMARY KEY,
    Team1ID INT NOT NULL,
    Team2ID INT NOT NULL,
    WinningTeamID INT NOT NULL,
    MatchDate DATE NOT NULL,
    
    FOREIGN KEY (Team1ID) REFERENCES Teams(TeamID),
    FOREIGN KEY (Team2ID) REFERENCES Teams(TeamID),
    FOREIGN KEY (WinningTeamID) REFERENCES Teams(TeamID)
);

-- ###############################################
-- Table "PlayerMatchStats"
-- Individual performance from a player in a match
-- Kills, deaths, assists?? 
-- what do you think about assists Emil?
-- ###############################################
CREATE TABLE PlayerMatchStats (
	MatchID INT,
    PlayerID INT,
    TeamID INT,
    Kills INT DEFAULT 0,
    Deaths INT DEFAULT 0,
    Assists INT DEFAULT 0, -- Maybe?
    
    PRIMARY KEY (MatchID, PlayerID),
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID) ON DELETE CASCADE,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID) ON DELETE CASCADE,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID) ON DELETE CASCADE
);

-- #############################################
-- Trigger "update_player_stats_after_match"
-- This trigger updates "wins" and "gmaesplayed"
-- #############################################
-- Set delimiter so MySQL doesnt stop at the first semicolon
DELIMITER //

-- Create trigger that runs AFTER a new match is inserted 
CREATE TRIGGER update_player_stats_after_match
AFTER INSERT ON Matches
FOR EACH ROW
BEGIN
	-- 1. Update GamesPlayed for Players in Team 1
	UPDATE Players
    SET GamesPlayed = GamesPlayed + 1
    WHERE PlayerID IN (
		SELECT PlayerID
        FROM TeamMembers
        WHERE TeamID = NEW.Team1ID
	);
    
    -- 2. Update GamesPlayed for Players in Team 2
    UPDATE Players
    SET GamesPlayed = GamesPlayed + 1
    WHERE PlayerID IN (
		SELECT PlayerID
        FROM TeamMembers
        WHERE TeamID = NEW.Team2ID
	);
    
    -- 3. Update Wins only for players in the WinningTeam
    UPDATE Players
    SET Wins = Wins + 1
    WHERE PlayerID IN (
		SELECT PlayerID
        FROM TeamMembers
        WHERE TeamID = NEW.WinningTeamID
	);
END //

-- Reset the delimiter
DELIMITER ;

DELIMITER //

CREATE FUNCTION GetPlayerKDA(p_PlayerID INT)
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
	DECLARE totalKills INT;
    DECLARE totalDeaths INT;
    DECLARE totalAssists INT;
    DECLARE playerName VARCHAR(100);
    DECLARE result VARCHAR(255);
    
    SELECT
		COALESCE(SUM(Kills), 0),
        COALESCE(SUM(Deaths), 0),
        COALESCE(SUM(Assists), 0)
	INTO totalKills, totalDeaths, totalAssists
    FROM PlayerMatchStats
    WHERE PlayerID = p_PlayerID;
    
    SELECT Name INTO playerName
    FROM Players
    WHERE PlayerID = p_playerID;
    
    SET result = CONCAT(playerName, "'s KDA is ", totalKills, '/', totalDeaths, '/', totalAssists);
    return result;
END //

DELIMITER ;










