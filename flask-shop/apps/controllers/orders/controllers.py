from flask import Blueprint, render_template

from apps.common.auth import signin_required
from apps.controllers.carts import get_carts
from apps.controllers.orders import get_orders
from apps.database.models import Category

app = Blueprint('orders', __name__, url_prefix='/orders')


@app.route('', methods=['GET'])
@signin_required
def index():
    categories = Category.query.all()
    return render_template('orders/index.html', carts=get_carts(), categories=categories, orders=get_orders())
