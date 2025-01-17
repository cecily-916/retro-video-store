# Import necessary packages
from typing import NewType
from flask import Blueprint, json, jsonify, request, make_response
from flask_sqlalchemy import _make_table
from app import db
from app.models.rental import Rental
from app.models.video import Video
from app.models.customer import Customer


# Create Blueprint for rentals

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# ----------------------------------------
# ----------- RENTALS ENDPOINTS ----------
# ----------------------------------------

# POST rentals/check-out should:
# create a rental for the specific video and customer.
# create a due date. The rental's due date is the seven days from the current date.

@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video():
    request_body = request.get_json()
    
    # Existence check
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer id"}, 400
    elif "video_id" not in request_body:
        return {"details": "Request body must include video id"}, 400

    # Validity check
    try:
        customer = Customer.query.get(request_body["customer_id"])
        video = Video.query.get(request_body["video_id"])
        if not customer or not video:
            return {"details": "Customer or video not found"}, 404
    except:
        return "Invalid input", 404
    
    if video.videos_checked_out_count() == video.total_inventory:
        return jsonify({
            "message": "Could not perform checkout"
        }), 400

    new_rental = Rental(
        customer_id=customer.id,
        video_id=video.id,
        checked_out=True
        )

    db.session.add(new_rental)
    db.session.commit()

    response_body = {
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": video.videos_checked_out_count(),
        "available_inventory": video.available_inventory()        
    }

    return response_body, 200

@rentals_bp.route("/check-in", methods=["POST"])
def check_in_video():
    """
    The approach here was similar to that of a PUT method because we 
    are updating the rental so that it is no longer considered during 
    the check-out count and teh available inventory reflects these 
    changes as well.
    """
    request_body = request.get_json()

    if "customer_id" not in request_body:
        return {"details": "Request body must include customer id"}, 400
    elif "video_id" not in request_body:
        return {"details": "Request body must include video id"}, 400

    try:
        customer = Customer.query.get(request_body["customer_id"])
        video = Video.query.get(request_body["video_id"])
        if not customer or not video:
            return {"details": "Customer or video not found"}, 404
    except:
        return "Invalid input", 404

    try:
        rental = Rental.query.filter_by(customer_id=customer.id, video_id=video.id).first()
        if not rental:
            return {"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}, 400
    except:
        return {"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}, 400

    
    rental.customer_id = customer.id
    rental.video_id = video.id
    rental.checked_out=False

    db.session.commit()

    response_body = {
        "customer_id": rental.customer_id,
        "video_id": rental.video_id,
        "videos_checked_out_count": video.videos_checked_out_count(),
        "available_inventory": video.available_inventory()        
    }

    return response_body, 200