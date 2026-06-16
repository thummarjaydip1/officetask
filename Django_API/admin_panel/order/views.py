from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# pdf download use import statement
from django.template.loader import get_template
from xhtml2pdf import pisa


@login_required(login_url="auth_login")
def order_now(request, id):

    product = Product.objects.get(id=id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        order = Order.objects.create(
            product=product,
            product_name=product.name,
            price=product.price,
            quantity=quantity,
            contact=contact,
            address=address,
            user=request.user,
        )
        OrderHistory.objects.create(
            order=order, status="Pending", message="Order placed successfully"
        )
        messages.success(request, "Place order successfully")
        return redirect("order_display")
    return render(request, "order/order_now.html", {"product": product})


@login_required(login_url="auth_login")
def order_history(request, id):
    order = Order.objects.get(id=id)
    history = OrderHistory.objects.filter(order=order)

    return render(
        request, "order/order_history.html", {"history": history, "order": order}
    )


@login_required(login_url="auth_login")
def order_display(request):
    data = Order.objects.filter(user=request.user)
    # search data
    search = request.GET.get("search")
    if search:
        data = data.filter(Q(product_name__contains=search))

    # filter data to status
    status_fields = Order._meta.get_field("status").choices

    status = request.GET.get("status")
    if status:
        data = data.filter(status=status)

    # filter data to date
    startdate = request.GET.get("startdate")
    enddate = request.GET.get("enddate")
    if startdate and enddate:
        data = data.filter(order_date__range=[startdate, enddate])
    return render(
        request,
        "order/order_display.html",
        {"data": data, "status_fields": status_fields},
    )


@login_required(login_url="auth_login")
def order_user_edit(request, id):
    try:
        data = Order.objects.get(id=id)
        if request.user == data.user:
            if data.status == "Pending":
                if request.method == "POST":
                    data.quantity = int(request.POST.get("quantity"))
                    data.contact = request.POST.get("contact")
                    data.address = request.POST.get("address")
                    data.total_price = int(data.product.price) * data.quantity
                    data.save()
                    messages.success(request, "Order Edit Successfully")
                    return redirect("order_display")
            else:
                messages.warning(request, "only pending record are updated")
                return redirect("error_page")
        else:
            messages.warning(request, "You cant update only your order")
            return redirect("error_page")
        return render(request, "order/order_user_edit.html", {"data": data})
    except:
        messages.warning(request, "this id order not available")
        return redirect("error_page")


@login_required(login_url="auth_login")
def order_user_delete_table(request, id):
    try:
        data = Order.objects.get(id=id)
        if request.user == data.user:
            data.delete()
            messages.warning(request, "Order Deleted Successfully")
            return redirect("order_display")
        else:
            messages.warning(request, "You cant delete only your order")
            return redirect("error_page")
    except:
        messages.warning(request, "this id order not available")
        return redirect("error_page")


@login_required(login_url="auth_login")
def bill_system(request, id):
    try:
        data = Order.objects.get(id=id)
        if request.user != data.user:
            messages.warning(request, "Can't show anthor user bill")
            return redirect("error_page")
        return render(request, "order/bill_system.html", {"data": data})
    except:
        messages.warning(request, "this id bill not available")
        return redirect("error_page")


@login_required(login_url="auth_login")
def pdf_download(request, id):
    try:
        data = Order.objects.get(id=id)
        if request.user != data.user:
            messages.warning(request, "Can't download anthor user bill")
            return redirect("error_page")
        template = get_template("order/bill_system.html")
        html = template.render({"data": data})
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f"attachment; filename = {data.user}_{data.product_name}_{data.id}_bill.pdf"
        )
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("Pdf Generate Error")
        return response
    except:
        messages.warning(request, "this id order not available can't pdf download")
        return redirect("error_page")
