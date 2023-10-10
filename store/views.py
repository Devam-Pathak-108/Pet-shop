from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.shortcuts import get_object_or_404


# Create your views here.

def contactUs(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer= customer, complete = False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
        
    else :
        items= []
        order = {"get_cart_total":0, "get_cart_items":0}
        cartItems= order['get_cart_items']

    context ={ 'cartItems':cartItems, 'shipping':False,'product':productDetails}
    return render(request, 'store/contactUs.html',context)

def productDetails(request,productName):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer= customer, complete = False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
        
    else :
        items= []
        order = {"get_cart_total":0, "get_cart_items":0}
        cartItems= order['get_cart_items']

    
    productDetails = Product.objects.get(name = productName)
    context ={ 'cartItems':cartItems, 'shipping':False,'product':productDetails}
    return render(request, 'store/productDetails.html',context)

def home(request):
    
    if request.user.is_authenticated:
        customer,created = Customer.objects.get_or_create(user=request.user, name=request.user)
        # customer = request.user.customer
        order , created = Order.objects.get_or_create(customer= customer, complete = False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
        
    else :
        items= []
        order = {"get_cart_total":0, "get_cart_items":0}
        cartItems= order['get_cart_items']

    
    context ={ 'cartItems':cartItems, 'shipping':False}
    return render(request,'store/home.html',context)

def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'store/signup.html', {'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'store/signup.html', 
                 {'form':UserCreationForm,
                 'error':'Username already taken. Choose new username.'})
        else:
            return render(request, 'store/signup.html', 
             {'form':UserCreationForm, 'error':'Passwords do not match'})


def logoutaccount(request):        
    logout(request)
    return redirect('store')

def loginaccount(request):    
    if request.method == 'GET':
        return render(request, 'store/login.html', 
                      {'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request,'store/login.html', 
                    {'form': AuthenticationForm(), 
                    'error': 'username and password do not match'})
        else: 
            login(request,user)
            return redirect('store')
    

def store(request):
    
    if request.user.is_authenticated:
        customer,created = Customer.objects.get_or_create(user=request.user, name=request.user)
        # customer = request.user.customer
        order , created = Order.objects.get_or_create(customer= customer, complete = False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
        
    else :
        items= []
        order = {"get_cart_total":0, "get_cart_items":0}
        cartItems= order['get_cart_items']

    searchProduct= request.GET.get('searchProduct')
    if searchProduct:
        selectedProduct = Product.objects.filter(name__icontains = searchProduct)
    else:
        selectedProduct= False
    
    products = Product.objects.all()
    context ={"Products":products, 'cartItems':cartItems, 'shipping':False, 'searchProducts':selectedProduct}
    return render(request,'store/store.html',context)

def cart(request):
    
    if request.user.is_authenticated:
        customer,created = Customer.objects.get_or_create(user=request.user, name=request.user)
        # customer = request.user.customer
        order , created = Order.objects.get_or_create(customer= customer, complete = False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
        
    else :
        items= []
        order = {"get_cart_total":0, "get_cart_items":0}
        cartItems= order['get_cart_items']

    
    context ={"items": items, "order":order,'cartItems':cartItems, 'shipping':False}
    return render(request,'store/cart.html',context)

def checkout(request):
    
    
    if request.user.is_authenticated:
        customer,created = Customer.objects.get_or_create(user=request.user, name=request.user)
        # customer = request.user.customer
        order , created = Order.objects.get_or_create(customer= customer, complete = False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
        
    else :
        items= []
        order = {"get_cart_total":0, "get_cart_items":0}
        cartItems= order['get_cart_items']

    
    context ={"items": items, "order":order,'cartItems':cartItems,  'shipping':False}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print(productId)
    print(action)
    customer,created = Customer.objects.get_or_create(user=request.user, name=request.user)
    # customer = request.user.customer
    product = Product.objects.get(id=productId)
    order , created = Order.objects.get_or_create(customer= customer, complete = False)
    orderItem , created= OrderItem.objects.get_or_create(order = order, product= product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action =="remove":
        orderItem.quantity=  (orderItem.quantity-1)
    
    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse("Item was added ", safe = False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer,created = Customer.objects.get_or_create(user=request.user, name=request.user)
        # customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer, complete = False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode']
            )
        # print(data['shipping']['address'])
        
    else:
        print("user not loged in")
    return JsonResponse("payment made", safe = False)
