from django.shortcuts import get_object_or_404, redirect, render

from .forms import BusinessRequestCreateForm, BusinessRequestWorkflowForm
from .models import BusinessRequest


def request_list(request):
    return render(
        request,
        "requests_app/request_list.html",
        {"business_requests": BusinessRequest.objects.all()},
    )


def request_create(request):
    if request.method == "POST":
        form = BusinessRequestCreateForm(request.POST)
        if form.is_valid():
            business_request = form.save()
            return redirect("requests_app:detail", pk=business_request.pk)
    else:
        form = BusinessRequestCreateForm()
    return render(request, "requests_app/request_form.html", {"form": form})


def request_detail(request, pk):
    business_request = get_object_or_404(BusinessRequest, pk=pk)
    return render(
        request,
        "requests_app/request_detail.html",
        {"business_request": business_request},
    )


def request_update(request, pk):
    business_request = get_object_or_404(BusinessRequest, pk=pk)
    if request.method == "POST":
        form = BusinessRequestWorkflowForm(request.POST, instance=business_request)
        if form.is_valid():
            form.save()
            return redirect("requests_app:detail", pk=business_request.pk)
    else:
        form = BusinessRequestWorkflowForm(instance=business_request)
    return render(
        request,
        "requests_app/request_update.html",
        {"business_request": business_request, "form": form},
    )

# Create your views here.
