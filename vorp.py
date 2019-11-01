import numpy as np
import pandas as pd
import lxml.html as lh
from lxml.cssselect import CSSSelector
import requests
from bs4 import BeautifulSoup
from lxml import etree, objectify

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
doc = lh.fromstring(source.text)

player_sel = CSSSelector("[id$='line_score']")



players = player_sel(doc)
player_list = [player.text for player in players]
print(player_list)











source = requests.get("https://www.basketball-reference.com/leagues/NBA_2020_advanced.html")

tree = lh.fromstring(source.text)

#print(lh.tostring(tree))

player_sel = CSSSelector(" th+ .left > a, #advanced_stats_clone > tbody > tr:nth-child(2) > td") 

vorp_sel = CSSSelector('.right:nth-child(29)')


players = player_sel(tree)
vorps = vorp_sel(tree)
#print(results)



player_list = [player.text for player in players]
vorp_list = [vorp.text for vorp in vorps]

data = {"Name":player_list, "VORP":vorp_list}
df = pd.DataFrame(data)

print(df)


