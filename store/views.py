import json
import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .cart import Cart
from .forms import OrderForm
from .models import Category, Product, Order, OrderItem


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('cart_view')

def success(request):
    return render(request, 'store/success.html')

@property
def get_display_price(self):
    return "%.2f" % (self.price / 100)

def change_quantity(request, product_id):
    action = request.GET.get('action', '')
    if action:
        quantity = 1 if action == 'increase' else -1
        cart = Cart(request)
        cart.add(product_id, quantity, True)
    return redirect('cart_view')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)
    return render(request, 'store/cart_view.html', {'cart': cart})

@login_required
def checkout(request):
    cart = Cart(request)

    if cart.get_total_cost() == 0:
        return redirect('cart_view')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            total_price = 0
            items = []

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                total_price += product.price * quantity

                items.append({
                    'price_data': {
                        'currency': 'php',
                        'product_data': {
                            'name': product.title,
                        },
                        'unit_amount': product.price,
                    },
                    'quantity': quantity,
                })

            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=items,
                mode='payment',
                success_url=f'{settings.WEBSITE_URL}cart/success/',
                cancel_url=f'{settings.WEBSITE_URL}cart/',
            )

            order = form.save(commit=False)
            order.created_by = request.user
            order.paid = False  # Set to True only after payment
            order.payment_intent = session.id
            order.paid_amount = total_price
            order.save()

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                OrderItem.objects.create(order=order, product=product, price=product.price, quantity=quantity)

            cart.clear()

            return redirect(session.url, code=303)
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
        'pub_key': settings.STRIPE_PUB_KEY,
    })

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'store/search.html', {'query': query, 'products': products})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)
    return render(request, 'store/category_detail.html', {'category': category, 'products': products})


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})
