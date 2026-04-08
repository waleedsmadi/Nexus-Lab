from django.shortcuts import render, redirect
from .forms import ReportForm
from .models import Report
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from django.core.paginator import Paginator
# Create your views here.



@login_required
@ratelimit(key='user', method='POST', rate='5/m', block=True)
def create_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('reports:reports_view_url')
        return render(request, 'reports/report_create.html', {'form': form}) 
    else:
        form = ReportForm(request=request)
    return render(request, 'reports/report_create.html', {'form': form})



@login_required
def view_reports(request):
    reports = Report.objects.filter(user=request.user)
    paginator = Paginator(reports, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    page_obj.elided_pages = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    return render(request, 'reports/reports_view.html', {'page_obj': page_obj})