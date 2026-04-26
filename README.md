# STAY UP Furniture - Django E-commerce Website

A modern furniture e-commerce website built with Django, featuring product catalogs, shopping cart functionality, user authentication, and responsive design.

## Features

### 🏠 **Core Functionality**
- **Product Catalog**: Browse furniture by category with filtering and search
- **Shopping Cart**: Add/remove items, update quantities
- **User Authentication**: Register, login, profile management
- **Order Management**: Complete checkout process
- **Admin Panel**: Full content management system

### 🎨 **Frontend Features**
- **Responsive Design**: Works on all devices
- **Product Gallery**: Image zoom and multiple views
- **Search & Filter**: Advanced product search
- **Interactive Cart**: Real-time updates
- **Modern UI**: Bootstrap 5 + Custom CSS

### 🛍️ **E-commerce Features**
- **Product Management**: Categories, variants, specifications
- **Pricing**: Regular/sale prices, stock management
- **Reviews & Ratings**: Customer feedback system
- **Wishlist**: Save products for later
- **Newsletter**: Email subscription

## Project Structure

```
STAY UP Furniture/
├── stayup_furniture/          # Main Django project
│   ├── settings.py           # Project configuration
│   └── urls.py              # Main URL routing
├── store/                   # Product catalog app
│   ├── models.py            # Products, categories, reviews
│   ├── views.py             # Product display logic
│   ├── admin.py             # Product admin interface
│   └── urls.py             # Product URLs
├── cart/                    # Shopping cart app
│   ├── models.py            # Cart, order models
│   ├── views.py             # Cart functionality
│   ├── admin.py             # Cart admin interface
│   └── urls.py             # Cart URLs
├── users/                   # User management app
│   ├── models.py            # Custom user model
│   ├── views.py             # User authentication
│   ├── forms.py             # User registration forms
│   └── urls.py             # User URLs
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── store/              # Store templates
│   ├── cart/               # Cart templates
│   └── users/              # User templates
├── static/                  # Static files
│   ├── css/style.css       # Custom styles
│   ├── js/main.js          # JavaScript functionality
│   └── images/            # Image assets
└── media/                   # User uploaded content
```

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Instructions

1. **Clone and Navigate**
   ```bash
   cd "STAY UP Furniture"
   ```

2. **Activate Virtual Environment**
   ```bash
   venv/Scripts/activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Website**
   - Frontend: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Admin Setup

### Creating Categories
1. Login to admin panel
2. Go to "Categories" under "Store"
3. Add categories like "Living Room", "Bedroom", "Office", etc.

### Adding Products
1. Go to "Products" under "Store"
2. Click "Add product"
3. Fill in product details
4. Add product images
5. Set specifications
6. Save product

### Managing Orders
- View customer orders in the admin panel
- Update order status
- Manage inventory

## Key Features Explained

### 🏬 **Product Catalog**
- Hierarchical categories (parent/child)
- Rich product descriptions
- Multiple product images
- Product specifications
- Stock management
- Sale pricing

### 🛒 **Shopping Cart**
- Session-based cart for guests
- Persistent cart for logged users
- Quantity updates
- Item removal
- Cart summary

### 👤 **User System**
- Custom user model with additional fields
- User profiles with avatars
- Order history
- Account management

### 🎯 **Search & Discovery**
- Full-text product search
- Category filtering
- Price range filtering
- Sort options (price, name, newest)

### 📱 **Responsive Design**
- Mobile-first approach
- Bootstrap 5 framework
- Custom CSS with modern design
- Interactive elements

## Deployment Notes

### Production Settings
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Set up proper static file serving
- Configure database (PostgreSQL recommended)
- Set up email backend
- Configure media file storage

### Security Considerations
- Enable HTTPS
- Set up CSRF protection
- Configure secure session settings
- Implement rate limiting
- Regular security updates

## Customization

### Adding New Features
1. Create new Django apps as needed
2. Add models for new functionality
3. Create views and templates
4. Update URL configurations
5. Admin interface configuration

### Styling
- Edit `static/css/style.css` for custom styles
- Modify templates for layout changes
- Add new JavaScript in `static/js/`

### Business Logic
- Extend models in respective apps
- Add custom management commands
- Implement business-specific features

## Support & Maintenance

### Regular Tasks
- Backup database regularly
- Update Django and dependencies
- Monitor security advisories
- Optimize database performance
- Update product inventory

### Common Issues
- Image uploads: Ensure `MEDIA_ROOT` permissions
- Static files: Run `collectstatic` in production
- Email: Configure SMTP settings
- Performance: Optimize queries and use caching

## Contributing

1. Follow Django best practices
2. Write clean, documented code
3. Test all changes
4. Use meaningful commit messages
5. Update documentation

## License

This project is for educational and commercial use. Please modify and customize according to your business needs.

---

**STAY UP Furniture** 🛋️ - Transform your living space with quality furniture, delivered with modern technology and exceptional service.