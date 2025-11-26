from django.core.management.base import BaseCommand
from base.factories import CategoryFactory, ProductFactory
from base.models import Category, Product


class Command(BaseCommand):
    help = "Generate fake data using factory_boy for categories and products"
    
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
        num_products = options['products']
        clear_data = options['clear']
        
        if clear_data:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data cleared successfully'))
        
        # Create categories first (factory will use get_or_create)
        self.stdout.write('Creating categories...')
        categories_created = 0
        
        # The CategoryFactory uses an Iterator, so we need to create enough instances
        # to cycle through all category names
        for i in range(10):
            try:
                category = CategoryFactory()
                categories_created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created category: {category.name}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  - Category may already exist: {e}'))
        
        # Create products
        self.stdout.write(f'\nCreating {num_products} products using factory_boy...')
        products_created = 0
        
        for i in range(num_products):
            try:
                product = ProductFactory()
                products_created += 1
                
                if (i + 1) % 10 == 0:
                    self.stdout.write(f'  Created {i + 1}/{num_products} products...')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  Error creating product: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully created {products_created} products!'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total categories: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total products: {Product.objects.count()}'))
