from flask import current_app
from app import db
from datetime import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey("videos.video_id"), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"), primary_key=True)
    due_date = db.Column(db.DateTime, nullable=False)
    # video = relationship("Video", back_populates="customer")
    # customer = relationship("Customer", back_populates="video")