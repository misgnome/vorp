from lxml.cssselect import CSSSelector

BOX_SELECTOR = CSSSelector(".center a ")
UNFORMATTED_URL = "https://www.basketball-reference.com{}"

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
    

def extract_box_scores_from_raw_box_score_pages(authorizer,season):
    steve_cur = authorizer.conn.cursor()
    steve_cur.execute("""
    select url,raw_html from raw_box_score_pages where season = %s
    """, (season,))

    box_scores = []
    for url,raw_html in steve_cur:
        tree = lh.fromstring(raw_html)

        ###
        pass
    steve_cur.close()
