from django import template

register = template.Library()

@register.filter
def cart_total(carrito):
    """
    Calcula el total del carrito sumando el precio por la cantidad de cada producto.
    """
    return sum(item['precio'] * item['cantidad'] for item in carrito.values())