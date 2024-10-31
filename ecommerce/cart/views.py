from django.shortcuts import render,redirect
from cart.models import Cart,Order_details,Payment
from shop.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
import razorpay



@login_required


def cart(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        c=Cart.objects.get(product=p,user=u)
        if(p.stock>0):
           c.quantity+=1
           c.save()
           p.stock-=1
           p.save()
    except:
        if(p.stock>0):
           c=Cart.objects.create(product=p,user=u,quantity=1)
           c.save()
           p.stock-=1
           p.save()
    return redirect('cart:cartview')


@login_required

def cart_view(request):
    u=request.user
    total=0
    c=Cart.objects.filter(user=u)
    for i in c:
        total+=i.quantity * i.product.price
    context={'cart':c,'total':total}
    return render(request,'cart.html',context)


@login_required
def cartremove(request,i):

    p = Product.objects.get(id=i)
    u = request.user

    try:
        c=Cart.objects.get(user=u,product=p)
        if(c.quantity>1):
            c.quantity-=1
            c.save()
            p.stock+=1
            p.save()
        else:
            c.delete()
            p.stock += 1
            p.save()
    except:
        pass
    return redirect('cart:cartview')


@login_required
def remove(request,i):

    p = Product.objects.get(id=i)
    u = request.user

    try:
        c=Cart.objects.get(user=u,product=p)
        c.delete()
        p.stock+=c.quantity
        p.save()
    except:
        pass
    return redirect('cart:cartview')


@login_required
def order(request):
    if(request.method=="POST"):
        address=request.POST['a']
        phone=request.POST['p']
        pin=request.POST['pi']

        u=request.user
        c=Cart.objects.filter(user=u)

        total=0
        for i in c:
            total+=i.quantity*i.product.price
        total=int(total*100)
        print(total)


        client=razorpay.Client(auth=('rzp_test_XH7nCa2hZ300xG','a6B9Rmcr0PLahvSSUSUeYysg')) #creates a client connection
        # using razorpay id and secret code

        response_payment=client.order.create(dict(amount=total,currency="INR"))  #creates an order with razorpay using razorpay client
        print(response_payment)
        order_id=response_payment['id']  #Retrieves the order_id from response
        order_status=response_payment['status'] #retrive status from response
        if(order_status=="created"):  #if status is created then store order_id in payment and order_detail table
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=Order_details.objects.create(product=i.product,user=u,no_of_item=i.quantity,address=address,phoneno=phone,pin=pin,order_id=order_id)
                o.save()
        else:
            pass
        response_payment['name']=u.username
        context={'payment':response_payment}
        return render(request,'payment.html',context)



    return render(request,'order.html')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

def payment_status(request,u):
     user = User.objects.get(username=u)
     if (not request.user.is_authenticated):  # if user is not authenticated
          login(request, user)  # allowing request user to login


     if(request.method=="POST"):
        response=request.POST
        print(response)
        print(u)


        param_dict={
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature'],
        }

        client = razorpay.Client(auth=('rzp_test_XH7nCa2hZ300xG','a6B9Rmcr0PLahvSSUSUeYysg'))
        print(client)
        try:
            status=client.utility.verify_payment_signature(param_dict)
            print(status)

            p=Payment.objects.get(order_id=response['razorpay_order_id'])
            p.razorpay_payment_id=response['razorpay_payment_id']
            p.paid=True
            p.save()

            

            user=User.objects.get(username=u)
            o=Order_details.objects.filter(user=user,order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status='paid'
                i.save()

            # after sucessfull payment dlete cart item

            c=Cart.objects.filter(user=user)
            c.delete()

        except:
            pass
     return render(request,'payment_status.html',{'status':status})

def your_orders(request):
    u=request.user
    k=Order_details.objects.filter(user=u,payment_status="paid")

    context={'orders':k}
    return render(request,'your_orders.html',context)