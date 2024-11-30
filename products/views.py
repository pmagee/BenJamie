from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage

import json

def product_list(request, category_id=None):
    data = open('static/json/display_data.json').read()
    jsonData = json.loads(data)

    categories = Category.objects.all()
    category = None
    products = Product.objects.filter(available=True)
    display = jsonData

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, available=True)
    
    paginator = Paginator(products,12)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try: 
        products = paginator.page(page)
    except (EmptyPage,InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/category.html',{'prods':products, 'display':display,'categories':categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product':product}) 

def filter_view(request):
    # Fetch all categories for the filter dropdown
    categories = Category.objects.all()

    # Initialize query with all products
    qs = Product.objects.filter(available=True)

    # Check if the request contains search parameters
    title_contains_query = request.GET.get('title_contains', '').strip()
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category_name = request.GET.get('category')

    # Apply filters if query parameters are provided
    if any([title_contains_query, price_min, price_max, category_name]):
        if title_contains_query:
            qs = qs.filter(title__icontains=title_contains_query)
        if price_min != '' and price_min is not None:           
            qs = qs.filter(price__gte=price_min)
        if price_max != '' and price_max is not None:
            qs = qs.filter(price__lte=price_max)
        if category_name and category_name != "Choose...":
            qs = qs.filter(category__name=category_name)
    
    # Debugging
    print(f"Categories: {list(categories)}")  # Print the categories for debugging
    print(f"Filtered Products: {list(qs)}")   # Print filtered products for debugging

    # Paginate results
    paginator = Paginator(qs, 12)  # Show 12 products per page
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        qs = paginator.page(page)
    except (EmptyPage, InvalidPage):
        qs = paginator.page(paginator.num_pages)

    # Render the template
    return render(
        request,
        'shop/category.html',
        {
            'qs': qs,  # Pass the filtered or default query set
            'categories': categories,  # Pass the categories for the dropdown
        },
    )



