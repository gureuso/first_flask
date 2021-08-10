from flask import Blueprint, render_template

from apps.controllers.carts import get_carts
from apps.controllers.orders import get_orders
from apps.database.models import Category, Product

app = Blueprint('category', __name__, url_prefix='/categories')


@app.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    categories = Category.query.all()
    category = Category.query.filter(Category.id == category_id).first()
    products = Product.query.filter(Product.category_id == category_id).order_by(Product.id.desc()).limit(12).all()
    return render_template('category/detail.html', categories=categories, products=products, category=category,
                           orders=get_orders(), carts=get_carts())
