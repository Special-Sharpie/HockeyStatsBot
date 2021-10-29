Welcome and thank you for adding HockeyBot to your discord server! HockeyBot is your one stop shop for all the hockey stats you want, on the fly! See below for list of working commands!
This page is your key to understanding every command as well as parameters that are required in order to retrieve live updating data from the NHL website!

Commands:
1.	HS-teamID – This is the most important command, as most of the team-based commands run of the IDs provided. (Deprecated, likely to be removed in future version.)
2.	HS-teamWL – When run, this command returns the current season Win/loss/OT record for the requested team, requiring 1 parameter, the opposing teams Abbreviation. Example: HS-teamWL CGY.
3.	HS-lifeWL – This command returns the lifetime Win/Loss at home, on the road, stats between two teams. This requires two parameters, the first Abbreviation, and second Abbreviation. Example: HS-lifeWL CGY EDM
4.	HS-Pstats – This command returns the most relevant stats for each player. This takes three parameters, the name which is required, a season, and a season type character (both of which are optional). Example: HS-Pstats JacobMarkstrom or HS-Pstats ConnorMcDavid 20192020 P 
5.	(Deprecated, likely to be removed in future version.)In-depth player stats. This is a collection of commands with exactly same requirements (except the season type code) as HS-Pstats, only one stat is returned opposed to all.
    A.	Goalies:
        a.	HS-Gwins – Returns total wins for the season.
        b.	HS-Gloss – Returns total losses for the season.
        c.	HS-Gotl – Return total overtime losses for the season.
        d.	HS-Gshutout – Returns total shutouts for the season.
        e.	HS-Gsaves – Returns total saves for the season.
        f.	HS-GSavep – Returns Save Percentage for the season.
        g.	HS-Ggaa – Returns Goals Against Average for the season.
        h.	HS-Ggoala – Returns total Goals Against for the season.
        i.	HS-Gshota – Returns total shots face for the season.
        j.	HS-Ggames – Returns total games played for the season.
        k.	HS-Gtoi – Returns total time on ice for the season.
    B.	Skaters:
        a.	HS-Pgoals – Returns total goals for the season.
        b.	HS-Passists – Returns total assists for the season.
        c.	HS-Ppoints – Returns total points for the season.
        d.	HS-Pgplayed – Return total games played for the season.
        e.	HS-Pshots – Returns total shots taken during the season.
        f.	HS-Pppgoals – Returns total Power Play goals for the season.
        g.	HS-Ppppoints – Returns total Power Play points for the season.
        h.	HS-Potgoals – Returns total Overtime goals for the season.
        i.	HS-Pshgoals – Returns total Short Handed goals for the season.
        j.	HS-Pgwgoals – Returns total Game Winning goals for the season.
        k.	HS-Pplusminus – Returns the players Plus/Minus rating for the season.
        l.	HS-Phits – Returns total Hits of the season.
        m.	HS-Pbshots – Returns total Blocked Shots for the season.
        n.	HS-Ppenalty – Returns total Penalty Minutes for the season.
        o.	HS-Ptoi – Returns total Time On Ice for the season.

6.	HS-Gnext – This command returns the next game date for the requested team, checking the next 10 days from the date the command was run. It only requires one parameter, a team Abbreviation. Example: HS-Gnext CGY
7.	HS-Glast – This command returns the last game date played by the requested team, checking the last 10 days from the date the command was run. It only requires one parameter, a team Abbreviation. Example: HS-Glast CGY
8.	HS-Gtoday – This command returns some info about the game of that current day of the requested team. It will return the game's matchup, and game stats as they become available. It only requires one parameter, a team ID. Example: HS-Gtoday CGY
9.	HS-divStandings – (Being re-worked. Does not return proper data.)This command returns the current season’s, and only he current season’s, divisional standings. This requires one parameter, the division. The 2020-2021 season has brought us new division. The accepted format of the division name is as follows: CENTRAL: “Central”, EAST: “East”, NORTH: “North”, WEST: “West”.
10.	HS-confStandings – Conferences are not in use in 2020-2021 This command returns the current season’s, conference standings. This requires one parameter, the conference(Eastern, Western). Example: HS-confStandings Western
11.	HS-leagueStandings – This command returns the standings for the entire league, and can be run for any season in NHL history. This command has no required parameters, but can be passed an optional season. Example: HS-leagueStandings or Hs-leagueStandings 20182019
12.	HS-playoffStandings – This command returns the data of any requested playoff series, from any round, during any season. It will return the team matchup, as well as the record for the series. This command requires three parameters, a team abbreviation, a playoff round (SCQ, R1, R2, CF, SCF), and the season. Note, SCQ only works for the 20192020 qualifier round. Exmaple: HS-playOffstandings CGY SCQ 20192020
13.	HS-daySummary – Returns a rundown of all games happening on the requested day. Can be passed an optional parameter Date (YYYY-MM-DD). Example: HS-daySummary or HS-daySummary 2021-10-29
14.	HS-skaterCareer – Returns the entire NHL career of the requested player. NOTE: This command returns a lot of data, and only works with active players. Use HS-ATplayerStats for non active players. Example: HS-skaterCareer ZdenoChara
15.	HS-next7 – Returns the schedule of the requested team over the following 7 days, giving the user the date and time of the upcoming in that over that period. Parameters: Team Abbreviation. Example: HS-next7 CGY.
16.	HS-perGame – Returns a player's stat over total games played. Takes two parameters, a player, and a stat. Use HS-statCodes for all stat codes. Example: HS-perGame EliasLindholm points
17.	HS-setTimezone – Updates the preferred timezone of the requestion server to change the timezone, run the command, and pass it a timezone code. The codes are: EASTERN TIME: ET, CENTRAL TIME: CT, MOUNTAIN TIME: MT, and PACIFIC TIME: PT. Example: HS-setTimezone ET
18. HS-draftByYear - Returns all draft picks of the requested team from the requested year. Exmaple: HS-draftByYear NYR 2020.
19. HS-Pinfo - Returns a suite of information about the requested player. Example HS-Pinfo JohnnGaudreau
20. HS-Tinfo - Returns a suite of information about the requested team. Example HS-Tinfo CGY
21. HS-ATplayerStats - Returns the career stats of all active and unactive NHL players. Similar to skaterCareer, only with less data and support for goalies. Example: HS-ATplayerStats JaromeIginla
22. HS-statLeader: Returns the highest scorers of the requested stat from high to low, takes the team abbreviation, how many places (top 10, top 5 etc) and the stat, which defaults to points. Example: HS-statLeaders CGY 10 goals
23. HS-singleStat: Returns a single requested stat. Takes 3 parameters, a player name, a stat code, and a season which is optional. Use HS-statCodes for all stat codes. Example: HS-singleStat BlakeColeman faceOffPct 20202021
24. HS-commandHistory - Sends the requesting a user a JSON file with all the command attempts after version 1.4.0.
25.	HS-info – I’m sure you have figured this one out… This command gets you here.

Errors:
There are three main errors that will be raised by HockeyBot, and this section here will explain them and help the end user find their mistake.
1.	MissingRequiredArguments: This error is raised whenever a required parameter is missing from the command, the best solve for this is to verify you command with the commands in this document in-order to determine which parameter you are missing.
2.	CommandNotFound: This error is straight forward, what you have requested is not a command, this could be due to a typo in the command itself or just requesting a command that does not exist. Please note, if you have a command for a certain stat that is not listed, let me know and I will look into adding it!
3.	CommandInvokeError: This error is raised anytime there is an issue with the provided parameters, typically it is caused by a typo in one of the parameters, or more than the required amount was given. Best fix is to check what you requested for any spelling errors or typos and check this document to ensure you have the correct parameters.
If any errors persist, feel free to email me at hockeystatsbot@gmail.com and I will investigate!
