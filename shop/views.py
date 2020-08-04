from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import product, imageslider, cart, Order
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views import View

# Create your views here.
class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        products = product.objects.all()
        slider = imageslider.objects.all()
        params = {'products': products, 'slider': slider}
        return render(request, 'index.html', params)
'''
def index(request):
    products = product.objects.all()
    slider = imageslider.objects.all()
    params = {'products': products, 'slider': slider}
    return render(request, 'index.html', params)
'''     

def add_to_cart(request):
    context = {}
    items = cart.objects.filter(user__id=request.user.id, status=False)
    context['items'] = items
    if request.user.is_authenticated:
        if request.method == "POST":
            pid = request.POST['pid']
            qty = request.POST['qty']
            is_exist = cart.objects.filter(
                products__id=pid, user__id=request.user.id, status=False)
            if len(is_exist) > 0:
                context['msg'] = 'Product alreaday exists in cart'
                context['cls'] = 'alert alert-warning'
            else:
                products = get_object_or_404(product, id=pid)
                usr = get_object_or_404(User, id=request.user.id)
                c = cart(user=usr, products=products, quantity=qty)
                c.save()
                context['msg'] = 'Product Added to cart'
                context['cls'] = 'alert alert-success'
    else:
        context['status'] = 'Login Required to view cart'

    return render(request, 'cart.html', context)


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(
                    request, 'Username already taken Try other username')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print('Account created')
                return redirect('/')
        else:
            messages.info(request, 'Password Dosent matching ')
            return redirect('register')
    def get(self, request, *args, **kwargs):
         return render(request, 'register.html')
        
'''
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(
                    request, 'Username already taken Try other username')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print('Account created')
                return redirect('/')
        else:
            messages.info(request, 'Password Dosent matching ')
            return redirect('register')

    else:
        return render(request, 'register.html')
'''
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Password not matching ')
            return redirect('login')
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

'''
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Password not matching ')
            return redirect('login')
    else:
        return render(request, 'login.html')
'''
class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('login')
'''
def logout(request):
    auth.logout(request)
    return redirect('login')

'''
class get_cart_dataView(APIView):
    def get(self, request, *args, **kwargs):
        items = cart.objects.filter(user__id=request.user.id, status=False)
        total, quantity = 0, 0
        for i in items:
            total += float(i.products.final_price) * float(i.quantity)
            quantity += int(i.quantity)

        res = {
            "total": total, "quan": quantity,
        }
        return JsonResponse(res)
'''
def get_cart_data(request):
    items = cart.objects.filter(user__id=request.user.id, status=False)
    total, quantity = 0, 0
    for i in items:
        total += float(i.products.final_price) * float(i.quantity)
        quantity += int(i.quantity)

    res = {
        "total": total, "quan": quantity,
    }
    return JsonResponse(res)
'''
class change_quanView(APIView):
    def get(self, request, *args, **kwargs):
        if 'quantity' in request.GET:
            cid = request.GET["cid"]
            qty = request.GET["quantity"]
            cart_obj = get_object_or_404(cart, id=cid)
            cart_obj.quantity = qty
            cart_obj.save()
            return HttpResponse(cart_obj.quantity)

        if 'delete_cart' in request.GET:
            id = request.GET['delete_cart']
            cart_obj = get_object_or_404(cart, id=id)
            cart_obj.delete()
            return HttpResponse(1)
'''
def change_quan(request):
    if 'quantity' in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(cart, id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)

    if 'delete_cart' in request.GET:
        id = request.GET['delete_cart']
        cart_obj = get_object_or_404(cart, id=id)
        cart_obj.delete()
        return HttpResponse(1)
'''
class process_paymentView(APIView):
    def get(self, request, *args, **kwargs):
        items = cart.objects.filter(user__id=request.user.id, status=False)
        products = ""
        amt = 0
        inv = "INV1001-"
        cart_ids =""
        p_ids =""
        for j in items:
            products += str(j.products.product_name)+ "\n"
            p_ids += str(j.products.id) +","
            amt += float(j.products.final_price)
            inv += str(j.id)
            cart_ids += str(j.id)+","
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': str(amt),
            'item_name': products,
            'invoice':inv,
            'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                            reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                            reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                                reverse('payment_cancelled')),  
        }
        usr = User.objects.get(username=request.user.username)
        ord = Order(cust_id=usr,cart_ids=cart_ids,product_ids=p_ids)
        ord.save()
        ord.invoice_id = str(ord.id)+inv
        ord.save()
        request.session["order_id"] = ord.id

        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'process_payment.html', { 'form': form})
'''
def process_payment(request):
    items = cart.objects.filter(user__id=request.user.id, status=False)
    products = ""
    amt = 0
    inv = "INV1001-"
    cart_ids =""
    p_ids =""
    for j in items:
        products += str(j.products.product_name)+ "\n"
        p_ids += str(j.products.id) +","
        amt += float(j.products.final_price)
        inv += str(j.id)
        cart_ids += str(j.id)+","
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amt),
        'item_name': products,
        'invoice':inv,
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              reverse('payment_cancelled')),  
    }
    usr = User.objects.get(username=request.user.username)
    ord = Order(cust_id=usr,cart_ids=cart_ids,product_ids=p_ids)
    ord.save()
    ord.invoice_id = str(ord.id)+inv
    ord.save()
    request.session["order_id"] = ord.id

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', { 'form': form})
'''
class payment_doneView(APIView):
    def get(self, request, *args, **kwargs):
        if "order_id" in request.session:
            order_id = request.session["order_id"]
            ord_obj = get_object_or_404(Order,id=order_id)
            ord_obj.status=True
            ord_obj.save()
        
            for i in ord_obj.cart_ids.split(",")[:-1]:
                cart_object = cart.objects.get(id=i)
                cart_object.status=True
                cart_object.save()

        return render(request, 'success.html')
'''
def payment_done(request):
    if "order_id" in request.session:
        order_id = request.session["order_id"]
        ord_obj = get_object_or_404(Order,id=order_id)
        ord_obj.status=True
        ord_obj.save()
        
        for i in ord_obj.cart_ids.split(",")[:-1]:
            cart_object = cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()

    return render(request, 'success.html')
'''
class payment_cancelledView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'unsuccess.html')
'''
def payment_cancelled(request):
    return render(request, 'unsuccess.html')
'''

class order_historyView(View):
    def get(self, request, *args, **kwargs):
        context ={}
        all_orders = []
        orders = Order.objects.filter(cust_id__id=request.user.id).order_by("-id")
        for order in orders:
            products = []
            for id in order.product_ids.split(",")[:-1]:
                pro = get_object_or_404(product, id=id)
                products.append(pro)
            ord = {
                "order_id":order.id,
                "products":products,
                "invoice":order.invoice_ids,
                "status":order.status,
                "date":order.processed_on,
            }
            all_orders.append(ord)
        context["order_history"] = all_orders
        return render(request, 'profile.html', context)

'''
def order_history(request):
    context ={}
    all_orders = []
    orders = Order.objects.filter(cust_id__id=request.user.id).order_by("-id")
    for order in orders:
        products = []
        for id in order.product_ids.split(",")[:-1]:
            pro = get_object_or_404(product, id=id)
            products.append(pro)
        ord = {
            "order_id":order.id,
            "products":products,
            "invoice":order.invoice_ids,
            "status":order.status,
            "date":order.processed_on,
        }
        all_orders.append(ord)
    context["order_history"] = all_orders
    return render(request, 'profile.html', context)
'''