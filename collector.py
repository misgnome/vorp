import requests
import const

UNFORMATTED_URL = "https://www.basketball-reference.com/leagues/NBA_{0}_games-{1}.html"
HEADERS = {'user-agent': 'samuel-leonards/V0RP'}


def has_game_info_page(authorizer, url):
    cur = authorizer.conn.cursor()
    cur.execute("""
    select 1 from game_info_pages where url = %s
    """, (url,))
    if cur.fetchone():
        return True
    return False


def add_game_info_page(authorizer, url, text):
    cur = authorizer.conn.cursor()
    cur.execute("""
    insert into game_info_pages (url,text)
    values (%s,%s)""", (url,text))
    authorizer.conn.commit()
    cur.close()


def collect_raw_games(authorizer, season):
    """Request and store `game_info_pages` that are not in db"""
    for month in const.BASKETBALL_MONTHS:
        url = UNFORMATTED_URL.format(season, month)

        if db_has_game_info_page(authorizer,season):
            continue

        r = requests.get(url, headers=HEADERS)
        add_game_info_page(authorizer, url, r.text)

    





