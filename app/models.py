from app import db

class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each news item
    content = db.Column(db.Text, nullable=False)  # Stores the news content
    is_false = db.Column(db.Boolean, default=False, nullable=False)  # Indicates if the news is fake or real

    def __init__(self, content, is_false) -> None:
        self.content = content
        self.is_false = is_false

    def __repr__(self):
        return f"<News id={self.id}, is_false={self.is_false}>"

