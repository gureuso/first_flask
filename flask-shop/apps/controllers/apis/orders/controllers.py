from datetime import datetime

from flask import Blueprint, request
from flask_login import current_user

from apps.common.auth import api_signin_required
from apps.common.response import ok, error
from apps.database.models import Order, Delivery, Product, Cart
from apps.database.session import db

app = Blueprint('apis_orders', __name__, url_prefix='/apis/orders')


@app.route('', methods=['POST'])
@api_signin_required
def create_order():
    return ok()
