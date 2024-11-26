from django.views import View
from .models import Product, Customer, OrderPlaced, Cart
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles})


def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, product=product).exists()
    else:
        cart = False
    return render(request, 'app/productdetail.html', {'product': product, 'in_cart': cart})


def search(request):
    search_query = request.GET.get('search')

    # Check if search_query is not None and is not an empty string
    if search_query:
        products = Product.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    else:
        # Return an empty queryset if search_query is None or empty
        products = Product.objects.none()

    return render(request, 'app/search.html', {'products': products, 'search_query': search_query})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 50
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount = amount+shipping_amount
        return render(request, 'app/addtocart.html', {'carts': cart, 'amount': amount, 'total_amount': total_amount})


@login_required
def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 50
        total_amount = 0.0
        user = request.user
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount = amount+shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'total_amount': total_amount,
            }
            return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 50
        total_amount = 0.0
        user = request.user
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount = amount+shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'total_amount': total_amount,
            }
            return JsonResponse(data)


@login_required
def remove_cart_item(request, id):
    cart = Cart.objects.filter(id=id)
    cart.delete()
    return redirect('/cart')


def buy_now(request):
    return render(request, 'app/buynow.html')


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'address': add})


@login_required
def orders(request):
    orderplaced = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {"order_placed": orderplaced})


def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.filter(category="M")
    elif data == "Redmi" or data == "Samsung":
        mobile = Product.objects.filter(category="M").filter(brand=data)
    elif data == "Below":
        mobile = Product.objects.filter(
            category="M").filter(discount_price__lt=20000)
    elif data == "Above":
        mobile = Product.objects.filter(
            category="M").filter(discount_price__gt=20000)
    return render(request, 'app/mobile.html', {'mobile': mobile})


def laptop(request, data=None):
    if data == None:
        laptop = Product.objects.filter(category="L")
    elif data == "HP" or data == "Dell" or data == "Apple":
        laptop = Product.objects.filter(category="L").filter(brand=data)
    elif data == "Below":
        laptop = Product.objects.filter(
            category="L").filter(discount_price__lt=40000)
    elif data == "Above":
        laptop = Product.objects.filter(
            category="L").filter(discount_price__gt=50000)
    return render(request, 'app/laptop.html', {'laptop': laptop})


def topwear(request, data=None):
    if data == None:
        topwear = Product.objects.filter(category="TW")
    elif data == "Zara" or data == "Goofy":
        topwear = Product.objects.filter(category="TW").filter(brand=data)
    elif data == "Below":
        topwear = Product.objects.filter(
            category="TW").filter(discount_price__lt=500)
    elif data == "Above":
        topwear = Product.objects.filter(
            category="TW").filter(discount_price__gt=500)
    return render(request, 'app/topwear.html', {'topwear': topwear})


def bottomwear(request, data=None):
    if data == None:
        bottomwear = Product.objects.filter(category="BW")
    elif data == "Zara" or data == "Nike":
        bottomwear = Product.objects.filter(category="BW").filter(brand=data)
    elif data == "Below":
        bottomwear = Product.objects.filter(
            category="BW").filter(discount_price__lt=500)
    elif data == "Above":
        bottomwear = Product.objects.filter(
            category="BW").filter(discount_price__gt=500)
    return render(request, 'app/bottomwear.html', {'bottomwear': bottomwear})


def customerregistration(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Account created successfully")
            # return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=request.user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 50
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        total_amount = amount+shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'total_amount': total_amount, "cart_items": cart_items, "shipping_amount": shipping_amount})


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            locality = form.cleaned_data['locality']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, city=city,
                           locality=locality, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'Congratulations, Profile Updated Successfully')
            return render(request, 'app/profile.html', {'form': form})


@login_required
def payment_done(request):
    user = request.user
    cust_id = request.GET.get('custid')
    customer = Customer.objects.get(id=cust_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')
