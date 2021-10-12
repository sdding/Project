import pandas as pd
melon = pd.read_csv('Melon.csv')
genie = pd.read_csv('Genie.csv')

# Melon 차트
from datetime import datetime
melon['Date'] = pd.to_datetime(melon['Date'])
melon['Days'] = datetime.today() - melon['Date']
melon['Days'] = melon['Days'].dt.days

def func(df):
  if df['Days'] == 0:
    return df['Like']
  elif (df['Days'] <= 100) and (df['Days'] > 0):
    return df['Like'] // df['Days']
  elif (df['Days'] > 100) and (df['Days'] <= 365):
    return df['Like'] // 100
  else:
    return df['Like'] // 365

melon['Like_per_day'] = melon.apply(lambda x : func(x), axis=1)
melon2 = melon.sort_values(by='Like_per_day', ascending=False)
melon2.reset_index(inplace=True)
melon2.drop('index', axis=1, inplace=True)
melon2['New_Rank'] = melon2.index + 1

from sklearn.linear_model import LinearRegression, LogisticRegression

model1 = LinearRegression()

train = melon2.sample(frac = 0.8, random_state=1)
test = melon2.drop(train.index)

features = ['Like_per_day', 'Like'] 
target = ['Melon_Rank']

X_train = train[features]    
X_test = test[features]
y_train = train[target]
y_test = test[target]

model1.fit(X_train, y_train)    # 모델 학습
y_pred = model1.predict(X_test)    # 모델 예측

from sklearn.metrics import mean_absolute_error, r2_score

print("MAE score :", mean_absolute_error(y_test, y_pred))
print("R2 score :", r2_score(y_test, y_pred))

##########################################################################

# Genie 차트
def R(text):
  text = text.replace(',','')
  return int(text)
genie['Like'] = genie['Like'].apply(R)
genie['Date'] = pd.to_datetime(genie['Date'])
genie['Days'] = datetime.today() - genie['Date']
genie['Days'] = genie['Days'].dt.days

genie['Like_per_day'] = genie.apply(lambda x : func(x), axis=1)
genie2 = genie.sort_values(by='Like_per_day', ascending=False)
genie2.reset_index(inplace=True)
genie2.drop('index', axis=1, inplace=True)
genie2['New_Rank'] = genie2.index + 1

model2 = LinearRegression()

train = genie2.sample(frac = 0.8, random_state=1)
test = genie2.drop(train.index)

features = ['Like', 'Like_per_day']    
target = ['Genie_Rank']

X_train = train[features]    
X_test = test[features]
y_train = train[target]
y_test = test[target]

model2.fit(X_train, y_train)    # 모델 학습
y_pred = model2.predict(X_test)    # 모델 예측

print("MAE score :", mean_absolute_error(y_test, y_pred))
print("R2 score :", r2_score(y_test, y_pred))


import pickle

saved_model = pickle.dumps(model1)

L_from_pickle = pickle.loads(saved_model)

import joblib

joblib.dump(model1, 'L_model.pkl')  

model_x = joblib.load('L_model.pkl')



