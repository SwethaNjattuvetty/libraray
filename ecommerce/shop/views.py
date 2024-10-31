from shop.models import Category,Product
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
# Create your views here.
def allcategories(request):
    c=Category.objects.all()
    context={'cat':c}
    return render(request,'category.html',context)

def products(request,p):
    c=Category.objects.get(id=p)
    p= Product.objects.filter(category=c)
    context={'cat':c,'product':p}
    return render(request,'products.html',context)

def details(request,p):
    k = Product.objects.get(id=p)
    context={'detail':k}
    return render(request,'details.html',context)

# Create your views here.
def register(request):
    if request.method=="POST":
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['e']

        if (p==cp):
             u=User.objects.create_user(username=u,password=p,first_name=f,last_name=l,email=e)
             u.save()
        else:
             return HttpResponse("passwords are not same")

        return redirect('shop:login')
    return render(request,'register.html')
def user_login(request):
    if(request.method=="POST"):

        u = request.POST['u']
        p = request.POST['p']
        user = authenticate(username=u,password=p)
        if user:
            login(request,user)

            return redirect('shop:categories')
        else:
            messages.error(request,"invalid user name or password")
    return render(request,'login.html')


def user_logout(request):
    logout(request)
    return redirect('shop:login')


def addcategory(request):
    if request.method=='POST':
        name= request.POST['n']
        desc=request.POST['d']
        image=request.FILES['i']

        k=Category.objects.create(name=name,desc=desc,image=image)
        k.save()
        return redirect('shop:categories')
    return render(request,'add category.html')


def addproduct(request):
    if request.method=='POST':
        name= request.POST['n']
        desc=request.POST['d']
        image=request.FILES['i']
        price=request.POST['p']
        stock=request.POST['s']
        category = request.POST['c']
        m=Category.objects.get(name=category)
        k=Product.objects.create(name=name,desc=desc,image=image,price=price,stock=stock,category=m)
        k.save()

        return redirect('shop:categories')
    return render(request, 'add product.html')

def addstock(request,p):
    product=Product.objects.get(id=p)

    if request.method=="POST":
        product.stock=request.POST['n']
        product.save()
        return redirect('shop:categories')

    context={'pro':product}
    return render(request,'addstock.html',context)