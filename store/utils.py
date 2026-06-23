import json

from django.core.exceptions import MultipleObjectsReturned

from .models import Customer, Order, OrderItem, Product


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES["cart"])
    except:
        cart = {}

    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
    cartItems = order["get_cart_items"]

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = product.price * cart[i]["quantity"]

            order["get_cart_total"] += total
            order["get_cart_items"] += cart[i]["quantity"]

            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageURL": product.imageURL,
                    "stock": product.stock,
                    "in_stock": product.in_stock,
                },
                "quantity": cart[i]["quantity"],
                "get_total": total,
            }
            items.append(item)

            if not product.digital:
                order["shipping"] = True
        except:
            pass

    return {"cartItems": cartItems, "order": order, "items": items}


def cartData(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={"name": request.user.username, "email": request.user.email},
        )
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]

    return {"cartItems": cartItems, "order": order, "items": items}


def guestOrder(request, data):
    name = data["form"]["name"]
    email = data["form"]["email"]

    cookieData = cookieCart(request)
    items = cookieData["items"]

    try:
        customer, created = Customer.objects.get_or_create(email=email)
    except MultipleObjectsReturned:
        customer = Customer.objects.filter(email=email).first()
        customer.name = name
        customer.save()
        created = False
    else:
        customer.name = name
        customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item["product"]["id"])

        # Stock validation for guest checkout
        if product.stock is not None and item["quantity"] > product.stock:
            available = max(product.stock, 0)
            if available <= 0:
                continue
            item["quantity"] = available

        OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item["quantity"],
        )

    return customer, order
