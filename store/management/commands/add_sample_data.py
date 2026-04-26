from django.core.management.base import BaseCommand
from store.models import Category, Product, ProductImage, ProductSpecification

class Command(BaseCommand):
    help = 'Adds sample furniture data to the database'

    def handle(self, *args, **options):
        # Create Categories
        categories_data = [
            {'name': 'Living Room', 'slug': 'living-room', 'description': 'Sofas, chairs, coffee tables and more for your living space'},
            {'name': 'Bedroom', 'slug': 'bedroom', 'description': 'Beds, nightstands, dressers and bedroom essentials'},
            {'name': 'Dining Room', 'slug': 'dining-room', 'description': 'Dining tables, chairs and cabinets'},
            {'name': 'Office', 'slug': 'office', 'description': 'Desks, office chairs and workspace furniture'},
            {'name': 'Outdoor', 'slug': 'outdoor', 'description': 'Patio furniture and outdoor decor'},
            {'name': 'Kids', 'slug': 'kids', 'description': 'Furniture designed especially for children'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create Products
        products_data = [
            {
                'name': 'Modern Leather Sofa',
                'slug': 'modern-leather-sofa',
                'category': 'living-room',
                'price': 1299.99,
                'short_description': 'Premium Italian leather 3-seater sofa with modern design',
                'description': 'Experience luxury comfort with our Modern Leather Sofa. Crafted from premium Italian leather, this 3-seater sofa features a sleek contemporary design that complements any living room decor. The high-density foam cushions provide exceptional support while maintaining their shape over time.',
            },
            {
                'name': 'Oak Dining Table',
                'slug': 'oak-dining-table',
                'category': 'dining-room',
                'price': 899.99,
                'short_description': 'Solid oak dining table seats 6-8 people',
                'description': 'Crafted from solid oak wood, this dining table comfortably seats 6-8 people. The natural grain patterns add warmth and character to your dining room. Perfect for family gatherings and dinner parties.',
            },
            {
                'name': 'Ergonomic Office Chair',
                'slug': 'ergonomic-office-chair',
                'category': 'office',
                'price': 449.99,
                'short_description': 'Full mesh back ergonomic chair with lumbar support',
                'description': 'Work in comfort with our Ergonomic Office Chair. Featuring a full mesh back for breathability, adjustable lumbar support, and customizable armrests, this chair is designed to keep you productive throughout the workday.',
            },
            {
                'name': 'Platform Bed Frame',
                'slug': 'platform-bed-frame',
                'category': 'bedroom',
                'price': 699.99,
                'short_description': 'Modern platform bed with upholstered headboard',
                'description': 'Elevate your bedroom with our Platform Bed Frame. The sleek modern design features an upholstered headboard and low-profile frame that creates a contemporary look. No box spring required.',
            },
            {
                'name': 'Patio Lounge Set',
                'slug': 'patio-lounge-set',
                'category': 'outdoor',
                'price': 799.99,
                'short_description': '4-piece wicker patio lounge set with cushions',
                'description': 'Transform your outdoor space with this 4-piece wicker lounge set. Includes 2 lounge chairs, 1 loveseat, and 1 coffee table. Weather-resistant cushions included.',
            },
            {
                'name': 'Kids Study Desk',
                'slug': 'kids-study-desk',
                'category': 'kids',
                'price': 249.99,
                'short_description': 'Adjustable height desk with storage compartments',
                'description': 'Designed for growing children, this study desk features adjustable height settings, plenty of storage compartments, and a built-in book rack. Perfect for homework and creative activities.',
            },
            {
                'name': 'Velvet Accent Chair',
                'slug': 'velvet-accent-chair',
                'category': 'living-room',
                'price': 399.99,
                'short_description': 'Luxurious velvet armchair with gold legs',
                'description': 'Add a touch of elegance to any room with our Velvet Accent Chair. The plush velvet upholstery and gold metal legs create a sophisticated look that works in both modern and traditional spaces.',
            },
            {
                'name': 'Nightstand Set',
                'slug': 'nightstand-set',
                'category': 'bedroom',
                'price': 299.99,
                'short_description': 'Pair of modern nightstands with drawers',
                'description': 'Complete your bedroom with this matching pair of nightstands. Each features 2 spacious drawers for storage and a sleek modern design that complements any decor style.',
            },
        ]

        for prod_data in products_data:
            category = categories[prod_data.pop('category')
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={
                    **prod_data,
                    'category': category,
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(products_data)} products in {len(categories)} categories!'))
