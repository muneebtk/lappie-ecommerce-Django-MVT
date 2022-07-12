from django.conf import settings
from django.shortcuts import redirect, render
from store.models import CouponUser
from store.models import Product
from orders.models import OrderProduct
from store. models import CartItem
from . models import Order, Payment
from orders.models import Address
import datetime
import razorpay
from django.contrib import messages



# views

def place_order(request,total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count<=0:
        return redirect('home')

    grand_total= 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total/100)
    coup=CouponUser.objects.filter(cur_user=request.user)
    discount = 0

    if coup:
        for x in coup:
            discount = x.coupon.discount_amount
        grand_total = (total-discount)+tax

    else:
        grand_total = total+tax
   

    address = 0
    orders = 0
    if request.method == 'POST':
        try:
            if 'address' in request.POST:
                address = request.POST['address']
                address = Address.objects.get(id=address)
                data = Order()
                data.user = current_user
                data.address = address
                data.order_total = grand_total
                data.tax = tax
                data.ip = request.META.get('REMOTE_ADDR')
                data.save()
                # generate order number
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d= datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d")
                order_number = current_date + str(data.id)
                request.session['order_number'] = order_number
                data.order_number = order_number
                data.save()
   
                orders = Order.objects.get(user= current_user, is_ordered =False, order_number=order_number)
            else:
                messages.error(request,'Please select an address to continue.')
                return redirect('checkout')
        except:
            messages.error(request,'Something goes wrong..please try again.')
            return redirect('checkout')
    else:
        pass
    context={
            'address': address,
            'orders' : orders,
            'cart_items': cart_items,
            'total': total,
            'quantity': quantity,
            'tax': tax,
            'grand_total': grand_total,
            'discount':discount,
                    }
    return render(request,'orders/place_order.html',context)    
def payments(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    grand_total = 0
    tax = 0
    quantity = 0
    total = 0
    amount = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
    tax = (2*total)/100
    if CouponUser.objects.filter(cur_user=request.user).exists():
        coup = CouponUser.objects.get(cur_user=request.user)
        discount = coup.coupon.discount_amount
        grand_total = int((total-discount)+tax)
    else:
        grand_total = int(total+tax)
    c_user = Order.objects.filter(user=request.user,is_ordered=True)
    
    if c_user :
        c = CouponUser.objects.filter(cur_user=request.user)
        c.delete()
    else:
        pass

    # grand_total = int(total + tax) * 100
    amount = grand_total*100



    # RazorPay
    
    client = razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_KEY))

    # create order
     
    response_payment = client.order.create(dict(amount=amount,currency='INR'))
    order_id = response_payment['id']
    order_status = response_payment['status']
    if order_status == 'created':
        pay=Payment()
        pay.user = current_user
        pay.amount_paid = grand_total
        pay.order_id = order_id
        pay.save()
    
        context = {
            'payment' : response_payment,
            'current_user':current_user,
            'grand_total':grand_total,
        }
        return render(request,'orders/payments.html',context)
    else:
        pass

    return render(request,'orders/payments.html')

def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature'],

    }
    # create client instance
    
    client = razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_KEY))
    try:
        status = client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(user=request.user,order_id = response['razorpay_order_id'])
        payment.payment_id = response['razorpay_payment_id']
        payment.paid = True
        payment.save()
        
        order_number = request.session['order_number']
        order = Order.objects.get(order_number=order_number)
        order.is_ordered = True
        order.payment = payment
        order.status = 'Completed'
        order.save()

        user = request.user
        cart_items = CartItem.objects.filter(user=user) 
        for cart_item in cart_items:
            pro_data = OrderProduct()
            pro_data.order_id = order.id
            pro_data.payment = payment
            pro_data.user_id = request.user.id
            pro_data.product_id = cart_item.product_id
            pro_data.quantity = cart_item.quantity
            pro_data.product_price = cart_item.product.price
            pro_data.ordered = True
            pro_data.save()

            # item = CartItem.objects.get(id=cart_item.id)
            # product_variation = item.variations.all()
            # pro_data = OrderProduct.objects.get(id=pro_data.id)
            # pro_data.variations.set(product_variation)
            # pro_data.save()

            pr = cart_item.product
            product = Product.objects.get(id=pr.id)
            product.stock -= cart_item.quantity
            product.save()
        cart_items.delete()
        return render(request,'orders/payment_success.html')
    except:
        status = client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id = response['razorpay_order_id'])
        payment.payment_id = response['razorpay_payment_id']
        payment.paid = False
        payment.save()
        
        order_number = request.session['order_number']
        order = Order.objects.get(order_number=order_number)
        order.is_ordered = False
        order.status = 'Failed'
        order.save()
        user = request.user
        cart_items = CartItem.objects.filter(user=user) 
        for cart_item in cart_items:
            product_variation = cart_items.variations.all()
            pro_data = OrderProduct()
            pro_data.order_id = order.id
            pro_data.payment = payment
            pro_data.user_id = request.user.id
            pro_data.product_id = cart_item.product_id
            pro_data.variations.set(product_variation)
            pro_data.quantity = cart_item.quantity
            pro_data.product_price = cart_item.product.price
            pro_data.ordered = True
            pro_data.save()


        return render(request,'orders/payment_failed.html')

def payment_success(request):
    return render(request,'orders/payment_success.html',)

def payment_failed(request):
    return render(request,'orders/payment_failed.html',)
    


