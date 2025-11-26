from django.core.management.base import BaseCommand
from faker import Faker
from base.models import Category, Product
import random


class Command(BaseCommand):
    help = "Prepare the database with realistic categories and products"
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--products',
            type=int,
            default=50,
            help='Number of products to create (default: 50)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing categories and products before creating new ones'
        )
    
    def handle(self, *args, **options):
        fake = Faker()
        num_products = options['products']
        clear_data = options['clear']
        
        if clear_data:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data cleared successfully'))
        
        # Define categories with realistic product templates
        categories_data = {
            'Electronics': [
                'Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smart Watch',
                'Wireless Mouse', 'Keyboard', 'Monitor', 'USB Cable', 'Power Bank',
                'Bluetooth Speaker', 'Webcam', 'External Hard Drive', 'Gaming Console',
                'Smart TV', 'Wireless Earbuds', 'Charger', 'HDMI Cable', 'Router'
            ],
            'Clothing': [
                'T-Shirt', 'Jeans', 'Jacket', 'Dress', 'Sweater', 'Hoodie',
                'Shorts', 'Skirt', 'Blazer', 'Coat', 'Polo Shirt', 'Cardigan',
                'Leggings', 'Sweatpants', 'Tank Top', 'Suit', 'Scarf', 'Hat'
            ],
            'Food & Beverages': [
                'Coffee', 'Tea', 'Juice', 'Water', 'Soda', 'Energy Drink',
                'Chocolate', 'Chips', 'Cookies', 'Candy', 'Nuts', 'Protein Bar',
                'Cereal', 'Pasta', 'Rice', 'Bread', 'Milk', 'Yogurt'
            ],
            'Home & Garden': [
                'Lamp', 'Pillow', 'Blanket', 'Curtains', 'Rug', 'Vase',
                'Picture Frame', 'Candle', 'Plant Pot', 'Garden Tools',
                'Watering Can', 'Cushion', 'Mirror', 'Clock', 'Storage Box'
            ],
            'Sports & Outdoors': [
                'Yoga Mat', 'Dumbbell', 'Resistance Band', 'Jump Rope',
                'Water Bottle', 'Backpack', 'Tent', 'Sleeping Bag',
                'Camping Chair', 'Bicycle', 'Helmet', 'Running Shoes',
                'Soccer Ball', 'Basketball', 'Tennis Racket', 'Fitness Tracker'
            ],
            'Books & Media': [
                'Novel', 'Magazine', 'Comic Book', 'Textbook', 'Cookbook',
                'Biography', 'Self-Help Book', 'Children\'s Book', 'Dictionary',
                'Art Book', 'Music CD', 'DVD', 'Vinyl Record', 'Notebook'
            ],
            'Toys & Games': [
                'Board Game', 'Puzzle', 'Action Figure', 'Doll', 'LEGO Set',
                'Playing Cards', 'Stuffed Animal', 'Remote Control Car',
                'Building Blocks', 'Educational Toy', 'Video Game', 'Collectible'
            ],
            'Health & Beauty': [
                'Shampoo', 'Conditioner', 'Body Wash', 'Face Cream', 'Lotion',
                'Perfume', 'Deodorant', 'Toothpaste', 'Makeup', 'Nail Polish',
                'Hair Dryer', 'Electric Shaver', 'Vitamins', 'First Aid Kit'
            ],
            'Automotive': [
                'Car Charger', 'Phone Mount', 'Air Freshener', 'Cleaning Kit',
                'Tire Pressure Gauge', 'Jump Starter', 'Dash Cam', 'Floor Mats',
                'Seat Covers', 'Sunshade', 'Emergency Kit', 'Tool Set'
            ],
            'Office Supplies': [
                'Pen', 'Pencil', 'Notebook', 'Stapler', 'Paper Clips',
                'Sticky Notes', 'Highlighter', 'Folder', 'Binder', 'Calculator',
                'Desk Organizer', 'Whiteboard', 'Markers', 'Scissors', 'Tape'
            ],
        }
        
        # Create categories
        self.stdout.write('Creating categories...')
        categories = {}
        for category_name in categories_data.keys():
            category, created = Category.objects.get_or_create(name=category_name)
            categories[category_name] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created category: {category_name}'))
            else:
                self.stdout.write(f'  - Category already exists: {category_name}')
        
        # Create products
        self.stdout.write(f'\nCreating {num_products} products...')
        products_created = 0
        
        for i in range(num_products):
            # Select a random category
            category_name = random.choice(list(categories_data.keys()))
            category = categories[category_name]
            
            # Select a random product template from that category
            product_templates = categories_data[category_name]
            base_name = random.choice(product_templates)
            
            # Add some variation to the product name
            brand_prefixes = ['Premium', 'Deluxe', 'Pro', 'Ultra', 'Elite', 'Classic', 'Modern', 'Eco']
            colors = ['Black', 'White', 'Blue', 'Red', 'Green', 'Silver', 'Gold', 'Gray']
            sizes = ['Small', 'Medium', 'Large', 'XL']
            
            # Randomly decide what variation to add
            variation_type = random.choice(['brand', 'color', 'size', 'none', 'brand_color'])
            
            if variation_type == 'brand':
                product_name = f"{random.choice(brand_prefixes)} {base_name}"
            elif variation_type == 'color':
                product_name = f"{random.choice(colors)} {base_name}"
            elif variation_type == 'size':
                product_name = f"{base_name} ({random.choice(sizes)})"
            elif variation_type == 'brand_color':
                product_name = f"{random.choice(brand_prefixes)} {random.choice(colors)} {base_name}"
            else:
                product_name = base_name
            
            # Generate realistic price based on category
            price_ranges = {
                'Electronics': (29.99, 999.99),
                'Clothing': (9.99, 199.99),
                'Food & Beverages': (0.99, 29.99),
                'Home & Garden': (4.99, 149.99),
                'Sports & Outdoors': (9.99, 299.99),
                'Books & Media': (4.99, 49.99),
                'Toys & Games': (5.99, 99.99),
                'Health & Beauty': (3.99, 79.99),
                'Automotive': (9.99, 199.99),
                'Office Supplies': (0.99, 49.99),
            }
            
            min_price, max_price = price_ranges[category_name]
            price = round(random.uniform(min_price, max_price), 2)
            
            # Generate stock quantity
            stock = random.randint(0, 100)
            
            # Generate description
            descriptions = [
                f"High-quality {base_name.lower()} perfect for everyday use.",
                f"Premium {base_name.lower()} with excellent features and durability.",
                f"Best-selling {base_name.lower()} at an affordable price.",
                f"Top-rated {base_name.lower()} loved by customers.",
                f"Professional-grade {base_name.lower()} for optimal performance.",
                f"Stylish and functional {base_name.lower()} for modern living.",
                f"Eco-friendly {base_name.lower()} made with sustainable materials.",
                f"Innovative {base_name.lower()} with cutting-edge technology.",
            ]
            description = random.choice(descriptions)
            
            # Create the product
            product = Product.objects.create(
                name=product_name,
                category=category,
                price=price,
                stock=stock,
                description=description
            )
            
            products_created += 1
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'  Created {i + 1}/{num_products} products...')
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully created {products_created} products!'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total categories: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total products: {Product.objects.count()}'))