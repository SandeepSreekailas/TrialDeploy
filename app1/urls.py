from django.urls import path
from .import views

urlpatterns = [
    path("",views.home,name='home'),
    path("view_book",views.view_book,name='view_book'),
    path("create_book",views.create_book,name='create_book'),
    path("update_book/<int:id>",views.update_book,name='update_book'),
    path("delete_book/<int:id>",views.delete_book,name='delete_book'),
    path("register",views.register_view,name='register_view'),
    path("login",views.login_view,name='login_view'),
    path("logout",views.logout_view,name='logout_view'),
    path("add_to_cart/<int:book_id>",views.add_to_cart,name='add_to_cart'),
    path("cart",views.cart_view,name='cart_view'),
    path("remove_from_cart/<int:book_id>",views.remove_from_cart,name='remove_from_cart'),
    path("clear_cart",views.clear_cart,name='clear_cart'),
    path("buy_now/<int:book_id>",views.buy_now,name='buy_now'),
    path("success",views.payment_success,name='success'),
    path("cancel",views.payment_cancel,name='cancel'),
]