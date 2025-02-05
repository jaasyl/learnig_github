from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.
def index(request):
    categories = Category.objects.all()
    x = Product.objects.all()
    return render(request, 'home.html', {'pro': x, 'cat': categories})

def shopfn(request):
    return render(request, 'shop.html')

def viewfn(request, s_id):
    z = Product.objects.get(id=s_id)
    return render(request, 'view.html', {'s': z})

def catfn(request, c_id):
    x = Product.objects.filter(category=c_id)
    categories = Category.objects.all()
    return render(request, 'category.html', {'post': x, 'cat': categories})

def registerfn(request):
    if request.method == 'POST':
        a = request.POST['uname']
        b = request.POST['fn']
        c = request.POST['ln']
        d = request.POST['em']
        g = request.POST['ad']
        h = request.POST['ph']
        e = request.POST['p1']
        f = request.POST['p2']
        
        if e == f:
            if User.objects.filter(username=a).exists():
                return HttpResponse('username taken')
            elif User.objects.filter(email=d).exists():
                return HttpResponse('email already taken')     
            else:
                user = User.objects.create_user(
                    username=a,
                    first_name=b,
                    last_name=c,
                    email=d,
                    password=e
                )
                Customer.objects.create(
                    user=user,
                    phone=h,
                    address=g
                )
                return HttpResponse("hello")
        else:
            messages.error(request, 'password not matching')
            return render(request, 'register.html')
    else:    
        return render(request, 'register.html')

def loginfn(request):
    if request.method == 'POST':
        a = request.POST['uname']
        p1 = request.POST['password']
        x = auth.authenticate(username=a, password=p1)
        if x:
            auth.login(request, x)
            return redirect('/')
        else:
            messages.error(request, 'invalid user name or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')     

def add_to_cart(request):
    if request.POST:
        user = request.user
        if not user.is_authenticated or not hasattr(user, 'customer'):
            messages.error(request, 'User has no customer profile.')
            return redirect('cart')  # Redirect to cart view

        customer = user.customer
        quantity = request.POST.get('quantity')
        product_id = request.POST.get('product_id')
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        product = Product.objects.get(pk=product_id)
        OrderedItem.objects.create(
            product=product,
            owner=cart_obj,
            quantity=quantity
        )
        return redirect("cart")  # Redirect to cart view

def cart_view(request):
    user = request.user
    if user.is_authenticated and hasattr(user, 'customer'):
        customer = user.customer
        cart_obj = Order.objects.get(owner=customer, order_status=Order.CART_STAGE)
        cart_items = cart_obj.ordereditem_set.all()  # Assuming OrderedItem is related to Order
    else:
        cart_items = []  # No items if user is not authenticated or has no customer profile

    return render(request, 'cart.html', {'cart': cart_items})

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session["cart"] = cart
    return redirect("cart")  # Updated to use the named URL pattern
