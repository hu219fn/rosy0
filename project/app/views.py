from django.shortcuts import HttpResponse, render, redirect
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from .forms import *

class SignupViews(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'auth/signup.html'
    success_url = '/'
    def form_valid(self, form):
        login(self.request, form.save())
        return redirect('/')
    
@login_required
def logoutViews(request):
    logout(request)
    return render(request, 'auth/logout.html')

def index(request):
    return render(request, 'index.html', {'items':Product.objects.all().order_by('-date')})

class Search_products(ListView):
    model = Product
    template_name = 'search_products.html'
    context_object_name = 'items'
    def get_queryset(self):
        search = self.request.GET['search_products']
        return Product.objects.filter(title__icontains=search).order_by('-date')

def makeup(request):
    return render(request, 'categories/makeup.html', {'items':Product.objects.filter(category='Makeup')})

def care_products(request):
    return render(request, 'categories/care_products.html', {'items':Product.objects.filter(category='Care Products')})

def perfumes(request):
    return render(request, 'categories/perfumes.html', {'items':Product.objects.filter(category='Perfumes')})

def presents(request):
    return render(request, 'categories/presents.html', {'items':Product.objects.filter(category='Presents')})

def men_clothes(request):
    return render(request, 'categories/men_clothes.html', {'items':Product.objects.filter(category='Men Clothes')})

def women_clothes(request):
    return render(request, 'categories/women_clothes.html', {'items':Product.objects.filter(category='Women Clothes')})

def girls_clothes(request):
    return render(request, 'categories/girls_clothes.html', {'items':Product.objects.filter(category='Girls\' Baby Clothes')})

def boys_clothes(request):
    return render(request, 'categories/boys_clothes.html', {'items':Product.objects.filter(category='boys\' Baby Clothes')})

def detail(request, id):
    item = Product.objects.get(id=id)
    if request.method == 'POST':
        Order.objects.create(
            title=item.title,
            caption=item.caption,
            price=int(item.price) * int(request.POST['count']),
            sell=item.sell,
            category=item.category,
            account = item.account,
            photo=item.photo,
            user = request.user,
            number = id,
            count = request.POST['count'],
        ).save()
        return redirect('/orders/')
    return render(request,'detail.html',{'item':item})

@login_required
def management(request):
    if request.user.username == 'rosy':
        return render(request, 'management.html', {'items':Product.objects.all(),'users':User.objects.all()})
    else:
        return redirect('/')

@login_required
def management_makeup(request):
    if request.user.username == 'rosy':
        return render(request, 'management.html', {'items':Product.objects.filter(category='Makeup')})
    else:
        return redirect('/')

@login_required
def management_careProducts(request):
    if request.user.username == 'rosy':
        return render(request, 'management.html', {'items':Product.objects.filter(category='Care Products')})
    else:
        return redirect('/')
        
@login_required
def management_perfumes(request):
    if request.user.username == 'rosy':
        return render(request, 'management.html', {'items':Product.objects.filter(category='Perfumes')})
    else:
        return redirect('/')
        
@login_required
def management_presents(request):
    if request.user.username == 'rosy':
        return render(request, 'management.html', {'items':Product.objects.filter(category='Presents')})
    else:
        return redirect('/')

@login_required
def management_men_clothes(request):
    if request.user.username == 'rosy':
        return render(request, 'management.html', {'items':Product.objects.filter(category='Men Clothes')})
    else:
        return redirect('/')
    
@login_required
def management_women_clothes(request):
    if request.user.username == 'rosy':
        return render(request, 'management.html', {'items':Product.objects.filter(category='Women Clothes')})
    else:
        return redirect('/')

@login_required
def management_girls_clothes(request):
    if request.user.username == 'rosy':
        return render(request, 'management.html', {'items':Product.objects.filter(category='Girls\' Baby Clothes')})
    else:
        return redirect('/')

@login_required
def management_boys_clothes(request):
    if request.user.username == 'rosy':
        return render(request, 'management.html', {'items':Product.objects.filter(category='Boys\' Baby Clothes')})
    else:
        return redirect('/')
    
@method_decorator(login_required, name='dispatch')
class CreateProduct(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'create_product.html'
    success_url = '/management/'

@login_required
def search_products_management(request):
    if request.user.username == 'rosy':
        return render(request, 'search_products_management.html',{'users':User.objects.all(),'items':Product.objects.filter(title__icontains=request.GET.get('search_products_management'))})
    else:
        return redirect('/')
    
@login_required
def search_users_management(request):
    if request.user.username == 'rosy':
        return render(request, 'search_users_management.html',{'users':User.objects.filter(username__icontains=request.GET.get('search_users_management')),'items':Product.objects.all()})
    else:
        return redirect('/')

@method_decorator(login_required, name='dispatch')
class UpdateProduct(UpdateView):
    model = Product
    fields = ['photo','sell']
    template_name = 'update_product.html'
    success_url = '/management/'

@login_required
def delete_product(request,id):
    if request.user.username == 'rosy':
        item = Product.objects.get(id=id)
        orders = Order.objects.filter(number=id)
        if request.method == 'POST':
            item.delete()
            for order in orders:
                order.delete()
            return redirect('/management/')
        return render(request, 'delete_product.html',{'item':item})
    else:
        return redirect('/')

@login_required
def orders_product(request, id):
    if request.user.username == 'rosy':
        item = Product.objects.get(id=id)
        orders = Order.objects.filter(number=id)
        return render(request, 'orders_product.html',{'items':orders,'product':item})
    else:
        return redirect('/')

@login_required
def delete_user(request, id):
    if request.user.username == 'rosy':
        user = User.objects.get(id=id)
        if request.method == 'POST':
            user.delete()
            return redirect('/management/')
        return render(request, 'delete_user.html',{'user':user})
    else:
        return redirect('/')

@login_required
def user(request, id):
    if request.user.username == 'rosy':
        user = User.objects.get(id=id)
        orders = Order.objects.filter(user=user)
        return render(request, 'user.html',{'user':user,'items1':orders.filter(account='𝑹𝑶𝑺𝒀 𝑺𝑻𝑶𝑹𝑬'),'items2':orders.filter(account='𝑽𝑰𝑪𝑻𝑶𝑹𝑰𝑨 𝑺𝑻𝑶𝑹𝑬')})
    else:
        return redirect('/')
    
@login_required
def orders(request):
    return render(request, 'orders.html',{'ordersROSY':Order.objects.filter(user=request.user,account='𝑹𝑶𝑺𝒀 𝑺𝑻𝑶𝑹𝑬'),'ordersVICTORIA':Order.objects.filter(user=request.user,account='𝑽𝑰𝑪𝑻𝑶𝑹𝑰𝑨 𝑺𝑻𝑶𝑹𝑬')})

@login_required
def order_delete(request, id):
    order = Order.objects.get(id=id)
    if request.user == order.user :
        order.delete()
        return redirect('/orders/')
    else:
        return redirect('/orders/')

def discounts(request):
    return render(request, 'disc/discounts.html',{'discounts':Sale.objects.all().order_by('-date')})

@method_decorator(login_required, name='dispatch')
class Discount_delete(DeleteView):
    model = Sale
    template_name = 'disc/delete.html'
    success_url = '/discounts/'

@method_decorator(login_required, name='dispatch')
class Discount_update(UpdateView):
    model = Sale
    fields = '__all__'
    template_name = 'disc/update.html'
    success_url = '/discounts/'
    
@method_decorator(login_required, name='dispatch')
class Discount_create(CreateView):
    model = Sale
    fields = '__all__'
    template_name = 'disc/create.html'
    success_url = '/discounts/'