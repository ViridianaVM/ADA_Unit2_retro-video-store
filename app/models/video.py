from flask import current_app
from app import db
from datetime import datetime
from sqlalchemy.orm import backref, relationship


#This function is used to default an attribute to the value of another attribute
def default_available_inventory(context):
    return context.get_current_parameters()['total_inventory']


class Video(db.Model):
    __tablename__ = "videos"
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer, default = 0)
    available_inventory = db.Column(db.Integer, default = default_available_inventory)
    customer = db.relationship("Rental", backref="video", lazy=True)
    

    def to_json(self):
        return{
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }