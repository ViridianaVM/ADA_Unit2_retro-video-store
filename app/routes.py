from app import db
import requests
from flask import request, Blueprint, make_response
from flask import jsonify
from sqlalchemy import exc
from .models.customer import Customer
from .models.video import Video
from .models.rental import Rental
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import re


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

"""
Helper functions
"""
def wrong_input(message):
    return {
            "error": message
        }

"""
CRUD for Customer
"""

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    #Reads the HTTP request boby with:
    request_body = request.get_json()
    if len(request_body) == 3:
        new_customer = Customer(name = request_body["name"], postal_code = request_body["postal_code"], phone = request_body["phone"])
        
        db.session.add(new_customer)
        db.session.commit()

        response = {
            "id" : new_customer.customer_id
        }
        return make_response(jsonify(response),201)

    elif ("name" not in request_body) or ("postal_code" not in request_body) or ("phone" not in request_body) or ("videos_checked_out_count" not in request_body):
        return make_response(wrong_input("Invalid data"),400)


@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers_response = []

    customers = Customer.query.all()

    for customer in customers:
        customers_response.append(customer.to_json())
    return jsonify(customers_response), 200


@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_one_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return make_response(customer.to_json(), 200)


@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_rentals_by_customer(customer_id):

    customer = Customer.query.get_or_404(customer_id)

    rentals_by_customer = []
    rentals = db.session.query(Rental)\
        .join(Customer, Customer.customer_id==Rental.customer_id)\
            .join(Video, Video.video_id==Rental.video_id)\
                .filter(Customer.customer_id==customer_id).all()

    for rental in rentals:
        rentals_by_customer.append({
            "title": Video.query.get(rental.video_id).title,
            "release_date": Video.query.get(rental.video_id).release_date,
            "due_date": rental.due_date
        })

    response = jsonify(rentals_by_customer)
    return make_response(response, 200)



@customers_bp.route("/<customer_id>",methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):

    updates_body = request.get_json()
    
    if customer_id is None or updates_body == {}:
        return make_response(jsonify(""),400)

    customer = Customer.query.get_or_404(customer_id)

    customer.name = updates_body["name"]
    customer.postal_code = int(updates_body["postal_code"])
    customer.phone = updates_body["phone"]

    db.session.commit()
    return make_response(customer.to_json(),200)



@customers_bp.route("/<customer_id>",methods=["DELETE"], strict_slashes=False)
def delete_task(customer_id):

    customer = Customer.query.get_or_404(customer_id)

    db.session.delete(customer)
    db.session.commit()

    response = {"id": int(customer_id)}
    return make_response(response,200)



"""
CRUD for Video
"""

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_video():
    #Reads the HTTP request boby with:
    request_body = request.get_json()
    if len(request_body) == 3:
        new_video = Video(title = request_body["title"], release_date = request_body["release_date"], total_inventory = request_body["total_inventory"] )
        
        db.session.add(new_video)
        db.session.commit()

        response = {
            "id" : new_video.video_id
        }
        return make_response(jsonify(response),201)

    elif ("title" not in request_body) or ("release_date" not in request_body) or ("total_inventory" not in request_body):
        return make_response(wrong_input("Invalid data"),400)


@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_videos():
    videos_response = []
    videos = Video.query.all()

    for video in videos:
        videos_response.append(video.to_json())
    return jsonify(videos_response), 200


@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_one_video(video_id):
    video = Video.query.get_or_404(video_id)
    response = video.to_json()
    return make_response(jsonify(response), 200)


@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def get_rentals_by_video(video_id):

    video = Video.query.get_or_404(video_id)

    rentals_by_video = []
    rentals = db.session.query(Rental)\
        .join(Video, Video.video_id==Rental.video_id)\
            .join(Customer, Customer.customer_id==Rental.customer_id)\
                .filter(Video.video_id==video_id).all()

    for rental in rentals:
        rentals_by_video.append({
            "name": Customer.query.get(rental.customer_id).name,
            "phone": Customer.query.get(rental.customer_id).phone,
            "postal_code": Customer.query.get(rental.customer_id).postal_code,
            "due_date": rental.due_date
        })

    response = jsonify(rentals_by_video)
    return make_response(response, 200)


@videos_bp.route("/<video_id>",methods=["PUT"], strict_slashes=False)
def update_video(video_id):

    updates_body = request.get_json()
    try:
        video = Video.query.get_or_404(video_id)
    except exc.SQLAlchemyError as error:
        return make_response(wrong_input("Invalid video id"), 400)

    video.title = updates_body["title"]
    video.release_date = updates_body["release_date"]
    video.total_inventory = updates_body["total_inventory"]

    db.session.commit()
    return make_response(video.to_json(),200)



@videos_bp.route("/<video_id>",methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    
    video = Video.query.get_or_404(video_id)

    db.session.delete(video)
    db.session.commit()

    response = {"id": int(video_id)}
    return make_response(response,200)



"""
CRUD for Rental
"""

@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def create_rental_checkout():
    request_body = request.get_json()

    v_id = request_body["video_id"]
    c_id = request_body["customer_id"]

    try:
        video = Video.query.get_or_404(v_id)
    except exc.SQLAlchemyError as error:
        return make_response(wrong_input("Invalid video id"), 400)
    
    if video.available_inventory == 0:
        return make_response(wrong_input("No inventory available"),400)
    
    try:
        customer = Customer.query.get_or_404(c_id)
    except exc.SQLAlchemyError as error:
        return make_response(wrong_input("Invalid customer id"), 400)

    rental = Rental(customer_id=c_id, video_id=v_id)

    customer.videos_checked_out_count += 1
    if video.available_inventory > 0:
        video.available_inventory -= 1

    db.session.add(rental)
    db.session.commit()

    response = {
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "due_date": rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }

    return make_response(jsonify(response),200)


@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def create_rental_checkin():
    request_body = request.get_json()
    v_id = request_body["video_id"]
    c_id = request_body["customer_id"]

    try:
        video = Video.query.get_or_404(v_id)
    except exc.SQLAlchemyError as error:
        return make_response(wrong_input("Invalid video id"), 400)

    try:
        customer = Customer.query.get_or_404(c_id)
    except exc.SQLAlchemyError as error:
        return make_response(wrong_input("Invalid customer id"), 400)

    #https://programmersought.com/article/18362593970/
    rental = db.session.query(Rental)\
                .filter(Rental.customer_id==c_id, Rental.video_id==v_id).first()
    if rental == None:
        return make_response(wrong_input("Rental not fount"),400)

    customer.videos_checked_out_count -= 1
    video.available_inventory += 1

    db.session.delete(rental)
    db.session.commit()

    response = {
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }
    return make_response(jsonify(response),200)

