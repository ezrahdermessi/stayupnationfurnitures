from .models import Cart

def cart(request):
    cart = None
    cart_items = 0
    cart_total = 0
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    if cart:
        cart_items = cart.get_total_items()
        cart_total = cart.get_total_price()
    
    return {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }