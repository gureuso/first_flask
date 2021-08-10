# -*- coding: utf-8 -*-
from flask_login import current_user

from apps.database.models import Cart


def get_carts():
    carts = dict()
    if not current_user.is_authenticated:
        return carts

    cart_list = Cart.query.filter(Cart.user_id == current_user.id).all()
    check_cart_list = []
    for cart in cart_list:
        for cart2 in cart_list:
            if cart.product_id == cart2.product_id:
                if cart.id not in check_cart_list:
                    carts.setdefault(cart.product_id, dict(cnt=0, cart=cart))
                    carts[cart.product_id]['cnt'] += 1
                    check_cart_list.append(cart.id)
    return carts
