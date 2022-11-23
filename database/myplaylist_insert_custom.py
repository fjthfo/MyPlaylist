from sqlalchemy import create_engine
import pymysql
import pandas as pd
import pymysql as pm
import spotipy
import pprint
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(
    client_id='9719ffa5fb274362bad059926bc74082', client_secret='9992d22f8fd44e80a23950cee77f1cb2')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


artist_name = []
track_name = []
# track_popularity = []
artist_id = []
track_id = []
for i in range(0, 100, 50):
    track_results = sp.search(
        q='genre:k-pop', type='track', limit=50, offset=i)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        artist_id.append(t['artists'][0]['id'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        # track_popularity.append(t['popularity'])

track_df = pd.DataFrame({
    'track_id': track_id,
    'track_name': track_name,
    'artist_id': artist_id,
    'artist_name': artist_name})
# 'track_popularity': track_popularity,

# artist_popularity = []
artist_genres = []
artist_externalurl = []
# artist_followers = []
for a_id in track_df.artist_id:
    artist = sp.artist(a_id)
    # artist_genres.append(artist['genres'])
    artist_externalurl.append(artist['external_urls'])

# artist_popularity.append(artist['popularity'])
# artist_followers.append(artist['followers']['total'])

track_df = track_df.assign(
    artist_externalurl=artist_externalurl)
# artist_genres=artist_genres)
# artist_popularity = artist_popularity, artist_followers = artist_followers,
track_df.head()
pd.set_option('display.max_columns', None)
# pprint.pprint(track_df)
track_df


# print(track_df.shape)

# track_df.head()
# print(track_df)
# pprint.pprint(track_df)


# pip install pymysql
# pip install sqlalchemy

# MySQL Connector using pymysql
pymysql.install_as_MySQLdb()

# {} 안에 해당하는 정보 넣기. {}는 지우기.
engine = create_engine(
    "mysql+mysqldb://root:1234@localhost:3306/myplaylistdb".format(user='root', pw='1234', db='myplaylistdb'))
conn = engine.connect()

# MySQL에 저장하기
# 변수명은 이전에 만든 데이터프레임 변수명
# name은 생성할 테이블명
# index=False, 인덱스 제외
track_df.to_sql(name='Song', con=engine,
                if_exists='append', index=False)
conn.close()
