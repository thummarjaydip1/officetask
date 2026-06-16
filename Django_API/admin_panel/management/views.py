from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta

import requests
from account.models import User
from order.models import Order, OrderHistory
from product.models import Product, Category


def index(request):
    if request.user.is_authenticated:

        # count of user
        total_user = User.objects.count()

        # count of order
        total_order = Order.objects.count()

        # count of product
        total_product = Product.objects.count()

        # count revenue in month (dollar with k)
        current_month = now().month
        month_total = Order.objects.filter(order_date__month=current_month).aggregate(
            total=Coalesce(Sum("total_price"), 0)
        )
        revenue_month_profit = month_total["total"] / 1000 / 96.38

        # Grow bussiness in month
        target = revenue_month_profit * 1.275  #  $ 20k che (1912600 ruppess)
        if target > 0:
            grow_month = (revenue_month_profit / target) * 100
        else:
            grow_month = 0

        # total profit
        order = Order.objects.all()
        total_profit = 0
        for i in order:
            total_profit += i.total_price
        total_profit = (total_profit / 1000) / 96.38

        # count year profite (dollar with K)
        current_year = now().year
        year_total = Order.objects.filter(order_date__year=current_year).aggregate(
            total=Coalesce(Sum("total_price"), 0)
        )
        year_profit = year_total["total"] / 1000 / 96.38

        # count week profite (dollar with K)
        today = now()
        current_week = today - timedelta(days=7)
        week_total = Order.objects.filter(order_date__gte=current_week).aggregate(
            total=Coalesce(Sum("total_price"), 0)
        )
        week_profit = week_total["total"] / 1000 / 96.38

        # count today profite (dollar with K)
        current_day = now().date()
        day_total = Order.objects.filter(order_date__gte=current_day).aggregate(
            total=Coalesce(Sum("total_price"), 0)
        )
        day_profit = day_total["total"] / 1000 / 96.38

        # new project card
        new_pro_val = 862
        new_pro_per = 18

        # sessions variable default value
        sessions = 2856

        # user display
        user = User.objects.all()

        # top shell product dispaly
        top_shell = Product.objects.annotate(total_qty=Sum("order__quantity")).order_by(
            "-total_qty"
        )[:5]

    else:
        total_user = 0
        total_order = 0
        total_product = 0
        revenue_month_profit = 0
        grow_month = 0
        total_profit = 0
        year_profit = 0
        week_profit = 0
        day_profit = 0
        new_pro_val = 0
        new_pro_per = 0
        sessions = 0
        user = []
        top_shell = []

    return render(
        request,
        "dashboard/index.html",
        {
            "total_user": total_user,
            "total_order": total_order,
            "total_product": total_product,
            "revenue_month_profit": revenue_month_profit,
            "grow_month": grow_month,
            "total_profit": total_profit,
            "year_profit": year_profit,
            "week_profit": week_profit,
            "day_profit": day_profit,
            "new_pro_val": new_pro_val,
            "new_pro_per": new_pro_per,
            "sessions": sessions,
            "user": user,
            "top_shell": top_shell,
        },
    )


def error_page(request):
    return render(request, "dashboard/pages-misc-error.html")


def maintenance_page(request):
    return render(request, "dashboard/pages-misc-under-maintenance.html")


def tables(request):
    try:
        data = User.objects.all()
        category = Category.objects.all()
        product = Product.objects.all()
        order = Order.objects.all()

        search_user = request.GET.get("search_user")
        if search_user:
            data = data.filter(Q(username__icontains=search_user))

        search_category = request.GET.get("search_category")
        if search_category:
            category = category.filter(Q(name__contains=search_category))

        search_product = request.GET.get("search_product")
        if search_product:
            product = product.filter(Q(name__icontains=search_product))

        search_order = request.GET.get("search_order")
        if search_order:
            order = order.filter(Q(product_name__icontains=search_order))
        return render(
            request,
            "dashboard/tables-basic.html",
            {"data": data, "category": category, "product": product, "order": order},
        )
    except:
        messages.warning(request, "search or display error")
        return redirect("error_page")


@login_required(login_url="auth_login")
def user_table_edit(request, id):
    try:
        if request.user.role == "admin" or request.user.role == "staff":
            user = User.objects.get(id=id)
            if request.method == "POST":
                user.username = request.POST.get("username")
                user.email = request.POST.get("email")
                user.contact = request.POST.get("contact")
                user.role = request.POST.get("role")
                user.save()
                messages.success(request, "User info edit Successfully")
                return redirect("tables")
        else:
            messages.warning(request, "Only staff and admin edit User table")
            return redirect("error_page")
        return render(request, "dashboard/user_table_edit.html", {"user": user})
    except:
        messages.warning(request, "this id user not available")
        return redirect("error_page")


@login_required(login_url="auth_login")
def user_table_delete(request, id):
    try:
        if request.user.role == "admin":
            user = User.objects.get(id=id)
            user.delete()
            messages.warning(request, "User Delete this Record")
            return redirect("tables")
        else:
            messages.warning(request, "Only admin delete User table")
            return redirect("error_page")
    except:
        messages.warning(request, "this id user not available")
        return redirect("error_page")


@login_required(login_url="auth_login")
def order_admin_edit_table(request, id):
    try:
        if request.user.role == "admin" or request.user.role == "staff":
            order = Order.objects.get(id=id)
            if request.method == "POST":
                old_status = order.status
                order.status = request.POST.get("status")
                order.save()
                new_status = order.status

                OrderHistory.objects.create(
                    order=order,
                    status=new_status,
                    message=f"order change from {old_status} to {new_status}",
                )
                messages.success(request, "Order Status changed successfully")
                return redirect("tables")
        else:
            messages.warning(request, "Only staff and admin edit Order Status")
            return redirect("error_page")
        return render(
            request, "dashboard/order_admin_edit_table.html", {"order": order}
        )
    except:
        messages.warning(request, "this id order not available")
        return redirect("error_page")


@login_required(login_url="auth_login")
def order_admin_delete_table(request, id):
    try:
        if request.user.role == "admin":
            data = Order.objects.get(id=id)
            data.delete()
            messages.warning(request, "Order Deleted Successfully")
            return redirect("tables")
        else:
            messages.warning(request, "Only admin delete Order")
            return redirect("error_page")
    except:
        messages.warning(request, "this id order not available")
        return redirect("error_page")


def news(request):
    try:
        api_key = "9d78aff7e490472094657776e19f57a9"

        query = request.GET.get("q")

        india_url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"

        india_news = requests.get(india_url).json()

        articles = india_news["articles"]

        return render(request, "dashboard/news.html", {"articles": articles})
    except:
        messages.warning(request, "News API problem")
        return redirect("maintenance_page")


def documentation(request):
    return render(request, "dashboard/documentation.html")
