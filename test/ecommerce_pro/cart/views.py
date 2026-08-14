from django.shortcuts import render, redirect
from shop.models import Product
from cart.models import CartItem
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url="auth_login")
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    user = request.user

    if request.method == "POST":
        quantity = request.POST.get("quantity")

        total_price = product.price * int(quantity)

        CartItem.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )
        return redirect("user_cart")
    return render(request, "cart/add_to_cart.html", {"product":product})


@login_required(login_url="auth_login")
def user_cart(request):
    cart = CartItem.objects.filter(user=request.user)
    return render(request, "cart/user_cart.html", {"cart":cart})


@login_required(login_url="auth_login")
def update_cart(request, id):
    cart = CartItem.objects.get(id=id)
    if request.method == "POST":
        cart.quantity = request.POST.get("quantity")

        total_price = cart.product.price * int(cart.quantity)

        cart.total_price = total_price

        cart.save()
        return redirect("user_cart")

    return render(request, "cart/update_cart.html", {"cart":cart})


@login_required(login_url="auth_login")
def delete_cart(request, id):
    data = CartItem.objects.get(id=id)
    data.delete()
    return redirect("user_cart")