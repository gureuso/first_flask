from flask import Blueprint, request
from flask_login import current_user

from apps.common.auth import api_signin_required
from apps.common.response import ok, error
from apps.database.models import Product, Cart
from apps.database.session import db

app = Blueprint('apis_carts', __name__, url_prefix='/apis/carts')


@app.route('', methods=['POST'])
@api_signin_required
def create_cart():
    form = request.form
    product_id = form['product_id']

    product = Product.query.filter(Product.id == product_id).first()
    if not product:
        return error(40000)

    cart = Cart(product_id=product_id, user_id=current_user.id)
    db.session.add(cart)
    db.session.commit()
    return ok()
