from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
import os

from allauth.account.utils import perform_login
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify

from .models import Userprofile

from store.forms import ProductForm
from store.models import Product, OrderItem, Order

import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)
handler = logging.FileHandler('auth_activity.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        logger.info(f"Login - User: {user.username}, IP: {get_client_ip(self.request)}")
        return super().form_valid(form)
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


def vendor_detail(request, pk):
   user = User.objects.get(pk=pk)
   products = user.products.filter(status=Product.ACTIVE)

   return render(request, 'userprofile/vendor_detail.html',{
   'user': user,   
   'products': products,             
   })

@login_required
def my_store(request):
   products = request.user.products.exclude(status=Product.DELETED)
   order_items = OrderItem.objects.filter(product__user=request.user)

   return render(request, 'userprofile/my_store.html', {
   'products': products,
   'order_items': order_items
   })

@login_required
def my_store_order_detail(request, pk):
   order = get_object_or_404(Order, pk=pk)

   return render(request, 'userprofile/my_store_order_detail.html', {
   'order': order
   })

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()

            messages.success(request, 'A new item was added.')
            return redirect('my_store')
    else:
        form = ProductForm()

    return render(request, 'userprofile/add_product.html', {
        'title': 'Add item',
        'form': form,
    })

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product details updated successfully!')
            return redirect('my_store')
    else:
        form = ProductForm(instance=product)

    return render(request, 'userprofile/add_product.html', {
        'title': 'Edit Product',
        'form': form,
        'product': product
    })


@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()

    messages.success(request, 'The item has been deleted.')

    return redirect('my_store')

@login_required
def myaccount(request):
   return render(request, 'userprofile/myaccount.html')


logger = logging.getLogger(__name__)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            perform_login(request, user)
            Userprofile.objects.create(user=user)

            logger.info(f"Signup - User: {user.username}, IP: {get_client_ip(request)}")

            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'userprofile/signup.html', {
        'form': form
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate user
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def view_auth_logs(request):
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'auth_activity.log')
    try:
        with open(log_path, 'r') as log_file:
            content = log_file.read()
        return HttpResponse(f"<pre>{content}</pre>")
    except FileNotFoundError:
        return HttpResponse("Log file not found.", status=404)