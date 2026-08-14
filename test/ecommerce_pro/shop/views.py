from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Order

def auth_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        return redirect("auth_login")
    return render(request, "user/add_user.html")


def auth_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("index")
        else:
            return redirect("auth_login")
    return render(request, "user/login_user.html")


def auth_logout(request):
    logout(request)
    return redirect("index")

@login_required(login_url="auth_login")
def user_profile(request):
    user = request.user
    return render(request, "user/profile.html", {"user":user})

@login_required(login_url="auth_login")
def update_profile(request):
    user = request.user
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.password = request.POST.get("password")
        user.email = request.POST.get("email")
        user.save()
        return redirect("user_profile")
    return render(request, "user/profile_update.html", {"user":user})


def delete_user(request):
    user = request.user
    data = User.objects.get(id=user.id)
    data.delete()
    return redirect("index")


def user_list(request):
    user = User.objects.all()
    return render(request, "user/user_list.html", {"user":user})


def index(request):
    data = Product.objects.all()
    return render(request, "index.html", {"data":data})


def add_product(request):   
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            image=image
        )
        return redirect("index")
    return render(request, "product/add_product.html")

def list_product(request):
    product = Product.objects.all()
    return render(request, "product/list_product.html", {"product":product})


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, "product/product_details.html", {"product":product})


def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")

        if product.image:
            product.image = request.FILES.get("image")
        product.save()
        return redirect("list_product")
    return render(request, "product/update_product.html", {"product":product})


def delete_product(request, id):
    data = Product.objects.get(id=id)
    data.delete()
    return redirect("list_product")


@login_required(login_url="auth_login")
def order_now(request, id):
    product = Product.objects.get(id=id)
    
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        total_price = product.price * int(quantity)

        order = Order.objects.create(
            user=request.user,
            quantity=quantity,
            total_price=total_price,
            phone=phone,
            address=address
        )
        order.products.add(product)
        return redirect("user_order")
    return render(request, "order/order_now.html", {"product":product})


@login_required(login_url="auth_login")
def user_order(request):
    order = Order.objects.filter(user=request.user)
    return render(request, "order/user_order.html", {"order":order})


@login_required(login_url="auth_login")
def order_detail(request, id):
    order = Order.objects.get(id=id)
    return render(request, "order/order_detail.html", {"order":order})


@login_required(login_url="auth_login")
def update_order(request, id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.quantity = request.POST.get("quantity")
        order.phone = request.POST.get("phone")
        order.address = request.POST.get("address")

        total_price = 0
        for i in order.products.all():
            total_price = i.price * int(order.quantity)

        order.total_price = total_price
        order.save()
        return redirect("user_order")
    return render(request, "order/update_order.html", {"order":order})


@login_required(login_url="auth_login")
def delete_order(request, id):
    data = Order.objects.get(id=id)
    data.delete()
    return redirect("user_order")