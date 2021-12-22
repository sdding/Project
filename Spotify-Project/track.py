import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

cid = '9b73b4f7c7034bfcb6308b167f1c0852' 
secret = '2920f99719ba47aeab5525c08b977586' 
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Spotify에서 곡의 특성과 이미지 가져오기
def get_info(track, artist):
    track_info = sp.search(q=track, limit = 50, type='track')   # 상위 50개 검색
    
    count = 0
    for i in range(50): 
        if artist.lower() in track_info['tracks']['items'][i]['album']['artists'][0]['name'].lower():
            track_id = track_info['tracks']['items'][i]['id']                               # 곡의 id
            track_image = track_info['tracks']['items'][i]['album']['images'][0]['url']     # 앨범의 이미지
            popularity = track_info['tracks']['items'][i]['popularity']
            name = track_info['tracks']['items'][i]['album']['artists'][0]['name']
            count += 1
            break
        elif count == 0:
            return "찾는 곡이 없습니다"

    # 곡의 특성들
    features = sp.audio_features(tracks=[track_id])
    danceability = features[0]['danceability'] 
    energy = features[0]['energy'] 
    loudness = features[0]['loudness'] 
    speechiness = features[0]['speechiness']            # 말하는 정도
    acousticness = features[0]['acousticness']
    instrumentalness = features[0]['instrumentalness']  # 곡의 보컬이 있는 정도
    liveness = features[0]['liveness']
    valence = features[0]['valence']                    # 곡의 밝음 정도
    tempo = features[0]['tempo'] 

    result = [popularity, danceability,
            energy, loudness,
            speechiness, acousticness,
            instrumentalness, liveness,
            valence, tempo]
    
    return result, track, name, track_image