from flask import Blueprint, request, jsonify
from services.llm_service import analyze_code
from models import Review
from services.review_service import get_all_reviews, get_review_by_id
from datetime import datetime
from extension import db

review_bp = Blueprint('review_bp', __name__)                #blueprint for all review-related routes is created

@review_bp.route('/api/review', methods=['POST'])           #REVIEW CREATED
def create_review():                                        #POST request to create a new code review
    data = request.get_json()                               #JSON data from frontend extracted
    language = data.get('language')
    code = data.get('code')

    if not language or not code:                            #user input validated
        return jsonify({'error': 'Language and code are required.'}), 400

    result = analyze_code(language, code)                   #code and language sent to OpenAI model for analysis
    review = result.get("review", "No review generated.")
    score = result.get("score", 0)

    new_review = Review(                                    #save the review into the database
        language=language,
        code=code,
        review_text=review,
        score=score,
        created_at=datetime.utcnow()
    )
    db.session.add(new_review)
    db.session.commit()

    return jsonify({                                        #review sent back to the frontend as JSON response
        'id': new_review.id,
        'language': new_review.language,
        'code': new_review.code,
        'review_text': new_review.review_text,
        'score': new_review.score,
        'created_at': new_review.created_at.isoformat()
    }), 201


@review_bp.route('/api/reviews', methods=['GET'])           #GET ALL REVIEWS
def get_reviews():                                          #all reviews stored in database retrieved
    """Return all stored reviews."""
    reviews = Review.query.order_by(Review.created_at.desc()).all() #reviews ordered by creation date, most recent first
    return jsonify([                                        #review objects converted to JSONS
        {
            'id': r.id,
            'language': r.language,
            'code': r.code,
            'review_text': r.review_text,
            'score': r.score,
            'created_at': r.created_at.isoformat()
        } for r in reviews
    ])


@review_bp.route('/api/review/<int:review_id>', methods=['GET']) #GET REVIEW BY ID
def get_review(review_id):                                  #fetch a speific review by using its unique ID
    r = get_review_by_id(review_id)                         #try to find the review by ID   
    if not r:
        return jsonify({'error': 'Review not found.'}), 404

    return jsonify({                                        #return the review as JSON    
        'id': r.id, 
        'language': r.language,
        'code': r.code,
        'review_text': r.review_text,
        'score': r.score,
        'created_at': r.created_at
    })

@review_bp.route('/api/review/<int:review_id>', methods=['DELETE']) #DELETE REVIEW BY ID
def delete_review(review_id):                               #delete specific review by its ID
    review = Review.query.get(review_id) 
    if not review:
        return jsonify({"error": "Review not found."}), 404

    db.session.delete(review)                               #review removed from the database
    db.session.commit()
    return jsonify({"message": f"Review {review_id} deleted."}), 200


@review_bp.route("/api/reviews", methods=["DELETE"])        #DELETE ALL REVIEWS
def delete_all():                                           #delete all reviews from the database
    reviews = Review.query.all()
    for r in reviews:
        db.session.delete(r)
    db.session.commit()
    return jsonify({"message": f"Deleted {len(reviews)} reviews."}), 200 #return count of deleted reviews
