from flask import Blueprint, send_from_directory, render_template

from apps.controllers.carts import get_carts
from apps.controllers.orders import get_orders
from apps.database.models import Category, Product
from config import Config

app = Blueprint('index', __name__, url_prefix='/')


@app.route('/', methods=['GET'])
def index():
    categories = Category.query.all()
    products = Product.query.order_by(Product.id.desc()).limit(12).all()
    return render_template('main/index.html', categories=categories, products=products, orders=get_orders(), carts=get_carts())


@app.route('favicon.ico')
def favicon():
    return send_from_directory(Config.STATIC_DIR, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
