import factory
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory
from .models import Category, Product, User


class CategoryFactory(DjangoModelFactory):
    """Factory for creating Category instances with realistic data."""
    
    class Meta:
        model = Category
        django_get_or_create = ('name',)
    
    name = factory.Iterator([
        'Electronics',
        'Clothing',
        'Food & Beverages',
        'Home & Garden',
        'Sports & Outdoors',
        'Books & Media',
        'Toys & Games',
        'Health & Beauty',
        'Automotive',
        'Office Supplies',
    ])


class ProductFactory(DjangoModelFactory):
    """Factory for creating Product instances with realistic data."""
    
    class Meta:
        model = Product
    
    name = Faker('word')
    category = SubFactory(CategoryFactory)
    price = Faker('pydecimal', left_digits=3, right_digits=2, positive=True, min_value=1, max_value=999)
    stock = Faker('random_int', min=0, max=100)
    description = Faker('text', max_nb_chars=200)
    # Note: image field will use the default placeholder


class UserFactory(DjangoModelFactory):
    """Factory for creating User instances."""
    
    class Meta:
        model = User
        django_get_or_create = ('username',)
    
    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    role = factory.Iterator(['cashier', 'manager'])
    is_active = True
    is_staff = False
    is_superuser = False
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Set password after user creation."""
        if not create:
            return
        
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password('password123')
