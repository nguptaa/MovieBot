#---------DEPENDENCIES---------#
import requests
from bs4 import BeautifulSoup
from datetime import datetime

#---------USER INPUT---------#
movie_or_tv_show = input("Enter Movie or TV Show: ").replace(' ', '_')


#---------EXCEPTION HANDLING---------#
try:
    #---------CURRENT YEAR---------#
    now = datetime.now()
    current_year = now.year

    #---------FUNCTION TO GET HTML FROM URL---------#
    def getHTML(url):
        response = requests.get(url)
        return BeautifulSoup(response.content, 'lxml')

    #---------GETTING TITLE ID OF TV SHOW FROM IMDB SEARCH---------#
    imdb_home_page = getHTML("https://www.imdb.com/find?" + movie_or_tv_show)
    find_show_id = imdb_home_page.findAll('td', class_='result_text')[0]
    fetch_anchor_tag = find_show_id.find('a')
    fetch_link = fetch_anchor_tag['href']
    show_id = fetch_link[7:17]

    #---------CHECKING WEATHER IT IS MOVIE OR TVSHOW---------#
    imdb_page = getHTML("https://www.imdb.com/title/" + show_id)
    movie_show_date_year = imdb_page.find('div', class_='subtext').findAll('a')[-1]
    if 'TV Series' in movie_show_date_year.text.strip():
        print("TV Show Entered xD")
        #---------GETTING TV SHOW RELEASE DATE IMDB---------#
        imdb_page = getHTML("https://www.imdb.com/title/" + show_id)
        show_date_year = imdb_page.find(
            class_='seasons-and-year-nav').find_all('a')
        show_years = []
        for year in show_date_year:
            year = year.text.strip()
            if len(year) == 4:
                show_years.append(year)
        show_year = show_years[0]
        show_last_year = show_years[1]

        #---------DISPLAYING STATUS OF SHOW---------#
        if int(show_year) < current_year:
            print("The show has finished streaming all its episodes.")
        elif (int(show_year) > current_year) and (int(show_year)-1 != int(show_last_year)):
            print("The next season begins in " + show_year + ".")
        elif (int(show_year) > current_year) and (int(show_year)-1 == int(show_last_year)):
            imdb_episode_url = "https://www.imdb.com/title/" + \
                show_id + "episodes?year=" + show_last_year
            imdb_episode_page = getHTML(imdb_episode_url)
            airdate = []
            show_date = imdb_episode_page.findAll(class_='airdate')
            for ad in show_date:
                ad = ad.text.strip()
                if len(ad) != 4:
                    airdate.append(ad)
            show_date = airdate[-1]
            if '.' in show_date:
                show_date = show_date.replace('.', '')
            show_date = datetime.strptime(show_date, '%d %b %Y').date()
            if show_date <= now.date():
                print("The next season begins in " + show_year + ".")
            elif show_date > now.date():
                print('The next episode airs on ' + str(show_date) + '.')

        elif int(show_year) == current_year:
            imdb_episode_url = "https://www.imdb.com/title/" + \
                show_id + "episodes?year=" + show_year
            imdb_episode_page = getHTML(imdb_episode_url)
            airdate = []
            show_date = imdb_episode_page.findAll(class_='airdate')
            for ad in show_date:
                ad = ad.text.strip()
                if len(ad) != 4:
                    airdate.append(ad)
            show_date = airdate[-1]
            if '.' in show_date:
                show_date = show_date.replace('.', '')
            show_date = datetime.strptime(show_date, '%d %b %Y').date()
            if show_date <= now.date():
                print('The show has finished streaming all its episodes of this year' +
                    '(' + str(current_year) + ').')
            elif show_date > now.date():
                print('The next episode airs on ' + str(show_date) + '.')
    
    else:
        print("Movie Entered xD")
        imdb_page = getHTML("https://www.imdb.com/title/" + show_id)
        moviedate = imdb_page.find('div', class_='subtext').findAll('a')[-1]
        movie_date=[]
        for x in moviedate.text.strip():
            if x == '(':
                break
            movie_date.append(x)
        movie_date=''.join(movie_date)
        print(movie_date)
        movie_date = datetime.strptime(str(movie_date), '%d %B %Y')
        print(movie_date)

        

except Exception as e:
    print("ERROR")
