from models import Review, db

def save_review(language, code, review_text, score):
    review = Review(language=language, code=code, review_text=review_text, score=score )
    db.session.add(review)
    db.session.commit()
    return review

def get_all_reviews():
    """Retrieve all stored reviews."""
    return Review.query.order_by(Review.created_at.desc()).all()


def get_review_by_id(review_id):
    return Review.query.get(review_id)

def get_reviews():
    return Review.query.order_by(Review.created_at.desc()).all()

def delete_review(review_id):
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    return False

