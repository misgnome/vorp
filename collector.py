import requests
import const

UNFORMATTED_URL = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html"
HEADERS = {'user-agent': 'samuel-leonards/V0RP'}

def has_raw_box_score_page(authorizer, url):
    cur = authorizer.conn.cursor()
    cur.execute("""
    select 1 from raw_pages where (url,type) = (%s, %s)
    """, (url, const.BOX_SCORE_PAGE_TYPE))
    if cur.fetchone():
        return True
    return False


def has_raw_schedule_page(authorizer, url):
    cur = authorizer.conn.cursor()
    cur.execute("""
    select 1 from raw_pages where (url,type) = (%s, %s)
    """, (url, const.SCHEDULE_PAGE_TYPE))
    if cur.fetchone():
        return True
    return False


def add_raw_page(authorizer, url, season, text, _type):
    cur = authorizer.conn.cursor()
    cur.execute("""
    insert into raw_pages (url,season,raw_html,type)
    values (%s,%s,%s,%s)""", (url,season,text, _type))
    authorizer.conn.commit()
    cur.close()


def collect_raw_schedule_pages(authorizer, season):
    """Request and store `schedule_and_results_pages` that are not in db"""
    for month in const.BASKETBALL_MONTHS:
        url = UNFORMATTED_URL.format(season, month)

        if has_raw_schedule_page(authorizer,url):
            continue # do not add again

        r = requests.get(url, headers=HEADERS)
        add_raw_page(authorizer, url, season, r.text,
                const.SCHEDULE_PAGE_TYPE)

    
def collect_raw_box_score_pages(authorizer, season, box_score_page_urls):
    for url in box_score_page_urls:

        if has_raw_box_score_page(authorizer,url):
            continue # do not add again

        r = requests.get(url, headers=HEADERS)
        add_raw_page(authorizer, url, season, r.text,
                const.BOX_SCORE_PAGE_TYPE)




