
from django.shortcuts import get_object_or_404, redirect, render
from orders.models import Address

from store.forms import AddressForm
from . models import CartItem, CouponUser, Coupons, Product,Cart, Variation, Wishlist
from category.models import Category
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from orders.models import Order
from django.contrib import messages


# Create your views here.


def store(request,category_slug = None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category , slug=category_slug)
        products = Product.objects.all().filter(category=categories,is_available = True)
        paginator = Paginator(products,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        if request.method=='POST':
            sort = request.POST['sort']
            if sort == 'high':
                products = Product.objects.filter(category=categories,is_available = True).order_by('-price')
                paginator = Paginator(products,8)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
                product_count = products.count()
            else:
                products = Product.objects.filter(category=categories,is_available = True).order_by('price')
                paginator = Paginator(products,8)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
                product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        if request.method == 'POST':
            sort = request.POST['sort']
            if sort == 'high':
                products = Product.objects.filter(is_available = True).order_by('-price')
                paginator = Paginator(products,8)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
                product_count = products.count()
            
            else:
                products = Product.objects.filter(is_available = True).order_by('price')
                paginator = Paginator(products,8)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
                product_count = products.count()

    context = {
        'products': paged_products,
        'product_count' : product_count,

    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug,slug = product_slug)
        related_product = Product.objects.filter(category__slug = category_slug).exclude(category__slug = category_slug,slug = product_slug)[0:6]
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()

    except Exception as e:
        raise e


    context = {
        'single_product' : single_product ,
        'in_cart': in_cart,
        'related_product':related_product,
    }
    return render(request,'store/product_detail.html',context)

# cart views

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# adding an item to cart

def add_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variation = []
        if request.method=='POST':
            for item in request.POST:
                key = item 
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        else:
            messages.error(request,'Please select a variation to continue')
            return redirect(product_detail)

      
        is_cart_item_exists =  CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists :
            cart_item = CartItem.objects.filter(product=product,user=current_user)
            

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product,quantity=1, user=current_user)
                if len(product_variation ) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    # item.variations.add(item)     
                item.save()


        else:
            cart_item = CartItem.objects.create(product = product,quantity=1,user=current_user)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')

    else:
        product_variation = []
        if request.method=='POST':
            for item in request.POST:
                key = item 
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        else:
            messages.error(request,'Please select a variation to continue.')
            return redirect(product_detail)

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()

        # variations 

        is_cart_item_exists =  CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exists :
            cart_item = CartItem.objects.filter(product=product,cart=cart)
            

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product,quantity=1, cart=cart)
                if len(product_variation )> 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    item.variations.add(item)     
                item.save()


        else:
            cart_item = CartItem.objects.create(product = product,quantity=1,cart=cart)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')

# deleting item from cart

def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product,id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product,cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id, cart_item_id):
    
    product = get_object_or_404(Product,id = product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        coupon = 0
        if request.user.is_authenticated:                    
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
                total += (cart_item.product.price*cart_item.quantity)
                quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total+tax
        coupon = 0
        discount_amount = 0
        if request.method == 'POST':
            if 'code' in request.POST:
                if Order.objects.filter(user=request.user,is_ordered ="True").exists():
                    messages.error(request,'Sorry,You are not eligible for this coupen..')
                    return redirect('cart')
                else:
                    code = request.POST['code']
                    if Coupons.objects.filter(coupon_name=code).exists():
                        coupon = Coupons.objects.get(coupon_name=code)
                        limit=coupon.limit
                        discount_amount = coupon.discount_amount
                        if total >= limit:
                            if not CouponUser.objects.filter(cur_user=request.user).exists():
                                x = CouponUser()
                                x.cur_user = request.user
                                x.coupon = coupon
                                x.save()
                            else:
                                pass
                            grand_total = (total-discount_amount)+tax
                            
                        else:
                            grand_total = total+tax
                            messages.error(request,f'Buy for above "{coupon.limit}" to get the offer.')
                            return redirect('cart')
                    else:
                        messages.error(request,'That is a wrong code.')
                        return redirect('cart') 
            else:                     
               pass
        else:
            pass
        coupon1 = Coupons.objects.all()
        tax = (2*total)/100
        grand_total = int(grand_total)

    except ObjectDoesNotExist:
        pass
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total': grand_total, 
        'coupon':coupon,
        'coupon1':coupon1,
        'discount':discount_amount,
    }

    return render(request,'store/cart.html',context)


@login_required(login_url='login')
def wishlist(request):
    current_user=request.user
    products = Wishlist.objects.filter(user=current_user)
    context = {
        'products' : products,
    }

    return render(request,'store/wishlist.html',context)

@login_required(login_url='login')
def add_wishlist(request,product_id):
    data=Wishlist()
    current_user=request.user
    product= Product.objects.get(id=product_id)
    wish = Wishlist.objects.filter(user=current_user,product=product).exists()

    if not wish:
        product = Product.objects.get(id=product_id)
        data.product = product
        data.user = current_user
        data.save()
    return redirect('wishlist')

def remove_wishlist_item(request,product_id):
    user=request.user
    product = Wishlist.objects.get(id=product_id)
    product.delete()
    return redirect('wishlist')

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('is_available').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context={
        'products' : products,
        'product_count': product_count,
    }
    return render(request,'store/store.html',context)

@login_required(login_url='login')
def checkout(request,  total=0, quantity=0, cart_items=None):
    address = 0
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = Address()
            data.user=request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.pincode = form.cleaned_data['pincode']   
            data.save()
            return redirect('checkout')
        else:
            pass            

    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:  # user authentication 
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
            address = Address.objects.filter(user=request.user)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100

        # coup = CouponUser.objects.get(cur_user=request.user)
        # print(coup,',,,,,,,,,,,,,,,,,,,,,,,,')
        # if coup:
        #     total -= coup.coupon.discount_amount
        #     grand_total = int(total+tax)
        #     print(grand_total,'///////////////////////')

        # else:
        #     print(grand_total,'///////////////////////')
        #     grand_total = total+tax  

    except ObjectDoesNotExist:
        pass
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total': grand_total, 
        'address' : address,
    }
    return render(request,'store/checkout.html',context)

def delete_address(request,id):
    try:
        address = Address.objects.get(id=id)
        address.delete()
        return redirect('checkout')
    except:
        pass

def orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders':orders,
    }
    return render(request,'')

# def coupens(request):
#     coupen = Coupens.objects.all()
#     cart_items = CartItem.objects.filter(user=request.user,is_available=True)
#     for x in cart_items:
#         total = x.product.price*x.quantity


    

    

