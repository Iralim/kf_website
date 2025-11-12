from flask import Blueprint, render_template, redirect

from app import db
from app.models import House
from app.forms import HouseForm
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    houses = House.query.all()
    return render_template('index.html',houses=houses)

@main_bp.route('/details/<int:id>')
def details(id):
    house = House.query.get(id)
    return render_template('details.html', house=house)

@main_bp.route('/admin/')
def admin():
    houses = House.query.all()
    form = HouseForm()
    return render_template('admin.html', houses=houses, form=form)

@main_bp.route('/admin/add_house', methods=['POST'])
def add_house():
    form = HouseForm()
    print(f"===!!!=== {form.area}")
    new_house = House(
        title=form.title.data,
        description=form.description.data,
        square=form.square.data,
        area=form.area.data,
        price_base=form.price_base.data,
        price_with_communications=form.price_with_communications.data,
        price_ready=form.price_ready.data,
        mortgage_price_per_month=form.mortgage_price_per_month.data
    )

    db.session.add(new_house)
    db.session.commit()
    return redirect('/admin/')


