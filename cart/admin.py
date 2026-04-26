from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total', 'date')
    list_filter = ('status',)
    search_fields = ('order_number', 'user__username', 'shipping_name', 'shipping_email')
    readonly_fields = ('order_number', 'user', 'subtotal', 'shipping_amount', 'tax_amount', 'total_amount', 'created_at', 'updated_at')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'user', 'status', 'created_at'),
        }),
        ('Shipping', {
            'fields': ('shipping_name', 'shipping_email', 'shipping_phone', 'shipping_address', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country'),
        }),
        ('Totals', {
            'fields': ('subtotal', 'shipping_amount', 'tax_amount', 'total_amount'),
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
    )

    actions = ['mark_confirmed', 'mark_shipped', 'mark_delivered']

    @admin.action(description='Mark as Confirmed')
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, 'Orders marked as confirmed.')

    @admin.action(description='Mark as Shipped')
    def mark_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, 'Orders marked as shipped.')

    @admin.action(description='Mark as Delivered')
    def mark_delivered(self, request, queryset):
        queryset.update(status='delivered')
        self.message_user(request, 'Orders marked as delivered.')

    def total(self, obj):
        return f'${obj.total_amount}'
    total.short_description = 'Total'

    def date(self, obj):
        return obj.created_at.strftime('%b %d, %Y')
    date.short_description = 'Date'
