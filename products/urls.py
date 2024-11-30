from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('all_products/', views.product_list, name = 'all_products'),
    path('filter_search/', views.filter_view, name = 'filter_view'),
    path('<uuid:product_id>/', views.product_detail, name = 'product_detail'),
]