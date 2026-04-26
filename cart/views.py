from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
from django.http import HttpResponse
import json
import uuid

from .models import Cart, CartItem, Order, OrderItem
from .paystack import get_paystack_service
from store.models import Product

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def cart_detail(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required(login_url='/accounts/login/')
@require_POST
def add_to_cart(request):
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body or '{}')
        except json.JSONDecodeError:
            data = {}
    else:
        data = request.POST

    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1) or 1)
    
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity},
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse(
        {
            "success": True,
            "message": "Product added to cart",
            "cart_items": cart.get_total_items(),
            "cart_total": float(cart.get_total_price()),
        }
    )

@require_POST
def update_cart(request, item_id):
    """
    Update the quantity of an item in the cart.

    The frontend sends JSON, but we also support form-encoded data.
    """
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body or '{}')
        except json.JSONDecodeError:
            data = {}
        quantity = int(data.get('quantity', 1) or 1)
    else:
        quantity = int(request.POST.get('quantity', 1) or 1)
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()

    return JsonResponse(
        {
            "success": True,
            "cart_items": cart.get_total_items(),
            "cart_total": float(cart.get_total_price()),
        }
    )

def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    
    # If this is an AJAX / fetch call (e.g. DELETE from main.js), always return JSON
    if request.method == "DELETE" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "success": True,
                "cart_items": cart.get_total_items(),
                "cart_total": float(cart.get_total_price()),
            }
        )

    messages.success(request, "Item removed from cart")
    return redirect("cart:cart_detail")

def checkout(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product')
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        shipping_name = request.POST.get('shipping_name')
        shipping_email = request.POST.get('shipping_email')
        shipping_phone = request.POST.get('shipping_phone')
        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')
        shipping_state = request.POST.get('shipping_state')
        shipping_postal_code = request.POST.get('shipping_postal_code')
        shipping_country = request.POST.get('shipping_country')
        notes = request.POST.get('notes', '')

        if not (shipping_name and shipping_email and shipping_address and shipping_city and shipping_country):
            messages.error(request, 'Please fill in all required shipping details.')
        else:
            with transaction.atomic():
                subtotal = cart.get_total_price()
                tax_amount = 0
                shipping_amount = 0
                total_amount = subtotal + tax_amount + shipping_amount

                order_number = uuid.uuid4().hex[:10].upper()

                order = Order.objects.create(
                    order_number=order_number,
                    user=request.user if request.user.is_authenticated else None,
                    status='pending',
                    subtotal=subtotal,
                    tax_amount=tax_amount,
                    shipping_amount=shipping_amount,
                    total_amount=total_amount,
                    shipping_name=shipping_name,
                    shipping_email=shipping_email,
                    shipping_phone=shipping_phone,
                    shipping_address=shipping_address,
                    shipping_city=shipping_city,
                    shipping_state=shipping_state,
                    shipping_postal_code=shipping_postal_code,
                    shipping_country=shipping_country,
                    notes=notes,
                )

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.get_display_price(),
                    )

                cart.items.all().delete()

            messages.success(request, f'Order {order_number} placed successfully!')
            return redirect('cart:order_confirmation', order_number=order_number)
    
    profile = getattr(request.user, "profile", None) if request.user.is_authenticated else None

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'profile': profile,
    }
    return render(request, 'cart/checkout.html', context)


def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order_number': order_number,
    }
    return render(request, 'cart/order_confirmation.html', context)


@login_required(login_url='/accounts/login/')
def payment_page(request):
    """Page showing payment options (M-Pesa or Card)"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product')
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        shipping_name = request.POST.get('shipping_name')
        shipping_email = request.POST.get('shipping_email')
        shipping_phone = request.POST.get('shipping_phone')
        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')
        shipping_state = request.POST.get('shipping_state')
        shipping_postal_code = request.POST.get('shipping_postal_code')
        shipping_country = request.POST.get('shipping_country')
        notes = request.POST.get('notes', '')
        
        if not (shipping_name and shipping_email and shipping_address and shipping_city and shipping_country):
            messages.error(request, 'Please fill in all required details.')
            return redirect('cart:payment_page')
        
        request.session['shipping_info'] = {
            'shipping_name': shipping_name,
            'shipping_email': shipping_email,
            'shipping_phone': shipping_phone,
            'shipping_address': shipping_address,
            'shipping_city': shipping_city,
            'shipping_state': shipping_state,
            'shipping_postal_code': shipping_postal_code,
            'shipping_country': shipping_country,
            'notes': notes,
        }
        
        return redirect('cart:initiate_payment')
    
    profile = getattr(request.user, "profile", None) if request.user.is_authenticated else None
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'profile': profile,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'cart/payment.html', context)


@login_required(login_url='/accounts/login/')
def initiate_payment(request):
    """Initialize PayStack payment"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product')
    
    if not cart_items.exists():
        return redirect('cart:cart_detail')
    
    shipping_info = request.session.get('shipping_info', {})
    if not shipping_info:
        messages.error(request, 'Please fill in your delivery details first.')
        return redirect('cart:payment_page')
    
    total = float(cart.get_total_price())
    
    if total <= 0:
        messages.error(request, 'Invalid order amount')
        return redirect('cart:cart_detail')
    
    order_number = uuid.uuid4().hex[:10].upper()
    
    request.session['pending_order'] = {
        'order_number': order_number,
        'cart_data': [
            {
                'product_id': item.product.id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': float(item.product.get_display_price()),
            }
            for item in cart_items
        ],
        'total': total,
    }
    
    paystack = get_paystack_service()
    
    if settings.PAYSTACK_SECRET_KEY:
        callback_url = request.build_absolute_uri('/cart/payment/callback/')
        
        result = paystack.initialize_transaction(
            email=shipping_info.get('shipping_email'),
            amount=total,
            reference=order_number,
            callback_url=callback_url,
            metadata={
                'order_number': order_number,
                'shipping_info': shipping_info,
            }
        )
        
        if result.get('success'):
            return redirect(result['authorization_url'])
    
    messages.warning(request, 'Online payment is currently unavailable. Please use manual payment methods.')
    return redirect('cart:manual_order_create')


@login_required(login_url='/accounts/login/')
def payment_callback(request):
    """Handle PayStack payment callback"""
    reference = request.GET.get('reference')
    
    if not reference:
        messages.error(request, 'Invalid payment reference')
        return redirect('cart:payment_page')
    
    paystack = get_paystack_service()
    result = paystack.verify_transaction(reference)
    
    pending_order = request.session.get('pending_order', {})
    
    if result.get('success'):
        shipping_info = request.session.get('shipping_info', {})
        
        with transaction.atomic():
            order = Order.objects.create(
                order_number=pending_order.get('order_number', reference),
                user=request.user,
                status='paid',
                subtotal=pending_order.get('total', 0),
                tax_amount=0,
                shipping_amount=0,
                total_amount=pending_order.get('total', 0),
                shipping_name=shipping_info.get('shipping_name', ''),
                shipping_email=shipping_info.get('shipping_email', ''),
                shipping_phone=shipping_info.get('shipping_phone', ''),
                shipping_address=shipping_info.get('shipping_address', ''),
                shipping_city=shipping_info.get('shipping_city', ''),
                shipping_state=shipping_info.get('shipping_state', ''),
                shipping_postal_code=shipping_info.get('shipping_postal_code', ''),
                shipping_country=shipping_info.get('shipping_country', ''),
                notes=shipping_info.get('notes', ''),
            )
            
            for item_data in pending_order.get('cart_data', []):
                product = Product.objects.get(id=item_data['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item_data['quantity'],
                    price=item_data['price'],
                )
        
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        
        if 'pending_order' in request.session:
            del request.session['pending_order']
        if 'shipping_info' in request.session:
            del request.session['shipping_info']
        
        messages.success(request, f'Payment successful! Order {order.order_number} has been placed.')
        return redirect('cart:order_confirmation', order_number=order.order_number)
    
    messages.error(request, 'Payment verification failed. Please try again or use manual payment.')
    return redirect('cart:payment_page')


@login_required(login_url='/accounts/login/')
def manual_order_create(request):
    """Create order without online payment"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product')
    
    if not cart_items.exists():
        return redirect('cart:cart_detail')
    
    shipping_info = request.session.get('shipping_info', {})
    
    if not shipping_info:
        messages.error(request, 'Please fill in your delivery details first.')
        return redirect('cart:payment_page')
    
    with transaction.atomic():
        order_number = uuid.uuid4().hex[:10].upper()
        
        order = Order.objects.create(
            order_number=order_number,
            user=request.user,
            status='pending_payment',
            subtotal=cart.get_total_price(),
            tax_amount=0,
            shipping_amount=0,
            total_amount=cart.get_total_price(),
            shipping_name=shipping_info.get('shipping_name', ''),
            shipping_email=shipping_info.get('shipping_email', ''),
            shipping_phone=shipping_info.get('shipping_phone', ''),
            shipping_address=shipping_info.get('shipping_address', ''),
            shipping_city=shipping_info.get('shipping_city', ''),
            shipping_state=shipping_info.get('shipping_state', ''),
            shipping_postal_code=shipping_info.get('shipping_postal_code', ''),
            shipping_country=shipping_info.get('shipping_country', ''),
            notes=shipping_info.get('notes', ''),
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_display_price(),
            )
        
        cart.items.all().delete()
    
    if 'shipping_info' in request.session:
        del request.session['shipping_info']
    if 'pending_order' in request.session:
        del request.session['pending_order']
    
    messages.success(request, f'Order {order_number} created! Please complete payment to confirm.')
    return redirect('cart:order_confirmation', order_number=order_number)
