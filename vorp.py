import numpy as np
import pandas as pd
import lxml.html as lh
from lxml.cssselect import CSSSelector
import requests
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree, objectify
import re
import os
import json
from datetime import datetime as dt 
import time
import multiprocessing



soups = map( lambda x: BeautifulSoup(x['html'], 'lxml', parse_only = SoupStrainer("table")), scores)

tableses = map(lambda x: x.find_all("table"), soups)
#store contents of the page under doc

temps = [[tables[6],tables[14]] for tables in tableses]
tableses = temps

home_basics = [tables[1] for tables in tableses]
away_basics = [tables[0] for tables in tableses]

home_ids = [home_basic.get("id") for home_basic in home_basics]
away_ids = [away_basic.get("id") for away_basic in away_basics]

home_teams = [home_id[4:7] for home_id in home_ids]
away_teams = [away_id[4:7] for away_id in away_ids]

tables_strings = [str(tables[0]) + str(tables[1]) for tables in tableses]
soups = [BeautifulSoup(tables_string, 'lxml') for tables_string in tables_strings]

linkses = [soup.find_all('a') for soup in soups]


home_strings = [str(home_basic) for home_basic in home_basics]
away_strings = [str(away_basic) for away_basic in away_basics]


home_soups = [BeautifulSoup(home_string, 'lxml') for home_string in home_strings]
away_soups = [BeautifulSoup(away_string, 'lxml') for away_string in away_strings]

home_linkses = [home_soup.find_all('a') for home_soup in home_soups]
away_linkses = [away_soup.find_all('a') for away_soup in away_soups]






All_Home_Players = [[h.text for h in home_links] for home_links in home_linkses]


All_Away_Players = [[a.text for a in away_links] for away_links in away_linkses]

statses = [soup.find_all('td', {'data-stat':'mp'}) for soup in soups]
Dates = [box_page[11:19] for box_page in box_pages]
j = 0
for soup in soups:
	Date = box_pages[j][11:19]
	home_df = pd.DataFrame()
	home_df["Player"] = All_Home_Players[j]
	home_teamses = [home_teams[j]] * len(All_Home_Players[j])

	away_df = pd.DataFrame()
	away_df["Player"] = All_Away_Players[j]
	away_teamses = [away_teams[j]] * len(All_Away_Players[j])

	teams = [away_df, home_df]

	teams_df = pd.concat(teams)
	stats = soup.find_all('td',{'data-stat':'mp'})
	mps = []
	for stat in stats:
		mps.append(stat.text)

	Teams = away_teamses + home_teamses

	player_stats=[]
	team_minutes = []
	

	team_stats = pd.DataFrame(columns = ["Date", "FGA", "FTA", "ORB", "DRB", "TOV", "3PA"])
	t = 0	

	for tr in soup.find_all('tr'):
		tds = tr.find_all(['th', 'td'])
		for i in range(0, len(tds)-1):
			if tds[i].text == "Team Totals":
				
			
				team_stats = team_stats.append(pd.DataFrame([[Date] + [tds[i+3].text] + [tds[i+9].text] + [tds[i+11].text] + [tds[i+12].text] + [tds[i+17].text] +[tds[i+6].text]], columns = ["Date", "FGA", "FTA", "ORB", "DRB", "TOV", "3PA"]), ignore_index= True)

	temp = team_stats.iloc[0, 6] 

	#swap 3PA to make it Opp3PA
	team_stats.iloc[0, 6] = team_stats.iloc[1, 6]
	team_stats.iloc[1, 6] = temp

	team_stats = pd.DataFrame([team_stats.iloc[0]] * len(away_teamses) + [team_stats.iloc[1]] * len(home_teamses), columns = ["Date", "FGA","FTA", "ORB", "DRB", "TOV", "3PA"])
	

	for tr in soup.find_all('tr'):
		tds = tr.find_all(['th', 'td'])
		stats = []
		header = False
		DNP = True
		
		for i in range(0, len(tds)-1):
			if tds[i].text == "Starters" or tds[i].text == "Reserves" or tds[i+1].text == "Basic Box Score Stats":
				header = True
				break
			if tds[i].text == "Team Totals":
				header = True
				team_minutes.append(tds[i+1].text)
				break
			if tds[i+1].text != "Did Not Play":
				DNP = False
				stats.append(tds[i].text)
			else: 
				stats.append(tds[i].text)
				dnp = ["00:00"] + ["0"] * 19
				stats = stats + dnp		
		if not DNP: 
			stats.append(tds[-1].text)
		if not header: 
			t += 1
			stats = stats + list(team_stats.iloc[t-1])
			
			stats.append(Teams[t-1])
			
			
		if len(stats) == 29:
			player_stats.append(stats)
	
	if j == 0:
		master_df = pd.DataFrame(player_stats, columns = ["Player", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", \
			"TRB","AST","STL","BLK", "TOV", "PF", "PTS", "+/-", "Date", "TmFGA", "TmFTA", "TmORB", "TmDRB", "TmTOV", "Opp3PA","Team"])

		master_df["TmMP"] = team_minutes[0]


		# master_df["BPM"] = coeffs[0]*master_df["MP"]\
		#  + coeffs[1]*master_df["ORB%"]\
		#   + coeffs[2] * master_df["DRB%"]\
		#    + coeffs[3] * master_df["STL%"]\
		#     + coeffs[4] * master_df['BLK%']\
		#      + coeffs[5] * master_df["AST%"]\
		#       - coeffs[6] * master_df["USG%"] * master_df["TOV%"]\
		#        + coeffs[7] * master_df["USG%"] * (1 - master_df["TOV%"]) * (2 * (master_df["TS%"]-master_df["TmTS%"]) + coeffs[8] * master_df["AST%"] + coeffs[9] * (master_df["3PAr"] - master_df["3PAr"].mean()) - coeffs[10])\
		#         + coeffs[11] * master_df["AST%"]**(1/2) * master_df["TRB%"]**(1/2)

		
		
	else:
		df = pd.DataFrame(player_stats, columns = ["Player", "MP", "FG", "FGA", "FG%", "3P", "3PA","3P%", "FT", "FTA", "FT%", "ORB", "DRB", \
			"TRB","AST","STL","BLK", "TOV", "PF", "PTS", "+/-", "Date", "TmFGA", "TmFTA", "TmORB", "TmDRB", "TmTOV", "Opp3PA", "Team"])		
		
		
		df["TmMP"] = team_minutes[0]
		

		
		# df["BPM"] = coeffs[0]*df["MP"]\
		#  + coeffs[1]*df["ORB%"]\
		#   + coeffs[2] * df["DRB%"]\
		#    + coeffs[3] * df["STL%"]\
		#     + coeffs[4] * df['BLK%']\
		#      + coeffs[5] * df["AST%"]\
		#       - coeffs[6] * df["USG%"] * df["TOV%"]\
		#        + coeffs[7] * df["USG%"] * (1 - df["TOV%"]) * (2 * (df["TS%"]-df["TmTS%"]) + coeffs[8] * df["AST%"] + coeffs[9] * (df["3PAr"] - df["3PAr"].mean()) - coeffs[10])\
		#         + coeffs[11] * df["AST%"]**(1/2) * df["TRB%"]**(1/2)
		
		
		master_df = master_df.append(df)

	
	j += 1
master_df.replace('', 0, inplace=True)

master_df["MP"] = pd.to_datetime(master_df["MP"], format = "%M:%S")
master_df["MP"] = master_df["MP"].dt.minute + master_df["MP"].dt.second/60
master_df[["MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", \
	"TRB","AST","STL","BLK", "TOV", "PF", "PTS", "+/-", "TmFGA", "TmFTA", "TmORB", "TmDRB", "TmTOV", "Opp3PA"]] = master_df[["MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", \
	"TRB","AST","STL","BLK", "TOV", "PF", "PTS", "+/-", "TmFGA", "TmFTA", "TmORB", "TmDRB", "TmTOV", "Opp3PA"]].apply(pd.to_numeric)
master_df["Date"] = pd.to_datetime(master_df["Date"], format = "%Y%m%d")
master_df = master_df.reset_index( drop = True)

players = master_df["Player"].unique()



cumulative_basics = pd.DataFrame( columns = [ "Player", "Date", "Team", "MP", "FG", "FGA", "3P", "3PA", "FT", "FTA", "ORB", "DRB", \
				"TRB","AST","STL","BLK", "TOV", "PF", "PTS", "+/-", "TmFGA", "TmFTA", "TmORB", "TmDRB", "TmTOV", "Opp3PA", "TmMP"])

dates = master_df["Date"].unique()

i = 0


for date in dates:
	for player in players:
		playedToday = True
		if master_df[(player == master_df["Player"]) & (date == master_df["Date"])].empty:
			playedToday = False
		data = master_df[(player == master_df["Player"]) & (date >= master_df["Date"]) & playedToday][["Player", "Date", "Team", "MP", "FG", "FGA", "3P", "3PA", "FT", "FTA", "ORB", "DRB", \
				"TRB","AST","STL","BLK", "TOV", "PF", "PTS", "+/-", "TmFGA", "TmFTA", "TmORB", "TmDRB", "TmTOV", "Opp3PA", "TmMP"]]
		if not data.empty:
			
			stats = data[[ "MP", "FG", "FGA", "3P", "3PA", "FT", "FTA", "ORB", "DRB", \
				"TRB","AST","STL","BLK", "TOV", "PF", "PTS", "+/-", "TmFGA", "TmFTA", "TmORB", "TmDRB", "TmTOV", "Opp3PA", "TmMP"]].sum(axis = 0).to_frame().T
			
			stats["Player"] = data["Player"].iloc[0]
			stats["Date"] = data["Date"].iloc[0]
			stats["Team"] = data["Team"].iloc[0]
			stats = stats[[ "Player", "Date", "Team", "MP", "FG", "FGA", "3P", "3PA", "FT", "FTA", "ORB", "DRB", \
				"TRB","AST","STL","BLK", "TOV", "PF", "PTS", "+/-", "TmFGA", "TmFTA", "TmORB", "TmDRB", "TmTOV", "Opp3PA", "TmMP"]]
			cumulative_basics = cumulative_basics.append(stats)
			
				
			i+=1
			
cumulative_basics = cumulative_basics.reset_index(drop = True)
print(cumulative_basics)





