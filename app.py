from collector import collect_raw_box_score_pages
from collector import collect_raw_schedule_pages
from dotenv import load_dotenv
from indexer import extract_box_score_links_from_raw_schedule_pages 
import authorizer as auth




if __name__ == '__main__':
    load_dotenv()
    authorizer = auth.Authorizer()

    season = input("Enter the season you want to see a summary of. Refer to it by the year that year's finals is in: ")

    print("Producing VORPs for the {0}-{1} season.".format(str(int(season)-1),
        season))

    print("1) Full Season + Playoffs")
    print("2) Regular Season only")
    print("3) Playoffs only")
    print("4) First X games")

    names = ['FSP','RS','PO','1N']
    values = [False,False,False,False]
    select = int(input("\n" )[0])

    values[select-1] = True

    user_preferences = dict(zip(names, values))

    num_games = None
    if user_preferences['1N']:
        num_games = int(input("how many games?"))
    elif user_preferences['RS']:
        num_games = 1230

    # Fetch any schedule pages that are not already in our database 
    collect_raw_schedule_pages(authorizer, season)

    # Extract box scores from raw schedule and results pages
    # TODO: this can be optimized by storing the box score links that are
    # extracted in the db so they do not have to be recomputed every time
    box_score_page_urls = extract_box_score_links_from_raw_schedule_pages(authorizer, season)

    # Fetch any box score pages that are not already in our database 
    collect_raw_box_score_pages(authorizer,season, box_score_page_urls)



    

