from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.core.paginator import Paginator
from comment.forms import CommentForm, EditCommentForm
from comment.models import Comment
from django.http import JsonResponse
from django.db.models import F, Value
# Create your views here.




def products(request, category="all"):
    if category == "all":
        products = Product.objects.filter(available=True)
    else:
        products = Product.objects.filter(available=True, category=category)
    paginator = Paginator(products, 12)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    page_obj.elided_pages = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    return render(request, 'product/products.html', {'page_obj': page_obj})




def search_products(request):
    title = request.GET.get('title', '')
    full = not title # If the title is empty, it is True
    
    # 1. The Basic query
    prods_qs = Product.objects.annotate(
        final_price=F('price') - Coalesce(F('discount'), Value(0))
    )
    
    if title:
        prods_qs = prods_qs.filter(title__icontains=title)
    
    
    prods_qs = prods_qs


    # 2. get 13 items to confirm the existence of "more".
    prods_values = list(prods_qs.values('id', 'slug', 'title', 'description', 'img', 'final_price', 'discount', 'price')[:13])
    
    is_there_more = len(prods_values) > 12


    # take the first 12 for the actual data.
    data = prods_values[:12]
    exists = len(data) > 0

    # 3. Images processing
    for item in data:
        if item['img']:
            item['img'] = f"{request.scheme}://{request.get_host()}/media/{item['img']}"
        else:
            item['img'] = '/static/images/products/product-default-img.png'

    return JsonResponse({
        "status": "success", 
        "data": data,
        "full": full,
        "exists": exists,
        "is_there_more": is_there_more
    })
        


def load_more_products(request):
    try:
        # Make sure the start number is always an integer number.
        start = int(request.GET.get("more", 0))
    except (ValueError, TypeError):
        start = 0
        
    title = request.GET.get("title", '')
    # require 13 items (12 for display and 1 for inspection)
    end = start + 13 
    
    # The query that get more products 
    prods_qs = Product.objects.filter(title__icontains=title).annotate(
        final_price=F('price') - Coalesce(F('discount'), Value(0))
    ).order_by().distinct()

    # get data using 'slice'
    prods_values = list(prods_qs.values('id', 'slug', 'title', 'description', 'img', 'final_price', 'discount', 'price')[start:end])

    is_there_more = len(prods_values) > 12
    # take first 12 items to send
    data = prods_values[:12]
    
    for item in data:
        if item['img']:
            item['img'] = f"{request.scheme}://{request.get_host()}/media/{item['img']}"
        else:
            item['img'] = '/static/images/products/product-default-img.png'
    
    return JsonResponse({
        "status": "success",
        "data": data,
        "is_there_more": is_there_more
    })


    

    

def product(request, the_slug):
    form = CommentForm()
    product = get_object_or_404(Product, slug=the_slug)
    comments = Comment.objects.filter(product=product)
    

    return render(request, 'product/product.html', {'product': product, 'form': form, 'comments': comments})
