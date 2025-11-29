from django.shortcuts import render, get_object_or_404, redirect
from base.models import User, Category, Product, Transaction, TransactionProduct
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import ProductForm

from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta, datetime, time
import json

def create_update_category(request): 
    category_id = request.POST.get('category_id')
    category_name = request.POST.get('category_name')
    if category_id:  # Edit
        category = get_object_or_404(Category, id=category_id)
        category.name = category_name
        category.save()
        messages.success(request, 'تم تعديل الفئة بنجاح')
    #
    # --------------------------------------------------------------
    #
    else:  # Create
        Category.objects.create(name=category_name)
        messages.success(request, 'تم إضافة الفئة بنجاح')

def create_update_product(request):

    product_id = request.POST.get('product_id')
    if product_id:  # Edit
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل المنتج بنجاح')
        else:
            messages.error(request, 'حدث خطأ في تعديل المنتج')
    #
    # --------------------------------------------------------------
    #
    else:  # Create
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة المنتج بنجاح')
        else:
            messages.error(request, 'حدث خطأ في إضافة المنتج')
    return redirect('base:dashboard')

def home(request):
    # Calculate statsz
    valid_transactions = Transaction.objects.filter(is_refused=False)
    
    total_sales = valid_transactions.aggregate(total=Sum('total_amount'))['total'] or 0
    transaction_count = valid_transactions.count()
    products_count = Product.objects.count()
    
    avg_order_value = total_sales / transaction_count if transaction_count > 0 else 0
    
    recent_transactions = valid_transactions.order_by('-created_at')[:5]
    
    context = {
        'page': 'home',
        'total_sales': total_sales,
        'transaction_count': transaction_count,
        'products_count': products_count,
        'avg_order_value': avg_order_value,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'home.html', context)

def dashboard(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    transactions = Transaction.objects.filter(is_refused=False)    
    total_sales = Transaction.objects.filter(is_refused=False).aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
    total_sales = round(total_sales, 2)
    
    if request.method == 'POST': 
        if 'category_submit' in request.POST:
            create_update_category(request)
        if 'product_submit' in request.POST:
            create_update_product(request)
    
    product_form = ProductForm()

    context = {
        'page':'dashboard',
        'products': products,
        'categories': categories,
        'transactions': transactions,
        'total_sales': total_sales,
        'product_form': product_form
    }
    return render(request, 'dashboard.html', context)

def delete_category(request, category_id):
    try:
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        messages.success(request, 'تم حذف الفئة بنجاح')
        return redirect('base:dashboard')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('base:dashboard')

def delete_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.success(request, 'تم حذف المنتج بنجاح')
        return redirect('base:dashboard')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('base:dashboard')

def get_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        data = {
            'id': product.id,
            'name': product.name,
            'category_id': product.category.id,
            'price': str(product.price),
            'stock': product.stock,
            'description': product.description or ''
        }
        return JsonResponse({'success': True, 'product': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def products_view(request):
    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()
    products = Product.objects.all().order_by('-category')
    if request.method == 'GET':
        q = request.GET.get('q')
        category = request.GET.get('category')
        sort = request.GET.get('sort')
        if q:
            products = products.filter(name__icontains=q)
        if category:
            products = products.filter(category_id=category)
        if sort:
            if sort == 'name_asc':
                products = products.order_by('name')
            elif sort == 'name_desc':
                products = products.order_by('-name')
            elif sort == 'price_asc':
                products = products.order_by('price')
            elif sort == 'price_desc':
                products = products.order_by('-price')
            elif sort == 'stock_asc':
                products = products.order_by('stock')
            elif sort == 'stock_desc':
                products = products.order_by('-stock')

    if request.method == 'POST':
        product_ids = request.POST.getlist('product_id')
        if product_ids:
            transaction = Transaction.objects.create(user=user, total_amount=0)
            for product_id in product_ids:
                product = Product.objects.get(id=product_id)
                quantity = int(request.POST.get(f'product_{product_id}_quantity', 1))
                
                TransactionProduct.objects.create(transaction=transaction, product=product, quantity=quantity)


    context = {
        'page':'products',
        'user':user,
        'categories':categories,
        'products':products
    }
    return render(request, 'products.html', context)

def transactions_view(request):
    transactions = Transaction.objects.filter(is_refused=False).order_by('-created_at')
    refused_transactions = Transaction.objects.filter(is_refused=True).order_by('-created_at')
    context = {
        'page':'transactions',
        'transactions':transactions,
        'refused_transactions':refused_transactions
    }
    return render(request, 'transactions.html', context)

def refuse_transaction(request, transaction_id):
    try:
        transaction = get_object_or_404(Transaction, id=transaction_id)
        transaction.is_refused = True
        transaction.save()
        messages.success(request, 'تم إرجاع المعاملة بنجاح')
        return redirect('base:transactions')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('base:transactions')

def restore_transaction(request, transaction_id):
    try:
        transaction = get_object_or_404(Transaction, id=transaction_id)
        transaction.is_refused = False
        transaction.save()
        messages.success(request, 'تم استرجاع المعاملة بنجاح')
        return redirect('base:transactions')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('base:transactions')

def delete_transaction(request, transaction_id):
    try:
        transaction = get_object_or_404(Transaction, id=transaction_id)
        transaction.delete()
        messages.success(request, 'تم حذف المعاملة بنجاح')
        return redirect('base:transactions')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('base:transactions')

def reports_view(request):
    # Filter valid transactions
    valid_transactions = Transaction.objects.filter(is_refused=False)
    valid_transactions_products = TransactionProduct.objects.filter(transaction__is_refused=False)

    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            start_dt_naive = datetime.combine(start_date, time.min) 
            start_dt_aware = timezone.make_aware(start_dt_naive)

            end_dt_naive = datetime.combine(end_date, time.max)
            end_dt_aware = timezone.make_aware(end_dt_naive)

            
            valid_transactions = valid_transactions.filter(
                created_at__range=(start_dt_aware, end_dt_aware)
            )
            valid_transactions_products = valid_transactions_products.filter(
                transaction__created_at__range=(start_dt_aware, end_dt_aware)
            )
    

    categories = Category.objects.all()
    sales_by_category = []
    category_labels = []
    category_data = []
    
    for category in categories:
        products = category.product_set.all()
        category_total = valid_transactions_products.filter(product__in=products).aggregate(total=Sum('item_total'))['total'] or 0
        
        if category_total > 0:
            sales_by_category.append({'name': category.name, 'total': category_total})
            category_labels.append(category.name)
            category_data.append(float(category_total))
            
    top_products = Product.objects.annotate(
        total_sold=Sum('transactionproduct__quantity', filter=Q(transactionproduct__in=valid_transactions_products))
    ).order_by('-total_sold')[:5]
    
    total_sales = valid_transactions.aggregate(total=Sum('total_amount'))['total'] or 0
    
    total_transactions_count = valid_transactions.count()
    
    avg_transaction_value = total_sales / total_transactions_count if total_transactions_count > 0 else 0
    
    
    top_products_labels = [p.name for p in top_products if p.total_sold]
    top_products_data = [p.total_sold for p in top_products if p.total_sold]


    last_30_days = timezone.now() - timedelta(days=30)
    daily_sales_data = []
    daily_sales_labels = []
    
    current_date = last_30_days
    while current_date <= timezone.now():
        day_start = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = current_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        daily_total = valid_transactions.filter(
            created_at__range=(day_start, day_end)
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        daily_sales_labels.append(current_date.strftime('%Y-%m-%d'))
        daily_sales_data.append(float(daily_total))
        current_date += timedelta(days=1)



    context = {
        'page': 'reports',
        'total_sales': round(total_sales, 2),
        'total_transactions_count': total_transactions_count,
        'avg_transaction_value': round(avg_transaction_value, 2),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'top_products_labels': json.dumps(top_products_labels),
        'top_products_data': json.dumps(top_products_data),
        'daily_sales_labels': json.dumps(daily_sales_labels),
        'daily_sales_data': json.dumps(daily_sales_data),
    }
    return render(request, 'reports.html', context)