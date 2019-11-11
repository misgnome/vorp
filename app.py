import authorizer as auth

authorizer = auth.Authorizer()

if __name__ == '__main__':

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
    
    if user_preferences['1N']:
        num_games = int(input("how many games?"))
    elif user_preferences['RS']:
        num_games = 1230
    else:
        num_games = 0

    # Fetch any pages that are not already in our database 
    collect_raw_pages(authorizer, season)
    

