# -*- coding: utf-8 -*-
from flask_login import current_user

from apps.database.models import Order


def get_orders():
    orders = dict()
    if not current_user.is_authenticated:
        return orders

    order_list = Order.query.filter(Order.user_id == current_user.id).all()
    check_product_list = dict()
    for order in order_list:
        orders.setdefault(order.created_at, [])
        check_product_list.setdefault(order.created_at, [])
        if order.product in check_product_list[order.created_at]:
            for product in orders[order.created_at]:
                if product['id'] == order.product.id:
                    product['cnt'] += 1
        else:
            orders[order.created_at].append(dict(id=order.product.id, cnt=1, price=order.product.price, name=order.product.name))
        check_product_list[order.created_at].append(order.product)
    return orders
