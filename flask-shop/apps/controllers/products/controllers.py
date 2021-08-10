from flask import Blueprint, render_template

from apps.controllers.carts import get_carts
from apps.controllers.orders import get_orders
from apps.database.models import Category, Product

app = Blueprint('product', __name__, url_prefix='/products')


@app.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    categories = Category.query.all()
    product = Product.query.filter(Product.id == product_id).first()
    return render_template('product/detail.html', categories=categories, product=product, orders=get_orders(), carts=get_carts())
