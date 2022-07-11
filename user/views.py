from email.message import EmailMessage
from category.models import Category
from . models import user
from django.shortcuts import redirect, render
from .forms import EditProfileForm, RegistrationForm,VerifyForm
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

# verification email

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .verify import send
from .forms import  VerifyForm
from . import verify
import requests

from store . views import _cart_id
from store.models import CartItem, Cart
from orders.models import Order,OrderProduct




# views
# signup 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            password = form.cleaned_data['password']

            if user.objects.filter(phone_number=phone_number).exists():
                messages.error(request,'Phone Number already exists..')
                return redirect('register')
            else:
                user1 = user.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
                user1.phone_number = phone_number
                request.session['phone_number']=phone_number
                user1.save() 

            # send otp

                send(form.cleaned_data.get('phone_number'))
                messages.success(request,'we have sent you an otp..')
                return redirect('verify_code')
                

           
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request,'user/register.html',context) 

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user1 = auth.authenticate(email=email,password=password)
        if user1 is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists =  CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

# getting product variation by cart id

                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # get the cart items from the user to access his product variations

                    cart_item = CartItem.objects.filter(user=user1)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id =item_id)
                            item.quantity += 1
                            item.user=user1
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user1
                                item.save()


            except:
                pass
            auth.login(request,user1)
            messages.success(request,'you are logged in..')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
        else:
            messages.error(request,'Invalid Login Credentials..')
            return redirect('login')


    return render(request,'user/login.html') 

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'logged out successfully..')
    return redirect('home')

def home(request):
    return render(request,'user/home.html')

# Account activation

def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone_number=request.session['phone_number']

            user1=user.objects.get(phone_number=phone_number)
            user1.save()
            if verify.check(phone_number,code):
                user1.is_active = True
                user1.save()
                messages.success(request,'your account is verified..')
                return redirect('login')
            else:
                messages.error(request,'Invalid Otp')
                return redirect('verify_code')
    else:
        form = VerifyForm()
    return render(request,'user/verifycode.html',{'form':form})


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if user.objects.filter(email=email).exists():
            user1 = user.objects.get(email__iexact=email)
            
            # reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('user/reset_password_email.html',{
                'user': user1,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user1.pk)),
                'token' : default_token_generator.make_token(user1),
            })

            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('login') 

        else:
            messages.error(request,'Account does not exists..')
            return redirect('forgotpassword')
    return render(request,'user/forgotpassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user1 = user._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,user1.DoesNotExist):
        user1 = None

    if user1 is not None and default_token_generator.check_token(user1,token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
#Reset password


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user1 = user.objects.get(pk=uid)
            user1.set_password(password)
            user1.save()
            messages.success(request,'Password reset successful')
            return redirect('login')
        else:
            messages.error(request,'Your Password does not matching..')
            return redirect('resetpassword')
    else:
        return render(request,'user/resetpassword.html')
    

def account(request):
    orders = 0
    current_user=request.user
    user1=user.objects.get(email=current_user)
    order = Order.objects.filter(user=request.user,is_ordered=True)
    category = Category.objects.all()



    if order:
        orders = OrderProduct.objects.filter(user=request.user)

        count = orders.count()
    else:
        pass
        
    context={
        'user':user1,
        'orders':orders,
        'count':count,
        'order':order,
        'category':category,
    }

    return render(request,'user/profile.html',context)

def edit_account(request,id):
    current_user = user.objects.get(id=id)
    form = EditProfileForm(instance=current_user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST,instance=current_user)
        if form.is_valid():
            form.save()
            return redirect('account')

        else:
            pass
    context = {
        'form':form,
    }
    return render(request,'user/edit_account.html',context)

def orders(request):
    order = Order.objects.filter(user=request.user,is_ordered=True)
    category = Category.objects.all()
    orders = 0
    if order:
        orders = OrderProduct.objects.filter(user=request.user)

        count = orders.count()
    else:
        pass
    context = {
        'orders':orders,
        'count':count,
        'order':order,
        'category':category,
    }
    return render(request,'user/profile.html',context)
