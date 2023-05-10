from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django import forms

from api.models import Admin
from api.utils.pagination import Pagination
from api.utils.bootstrap import BootStrapModelForm
from api.utils.forms import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from api.utils.encrypt import md5


#                   1) Admin List
def admin_list(request):
    #   1. Searching
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict["username__contains"] = search_data

    #   2. Get all Employee Objects from DB by search criteria
    queryset = Admin.objects.filter(**data_dict)

    #   3. Pagination
    page_obj = Pagination(request, queryset, page_size=10)

    context = {
        "data_list": page_obj.page_queryset,  # Paged data
        "page_str": page_obj.html(),    # Generate page htmls
        "search_data": search_data,
    }

    return render(request, 'admin_list.html', context)


#                   2) Add a admin
def admin_add(request):
    title = "New Admin"

    if request.method == "GET":
        form = AdminModelForm()  # Instantiate the Form object
        return render(request, 'change.html', {"title": title, "form": form})

    # Get POST data
    form = AdminModelForm(data=request.POST)  # Validation process
    if form.is_valid():  # Validation succeeded
        # print(form.cleaned_data)  # Get all the verified information
        form.save()  # If the data is valid, save it to the database
        return redirect('api:admin_list')
    # Validation failed
    return render(request, 'change.html', {"title": title, "form": form})


#                   3) Edit admin
def admin_edit(request, nid):
    title = "Edit Admin Info"

    #   Get Admin Info by nid
    row_obj = Admin.objects.filter(id=nid).first()  # Object / None
    if not row_obj:
        return render(request, 'error.html')

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_obj)  # Add Admin object to Form
        return render(request, "change.html", {"title": title, "form": form})

    #   Pass the information filled by the current Admin to the Form, and the current Admin
    form = AdminEditModelForm(data=request.POST, instance=row_obj)
    #   check data
    if form.is_valid():
        form.save()
        return redirect('api:admin_list')
    return render(request, "change.html", {"title": title, "form": form})


#                   4) Delete admin
def admin_delete(request, nid):
    Admin.objects.filter(id=nid).delete()
    return redirect('api:admin_list')


#                   5) Reset admin password
def admin_reset(request, nid):
    row_obj = Admin.objects.filter(id=nid).first()  # Object/None
    if not row_obj:
        return render(request, 'error.html')

    title = f"Reset Password - {row_obj.last_name} {row_obj.first_name}"
    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {"title": title, 'form': form})

    form = AdminResetModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('api:admin_list')
    return render(request, 'change.html', {"title": title, 'form': form})
