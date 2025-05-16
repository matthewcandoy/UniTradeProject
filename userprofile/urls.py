from django.contrib.auth import views as auth_views
from userprofile.views import CustomLoginView, view_auth_logs
from django.urls import path

from . import views
urlpatterns = [
    path('admin/logs/', view_auth_logs, name='view_auth_logs'),
    path('signup/', views.signup, name='signup'),
    path('login/', CustomLoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('my-store/', views.my_store, name='my_store'),
    path('my-store/order-detail/<int:pk>/', views.my_store_order_detail, name='my_store_order_detail'),
    path('my-store/add-product/', views.add_product, name='add_product'),
    path('my-store/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('my-store/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
]