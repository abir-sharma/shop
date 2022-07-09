from distutils import log
from email.headerregistry import ContentDispositionHeader
from operator import le
from unicodedata import category
import django
from django.shortcuts import redirect, render
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.db.models import Q
from django.http import JsonResponse    
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def sign_up(request):
    if request.method=='POST':
        fm=UserCreationForm(request.POST)
        if fm.is_valid():
            fm.save()
    else:
        fm=UserCreationForm()
    return render(request,'app/sign_up.html',{'form':fm})

class ProductView(View):
    def get(self,request):
        topwear=Product.objects.filter(category="TW")
        bottomwear=Product.objects.filter(category="BW")
        mobiles=Product.objects.filter(category='M')
        laptops=Product.objects.filter(category="L")
        return render(request,'app/home.html',{'topwear':topwear,'bottomwear':bottomwear,'mobiles':mobiles})


class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',{'product':product})

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulations !!! Registered Successfully")
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})
    
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulatios ! Profil Updated Succesfully")
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',{'add':add})
    
@login_required
def checkout(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/checkout.html',{'add':add})

def done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')
    
@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',{"op":op})

def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        total_items=len(cart_product)
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
            total_amount=amount+shipping_amount
        return render(request,'app/cart.html',{'carts':cart,'totalamount':total_amount,'amount':amount,'totalItems':total_items})
    else:
        msg="Nothing to Show in Cart"
        return render(request,'app/cart.html',{'msg':msg})

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    item_already_in_cart=False
    if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    if not item_already_in_cart:
        Cart(user=user,product=product).save()
    return redirect('/cart')

def removecart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'amount':amount,
            'totalamount':amount+shipping_amount,
            'lenght':len(cart_product)
        }
        return JsonResponse(data)

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)
