from flask import Flask, render_template,request, redirect
from Prediction_helper import preprocessing, vectorizer, get_prediction
from Logger import logging

app = Flask(__name__)

logging.info('Flask server started')

data = dict()
Comment = []
positive = 0
negative = 0

@app.route("/")
def index():
    data['Comment'] = Comment
    data['positive'] = positive
    data['negative'] = negative

    logging.info('========== Open home page ============')

    return render_template('index.html', data=data)

@app.route("/", methods = ['post'])
def my_post():
    text = request.form['text']
    logging.info(f'Text : {text}')

    preprocessed_txt = preprocessing(text)
    logging.info(f'Preprocessed Text : {preprocessed_txt}')

    vectorized_txt = vectorizer(preprocessed_txt)
    logging.info(f'Vectorized Text : {vectorized_txt}')

    prediction = get_prediction(vectorized_txt)
    logging.info(f'Prediction : {prediction}')

    if prediction == 'negative':
        global negative
        negative += 1
    else:
        global positive
        positive += 1
    
    Comment.insert(0, text)
    return redirect(request.url)

if __name__ == "__main__":
    app.run()