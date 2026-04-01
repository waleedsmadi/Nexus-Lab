from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm
from product.models import Product
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from .models import Comment
from django.core.exceptions import PermissionDenied
# Create your views here.



@login_required()
@ratelimit(key="post:user", rate="5/m", block=True)
def add_comment(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            return redirect('product:product_url', the_slug=product.slug)
        return redirect('product:product_url', the_slug=product.slug)


    return redirect('product:product_url', the_slug=product.slug)




def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    product_slug = comment.product.slug
    if request.user != comment.user:
        raise PermissionDenied
    
    comment.delete()
    return redirect('product:product_url', the_slug=product_slug)




def edit_comment(request, comment_id):
    if request.method == 'POST': 
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        new_text = request.POST.get('text')
        
        if new_text:
            comment.text = new_text
            comment.save()
            return JsonResponse({'status': 'success', 'text': comment.text})
        
    return JsonResponse({'status': 'error'}, status=400)
    
