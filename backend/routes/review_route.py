from flask import Blueprint, request, jsonify
from services.llm_service import analyze_code
from models import Review
from services.review_service import get_all_reviews, get_review_by_id
from datetime import datetime
from extension import db

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/api/review', methods=['POST'])
def create_review():
    data = request.get_json()
    language = data.get('language')
    code = data.get('code')

    if not language or not code:
        return jsonify({'error': 'Language and code are required.'}), 400

    result = analyze_code(language, code)
    review = result.get("review", "No review generated.")
    score = result.get("score", 0)

     #save the review into the database
    new_review = Review(
        language=language,
        code=code,
        review_text=review,
        score=score,
        created_at=datetime.utcnow()
    )
    db.session.add(new_review)
    db.session.commit()

    return jsonify({
        'id': new_review.id,
        'language': new_review.language,
        'code': new_review.code,
        'review_text': new_review.review_text,
        'score': new_review.score,
        'created_at': new_review.created_at.isoformat()
    }), 201


@review_bp.route('/api/reviews', methods=['GET'])
def get_reviews():
    """Return all stored reviews."""
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return jsonify([
        {
            'id': r.id,
            'language': r.language,
            'code': r.code,
            'review_text': r.review_text,
            'score': r.score,
            'created_at': r.created_at.isoformat()
        } for r in reviews
    ])


@review_bp.route('/api/review/<int:review_id>', methods=['GET'])
def get_review(review_id):
    """Get a specific review by ID."""
    r = get_review_by_id(review_id)
    if not r:
        return jsonify({'error': 'Review not found.'}), 404

    return jsonify({
        'id': r.id,
        'language': r.language,
        'code': r.code,
        'review_text': r.review_text,
        'score': r.score,
        'created_at': r.created_at
    })

@review_bp.route('/api/review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found."}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": f"Review {review_id} deleted."}), 200

