from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from product.models import Product
from django.db.models import Value, F

def _get_total_cart_price(request):
    cart_content = request.session.get('cart')
    total_cart_price = 0
    if cart_content:
        products_ids = cart_content.keys()
        products = Product.objects.filter(id__in=products_ids)

        for prod in products:
            quantity = cart_content.get(str(prod.id),0)
            total_cart_price += (prod.final_price * quantity)
    return total_cart_price


def _get_total_product_price(request, prod_id):
    cart_content = request.session.get('cart')
    p_id = str(prod_id)
    quantity = cart_content.get(p_id)
    if not quantity:
        return 0
    
    try:
        product = Product.objects.get(id=prod_id)
        return product.final_price * quantity
    except Product.DoesNotExist:
        return 0
    



def view_cart(request):
    cart_content = request.session.get('cart')
    if not cart_content:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'products': [],
                'total_cart_price': 0,
                'total_cart_quantity': 0,
            })
        return render(request, 'cart/cart.html', {'products': [], 'total_cart_price': 0})
    


    products_ids = cart_content.keys()
    products = Product.objects.filter(id__in=products_ids)


    total_cart_price = 0
    json_products = []

    for prod in products:
        qty = cart_content.get(str(prod.id), 0)
        prod.cart_quantity = qty
        prod.total_product_price = prod.final_price * qty
        total_cart_price += prod.total_product_price
        

        json_products.append({
            'id': prod.id,
            'discount': prod.discount,
            'title': prod.title,
            'final_price': float(prod.final_price),
            'price': float(prod.price),
            'description': prod.description,
            'qty': qty,
            'total': float(prod.total_product_price),
            'img': prod.img.url if prod.img else '/static/images/products/product-default-img.png',
        })

        total_cart_quantity = sum(cart_content.values(), 0)


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'products': json_products,
            'total_cart_price': float(total_cart_price),
            'total_cart_quantity': total_cart_quantity,
        })
    return render(request, 'cart/cart.html', {'products': products, 'total_cart_price': total_cart_price})



def add_cart(request, product_id):
    status = 'empty'

    try:
        product = Product.objects.get(id=product_id)
    except (Product.DoesNotExist, ValueError):
        product_id = 0
    
    if product_id == 0:
        return JsonResponse(data={"status": status})
    

    
    p_id = str(product_id)

    # create cart dict if does not exist
    cart = request.session.get('cart', {})
    if not cart:
        request.session.set_expiry(6480000)
    if p_id in cart:
        cart[p_id] += 1
    else:
        cart[p_id] = 1


    # update the cart in the session
    request.session['cart'] = cart
    request.session.modified = True
    

    status = 'success'
    item_quantity = cart[p_id]

    total_cart_price = _get_total_cart_price(request)
    total_product_price = _get_total_product_price(request, product_id)
    return JsonResponse({
        "status": status,
        "item_quantity": item_quantity,
        "total_cart_quantity": sum(cart.values()),
        'total_cart_price': total_cart_price,
        'total_product_price': total_product_price
    }
    )


def delete_cart(request, product_id):
    cart = request.session.get('cart', {})
    p_id = str(product_id)
    
    if p_id in cart:
        del cart[p_id] # The product has been completely removed from the dictionary.
        request.session['cart'] = cart
        request.session.modified = True
        
    return JsonResponse({
        "status": "success",
        "total_cart_quantity": sum(cart.values(), 0)
    })


def minus_cart(request, product_id):
    cart = request.session.get('cart', {})
    p_id = str(product_id)
    
    if p_id in cart:
        if cart[p_id] > 1:
            cart[p_id] -= 1 # Just reduce the quantity
        else:
            del cart[p_id] # If it's 1 and press minus, delete the product.
            
    request.session['cart'] = cart
    request.session.modified = True
    
    total_cart_price = _get_total_cart_price(request)
    total_product_price = _get_total_product_price(request, product_id)
    return JsonResponse({
        "status": "success",
        "item_quantity": cart.get(p_id, 0),
        "total_cart_quantity": sum(cart.values(), 0),
        'total_cart_price': total_cart_price,
        'total_product_price': total_product_price,
    })
