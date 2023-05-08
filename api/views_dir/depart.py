from django import forms
from django.shortcuts import render, redirect

from api.utils.forms import DepartModelForm
from api.utils.pagination import Pagination
from api.models import Department


#               1) Department List
def depart_list(request):
    #   1. Get all Department objects from DB
    queryset = Department.objects.all()

    #   2. Pagination
    page_obj = Pagination(request, queryset, page_size=10)

    context = {
        "data_list": page_obj.page_queryset,  # Paged data
        "page_str": page_obj.html()  # generated page htmls
    }

    return render(request, '../templates/depart_list.html', context)


#               2) Add New Department

def depart_add(request):
    title = "New Department"

    if request.method == 'GET':
        form = DepartModelForm()    # Instantiate the Form object
        return render(request, '../templates/change.html', {'form': form, 'title': title})

    # Get POST data
    form = DepartModelForm(data=request.POST)   # Validation process
    if form.is_valid():  # Validation succeeded
        # print(form.cleaned_data)  # Get all the verified information
        form.save()  # if data valid, save to DB
        return redirect('api:depart_list')
    # Validation Failed(Display error messages on the page)
    # print(form.errors)
    return render(request, '../templates/change.html', {'form': form, 'title': title})  # The form after verification failure already has user data


#               3) Edit Department Info
# http://127.0.0.1:8000/api/depart/3/edit/
def depart_edit(request, nid):
    title = 'Edit Department Info'

    #   Get Department Object by nid
    row_object = Department.objects.filter(id=nid).first()  # Object / None
    if not row_object:
        return render(request, '../templates/error.html')

    if request.method == 'GET':
        form = DepartModelForm(instance=row_object)  # Add Department Object to Form
        return render(request, '../templates/change.html', {"form": form, 'title': title})

    #   Pass the information filled by the current user to the Form, and the current user
    form = DepartModelForm(data=request.POST, instance=row_object)
    #   Check data (validation process)
    if form.is_valid():  # Validation succeeded
        form.save()  # If the data is valid, save it to the database
        return redirect('api:depart_list')

    #   Validation failed (display error message on page)
    return render(request, '../templates/change.html', {'form': form, 'title': title})


#               4) Delete Department (with ?nid=id)
def depart_delete(request):
    # Get ID
    nid = request.GET.get('nid')
    # Do the DELETE operation
    Department.objects.filter(id=nid).delete()

    # Redirect to Department List
    return redirect("api:depart_list")


