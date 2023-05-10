from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import datetime

from api.utils.forms import OrderModelForm
from api.utils.pagination import Pagination
from api.models import Order


def order_list(request):
    queryset = Order.objects.all().order_by("-id")

    page_obj = Pagination(request, queryset)

    form = OrderModelForm()

    context = {
        "form": form,
        "data_list": page_obj.page_queryset,  # Paged data
        "page_str": page_obj.html()  # Generate page html
    }
    
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """ Add new order (Ajax request) """

    #   1.Verify the request sent by the user (ModelForm verifies)
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        #   Order id: dynamically calculate and allocate 'oid'
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        #   Save to DB
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)

    data_dict = {"status": False, 'error': form.errors}
    return JsonResponse(data_dict)


def order_delete(request):
    uid = request.GET.get("uid")

    exists = Order.objects.filter(id=uid).exists()

    if not exists:
        return JsonResponse({"status": False, 'error': "Delete failed, data does not exist"})

    Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})

def order_detail(request):
    """ Get detail order info by id """
    uid = request.GET.get("uid")

    row_dict = Order.objects.filter(id=uid).values("title", "price", "payment_status", "delivery_status", "user").first()  # 这样直接得到字典
    if not row_dict:
        return JsonResponse({"status": False, 'error': "Data doesn't exist!"})

    #   Obtained a dict form DB: row_dict = {'id': 1, 'title': 'xx', ...}
    result = {
        "status": True,
        'data': row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    uid = request.GET.get("uid")
    row_obj = Order.objects.filter(id=uid).first()
    if not row_obj:
        return JsonResponse({"status": False, 'tips': "The data does not exist, please refresh and try again"})

    form = OrderModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    data_dict = {"status": False, 'error': form.errors}
    return JsonResponse(data_dict)

