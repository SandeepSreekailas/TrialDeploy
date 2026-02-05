from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Cart
from .forms import BookForm, UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from django.urls import reverse

stripe.api_key=settings.STRIPE_SECRET_KEY


# Create your views here.

def home(request):
    return render(request, "home.html")

@login_required
def view_book(request):
    b=Book.objects.all()
    return render(request, "view_book.html",{"boo":b})

@login_required
def create_book(request):
    f=BookForm(request.POST or None, request.FILES or None)
    if f.is_valid():
        f.save()
        return redirect('view_book')
    return render(request, "create_book.html",{"frm":f})

@login_required
def update_book(request,id):
    book=Book.objects.get(id=id)
    f=BookForm(request.POST or None, request.FILES or None, instance=book)
    if f.is_valid():
        f.save()
        return redirect('view_book')
    return render(request, "create_book.html",{"frm":f})

@login_required
def delete_book(request,id):
    book=get_object_or_404(Book,id=id)
    if request.method=="POST":
        book.delete()
        return redirect('view_book')

    return render(request, "delete_book.html",{"book":book})


def register_view(request):
    f=UserRegistrationForm(request.POST or None)
    if request.method=='POST' and f.is_valid():
        f.save()
        return redirect('view_book')
    return render(request, "register.html",{"frm":f})
    
def login_view(request):
    f=UserLoginForm(request, data=request.POST or None)
    if request.method=='POST' and f.is_valid():
        user=f.get_user()
        login(request, user)
        return redirect('view_book')
    return render(request, "login.html",{"frm":f})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')

def add_to_cart(request,book_id):
    book = get_object_or_404(Book,id=book_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, "cart.html", {"cart_items": cart_items})

@login_required
def remove_from_cart(request,book_id):
    book = get_object_or_404(Book,id=book_id)
    cart_item = Cart.objects.get(user=request.user, book=book)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_view')

@login_required
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return redirect('cart_view')

def buy_now(request, book_id):
    cart_items = get_object_or_404(Cart, user=request.user, book_id=book_id)
    book=cart_items.book

    session=stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'inr',
                    'product_data':{    
                        'name':book.title,
                    },
                    'unit_amount': int(float(book.price) * 100),

                },
                'quantity':cart_items.quantity, 
            }
        ],

        mode="payment", 
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('cart_view')),
        
    )
    return redirect(session.url)    

def payment_success(request):
    return render(request, 'success.html')

def payment_cancel(request):
    return render(request, 'view_cart.html')