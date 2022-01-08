from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from django.views import View
from django.contrib.auth.decorators import login_required
from .decorators import admin_only
from django.contrib import auth
from .models import *
from .forms import *
import urllib.request
import json
# def test111(request):
#     if request.method=='POST':
#         print(request.POST.get('submit'))
#     return render(request, 'login.html')
def login_register(request):
        if  request.user.is_authenticated:
            return redirect('home')
        if request.method=="POST":
            if request.POST.get('submit')=='Signup':
                print('regis')
                username=request.POST.get('username1')
                password=request.POST.get('password1')
                email=request.POST.get('email')
                password2=request.POST.get('password11')
                code=random.randint(100000000, 999999999)
                while User.objects.filter(code=code).exists():
                    code = random.randint(100000000, 999999999)
                if User.objects.filter(username=username).exists():
                    return redirect('login_register')
                if password==password2:
                    ur=User.objects.create_user(username=username, password=password, email=email)
                    ur.code=code
                    ur.save()
                    auth.login(request, ur)
                    return redirect('home')
                else:
                    return redirect('login_register')
            if request.POST.get('submit')=='Signin':
                print('log')
                username = request.POST.get('username2')
                password = request.POST.get('password2')
                my_user = authenticate(request, username=username, password=password)
                if my_user is None:
                    return redirect('login_register')
                else:
                    auth.login(request, my_user)
                    u=User.objects.get(username=username)
                    if u.is_admin==True:
                        print('log1')
                        return redirect('waitaccept')
                    else:
                        return redirect('home')
        return render(request, 'login.html')


# class login(View):
#     def get(self,request):
#         if not request.user.is_authenticated:
#             return render(request, 'dangnhap/dangnhap.html')
#         else:
#             return redirect('home')
#     def post(self,request):
#         username = request.POST.get('username')
#         password= request.POST.get('password')
#         my_user = authenticate(request, username=username,password=password)
#         if my_user is None:
#             return redirect('login')
#         else:
#             auth.login(request, my_user)
#             return redirect('home')
@login_required
def logout(request):
    auth.logout(request)
    return redirect('login_register')


def home(request):
    if not request.user.is_authenticated:
        return redirect('login_register')
    pro = Product.objects.filter(owner=0, pending=False)
    c = []
    s = []
    ci = []
    for i in pro:
        c.append(i.country)
        s.append(i.state)
        ci.append(i.city)
    c = list(set(c))
    s = list(set(s))
    ci = list(set(ci))
    if request.method=="POST":
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        product = []
        pro1 = Product.objects.filter(owner=0, pending=False)
        pr = []
        for i in pro1:
            if i.country == country:
                pr.append(i)
        pr1 = []
        pr2 = []
        if state != 'null':
            for i in pr:
                        if i.state == state:
                            pr1.append(i)
            if city=='null':
                print('check')
                product=pr1
            if city != 'null':
                for i in pr1:
                    if i.city == city:
                        pr2.append(i)
                print('cherwerfck')
                product=pr2

        else:
            product=pr

        pro=product
    context = {'pro': pro , 'c': c, 's': s, 'ci': ci}
    return render(request, 'home.html', context)

@login_required
def my_product(request):
    pro=Product.objects.filter(owner=request.user.code)
    for i in pro:
        print(i.owner)
    return render(request, 'my_product.html', {'pro': pro})

@login_required
def search(country, state, city):
    pro1=Product.objects.filter(owner=0)
    product=[]
    pr=[]
    for i in pro1:
        if i.country==country:
            pr.append(i)
    pr1=[]
    for i in pr:
        if state!=None:
            if i.state==state:
                pr1.append(i)
        else:
            product=pr
    pr2=[]
    for i in pr1:
        if i.city!=None:
            if i.city==city:
                pr2.append(i)
        else:
            product=pr1
    return product

@login_required
def cart(request, pk):
    pro=Product.objects.get(id=pk)
    btc = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    btc_request = urllib.request.urlopen(btc)
    btc_response = btc_request.read()
    btc_object=json.loads(btc_response.decode('utf-8'))
    btc_price=round(pro.prime/int(float(btc_object['price'])), 6)
    xmr = "https://api.binance.com/api/v3/ticker/price?symbol=XMRUSDT"
    xmr_request = urllib.request.urlopen(xmr)
    xmr_response = xmr_request.read()
    xmr_object = json.loads(xmr_response.decode('utf-8'))
    xmr_price=round(pro.prime/int(float(xmr_object['price'])), 5)
    if request.method=="POST":
        code11=request.user.code
        print(code11)
        pro = Product.objects.get(id=pk)
        pro.pending=True
        pro.save()
        waitaccept.objects.create(product=pro.code, user=code11)
        return render(request, 'pending.html', {'pro': pro})
    context={'pro': pro, 'btc':btc_price,  'xmr':xmr_price, 'btcrealtime':btc_object['price'], 'xmrrealtime':xmr_object['price'] }
    return render(request, 'cart.html', context)


@login_required
def orders(request):
    code=request.user.code
    pro=waitaccept.objects.filter(user=code)
    return render(request, 'orders.html', {'pro': pro})

@login_required
def buy(code, id):
    print('11')
    pro=Product.objects.get(id=id)
    print('12')
    waitaccept.objects.create(product=pro.code, user=code)
    print('13')

@admin_only
@login_required
def waitaccept1(request):
    count=waitaccept.objects.all()
    return render(request, 'count.html', {"count": count})

@admin_only
@login_required
def success(request, pk):
    print(pk)
    item=waitaccept.objects.get(id=pk)
    ur=User.objects.get(code=item.user)
    pro=Product.objects.get(code=item.product)
    pro.owner=ur.code
    pro.save()
    item.delete()
    return redirect('waitaccept')

@admin_only
@login_required
def cancel(request, pk):
    item=waitaccept.objects.get(id=pk)
    pro=Product.objects.get(code=item.product)
    pro.pending=False
    pro.save()
    item.delete()
    return redirect('waitaccept')

@admin_only
@login_required
def addproduct(request):
        if request.method=='POST':
            type_item = request.POST['type_item']
            country = request.POST['country']
            prime = request.POST['prime']
            state = request.POST['state']
            city = request.POST['city']
            information = request.POST['information']
            code = random.randint(1000000000, 9999999999)
            while Product.objects.filter(code=code).exists():
                code = random.randint(1000000000, 9999999999)
            if Product.objects.create(type_item=type_item, country=country, prime=prime, state=state, city=city, information=information, code=code):
                return HttpResponse('Success')
            else:
                return HttpResponse('Do not success')
        return render(request, 'addproduct.html')

@login_required
def profile(request):
    ur = User.objects.get(id=request.user.id)
    if request.method == "POST":
        password = request.POST['password']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2 and ur.check_password(password)==True:
            ur.set_password(password2)
            ur.save()
            ur2 = authenticate(username=ur.username, password=password2)
            auth.login(request, ur2)
            return redirect('/')
        else:
            return HttpResponse('Do not Success')
    return render(request, 'profile.html')


@login_required
def messages(request):
    return render(request, 'messages.html')