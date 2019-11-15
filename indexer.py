from lxml.cssselect import CSSSelector
from bs4 import bs as bs, SoupStrainer as ss
import string 

BOX_SELECTOR = CSSSelector(".center a ")
UNFORMATTED_URL = "https://www.basketball-reference.com{}"
basic_stats_selector = ss("table", id = lambda x : x and x.endswith('-game-basic'))

def extract_box_scores_from_raw_box_score_pages(authorizer,season):
    steve_cur = authorizer.conn.cursor()
    steve_cur.execute("""
    select url,raw_html from raw_box_score_pages where season = %s
    """, (season,))

    box_scores = []
    for url,raw_html in steve_cur:
        game_soup = bs(raw_html, 'lxml', parse_only = basic_stats_selector)
        date = url[47:55]
    game_stats = []
    for tr in game_soup.find_all('tr'):
        tds = tr.find_all(['td', 'th'])
        player_stats = [td.text for td in tds]
        if player_stats[0] != "Starters" and player_stats[0] != "Reserves" and player_stats[0] != '': 
            game_stats.append(player_stats)
                ###
                pass
    steve_cur.close()

def extract_box_score_links_from_raw_schedule_pages(authorizer, season):

    # go into database and select pages
    cur = authorizer.conn.cursor()
    cur.execute("""
    select url,raw_html from raw_schedule_pages where season = %s
    """, (season,))

    box_urls = [] 
    for url,raw_html in cur:
        tree = lh.fromstring(raw_html)
        box_score_links_on_page = BOX_SELECTOR(tree)

        box_urls += [UNFORMATTED_URL.format(box_score_link.get('href')) for
                box_score_link in box_score_links_on_page]
    cur.close()
    return box_urls
    



def convert_box_scores_into_integrated_player_stats(authorizer, season): 
    scores = get_box_scores(authorizer, season)
    soups = [bs(soup['html'])]




