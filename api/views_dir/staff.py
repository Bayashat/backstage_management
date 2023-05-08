from django import forms
from django.shortcuts import render, redirect
from api.models import EmployeeInfo

from api.utils.forms import StaffModelForm
from api.utils.pagination import Pagination


#                   1) Staff List

def staff_list(request):
    #  1. Searching
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['first_name__contains'] = search_data

    #   2. Get all Employee Objects from DB by search criteria
    queryset = EmployeeInfo.objects.filter(**data_dict)

    #   3. Pagination
    page_obj = Pagination(request, queryset, page_size=5)

    context = {
        "data_list": page_obj.page_queryset,    # Paged data
        "page_str": page_obj.html(),    # Generated page htmls
        "search_data": search_data,
    }

    return render(request, '../templates/staff_list.html', context)


#                   2) Add New Staff
def staff_add(request):
    title = "New Staff"

    if request.method == 'GET':
        form = StaffModelForm()    # Instantiate the Form object
        return render(request, '../templates/change.html', {"form": form, 'title': title})

    # Get POST data
    form = StaffModelForm(data=request.POST)    # Validation process
    if form.is_valid():  # Validation succeeded
        # print(form.cleaned_data)  # data obtained by the verification success
        # If the data is valid, save it to the database
        form.save()
        return redirect('api:staff_list')
    # Validation failed (display error message on page)
    # print(form.errors)  # Error msg
    # The form after verification failure already has user data
    return render(request, '../templates/change.html', {"form": form, 'title': title})


#                   3) Edit Staff Info
def staff_edit(request, nid):
    title = 'Edit Staff Info'

    # Get Staff info by id
    row_object = EmployeeInfo.objects.filter(id=nid).first()  # Object/None
    if not row_object:
        return render(request, '../templates/error.html')

    if request.method == 'GET':
        form = StaffModelForm(instance=row_object)  # Add Staff info to Form
        return render(request, '../templates/change.html', {"form": form, 'title': title})

    # Pass the information filled by the current Staff to the Form, and the current Staff
    form = StaffModelForm(data=request.POST, instance=row_object)
    # check data (validation process)
    if form.is_valid():   # Validation succeeded
        form.save()  # If the data is valid, save it to the database
        return redirect('api:staff_list')

    # Validation failed (display error message on page)
    return render(request, '../templates/change.html', {'form': form, 'title': title})


#                   4) Delete Staff Info (with arg)

def staff_delete(request, nid):
    EmployeeInfo.objects.get(id=nid).delete()

    # Redirect to Employee List
    return redirect("api:staff_list")
