from django.contrib import admin
from base.models import User, Category, Product, Transaction, TransactionProduct

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(TransactionProduct)

