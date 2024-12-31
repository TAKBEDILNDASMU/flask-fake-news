from flask import jsonify, render_template, request 
from app import app, db
from app.models import News

@app.route("/")
def index():
    return render_template('index.html', title="index title", prediction=None)
@app.route("/history", methods=['GET'])
def history():
    histories = News.query.order_by(News.id.asc()).all()
    return render_template('history.html', histories=histories)

@app.route("/test", methods=['GET']) 
def test():
    return render_template('user.html')

@app.route("/predict", methods=['POST'])
def predict():
    try:
        data = request.get_json()
        news_text = data['news_text']
        predicted_class = data['predicted_class']
        if predicted_class == "REAL":
            predicted_class = False
        elif predicted_class == "FAKE":
            predicted_class = True

        new_news = News(content=news_text, is_false=predicted_class)
        db.session.add(new_news)
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Prediction saved to database"}), 200
    except Exception as e:
        return jsonify({'error': str(e)})
