from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from app.form import LoginForm, RegisterForm, OrderForm
from app.models import Cart, Product, Blog, Wishlist, CartItem


def index_view(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = cart.cartitem_set.all()
            cart_total = sum(item.total for item in cart_items)
        else:
            cart_items = []
            cart_total = 0
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wish = wishlist.product.all()
        popular = Product.objects.order_by('-price')
        recently_added = Product.objects.all().order_by('-id')[:10]
        products = Product.objects.all().order_by('-id')
        blogs = Blog.objects.all()
        return render(request=request,
                      template_name='index.html',
                      context={"products": products,
                               'blogs': blogs,
                               "cart_items": cart_items, "cart_total": cart_total,
                               'recently_added': recently_added,
                               'popular': popular,
                               'wish': wish})
    else:
        popular = Product.objects.all().order_by('-price')[:10]
        recently_added = Product.objects.all().order_by('-id')[:10]
        products = Product.objects.all()
        blogs = Blog.objects.all()
        return render(request=request,
                      template_name='index.html',
                      context={"products": products,
                               'blogs': blogs,
                               'recently_added': recently_added,
                               'popular': popular})


def about(request):
    return render(request, 'about.html')


def blog_grid_left_sidebar(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = cart.cartitem_set.all()
        cart_total = sum(item.total for item in cart_items)
    else:
        cart_items = []
        cart_total = 0
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.product.all()
    return render(request=request,
                  template_name='blog-grid-left-sidebar.html',
                  context={"products": products,
                           "cart_items": cart_items, "cart_total": cart_total})


def blog_single_left_sidebar(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = cart.cartitem_set.all()
        cart_total = sum(item.total for item in cart_items)
    else:
        cart_items = []
        cart_total = 0
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.product.all()
    return render(request=request,
                  template_name='blog-single-left-sidebar.html',
                  context={"products": products,
                           "cart_items": cart_items, "cart_total": cart_total})


def contact(request):
    return render(request, 'contact.html')


# def login(request):
#     return render(request, 'login.html')
#
#
# def register(request):
#     return render(request, 'login.html')

# def my_account(request):
#     return render(request, 'my-account.html')


def shop(request):
    product = Product.objects.all()
    return render(request, 'shop.html',
                  {'product': product})


# @login_required(login_url='login')
def single_view(request, product_id):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = cart.cartitem_set.all()
            cart_total = sum(item.total for item in cart_items)
        else:
            cart_items = []
            cart_total = 0
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wish = wishlist.product.all()
        category = Product.objects.get(category__title="New Arrival")
        popular = Product.objects.all().order_by('-price')[:10]
        product = Product.objects.filter(id=product_id).first()
        products = Product.objects.all()

        return render(request=request,
                      template_name='single-product.html',
                      context={'product': product,
                               "products": products,
                               "cart_items": cart_items, "cart_total": cart_total,
                               'popular': popular,
                               'category': category,
                               'wish': wish})

    else:
        category = Product.objects.get(category__title="New Arrival")
        popular = Product.objects.all().order_by('-price')[:10]
        product = Product.objects.filter(id=product_id).first()
        products = Product.objects.all()
        return render(request=request,
                      template_name='single-product.html',
                      context={'product': product,
                               "products": products,
                               'popular': popular,
                               'category': category})


def single_product_affiliate(request):
    return render(request, 'single-product-affiliate.html')


def single_product_variable(request):
    return render(request, 'single-product-variable.html')


def thank_you_page(request):
    return render(request, 'thank-you-page.html')


def my_account(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = cart.cartitem_set.all()
        cart_total = sum(item.total for item in cart_items)
    else:
        cart_items = []
        cart_total = 0
    return render(request=request,
                  template_name='my-account.html',
                  context={"cart_items": cart_items, "cart_total": cart_total})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    elif request.method == "POST":
        form = LoginForm(request=request,
                         data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(user=user,
                  request=request)

            return redirect('index')

    form = LoginForm()
    products = Product.objects.all()
    return render(request=request,
                  template_name='login.html',
                  context={"form": form, 'products': products})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    elif request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    form = RegisterForm()
    products = Product.objects.all()
    return render(request=request,
                  template_name='register.html',
                  context={'form': form, 'products': products})


def logout_view(request):
    logout(request=request)
    return redirect('index')

# WISHLIST


@login_required(login_url='login')
def product_wishlist_page(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = cart.cartitem_set.all()
        cart_total = sum(item.total for item in cart_items)
    else:
        cart_items = []
        cart_total = 0
    products = Product.objects.all().order_by('-id')
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wish = wishlist.product.all()
    return render(request=request,
                  template_name='wishlist.html',
                  context={"wish": wish,
                           "cart_items": cart_items, "cart_total": cart_total,
                           'products': products})


def add_wishlist_view(request, product_id):
    product = get_object_or_404(klass=Product, id=product_id)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.product.add(product)
    return redirect("product-wishlist-page")


def delete_wishlist_view(request, product_id):
    product = get_object_or_404(klass=Product, id=product_id)

    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.product.remove(product)
    return redirect('product-wishlist-page')


# ADD TO CART

def product_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = cart.cartitem_set.all()
        cart_total = sum(item.total for item in cart_items)
    else:
        cart_items = []
        cart_total = 0
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wish = wishlist.product.all()
    products = Product.objects.all()
    return render(request=request,
                  template_name='cart.html',
                  context={"cart_items": cart_items, "cart_total": cart_total,
                           'wish': wish,
                           'products': products})


def add_cart_view(request, product_id):
    product = Product.objects.filter(id=product_id).first()

    if request.method == "POST":
        quantity = int(request.POST['quantity'])
        cart = Cart.objects.create(user=request.user)
        if cart:
            cart = Cart.objects.filter(user=request.user).first()

        cart_items, created = CartItem.objects.get_or_create(product=product,
                                                             cart=cart)
        cart_items.quantity = cart_items.quantity - 1
        cart_items.quantity += quantity
        cart_items.save()
        return redirect('product-cart-page')


def delete_cart(request, product_id):
    cart_item = CartItem.objects.filter(cart__user=request.user, id=product_id).first()
    if cart_item:
        cart_item.delete()
        return redirect('product-cart-page')


def edit_cart_item_view(request, product_id):

    try:
        cart_item = CartItem.objects.get(pk=product_id,
                                         cart__user=request.user)

        if request.method == 'POST':
            quantity = int(request.POST['quantity'])
            cart_item.quantity = quantity
            cart_item.save()

        return redirect('product-cart-page')

    except CartItem.DoesNotExist:
        pass

    return redirect('product-cart-page')

# CHECKOUT


def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        cart = Cart.objects.filter(user=request.user).first()
        cart_items = cart.cartitem_set.all()

        total_sum = 0
        for cart_item in cart_items:
            total_sum += cart_item.product.price * cart_item.quantity

    except Cart.DoesNotExist:
        cart_items = []
        total_sum = 0
        cart = None

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Foydalanuvchi to'lov ma'lumotlarini saqlash va buyurtmalar bazasiga yozish mumkin
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total_sum
            if total_sum != 0:
                order.save()

            for cart_item in cart_items:
                # Buyurtma ro'yxatidagi har bir mahsulot uchun OrderItem yaratish mumkin,
                # agar kerak bo'lsa CartItem obyektini ishlatib olasiz
                pass

            # To'lov tizimi integratsiyasini amalga oshiring

            # Savatni tozalash
            if cart:
                cart.delete()

            return redirect('index')  # Yoki boshqa bir sahifaga o'tkazing

    else:
        form = OrderForm()

    products = Product.objects.all()
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wish = wishlist.product.all()
    return render(request, 'checkout.html',
                  {'form': form, 'cart_items': cart_items, 'total_sum': total_sum,
                   'wish': wish,
                   'products': products})


