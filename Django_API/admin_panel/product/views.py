from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import qrcode
from django.http import HttpResponse
from io import BytesIO


@login_required(login_url="auth_login")
def form_category(request):
    if request.user.role == "admin" or request.user.role == "staff":
        if request.method == "POST":
            category = request.POST.get("category")
            Category.objects.create(name=category)
            messages.success(request, "Added Category")
            return redirect("tables")
    else:
        messages.warning(request, "Only staff and admin add Category")
        return redirect("error_page")
    return render(request, "product/form_category.html")


@login_required(login_url="auth_login")
def form_category_edit(request, id):
    try:
        if request.user.role == "admin" or request.user.role == "staff":
            data = Category.objects.get(id=id)
            if request.method == "POST":
                data.name = request.POST.get("category")
                data.save()
                messages.success(request, "Category Edit Successfully")
                return redirect("tables")
        else:
            messages.warning(request, "Only staff and admin edit category")
            return redirect("error_page")
        return render(request, "product/form_category_edit.html", {"data": data})
    except:
        messages.warning(request, "this id category not available")
        return redirect("error_page")


@login_required(login_url="auth_login")
def form_category_delete(request, id):
    try:
        if request.user.role == "admin":
            category = Category.objects.get(id=id)
            category.delete()
            messages.warning(request, "Category Delete Sucessfully")
            return redirect("tables")
        else:
            messages.warning(request, "Only admin delete category")
            return redirect("error_page")
    except:
        messages.warning(request, "this id category not available")
        return redirect("error_page")


@login_required(login_url="auth_login")
def form_product(request):

    if request.user.role == "admin" or request.user.role == "staff":
        data = Category.objects.all()
        if request.method == "POST":
            category = request.POST.get("category")
            name = request.POST.get("name")
            price = request.POST.get("price")
            description = request.POST.get("description")
            image = request.FILES.get("image")

            category_id = Category.objects.get(id=category)
            Product.objects.create(
                name=name,
                price=price,
                description=description,
                image=image,
                category=category_id,
            )
            messages.success(request, "Product Added")
            return redirect("product_display")
    else:
        messages.warning(request, "Only staff and admin add Product")
        return redirect("error_page")
    return render(request, "product/form_product.html", {"data": data})


@login_required(login_url="auth_login")
def form_product_edit(request, id):
    try:
        if request.user.role == "admin" or request.user.role == "staff":
            product = Product.objects.get(id=id)
            category_data = Category.objects.all()

            if request.method == "POST":
                product.name = request.POST.get("name")
                category = request.POST.get("category")
                product.category = Category.objects.get(id=category)
                product.price = request.POST.get("price")
                product.description = request.POST.get("description")

                if request.FILES.get("image"):
                    product.image = request.FILES.get("image")
                product.save()
                messages.success(request, "Product edit successfully")
                return redirect("tables")
        else:
            messages.warning(request, "Only staff and admin edit Product")
            return redirect("error_page")
        return render(
            request,
            "product/form_product_edit.html",
            {"product": product, "category_data": category_data},
        )
    except:
        messages.warning(request, "this id product not available")
        return redirect("error_page")


@login_required(login_url="auth_login")
def form_product_delete(request, id):
    try:
        if request.user.role == "admin":
            product = Product.objects.get(id=id)
            product.delete()
            messages.warning(request, "Product Delete Successfully")
            return redirect("tables")
        else:
            messages.warning(request, "Only admin delete Product")
            return redirect("error_page")
    except:
        messages.warning(request, "this id product not available")
        return redirect("error_page")


def product_display(request):
    try:
        product = Product.objects.all()
        search = request.GET.get("search")
        if search:
            product = product.filter(
                Q(name__icontains=search) | Q(category__name__icontains=search)
            )

        category = request.GET.get("category")
        if category:
            product = Product.objects.filter(category_id=category)
        categories = Category.objects.all()
        return render(
            request,
            "product/product_display.html",
            {"product": product, "categories": categories},
        )
    except:
        messages.warning(request, "product display error")
        return redirect("error_page")


def product_display_id(request, id):
    product = Product.objects.get(id=id)
    return render(request, "product/qr_pro_display.html", {"product": product})


def product_qr(request, id):
    product = Product.objects.get(id=id)
    # product url generate
    product_url = request.build_absolute_uri(
        f"/product/product_display_id/{product.id}/"
    )

    qr = qrcode.make(product_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")


@login_required(login_url="auth_login")
def add_wishlist(request, id):

    product = Product.objects.get(id=id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    messages.success(request, "Addded Wishlist")
    return redirect("show_wishlist")


@login_required(login_url="auth_login")
def show_wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    product = wishlist.products.all()
    return render(request, "product/wishlist.html", {"product": product})


@login_required(login_url="auth_login")
def remove_wishlist(request, id):
    product = Product.objects.get(id=id)
    wishlist = request.user.wishlist
    wishlist.products.remove(product)
    messages.warning(request, "product remove to wishlist")
    return redirect("show_wishlist")
