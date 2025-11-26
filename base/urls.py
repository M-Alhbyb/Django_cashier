from django.urls import path
from base.views import home, products_view
app_name = 'base'

urlpatterns = [
  path('', home, name='home'),
  path('products', products_view, name='products')

]
