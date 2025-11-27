from django.urls import path
from base.views import (
    home, products_view, dashboard,
    delete_category, 
    delete_product, get_product, 
    transactions_view, 
    refuse_transaction, restore_transaction, delete_transaction,
    reports_view
)

app_name = 'base'

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('products/', products_view, name='products'),
    path('transactions/', transactions_view, name='transactions'),
    # Category CRUD
    path('category/delete/<int:category_id>/', delete_category, name='delete_category'),
    
    # Product CRUD
    path('product/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('product/get/<int:product_id>/', get_product, name='get_product'),

    # Transaction CRUD
    path('transaction/refuse/<int:transaction_id>/', refuse_transaction, name='refuse_transaction'),
    path('transaction/restore/<int:transaction_id>/', restore_transaction, name='restore_transaction'),
    path('transaction/delete/<int:transaction_id>/', delete_transaction, name='delete_transaction'),

    # Reports
    path('reports/', reports_view, name='reports'),
]
