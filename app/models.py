from . import db


class House(db.Model):
    __tablename__ = "houses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    square = db.Column(db.Integer, nullable=False)
    area = db.Column(db.String(20), nullable=False)
    price_base = db.Column(db.Integer, nullable=False)
    price_with_communications = db.Column(db.Integer)
    price_ready = db.Column(db.Integer)
    mortgage_price_per_month = db.Column(db.Integer)

    images = db.relationship(
        "HouseImage",
        back_populates="house",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<House {self.id} {self.title}>"


class HouseImage(db.Model):
    __tablename__ = "house_images"

    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(
        db.Integer,
        db.ForeignKey(House.id, ondelete="CASCADE"),
        nullable=False,
    )
    image_url = db.Column(db.String(512), nullable=False)

    house = db.relationship("House", back_populates="images")

    def __repr__(self):
        return f"<HouseImage {self.id} {self.image_url}>"
