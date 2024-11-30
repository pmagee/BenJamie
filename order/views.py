from django.shortcuts import render, get_object_or_404
from .models import Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


# Create your views here.
def thanks(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
    return render(request, 'thanks.html',{'customer_order': customer_order}) 

class orderHistory(LoginRequiredMixin, View):
    def get (self, request):
        if request.user.is_authenticated:
            email = str(request.user.email)
            order_details = Order.objects.filter(emailAddress=email)
        return render(request, 'orders_list.html', {'order_details': order_details})
