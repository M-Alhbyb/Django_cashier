from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

ROLES_CHOICES = (
    ('cashier', 'Cashier'),
    ('manager', 'Manager'),
)

class User(AbstractUser):
  role = models.CharField(max_length=50, default='cashier', choices=ROLES_CHOICES)

  def __str__(self):
    return self.username

class Category(models.Model):
  name = models.CharField(max_length=50, null=False, blank=False)

  def __str__(self):
    return self.name


class Product(models.Model):
  name = models.CharField(max_length=50)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.IntegerField(default=0)
  description = models.TextField(blank=True)
  image = models.ImageField(upload_to='products/', blank=True, null=True, default='products/placeholder.png')

  def __str__(self):
    return self.name

class Transaction(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  products = models.ManyToManyField(Product, through='TransactionProduct')
  created_at = models.DateTimeField(auto_now_add=True)
  total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  is_refused = models.BooleanField(default=False)
  def __str__(self):
    return f'{self.user} - {self.id}'

  def update_total_amount(self):
      total = sum(item.item_total for item in self.transaction_products.all())
      self.total_amount = total
      self.save()


class TransactionProduct(models.Model):
  transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, related_name='transaction_products')
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
  quantity = models.IntegerField(default=1)
  item_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

  def __str__(self):
    return f'{self.transaction} - {self.product}'

  def save(self, *args, **kwargs):
      if self.product:
          self.item_total = self.product.price * self.quantity
      super().save(*args, **kwargs)
      if self.transaction:
          self.transaction.update_total_amount()