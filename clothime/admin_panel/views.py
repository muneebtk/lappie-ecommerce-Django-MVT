from itertools import product
from django.shortcuts import redirect, render
from category.models import Category
from store.models import Coupons
from store.models import HomeCarousel
from orders.models import Order
from orders.models import Order, OrderProduct, Payment
from user.models import user
from store.models import FeaturedProduct, Product,Variation
from django.contrib.auth import logout
from django.contrib import messages,auth
from . forms import CategoryForm, CouponsForm, FeaturedProductForm, OrderForm, ProductForm,AdminForm, VariationForm,HomeCarouselForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions.datetime import ExtractMonth
import calendar
from django.db.models import Sum

# views.

acc = user.objects.filter(is_superadmin=True)

@user_passes_test(lambda u:u in acc,login_url='home')
def admin_panel(request):
    form = AdminForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email,password=password)
            if user is not None:
                if user.is_superadmin:
                    auth.login(request,user)
                    # email = request.POST['email']
                    request.session['email'] = email
                    messages.success(request,'Successfully logged in..!')
                    return redirect('a_home')
                else:
                    messages.error(request,'Sorry, You are not an admin..!')
                    return redirect('home')
            else:
                messages.error(request,'Please enter valid credentials..!')
                return redirect('admin_panel')
        else:
            messages.error(request,'Something goes wrong..')
            return redirect('admin_panel')

    return render(request,'admin_panel/admin_panel.html')

@user_passes_test(lambda u:u in acc,login_url='home')
def a_home(request):
    order = Order.objects.order_by('-created_at').all()[0:6]
    user1 = user.objects.get(is_superadmin=True)
    # category = Category.objects.all()
    product = Product.objects.all()

    labels = []
    data = []
    for x in product:
        labels.append(x.product_name)
        data.append(x.stock)
    
    count = user.objects.all().exclude(is_superadmin=True).count()

    total_amount = Order.objects.filter(is_ordered=True)
    total_orders = 0
    amount = 0
    for x in total_amount:
        amount += x.order_total
        total_orders += 1
    amount = round(amount)

     # today sale
    order3 = Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
    order2 = order3.filter(is_ordered=True)
    month_number = []
    total_order_month = []
    for x in order2:
        month_number.append(calendar.month_name[x['month']])
        total_order_month.append(x['count'])

    cur_date = now().date()
    today_sales = Order.objects.filter(created_at__date=cur_date, is_ordered=True).aggregate(Sum('order_total'))
    today_sales_sum=today_sales['order_total__sum']
    today_sales_count = Order.objects.filter(created_at__date=cur_date,is_ordered=True).count()
    yesterday_sales = Order.objects.filter(is_ordered=True,created_at__date=cur_date-timedelta(days=1)).aggregate(Sum('order_total'))
    yesterday_sales_sum=yesterday_sales['order_total__sum']
    

    context= {
    'order' : order,
    'user':user1,
    'labels':labels,
    'data':data,
    'count':count,
    'amount':amount,
    'total_orders':total_orders,
    'today_sale_total':today_sales,
    'yesterday_sales_sum':yesterday_sales_sum,
    'today_total_orders':today_sales_count,
    'month_number':month_number,
    'total_order_month':total_order_month,
    'today_sales_sum':today_sales_sum,

    }
    return render(request,'admin_panel/home.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')
def a_orders(request):
    orders = Order.objects.order_by('-created_at').all()
    context = {
        'orders':orders
    }
    return render(request,'admin_panel/orders.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')
def a_users(request):
    users = user.objects.order_by('id').all().exclude(is_superadmin='True')
    count = users.count()
    context = {
        'users':users,
        'user_count':count,
    }
    return render(request,'admin_panel/users.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')
def a_products(request):
    products = Product.objects.order_by('created_date').all()
    context = {
        'products':products
    }
    return render(request,'admin_panel/products.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')
def a_category(request):
    category = Category.objects.order_by('id').all()
    context = {
        'category':category
    }
    return render(request,'admin_panel/category.html',context)



@user_passes_test(lambda u:u in acc,login_url='home')
def a_featured_product(request):
    featured_product = FeaturedProduct.objects.order_by('-id').all()
    context = {
        'featured_product':featured_product
    }
    return render(request,'admin_panel/featured_product.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')
def a_variation(request):
    variation = Variation.objects.all()
    count = variation.count()
    context = {
        'variation':variation,
        'count':count,
    }
    return render(request,'admin_panel/variation.html',context)


@user_passes_test(lambda u:u in acc,login_url='home')
def a_payment(request):
    payment = Payment.objects.order_by('-id').all()
    context = {
        'payment':payment,
    }
    return render(request,'admin_panel/payment.html',context)


@user_passes_test(lambda u:u in acc,login_url='home')
def a_order_product(request):
    order_product = OrderProduct.objects.order_by('-id').all()
    context = {
        'order_product':order_product
    }
    return render(request,'admin_panel/order_product.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')
def a_block_user(request,id):
    try:
        user1 = user.objects.get(id=id)
        user1.is_active = False
        user1.save()
        logout(user1)
        messages.success(request,f'Block user"{ user1.first_name }" successfully..')
        return redirect('a_users')
        
    except:
        messages.error(request,'something went wrong..')
        return redirect('a_users')

@user_passes_test(lambda u:u in acc,login_url='home')
def a_unblock_user(request,id):
    try:
        user1 = user.objects.get(id=id)
        user1.is_active = True
        user1.save()
        messages.success(request,f'User "{ user1.first_name }" unblocked successfully..')
        return redirect('a_users')
        
    except:
        messages.error(request,'something went wrong..')
        return redirect('a_users')

@user_passes_test(lambda u:u in acc,login_url='home')
def a_add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Product added successfully..')
            return redirect('a_products')
        else:
            messages.error(request,'Something goes wrong..')
    else:
        pass
    return render(request,'admin_panel/add_product.html',{'form':form})

@user_passes_test(lambda u:u in acc,login_url='home')
def a_delete_product(request,id):
    try:
        product = Product.objects.get(id=id)
        product.delete()
        messages.success(request,f'{ product.product_name } deleted successfully..')
        return redirect('a_products')
    except ObjectDoesNotExist:
        return redirect('a_products')

@user_passes_test(lambda u:u in acc,login_url='home')
def a_edit_product(request,id):
    product = Product.objects.get(id=id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,f'"{ product.product_name }" details has been changed.')
            return redirect('a_products')
        else:
            pass
    else:
        form = ProductForm(instance=product)
    return render(request,'admin_panel/edit_product.html',{'form':form,'product':product})

@user_passes_test(lambda u:u in acc,login_url='home')
def a_add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            try:
                product = Product.objects.order_by('-created_date').all()[0]
                messages.success(request,f'Category {product.category} added for "{ product.product}" ..')
                return redirect('a_category')
            except:
                pass
        else:
            messages.error(request,'something went wrong..please try again..')
            return redirect('a_category')

    context = {
        'form':form,
    }
    return render(request,'admin_panel/add_category.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')
def a_edit_category(request,id):
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,f'"{ category.category_name }" details has been changed..!')
            return redirect('a_category')
        else:
            messages.success(request,'Something went wrong.. please try again later..!')
    else:
        context = {
            'form':form,
            'category':category
        }
    return render(request,'admin_panel/edit_category.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')
def a_delete_category(request,id):
    try:
        item = Category.objects.get(id=id)
        item.delete()
        messages.success(request,f'"{ item.category_name }" has been removed..!')
        return redirect('a_category')
    except ObjectDoesNotExist:
        messages.error('Something went wrong.. Please try again.')
        return redirect('a_category')

@user_passes_test(lambda u:u in acc,login_url='home')
def a_profile(request):
    profile = user.objects.get(is_superadmin=True)
    context = {
        'profile':profile
    }
    return render(request,'admin_panel/profile.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')
def a_delete_variation(request,id):
    try:
        variation = Variation.objects.get(id=id)
        variation.delete()
        messages.success(request,f'Variation "{ variation.variation_value }" is removes from { variation.product }.')
        return redirect(a_variation)
    except ObjectDoesNotExist:
        messages.error(request,'Something went wrong.. Please try again')
        return redirect(a_variation)

@user_passes_test(lambda u:u in acc,login_url='home')
def a_add_variation(request):
    form = VariationForm()
    if request.method == 'POST':
        form = VariationForm(request.POST)
        product = request.POST['product']
        variation_value = request.POST['variation_value']
        if Variation.objects.filter(product=product,variation_value=variation_value).exists():
            messages.error(request,'The variation is already exists.')
            return redirect(a_variation)
        else:
            if form.is_valid():
                form.save()
                variation = Variation.objects.order_by('-created_date').all()[0]
                messages.success(request,f'Variation "{ variation.variation_value }" added for "{ variation.product }"successfully..')
                return redirect(a_variation)
            else:
                messages.error(request,'Something went wrong, Please try again..')
                return redirect(a_variation)
    else:
        form = VariationForm()
        context = {
            'form':form
        }
    return render(request,'admin_panel/add_variation.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')
def a_edit_variation(request,id):
    variation = Variation.objects.get(id=id)
    form = VariationForm(instance=variation)
    if request.method == 'POST':
        form = VariationForm(request.POST,instance=variation)
        variation_value = variation.variation_value
        product = variation.product
        if Variation.objects.filter(product=product,variation_value=variation_value).exists():
            messages.error(request,'The variation is already exists.')
            return redirect(a_variation)
        else:
            if form.is_valid():
                form.save()
                messages.success(request,f'Variation details has been chaged for "{ variation.product}" ..')
                return redirect(a_variation)
            else:
                messages.error(request,'Something went wrong, Please try again..!')
                return redirect(a_variation)
    else:
        pass
    context={
    'form': form,
    'variation':variation,
    }
    return render(request,'admin_panel/edit_variation.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_logout(request):
    if 'email' in request.session:
        request.session.flush()
        auth.logout(request)
        messages.success(request,'Logged out successfully..!')
        return redirect('home')
    else:
        auth.logout(request)
        messages.success(request,'logged out successfully ..')
        return redirect('home')

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_view_order(request,id):
    order = Order.objects.get(id=id)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid:
            form.save()
            messages.success(request,'Edit successful.')
            return redirect(a_orders)
        else:
            messages.error(request,'Something goes wrong.')
            return redirect(a_orders)
    
    context = {
        'order':order,  
        'form':form,
    }
    return render(request,'admin_panel/view_order.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_category_search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            category = Category.objects.order_by('id').filter(Q(category_name__icontains=keyword)|Q(description__icontains=keyword))
            count = category.count()
            context = {
            'category':category,
            'count':count,
            }    
            return render(request,'admin_panel/category.html',context)

        else:
            return redirect(a_category)
        
    else:
        return redirect(a_category)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_add_featured_product(request):
    form = FeaturedProductForm()
    if request.method == 'POST':
        form = FeaturedProductForm(request.POST)
        if form.is_valid():
            product = request.POST['product']
            if FeaturedProduct.objects.filter(product=product).exists():
                messages.error(request,f'The product "{product}" already exist in featured products')
                return redirect(a_featured_product)
            else:
                form.save()
                messages.success(request,f'Featured prodcut "{product} "Added successfully')
                return redirect(a_featured_product)
        else:
            messages.error(request,'Something went wrong..! please try again.')
            return redirect(a_featured_product)
    else:
        pass
    context = {
        'form':form
    }
    return render(request,'admin_panel/add_featured_product.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_delete_featured_product(request,id):
    try:
        product = FeaturedProduct.objects.get(id=id)
        product.delete()
        messages.success(request,'Product deleted successfully..')
        return redirect(a_featured_product)
    except ObjectDoesNotExist:
        messages.error(request,'Something went wrong.. Please try again.')
        return redirect(a_featured_product)

def a_order_search(request):
    orders = 0
    order_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            orders = Order.objects.order_by('id').filter(Q(order_number__icontains=keyword)|Q(status__icontains=keyword))
            order_count=orders.count()
            return redirect(a_orders)
        else:
             pass
    else:
        pass
    context={
        'orders':orders,
        'order_count':order_count,
    }
    return render(request,'admin_panel/orders.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_user_search(request):
    users = 0
    user_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            users= user.objects.order_by('id').filter(Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword)|Q(username__icontains=keyword))
            user_count = users.count()
        else:
            pass
    else:
        pass
    context = {
        'users':users,
        'user_count':user_count,
    }
    return render(request,'admin_panel/users.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_product_search(request):
    products = 0
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('id').filter(Q(product_name__icontains=keyword)|Q(description__icontains=keyword))
            product_count = products.count()
        else:
            pass
    else:
        pass
    context = {
        'products':products,
        'product_count':product_count,
    }
    return render(request,'admin_panel/products.html',context)


@user_passes_test(lambda u:u in acc,login_url='home')            
def a_coupons(request):
    coupon = Coupons.objects.all()
    context = {
        'coupon':coupon,
    } 
    return render(request,'admin_panel/coupons.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_delete_featured_product(request,id):
    try:
        coupon = Coupons.objects.get(id=id)
        coupon.delete()
        messages.success(request,'Coupon deleted successfully..')
        return redirect(a_coupons)
    except ObjectDoesNotExist:
        messages.error(request,'Something went wrong.. Please try again.')
        return redirect(a_coupons)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_add_coupon(request):
    form = CouponsForm()
    if request.method == 'POST':
        form = CouponsForm(request.POST)
        if form.is_valid():
            form.save()
            coupon = Coupons.objects.order_by('-created_at').all()[0]
            messages.success(request,f'Coupon added"{ coupon.coupon_name }" Successfully.')
            return redirect(a_coupons)
        else:
            messages.error(request,'Something goes wrong..!')
            return redirect(a_coupons)
    form = CouponsForm()
    context = {
        'form':form,
    }
    return render(request,'admin_panel/add_coupons.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_delete_coupon(request,id):
    try:
        coupon = Coupons.objects.get(id=id)
        coupon.delete()
        messages.success(request,'Coupon deleted successfully..')
        return redirect(a_coupons)
    except:
        messages.error(request,'Something went wrong, Please try again.')
        return redirect(a_coupons)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_home_carousel(request):
    home_carousel = HomeCarousel.objects.all()
    context = {
         'home_carousel':home_carousel,
    }
    return render(request,'admin_panel/home_carousel.html',context)


@user_passes_test(lambda u:u in acc,login_url='home')            
def a_add_home_carousel(request):
    form = HomeCarouselForm()
    if request.method == 'POST':
        form = HomeCarouselForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Carousel saved successfully..')
            return redirect(a_home_carousel)
        else:
            messages.error(request,'Something goes wrong..')
            return redirect(a_home_carousel)
    else:
        pass
    context = {
        'form':form,
    }
    return render(request,'admin_panel/add_home_carousel.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_edit_home_carousel(request,id):
    carousel = HomeCarousel.objects.get(id=id)
    form= HomeCarouselForm(instance=carousel)
    if request.method == 'POST':
        form = HomeCarouselForm(request.POST,instance=carousel)
        if form.is_valid():
            form.save()
            messages.success(request,f'Changes for "{carousel.main_text}" added')
            return redirect(a_home_carousel)
        else:
            messages.success(request,'Something goes wrong.please try again.!')
            return redirect(a_home_carousel)
    else:
        pass
    context = {
        'form':form,
        'carousel':carousel,
    }
    return render(request,'admin_panel/edit_home_carousel.html',context)

@user_passes_test(lambda u:u in acc,login_url='home')            
def a_delete_home_carousel(request,id):
    try:
        carousel = HomeCarousel.objects.get(id=id)
        carousel.delete()
        messages.success(request,'Item deleted successfully..')
        return redirect(a_home_carousel)
    except:
        messages.error(request,'Something goes wrong..please try again.!')
        return redirect(a_home_carousel)

def a_edit_coupon(request,id):
    coupon = Coupons.objects.get(id=id)
    form= CouponsForm(instance=coupon)
    if request.method == 'POST':
        form = CouponsForm(request.POST,instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request,f'Changes for "{coupon.coupon_name}" added')
            return redirect(a_coupons)
        else:
            messages.error(request,'Something goes wrong.please try again.!')
            return redirect(a_coupons)
    else:
        pass
    context = {
        'form':form,
        'coupon':coupon,
    }
    return render(request,'admin_panel/edit_coupon.html',context)










