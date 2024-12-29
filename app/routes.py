from flask import jsonify, redirect, render_template, request, url_for
from sqlalchemy.sql.operators import is_false
from app import app, db
from app.models import News
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

# Load the trained LSTM model
model = load_model('lstm_model.h5')  # Replace with your actual path

# Load the tokenizer
tokenizer = joblib.load('tokenizer.pkl')

@app.route("/")
def index():
    return render_template('index.html', title="index title", prediction=None)

# @app.route("/users", methods=['GET'])
# def get_users():
#     users = User.query.order_by(User.id.asc()).all()
#
#     return render_template('user.html', users=users)
#
# @app.route("/users", methods=['POST'])
# def create_user():
#     username = request.form['username']
#
#     # if not valid username
#     if not username:
#         return "invalid input", 400
#
#     # create new user
#     new_user = User(username=username)
#     db.session.add(new_user)
#     db.session.commit()
#
#     return redirect(url_for("get_users"))

@app.route("/history", methods=['GET'])
def history():
    histories = News.query.order_by(News.id.asc()).all()
    return render_template('history.html', histories=histories)

@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Get form data
        news_text = request.form.get('user_input')
        print(f"user input: {news_text}")
        
        if not news_text:
            raise ValueError("No text provided. Please enter some news text.")

        # Transform the input text using TfidfVectorizer
        # vector_news = tfidf_vectorizer.transform([news_text]).toarray()

        maxlen = 100
        # Tokenize text
        tokenized_text = tokenizer.texts_to_sequences([news_text])
        padded_text = pad_sequences(tokenized_text, maxlen=maxlen)
        
        # Make prediction using the LSTM model
        # prediction = model.predict(vector_news)[0]

        # Predict
        prediction = model.predict(padded_text)
        predicted_class = prediction.argmax()  # Get the class index
        result = 'Berita Palsu' if predicted_class == 1 else 'Berita Asli'

        # Save to the Database
        new_news = News(content=news_text, is_false=predicted_class)
        db.session.add(new_news)
        db.session.commit()
        
        return render_template('index.html', 
                             prediction=predicted_class, 
                             user_input=news_text)
    except Exception as e:
        return jsonify({'error': str(e)})
