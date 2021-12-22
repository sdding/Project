# < Spotify Music Data >

## 음악 데이터의 특성들을 활용하여 딥러닝을 통해 장르를 예측
## 특정 음악을 입력받아 그와 유사한 음악을 추천하는 시스템
"""
데이터 분석
1. popularity에 따른 장르 분포
2. danceability에 따른 popularity 분포  
(가설 : danceability가 높을수록 popularity가 높을 것이다)
3. 특성들 간의 관계성
"""

import pandas as pd
df= pd.read_csv("SpotifyFeatures.csv")
df = df.drop("track_id", axis = 1)

df = df.drop_duplicates(['track_name'])
df = df.reset_index()
df.drop('index',axis=1,inplace=True)


# 장르의 개수
print("장르의 개수 :", len(df['genre'].unique()))

features = ['popularity', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
target = ['genre']
X = df[features]
y = df[target]

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y = le.fit_transform(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 2)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = 0.2, random_state = 2)

"""
# 다층 퍼셉트론 딥러닝
음악의 특성들을 통한 장르 예측
"""

import tensorflow as tf
from keras.callbacks import EarlyStopping

model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(512, activation='relu', input_shape=(10,)),
  tf.keras.layers.Dropout(0.1451),
  tf.keras.layers.Dense(512, activation='relu'),
  tf.keras.layers.Dropout(0.4726),
  tf.keras.layers.Dense(512, activation='relu'),
  tf.keras.layers.Dropout(0.7275),
  tf.keras.layers.Dense(27, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, y_train,
              epochs=50,
              batch_size = 256,
              validation_data=(X_val, y_val),
              callbacks=[EarlyStopping(monitor='val_loss',min_delta=0.0001, patience=3)])

model.evaluate(X_test,  y_test, verbose=2)

model.summary()

A = pd.DataFrame(pd.DataFrame(y).value_counts())
A = [i[0] for i in A.index]
B = pd.DataFrame(df['genre'].value_counts(normalize=True))
B['label'] = A


import numpy as np
# 장르와 라벨 
Label = {i : j for i, j in zip(A, B.index)}

def genre_pred(sample):
  D = {}
  for idx, i in enumerate(sample[0]):
    D[idx] = i

  return Label[sorted(D.items(), key = lambda item: item[1], reverse=True)[0][0]]


"""## 음악 추천(코사인 유사도 활용)"""

from sklearn.metrics.pairwise import cosine_similarity

# 비슷한 4곡 추천
def recommend(sample):
  simmillar_list = []
  
  for i, j in enumerate(df[features].values):
    simmillar_list.append([cosine_similarity([sample], [list(j)]), i])
    
  simmillar_list.sort()

  recommend_list = []
  for i in range(4):
    recommend_list.append([df['track_name'][simmillar_list[-i-1][1]], df['artist_name'][simmillar_list[-i-1][1]]])
  
  return recommend_list[0][0], recommend_list[0][1], recommend_list[1][0], recommend_list[1][1], recommend_list[2][0], recommend_list[2][1], recommend_list[3][0], recommend_list[3][1]