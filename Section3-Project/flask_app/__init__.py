from Model import *
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    L1 = request.form['Like']
    L2 = request.form['Like_per_day']

    pred = model1.predict(pd.DataFrame([[L1, L2]]))

    return render_template('predict.html', predict=pred)

if __name__ == '__main__':
    app.run()
