from bs4 import BeautifulSoup, element
import urllib.request
import pandas as pd
import numpy as np

pages = 3
rec_count = 0
rank = []
gname = []
platform = []

urlhead = 'https://www.vgchartz.com/games/games.php?page='
urltail = '&results=10&name=&console=&keyword=&publisher=&genre=&order=Sales&ownership=Both&boxart=Both&banner=Both&showdeleted=&region=All&goty_year=2019&developer=&direction=DESC&showtotalsales=0&shownasales=0&showpalsales=0&showjapansales=0&showothersales=0&showpublisher=0&showdeveloper=0&showreleasedate=0&showlastupdate=0&showvgchartzscore=0&showcriticscore=0&showuserscore=0&showshipped=0&alphasort=&showmultiplat=No'

for page in range(1, pages):
    surl = urlhead + str(page) + urltail
    r = urllib.request.urlopen(surl).read()
    soup = BeautifulSoup(r)
    print(f"Page: {page}")

    # vgchartz website is really weird so we have to search for
    # <a> tags with game urls
    game_tags = list(filter(
        lambda x: x.attrs['href'].startswith('http://www.vgchartz.com/game/'),
        # discard the first 10 elements because those
        # links are in the navigation bar
        soup.find_all("a")
    ))[10:]

    print(game_tags)

    for tag in game_tags:

        # add name to list
        gname.append(" ".join(tag.string.split()))
        print(f"{rec_count + 1} Fetch data for game {gname[-1]}")

        # get different attributes
        # traverse up the DOM tree
        data = tag.parent.parent.find_all("td")
        rank.append(np.int32(data[0].string))
        platform.append(data[2].find('img').attrs['alt'])
        rec_count += 1

columns = {
    'Rank': rank,
    'Name': gname,
    'Platform': platform,
}
print(rec_count)
df = pd.DataFrame(columns)
print(df.columns)
df = df[[
    'Rank', 'Name', 'Platform']]
df.to_csv("vgsales.csv", sep=",", encoding='utf-8', index=False)