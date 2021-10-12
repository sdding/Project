import requests
from bs4 import BeautifulSoup


def melon_chart():
    # 멜론차트 Top 100 
    header = {'User-Agent': 'Mozilla/5.0'}
    melon_url = "https://www.melon.com/chart/index.htm"

    melon_page = requests.get(melon_url, headers=header)
    melon_soup = BeautifulSoup(melon_page.content, 'html.parser')

    title_list = []
    for title in melon_soup.find_all('div', class_='ellipsis rank01'):
        title_list.append(title.find('a').text)
    
    artist_list = []
    for artist in melon_soup.find_all('div', class_='ellipsis rank02'):
        artist_list.append(artist.find('span', class_='checkEllipsis').text)
    
    album_list = []
    like_list = []
    date_list = []
    genre_list = []
    for album, title in zip(melon_soup.find_all('div', class_='ellipsis rank03'), title_list):
        album_list.append(album.find('a').text)
        album_id = album.find('a')['href'].split("\'")[1]
        album_page = requests.get(f'https://www.melon.com/album/detail.htm?albumId={album_id}', headers=header)
        album_soup = BeautifulSoup(album_page.content, 'html.parser')
        for info in album_soup.find_all('dl', class_='list'):
            date_list.append(info.find('dd').text)
            genre_list.append(info.select('dd')[1].text)
        for info in album_soup.find_all('button', title = '{} 좋아요'.format(title)):
            if info.find('span', class_='cnt').text.split()[1] != '0':
                like_list.append(info.find('span', class_='cnt').text.split()[1])

    melon_info =[]    
    for i in range(100):
        melon_info.append([title_list[i], artist_list[i], album_list[i], i+1, like_list[i], date_list[i], genre_list[i]])

    return melon_info

def bugs_chart():
    # 벅스차트 Top 100
    bugs_url = "https://music.bugs.co.kr/chart"
    bugs_page = requests.get(bugs_url)
    bugs_soup = BeautifulSoup(bugs_page.content, 'html.parser')

    title_list = []
    for title in bugs_soup.find_all('p', class_='title'):
        title_list.append(title.find('a').text)
    
    artist_list = []    # 아티스트가 두팀 이상인 것 해결 불가
    album_list = []

    L = []
    for album in bugs_soup.find_all('td', class_='left'):
        L.append(album.find('a')['title'])
        
    for i in range(len(L)):
        if i % 2 != 0:
            album_list.append(L[i])
        else:
            artist_list.append(L[i])    
    
    bugs_info = []
    for i in range(100):
        bugs_info.append([title_list[i], artist_list[i], album_list[i], i+1])
    
    return bugs_info

def genie_chart():

    # 지니차트 Top 100
    genie_url1 = "https://www.genie.co.kr/chart/top200"
    genie_url2 = "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20211007&hh=21&rtm=Y&pg=2"
    header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # Top 1~50
    genie_page1 = requests.get(genie_url1, headers=header)
    genie_soup1 = BeautifulSoup(genie_page1.content, 'html.parser')
    # Top 51~100
    genie_page2 = requests.get(genie_url2, headers=header)
    genie_soup2 = BeautifulSoup(genie_page2.content, 'html.parser')
    
    genie_info = []
    for info, i in zip(genie_soup1.find_all('td', class_='info'), range(1,51)):

        title = info.find('a', class_='title ellipsis').text.strip()
        artist = info.find('a', class_='artist ellipsis').text.strip()
        album = info.find('a', class_='albumtitle ellipsis').text.strip()
    
        album_url = 'https://www.genie.co.kr/detail/albumInfo?axnm={}'.format(info.find('a', class_='albumtitle ellipsis')['onclick'][18:26])
        
        like_page = requests.get(album_url, headers=header)
        like_soup = BeautifulSoup(like_page.content, 'html.parser')
        
        for info in like_soup.find_all('span', class_='sns-like'):
            like = info.find('em', id ='emLikeCount').text
        
        for info in like_soup.find_all('ul', class_='info-data'):
            date = info.find_all('span', class_='value')[-1].text.strip()
            genre = info.find_all('span', class_='value')[-4].text.strip()
        genie_info.append([title, artist, album, i, like, date, genre])

    for info, i in zip(genie_soup2.find_all('td', class_='info'), range(51, 101)):

        title = info.find('a', class_='title ellipsis').text.strip()
        artist = info.find('a', class_='artist ellipsis').text.strip()
        album = info.find('a', class_='albumtitle ellipsis').text.strip()
    
        album_url = 'https://www.genie.co.kr/detail/albumInfo?axnm={}'.format(info.find('a', class_='albumtitle ellipsis')['onclick'][18:26])
        
        like_page = requests.get(album_url, headers=header)
        like_soup = BeautifulSoup(like_page.content, 'html.parser')
        
        for info in like_soup.find_all('span', class_='sns-like'):
            like = info.find('em', id ='emLikeCount').text.replace(',', '')
        for info in like_soup.find_all('ul', class_='info-data'):
            date = info.find_all('span', class_='value')[-1].text.strip()
            genre = info.find_all('span', class_='value')[-4].text.strip()
        genie_info.append([title, artist, album, i, int(like), date, genre])
    
    return genie_info

def billboard_chart():
    # 빌보드 코리아 Top 100 
    url = "http://billboard.co.kr/chart/week/"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    billboard_info = []
    for info, i in zip(soup.find_all('div', class_='chart_tit_tt'), range(1, 101)):
        title = info.find('p', class_='chart_tit').text
        artist = info.find('span', class_='chart_artist').text
        billboard_info.append([title, artist, i])
    
    return billboard_info
import os
import sqlite3

DB_FILENAME = 'chart.db'
DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)

conn = sqlite3.connect('chart.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Genie;")
cur.execute("""CREATE TABLE Genie(
        Title VARCHAR(50) NOT NULL,
        Artist VARCHAR(50) NOT NULL,
        Album VARCHAR(50) NOT NULL,
        Genie_Rank INT NOT NULL,
        Like INT,
        Date VARCHAR(50),
        Genre VARCHAR(50)
    );"""
)
cur.execute("DROP TABLE IF EXISTS Melon;")
cur.execute("""CREATE TABLE Melon(
        Title VARCHAR(50) NOT NULL,
        Artist VARCHAR(50) NOT NULL,
        Album VARCHAR(50) NOT NULL,
        Melon_Rank INT NOT NULL,
        Like INT,
        Date VARCHAR(50),
        Genre VARCHAR(50)
    );"""
)
cur.execute("DROP TABLE IF EXISTS Bugs;")
cur.execute("""CREATE TABLE Bugs(
        Title VARCHAR(50) NOT NULL,
        Artist VARCHAR(50) NOT NULL,
        Album VARCHAR(50) NOT NULL,
        Bugs_Rank INT NOT NULL
    );"""
)

cur.execute("DROP TABLE IF EXISTS Billboard;")
cur.execute("""CREATE TABLE Billboard(
        Title VARCHAR(50) NOT NULL,
        Artist VARCHAR(50) NOT NULL,
        Billboard_Rank INT NOT NULL
    );"""
)

for info in genie_chart():
    cur.execute("INSERT INTO Genie (Title, Artist, Album, Genie_Rank, Like, Date, Genre) VALUES(?, ?, ?, ?, ?, ?, ?);", tuple(info))
    
for info in melon_chart():
    cur.execute("INSERT INTO Melon (Title, Artist, Album, Melon_Rank, Like, Date, Genre) VALUES(?, ?, ?, ?, ?, ?, ?);", tuple(info))

for info in bugs_chart():
    cur.execute("INSERT INTO Bugs (Title, Artist, Album, Bugs_Rank) VALUES(?, ?, ?, ?);", tuple(info))

for info in billboard_chart():
    cur.execute("INSERT INTO Billboard (Title, Artist, Billboard_Rank) VALUES(?, ?, ?);", tuple(info))

conn.commit()

