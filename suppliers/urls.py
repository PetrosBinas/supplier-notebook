from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_page, name='home'),
    path('home/notebook/', views.notebook_page, name='notebook'),
    path('home/monthly-expenses/', views.monthly_expenses, name='monthly-expenses'),
    path('home/yearly-expenses/', views.yearly_expenses, name='yearly-expenses'),
    path('home/products/', views.add_product_view, name='add-product'),
    path('home/suppliers/', views.add_supplier_view, name='suppliers')
]
