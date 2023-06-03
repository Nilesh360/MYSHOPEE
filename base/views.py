from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Product,Category,User
from .forms import ProductForm
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

# Create your views here.

def home(request):
    products = Product.objects.all()
    category = Category.objects.all()
    context={'products':products,'category':category}
    return render(request,'base/home.html',context)

def ProductView(request,pk):
    product = Product.objects.get(id=pk)
    context={'product':product}
    return render(request,'base/Product.html',context)

def updateProduct(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method=='POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/create_update_product.html',context)

def deleteProduct(request,pk):
    product = Product.objects.get(id=pk)
    if request.method=='POST':
        product.delete()
        return redirect('home')
    context = {'obj':product}
    return render(request,'base/delete_product.html',context)

def addProduct(request):
    form = ProductForm()
    if request.method=='POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/create_update_product.html',context)


def SearchedProduct(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    filter_products = Product.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(category__name__icontains=q)
    )
    category = Category.objects.all()
    current_category = q
    filter_product_count = filter_products.count()
    paginator = Paginator(filter_products, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context={'filter_product_count':filter_product_count,'filter_products':filter_products,'category':category,'page': page,'current_category':current_category,}
    response= render(request,'base/filtered_product.html',context)
    #response.set_cookie('key1',['val1','val2'])
    #response.delete_cookie('key1')
    return response

def LoginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        print(request.COOKIES.get('csrftoken'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Username or password does not exists')
        except:
            messages.error(request,'User does not exists')
    context={'page':page}
    return render(request,'base/login_register.html',context)


def logoutUser(request):
    logout(request)
    request.session.flush()
    return redirect('home')

def registerPage(request):
    page='register'
    form = UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occurred during registration")
    context = {'page':page,'form':form}
    return render(request,'base/login_register.html',context)

def navbar(request):
    categories = Category.objects.all()
    return {
        'categories': categories,
    }