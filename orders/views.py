from django.shortcuts import render, redirect
from orders.models import Order, OrderItem, OrderStatus
from product.models import Product
from wallet.models import Transaction, Wallet, TransactionType
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import CheckOutForm
from django_ratelimit.decorators import ratelimit


@login_required
@ratelimit(key="user", method='POST', rate='5/m', block=True)
@transaction.atomic
def checkout(request):

    # 2 - check if the user has a wallet
    if not hasattr(request.user, "wallet"):
        return redirect('wallet:wallet_url', username=request.user.username)
    

    # 3 - check if there are products in the cart
    cart_content = request.session.get('cart', {})
    if not cart_content:
        messages.error(request, 'The cart is empty')
        return redirect('cart:cart_view_url')
    

    if request.method == "POST":

        form = CheckOutForm(request.POST)
        if form.is_valid():
            
            #[1] - get the wallet number and the password (from the form)
            wallet_number = form.cleaned_data.get('wallet_number')
            password = form.cleaned_data.get('password')
        


            #[2] - get wallet and check if its his own wallet
            try:
                wallet = Wallet.objects.select_for_update().get(user=request.user, wallet_number=wallet_number)
            except Wallet.DoesNotExist:
                form.add_error('__all__', "The wallet number or password is incorrect.!")
                return render(request, 'orders/checkout_form.html', {"form": form})


            #[3] - check if the password is correct
            if not request.user.check_password(password):
                form.add_error('__all__', "The wallet number or password is incorrect.!")
                return render(request, 'orders/checkout_form.html', {"form": form})
            


            #[4] - get products
            products_id = cart_content.keys()
            products = Product.objects.select_for_update().filter(id__in=products_id)


        
            #[5] - for get total price and total quantity in cart
            total_cart_price = 0
            total_cart_quantity = 0
            order_items_to_create = []



            #[6] - calculate total price & quantity .. and make order items to add it in OrderItem model
            for prod in products:
                p_id = str(prod.id)
                qty = int(cart_content.get(p_id, 0))

                item_price = prod.final_price * qty
                total_cart_price += item_price
                total_cart_quantity += qty

                order_items_to_create.append(OrderItem(
                    product=prod,
                    quantity=qty,
                    price_at_purchase=prod.final_price
                ))



            #[7] - check if there is a balance
            if wallet.balance < total_cart_price:
                messages.error(request, 'Insufficient balance!')
                return redirect('cart:cart_view_url')
        



            #[8] - create the order
            order = Order.objects.create(
                user=request.user,
                total_price=total_cart_price,
                total_quantity=total_cart_quantity,
                is_paid=True,
                status=OrderStatus.Pending,
            )

        

            #[9] - add products to OrderItem
            for item in order_items_to_create:
                item.order = order
            OrderItem.objects.bulk_create(order_items_to_create)


            #[10] - Deduct the price from the wallet    
            wallet.balance -= total_cart_price
            wallet.save()


            #[11] - make the transaction
            Transaction.objects.create(
                wallet=wallet,
                amount=total_cart_price,
                transaction_type=TransactionType.Purchase,
                description=f"Purchase for Order: #{order.id}"
            )



            #[12] - clear the cart
            request.session['cart'] = {}
            request.session.modified = True



            messages.info(request, 'Your purchase was completed successfully')
            return redirect('cart:cart_view_url')
    
    else:
        form = CheckOutForm()
    return render(request, 'orders/checkout_form.html', {"form": form})




    
