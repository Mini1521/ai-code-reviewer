from extension import db
from datetime import datetime

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)                #unique ID for each review
    language = db.Column(db.String(10))                         #language name   
    code = db.Column(db.Text)                                   #code snippet    
    review_text = db.Column(db.Text)                            #AI feedback text
    score = db.Column(db.Integer)                               #quality score out of 10
    created_at = db.Column(db.DateTime, default=datetime.utcnow)   #timestamp of creation
