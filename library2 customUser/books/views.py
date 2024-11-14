from django.shortcuts import render
from books.models import Book
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):

    return render(request,'home.html')
@login_required
def add_books(request):

    if(request.method=='POST'):
       t=request.POST['t']
       a = request.POST['a']
       pg = request.POST['pg']
       pr = request.POST['pr']
       la = request.POST['la']
       c=request.FILES['i']
       f=request.FILES['f']

       b=Book.objects.create(title=t,author=a,pages=pg,price=pr,Language=la,cover=c,pdf=f)
       b.save()
       return view_books(request)

    return render(request,'add.html')
@login_required
def view_books(request):
    k=Book.objects.all()
    return render(request,'view.html',{'book':k})
@login_required
def detail(request,i):
    k=Book.objects.get(id=i)
    return render(request,'detail.html',{'book':k})
@login_required
def edit(request,i):
    k = Book.objects.get(id=i)

    if (request.method == 'POST'):
        k.title=request.POST['t']
        k.author = request.POST['a']
        k.pages = request.POST['pg']
        k.price = request.POST['pr']
        k.Language = request.POST['la']

        if request.FILES.get('i')==None:
            k.save()
        else:
            k.cover = request.FILES.get('i')

        if request.FILES.get('f')==None:
            k.save()
        else:
            k.pdf = request.FILES.get('f')
        k.save()
        return view_books(request)



    return render(request, 'edit.html', {'book': k})

@login_required
def delete(request,i):
     k=Book.objects.get(id=i)
     k.delete()
     return view_books(request)
from django.db.models import Q
def search(request):
    k=None
    if(request.method=="POST"):
        query=request.POST['q']
        if query:
            k=Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query)) # it checks the title and author feild of every records
            # filter functions returns only matching records
    return render(request,'search.html',{'book':k})





