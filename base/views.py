from django.shortcuts import render, get_object_or_404
from base.models import User, Category, Product


def home(request):
    return render(request, 'example_dashboard.html')


def products_view(request):
    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'user':user,
        'categories':categories,
        'products':products
    }
    return render(request, 'products/all.html', context)