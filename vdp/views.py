from django.shortcuts import render, redirect
from .forms import SubmissionForm
from .models import Submission
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from django.core.paginator import Paginator
# Create your views here.



@login_required
@ratelimit(key='user', method='POST', rate='5/m', block=True)
def submission(request):
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('vdp:submission_view_url')
        return render(request, 'vdp/submission.html', {'form': form}) 
    else:
        form = SubmissionForm(request=request)
    return render(request, 'vdp/submission.html', {'form': form})



@login_required
def submission_view(request):
    submissions = Submission.objects.filter(user=request.user)
    paginator = Paginator(submissions, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    page_obj.elided_pages = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    return render(request, 'vdp/submissions_view.html', {'page_obj': page_obj})