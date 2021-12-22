from track import *
from rec_model import *
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/recommend", methods=['GET', 'POST'])
def song_recommend():
    track_input = request.form['track']
    artist_input = request.form['artist']

    song_feature = get_info(track_input, artist_input)[0]
    artist = get_info(track_input, artist_input)[2]
    album_image = get_info(track_input, artist_input)[3]

    features_encoded = scaler.transform([song_feature])
    pred = model.predict(features_encoded)
    
    genre = genre_pred(pred)
    R = recommend(song_feature)
    return render_template('recommend.html', genre = genre, image = album_image, artist = artist, track=track_input, T1=R[0], A1=R[1], T2=R[2], A2=R[3], T3=R[4], A3=R[5], T4=R[6], A4=R[7])

if __name__ == '__main__':
    app.run()

