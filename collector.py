import requests
import const

UNFORMATTED_URL = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html"
HEADERS = {'user-agent': 'samuel-leonards/V0RP'}

def has_raw_box_score_page(authorizer, url):
    cur = authorizer.conn.cursor()
    cur.execute("""
    select 1 from raw_box_score_pages where url = %s
    """, (url,))
    if cur.fetchone():
        return True
    return False


def has_raw_schedule_page(authorizer, url):
    cur = authorizer.conn.cursor()
    cur.execute("""
    select 1 from raw_schedule_pages where url = %s
    """, (url,))
    if cur.fetchone():
        return True
    return False


def add_raw_box_score_page(authorizer, url, season, text):
    cur = authorizer.conn.cursor()
    cur.execute("""
    insert into raw_box_score_pages (url,season,raw_html)
    values (%s,%s,%s)""", (url,season,text))
    authorizer.conn.commit()
    cur.close()


def add_raw_schedule_page(authorizer, url, season, text):
    cur = authorizer.conn.cursor()
    cur.execute("""
    insert into raw_schedule_pages (url,season,raw_html)
    values (%s,%s,%s)""", (url,season,text))
    authorizer.conn.commit()
    cur.close()


def collect_raw_schedule_pages(authorizer, season):
    """Request and store `schedule_and_results_pages` that are not in db"""
    for month in const.BASKETBALL_MONTHS:
        url = UNFORMATTED_URL.format(season, month)

        if has_raw_schedule_page(authorizer,url):
            continue # do not add again

        r = requests.get(url, headers=HEADERS)
        add_raw_schedule_page(authorizer, url, season, r.text)

    
def collect_raw_box_score_pages(authorizer, season, box_score_page_urls):
    for url in box_score_page_urls:

        if has_raw_box_score_page(authorizer,url):
            continue # do not add again

        r = requests.get(url, header=HEADERS)
        add_box_score_page(authorizer, url, season, r.text)




