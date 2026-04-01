def cart_total_quantity(request):
    cart = request.session.get('cart', {})
    
    total_quantity = sum(cart.values())
    
    return {
        'global_cart_total': total_quantity
    }