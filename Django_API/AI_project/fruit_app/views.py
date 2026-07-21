from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Product, Category, Contact, Cart, CartItem
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ContactForm


def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

# Page views rendering the template pages

def home(request):
    products = Product.objects.filter(status=True).select_related('category').order_by('-created_at')[:6]
    return render(request, 'index.html', {'products': products})


def about(request):
    return render(request, 'about.html')


def products(request):
    products = Product.objects.filter(status=True).select_related('category')
    categories = Category.objects.all()

    search_query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()

    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) |
            Q(category__category_name__icontains=search_query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'products.html', {
        'products': products,
        'data': categories,
        'search_query': search_query,
        'selected_category': category_id,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk, status=True)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to add products to your cart.')
        return redirect('fruit_app:login')

    product = get_object_or_404(Product, pk=product_id, status=True)
    if product.stock <= 0:
        messages.error(request, 'This product is out of stock and cannot be added to your cart.')
        return redirect('fruit_app:product_detail', pk=product_id)

    quantity = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    quantity = max(1, quantity)

    cart = get_or_create_cart(request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, 'Product added to cart successfully.')
    return redirect('fruit_app:cart')


@login_required(login_url='fruit_app:login')
def cart(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.select_related('product').all()
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
    })


@login_required(login_url='fruit_app:login')
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem.objects.select_related('cart__user', 'product'), pk=item_id, cart__user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        if cart_item.product.stock > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, 'Cannot increase quantity. Stock limit reached.')
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    elif action == 'remove':
        cart_item.delete()
    else:
        messages.error(request, 'Invalid cart action.')

    return redirect('fruit_app:cart')


@login_required(login_url='fruit_app:login')
def clear_cart(request):
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared successfully.')
    return redirect('fruit_app:cart')


def contact(request):
    """Handle contact form submissions and save to DB."""
    if request.method == 'POST':
        # Only authenticated users can submit
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first to send a contact message.')
            return redirect('fruit_app:login')

        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            # Associate with the logged-in user
            contact.user = request.user
            contact.save()
            messages.success(request, 'Your message has been sent. We will get back to you soon.')
            return redirect('fruit_app:contact')
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def register(request):
    """Handle user registration with validation."""
    if request.user.is_authenticated:
        return redirect('fruit_app:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after registration
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
            return redirect('fruit_app:profile')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Handle user login with authentication."""
    if request.user.is_authenticated:
        return redirect('fruit_app:home')

    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')

            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host()):
                return redirect(next_url)
            return redirect('fruit_app:profile')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('fruit_app:home')


@login_required(login_url='fruit_app:login')
def profile(request):
    """Display user profile page (only for logged-in users)."""
    return render(request, 'profile.html', {'user': request.user})
