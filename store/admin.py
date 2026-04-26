from django import forms
from django.contrib import admin
from django.db import models
from django.utils.text import slugify
from django.utils.html import format_html
from django.core.files.images import get_image_dimensions

from .models import (
    Category,
    Product,
    ProductImage,
    ProductVideo,
    ProductSpecification,
    Decoration,
    DecorationImage,
    DecorationVideo,
    Review,
    NewsletterSubscription,
)

admin.site.site_header = "Stayup Nation Seller Dashboard"
admin.site.site_title = "Stayup Nation Admin"
admin.site.index_title = "Seller Tools"


def build_unique_slug(value, model, pk=None, fallback="item"):
    base = slugify(value) or fallback
    slug = base
    counter = 1
    while model.objects.filter(slug=slug).exclude(pk=pk).exists():
        counter += 1
        slug = f"{base}-{counter}"
    return slug


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)
    exclude = ('slug',)

    fieldsets = (
        (None, {
            'fields': ('name', 'parent', 'description', 'image'),
            'description': 'Create simple categories so customers can find products fast.'
        }),
        ('Visibility', {
            'fields': ('is_active',),
            'classes': ('collapse',),
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3})},
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].help_text = 'Example: Sofas, Dining Tables, Office Chairs.'
        form.base_fields['description'].help_text = 'Optional short description for this category.'
        return form

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = build_unique_slug(obj.name, Category, obj.pk, fallback="category")
        super().save_model(request, obj, form, change)


class ProductVideoInline(admin.StackedInline):
    model = ProductVideo
    extra = 1
    fields = ('title', 'video')
    verbose_name = 'Product Video'
    verbose_name_plural = 'Product Videos'


class DecorationImageInline(admin.StackedInline):
    model = DecorationImage
    extra = 0
    max_num = 10
    fields = ('image', 'alt_text', 'is_primary')
    verbose_name = 'Decoration Image'
    verbose_name_plural = 'Decoration Images'
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['image'].widget.attrs.update({'multiple': 'multiple', 'accept': 'image/*'})
        return formset


class DecorationVideoInline(admin.StackedInline):
    model = DecorationVideo
    extra = 1
    fields = ('title', 'video')
    verbose_name = 'Decoration Video'
    verbose_name_plural = 'Decoration Videos'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5
    fields = ('image', 'alt_text', 'is_primary')
    verbose_name = 'Image'
    verbose_name_plural = 'Images'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', 'name', 'category', 'price', 'in_stock', 'is_active')
    list_editable = ('in_stock', 'is_active')
    list_filter = ('category', 'in_stock', 'is_active')
    search_fields = ('name', 'short_description')
    exclude = ('slug',)
    inlines = [ProductImageInline, ProductVideoInline]
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    
    def admin_thumbnail(self, obj):
        first_image = obj.images.first()
        if first_image:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;">', first_image.image.url)
        return format_html('<img src="/static/admin/img/icon-noimage.svg" style="width: 50px; height: 50px;">')
    admin_thumbnail.short_description = 'Image'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'short_description', 'description'),
            'description': 'Start with the basic details customers will see.'
        }),
        ('Pricing', {
            'fields': ('price', 'sale_price'),
        }),
        ('Stock', {
            'fields': ('in_stock', 'stock_quantity'),
        }),
        ('Advanced Options', {
            'fields': ('featured', 'condition', 'is_active'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 4})},
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].help_text = 'Short, catchy product name.'
        form.base_fields['short_description'].help_text = 'A brief summary for quick browsing.'
        form.base_fields['description'].help_text = 'Full product details, features, and benefits.'
        form.base_fields['price'].help_text = 'Regular price (USD).'
        form.base_fields['sale_price'].help_text = 'Optional. Discounted price for sales.'
        form.base_fields['in_stock'].help_text = 'Is this product available for purchase?'
        form.base_fields['stock_quantity'].help_text = 'How many items are available?'
        return form

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = build_unique_slug(obj.name, Product, obj.pk, fallback="product")
        super().save_model(request, obj, form, change)

    actions = ['mark_active', 'mark_inactive']

    @admin.action(description='Mark selected products as Active')
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Mark selected products as Inactive')
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Decoration)
class DecorationAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'short_description')
    exclude = ('slug',)
    inlines = [DecorationImageInline, DecorationVideoInline]
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'short_description', 'description'),
            'description': 'Post your home design decoration with a clear title and summary.'
        }),
        ('Visibility', {
            'fields': ('is_active',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 4})},
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].help_text = 'Example: Modern Living Room Makeover.'
        form.base_fields['short_description'].help_text = 'Short summary that appears in the decorations list.'
        form.base_fields['description'].help_text = 'Full details about materials, style, and finish.'
        return form

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = build_unique_slug(obj.title, Decoration, obj.pk, fallback="decoration")
        super().save_model(request, obj, form, change)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified')
    search_fields = ('product__name', 'user__username')
    list_editable = ('is_verified',)
    date_hierarchy = 'created_at'
    readonly_fields = ('product', 'user', 'rating', 'title', 'content', 'created_at', 'updated_at')


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'value')
    search_fields = ('name', 'product__name', 'value')
    list_filter = ('product__category',)
    autocomplete_fields = ('product',)
