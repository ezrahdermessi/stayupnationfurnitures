from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/review/', views.add_review, name='add_review'),
    path('decorations/', views.decoration_list, name='decoration_list'),
    path('decorations/<slug:slug>/', views.decoration_detail, name='decoration_detail'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('search/', views.search, name='search'),
    path('api/search/', views.api_search, name='api_search'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]