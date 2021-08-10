from flask import Blueprint, request

from apps.common.response import ok
from apps.database.models import Product

app = Blueprint('apis_products', __name__, url_prefix='/apis/products')


@app.route('', methods=['GET'])
def products():
    return ok()

