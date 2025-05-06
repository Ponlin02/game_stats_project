-- Some simple queries to view stuff
SELECT * FROM matches;
SELECT * FROM playermatchstats;
SELECT * FROM players;
SELECT * FROM teammembers;
SELECT * FROM teams;

INSERT INTO Players (Name) VALUES
('Pontus'),
('Emil'),
('Gupta'),
('Lio'),
('Axel'),
('Tån');

INSERT INTO Teams (TeamName) Values
('G2'),
('FNC');

INSERT INTO TeamMembers (TeamID, PlayerID) Values
('1', '1'),
('1', '2'),
('1', '3'),
('2', '4'),
('2', '5'),
('2', '6');

INSERT INTO Matches (Team1ID, Team2ID, WinningTeamID, MatchDate) Values
('1', '2', '1', '2025-05-05');

INSERT INTO Matches (Team1ID, Team2ID, WinningTeamID, MatchDate) Values
('1', '2', '2', '2025-05-05');





