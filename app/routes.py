from app import db
import requests
from flask import request, Blueprint, make_response
from flask import jsonify
from .models.customer import Customer
from datetime import datetime
from dotenv import load_dotenv
import os


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")