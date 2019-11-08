import numpy as np
import pandas as pd
import lxml.html as lh
from lxml.cssselect import CSSSelector
import requests
from bs4 import BeautifulSoup
from lxml import etree, objectify
import re


# ask user for what season she wants to see VORP for
season = input("Enter the season you want to see a summary of. Refer to it by the year that year's finals is in: ")
output = "Producing VORPs for the " + str(int(season)-1) + "-" + season + " season."
print(output)

#Get web pages for seasons game schedule
months = ["october", "november", "december", "january", "february", "march", "april", "may", "june"]
urls  = ["https://www.basketball-reference.com/leagues/NBA_"+season+"_games-" + month + ".html" for month in months]
#use requests to parse html
sources = [requests.get(url) for url in urls]
#structure html as trees
trees = [lh.fromstring(source.text) for source in sources]

#iterate and grab all box score pages
box_sel = CSSSelector(".center a ")
box_months = [box_sel(tree) for tree in trees]
box_links = []
for month in box_months:
	for game in month:
		box_links.append(game)

box_pages= [link.get('href') for link in box_links]

box_urls= ["https://www.basketball-reference.com" + page for page in box_pages]

#use requests to parse html for one box score page


#box_sources = [requests.get(url) for url in box_urls]
#box_trees = [lh.fromstring(source.text) for source in box_sources]
source = requests.get(box_urls[0])
#store contents of the page under doc
soup = BeautifulSoup(source.content,'html5lib')

tables = soup.find_all("table")

temp = [tables[7],tables[15]]
tables = temp



home_advanced = tables[1]
away_advanced = tables[0]

home_id = home_advanced.get("id")
away_id = away_advanced.get("id")

home_team = home_id[4:7]
away_team = away_id[4:7]

tables_string = str(tables[0]) + str(tables[1])
soup = BeautifulSoup(tables_string, 'html5lib')

links = soup.find_all('a')
Players = []
for link in links:
	Players.append(link.text)



home_string = str(home_advanced)
away_string = str(away_advanced)


home_soup = BeautifulSoup(home_string, 'html5lib')
away_soup = BeautifulSoup(away_string, 'html5lib')

home_links = home_soup.find_all('a')
away_links = away_soup.find_all('a')

Home_Players = []
for h in home_links:
	Home_Players.append(h.text)

Away_Players = []
for a in away_links:
	Away_Players.append(a.text)




home_df = pd.DataFrame()
home_df["Player"] = Home_Players
home_teams = [home_team] * len(Home_Players)

away_df = pd.DataFrame()
away_df["Player"] = Away_Players
away_teams = [away_team] * len(Away_Players)

teams = [away_df, home_df]

teams_df = pd.concat(teams)

stats = soup.find_all('td',{'data-stat':'mp'})
mps = []
for stat in stats:
	mps.append(stat.text)

Teams = away_teams + home_teams

player_stats=[]
team_minutes = []

t = 0	
for tr in soup.find_all('tr'):
	tds = tr.find_all(['th', 'td'])
	stats = []
	header = False
	DNP = True
	for i in range(0, len(tds)-1):
	 	if tds[i].text == "Starters" or tds[i].text == "Reserves" or tds[i+1].text == "Advanced Box Score Stats":
	 		header = True
	 		break
	 	if tds[i].text == "Team Totals":
	 		header = True
	 		team_minutes.append(tds[i+1].text)
	 		break
	 	if tds[i+1].text != "Did Not Play":
	 		DNP = False
	 		stats.append(tds[i].text)
	
	stats.append(tds[-1].text)
	if not header: 
		t += 1
		
		if not DNP:
			stats.append(Teams[t-1])
			
	
	if len(stats) == 17:
		player_stats.append(stats)




df = pd.DataFrame(player_stats, columns = ["Player", "MP", "TS%", "eFG%", "3PAr", "FTr", "ORB%", "DRB%", "TRB%", "AST%", "STL%", "BLK%", "TOV%", "USG%", "ORtg", "DRtg", "Team"])
df["Team Minutes"] = team_minutes[0]
df["Date"] = box_pages[0][11:19]


print(df)





