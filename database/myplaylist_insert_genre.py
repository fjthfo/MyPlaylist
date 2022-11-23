from sqlalchemy import create_engine
import pymysql
import pandas as pd
import pymysql as pm
import spotipy
import pprint
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(
    client_id='4138812fa1734ecda42dbb93a130550a', client_secret='7d31da4fc40f420b8696ad675aac3dac')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artist_name = []
track_name = []
artist_id = []
track_id = []
for i in range(0, 800, 50):
    track_results = sp.search(
        q='year:2015-2022', type='track', limit=50, offset=i, market='KR')
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        artist_id.append(t['artists'][0]['id'])
        track_name.append(t['name'])
        track_id.append(t['id'])


track_df = pd.DataFrame({
    'track_id': track_id,
    'track_name': track_name,
    'artist_id': artist_id,
    'artist_name': artist_name})


print('1')

artist_genres = []

for a_id in track_df.artist_id:
    artist = sp.artist(a_id)
    artist_genres.append(artist['genres'])

print('2')
track_df = track_df.assign(
    artist_genres=artist_genres)
print('3')
track_df.head()
pd.set_option('display.max_columns', None)
print('4')
pprint.pprint(track_df)
print(track_df.shape)
track_df['artist_genres'] = track_df['artist_genres'].astype("string")
# pip install pymysql
# pip install sqlalchemy


# * sql 연동

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
