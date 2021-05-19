from flask import current_app
from sqlalchemy.orm import relationship
from app import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    registered_at = db.Column(db.DateTime, nullable=True)
    # video = relationship("Rental", back_populates="customer")


    def to_json(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count,
            "registered_at": self.registered_at
        }