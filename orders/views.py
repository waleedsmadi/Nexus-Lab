from django.shortcuts import render, redirect
from orders.models import Order, OrderItem, OrderStatus
from product.models import Product
from wallet.models import Transaction, Wallet, TransactionType
from accounts.models import AbstractUser
from django.db import transaction
from django.contrib.auth.decorators import login_required
from cart.views import _get_total_cart_price
from django.contrib import messages


@login_required
@transaction.atomic
def checkout(request):
    # 1 - get the cart
    cart_content = request.session.get('cart', {})
    if not cart_content:
        messages.error(request, 'The cart is empty')
        return redirect('cart:cart_view_url')
    


    # 2 - get wallet
    wallet = Wallet.objects.select_for_update().get(user=request.user)



    # 3 - get products
    products_id = cart_content.keys()
    products = Product.objects.select_for_update().filter(id__in=products_id)


    
    # 4 - for get total price and total quantity in cart
    total_cart_price = 0
    total_cart_quantity = 0
    order_item_to_create = []



    # 5 calculate total price & quantity .. and make order items to add it in OrderItem model
    for prod in products:
        p_id = str(prod.id)
        qty = int(cart_content.get(p_id, 0))

        item_price = prod.final_price * qty
        total_cart_price += item_price
        total_cart_quantity += qty

        order_item_to_create.append({
            'product': prod,
            'quantity': qty,
            'price': prod.final_price
        })



    # 6 - check if there is a balance
    if wallet.balance < total_cart_price:
        messages.error(request, 'Insufficient balance!')
        return redirect('cart:cart_view_url')
    



    # 7 - create the order
    order = Order.objects.create(
        user=request.user,
        total_price=total_cart_price,
        total_quantity=total_cart_quantity,
        is_paid=True,
        status=OrderStatus.Pending,
    )

    

    # 8 - add products to OrderItem
    for item in order_item_to_create:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price_at_purchase=item['price']
        )

    # 9 - Deduct the price from the wallet    
    wallet.balance -= total_cart_price
    wallet.save()


    # 10 - make the transaction
    Transaction.objects.create(
        wallet=wallet,
        amount=total_cart_price,
        transaction_type=TransactionType.Purchase,
        description=f"Purchase for Order: #{order.id}"
    )



    # 11 - clear the cart
    request.session['cart'] = {}
    request.session.modified = True



    messages.info(request, 'Your purchase was completed successfully')
    return redirect('cart:cart_view_url')





    
