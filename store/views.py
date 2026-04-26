from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json

from .models import Product, Category, Review, NewsletterSubscription, Decoration

def home(request):
    featured_products = Product.objects.filter(featured=True, is_active=True)[:8]
    new_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories = Category.objects.filter(is_active=True, parent=None)[:6]
    
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query)
        )
    
    # Price filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['price', '-price', 'name', '-name', '-created_at']:
        products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'category_slug': category_slug,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def decoration_list(request):
    decorations = Decoration.objects.filter(is_active=True)
    paginator = Paginator(decorations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'store/decoration_list.html', context)


def decoration_detail(request, slug):
    decoration = get_object_or_404(Decoration, slug=slug, is_active=True)
    related_decorations = Decoration.objects.filter(is_active=True).exclude(id=decoration.id)[:4]

    context = {
        'decoration': decoration,
        'related_decorations': related_decorations,
    }
    return render(request, 'store/decoration_detail.html', context)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'store/category.html', context)

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'results_count': products.count(),
    }
    return render(request, 'store/search.html', context)

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save to database
        # For now, we'll just show a success message
        from django.contrib import messages
        messages.success(request, 'Your message has been sent successfully!')
        return render(request, 'store/contact.html')
    
    return render(request, 'store/contact.html')


@login_required
@require_POST
def add_review(request, slug):
    """
    Handle review submission from the product detail modal.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)
    rating = int(request.POST.get('rating', 0) or 0)
    title = request.POST.get('title', '').strip()
    content = request.POST.get('content', '').strip()

    from django.contrib import messages

    if rating < 1 or rating > 5 or not content:
        messages.error(request, 'Please provide a rating and review text.')
        return render(request, 'store/product_detail.html', {
            'product': product,
            'related_products': Product.objects.filter(
                category=product.category, is_active=True
            ).exclude(id=product.id)[:4],
        })

    # Update or create a single review per user/product
    Review.objects.update_or_create(
        product=product,
        user=request.user,
        defaults={
            'rating': rating,
            'title': title,
            'content': content,
            'is_verified': True,
        },
    )

    messages.success(request, 'Thank you for reviewing this product!')
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': Product.objects.filter(
            category=product.category, is_active=True
        ).exclude(id=product.id)[:4],
    })


def api_search(request):
    """
    Lightweight JSON search endpoint used by live search JS.
    """
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        products = (
            Product.objects.filter(is_active=True)
            .filter(
                Q(name__icontains=query)
                | Q(short_description__icontains=query)
                | Q(category__name__icontains=query)
            )[:10]
        )
        for product in products:
            image = product.images.first()
            results.append(
                {
                    "name": product.name,
                    "slug": product.slug,
                    "price": str(product.get_display_price()),
                    "image": image.image.url if image else "",
                    "url": request.build_absolute_uri(
                        product.get_absolute_url()
                    )
                    if hasattr(product, "get_absolute_url")
                    else "",
                }
            )

    return JsonResponse({"results": results})


@require_POST
def newsletter_subscribe(request):
    """
    Subscribe an email address to the newsletter.
    Supports JSON and form submissions.
    """
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body or '{}')
        except json.JSONDecodeError:
            data = {}
        email = data.get('email', '').strip()
    else:
        email = request.POST.get('email', '').strip()

    if not email:
        return JsonResponse(
            {"success": False, "message": "Email is required."}, status=400
        )

    obj, created = NewsletterSubscription.objects.get_or_create(
        email=email,
        defaults={"is_active": True},
    )
    if not created and not obj.is_active:
        obj.is_active = True
        obj.save()

    return JsonResponse(
        {"success": True, "message": "You are subscribed to the newsletter!"}
    )


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
