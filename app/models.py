from . import db
from datetime import datetime

class House(db.Model):
    __tablename__ = "houses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    square = db.Column(db.Float, nullable=False)
    area = db.Column(db.Float, nullable=False)
    price_base = db.Column(db.Float, nullable=False)
    price_with_communications = db.Column(db.Float)
    price_ready = db.Column(db.Float)
    mortgage_price_per_month = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship(
        "HouseImage",
        back_populates="house",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<House {self.id} {self.title}>"

class HouseImage(db.Model):
    __tablename__ = "houses_images"

    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(
        db.Integer,
        db.ForeignKey("houses.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    image_url = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    house = db.relationship("House", back_populates="images")

    def __repr__(self):
        return f"<HouseImage {self.id} {self.image_url}>"