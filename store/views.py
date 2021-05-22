from django.shortcuts import render
from .models import *
from .utils import *    
from django.http import JsonResponse
import json
import datetime
# Create your views here.

def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    page = 'store'
    products = Product.objects.all()

    return render(request, 'store/store.html', {
        'page': page,
        'products' : products,
        'cartItems':cartItems,
    })

def cart(request):
    page = 'cart'
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return render(request, 'store/cart.html', {
        'page': page,
        'items':items,
        'order':order,
        'cartItems':cartItems,
    })   

def checkOut(request):
    page = 'checkout'
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return render(request, 'store/checkout.html', {
        'page': page,
        'items':items,
        'order':order,
        'cartItems':cartItems,
    })     

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print (action, productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    #we use get or create quz if the order already exists we want to add to it not creat a new one
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1) 
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()

    if orderItem.quantity < 1:
        orderItem.delete()            

def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )


    return JsonResponse('payment complete', safe=False)