from django.urls import path, include
from . import views
from shop.views import IndexView, RegisterView, LoginView, LogoutView, get_cart_dataView, change_quanView, payment_doneView, process_paymentView, payment_cancelledView, order_historyView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    #path("", views.index, name="index"),
    path("get_cart_data", get_cart_dataView.as_view(), name="get_cart_data"),
    #path("get_cart_data", views.get_cart_data, name="get_cart_data"),
    path("change_quan", change_quanView.as_view(), name="change_quan"),
    #path("change_quan", views.change_quan, name="change_quan"),
    #path("carts", add_to_cartView.as_view(), name="cart"),
    path("carts", views.add_to_cart, name="cart"),
    path("login", LoginView.as_view(), name="login"),
    #path("login", views.login, name="login"),
    path("register", RegisterView.as_view(), name="register"),
    #path("register", views.register, name="register"),
    path("logout", LogoutView.as_view(), name="logout"),
    #path("logout", views.logout, name="logout"),
    path("process_payment", process_paymentView.as_view(), name="process_payment"),
    #path("process_payment", views.process_payment, name="process_payment"),
    path("payment_done", payment_doneView.as_view(), name="payment_done"),
    #path("payment_done", views.payment_done, name="payment_done"),
    path("payment_cancelled", payment_cancelledView.as_view(), name="payment_cancelled"),
    #path("payment_cancelled", views.payment_cancelled, name="payment_cancelled"),
    path("order_history", order_historyView.as_view(), name="order_history"),
    #path("order_history", views.order_history, name="order_history"),
    
]