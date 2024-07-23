from django.shortcuts import HttpResponse, render, redirect
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import *

class SignupViews(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'ar/auth/signup.html'
    success_url = '/ar/'
    def form_valid(self, form):
        login(self.request, form.save())
        return redirect('/')
    
@login_required(login_url='ar/register/login')
def logoutViews(request):
    logout(request)
    return render(request, 'ar/auth/logout.html')

def index(request):
    return render(request, 'ar/index.html', {'items':Product.objects.all().order_by('-date')})

class Search_products(ListView):
    model = Product
    template_name = 'ar/search_products.html'
    context_object_name = 'items'
    def get_queryset(self):
        search = self.request.GET['search_products']
        return Product.objects.filter(title__icontains=search).order_by('-date')

def makeup(request):
    return render(request, 'ar/categories/makeup.html', {'items':Product.objects.filter(category='Makeup')})

def care_products(request):
    return render(request, 'ar/categories/care_products.html', {'items':Product.objects.filter(category='Care Products')})

def perfumes(request):
    return render(request, 'ar/categories/perfumes.html', {'items':Product.objects.filter(category='Perfumes')})

def presents(request):
    return render(request, 'ar/categories/presents.html', {'items':Product.objects.filter(category='Presents')})

def men_clothes(request):
    return render(request, 'ar/categories/men_clothes.html', {'items':Product.objects.filter(category='Men Clothes')})

def women_clothes(request):
    return render(request, 'ar/categories/women_clothes.html', {'items':Product.objects.filter(category='Women Clothes')})

def girls_clothes(request):
    return render(request, 'ar/categories/girls_clothes.html', {'items':Product.objects.filter(category='Girls\' Baby Clothes')})

def boys_clothes(request):
    return render(request, 'ar/categories/boys_clothes.html', {'items':Product.objects.filter(category='boys\' Baby Clothes')})

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
        return redirect('/ar/orders/')
    return render(request,'ar/detail.html',{'item':item})

@login_required(login_url='ar/register/login')
def management(request):
    if request.user.username == 'rosy':
        return render(request, 'ar/management.html', {'items':Product.objects.all(),'users':User.objects.all()})
    else:
        return redirect('/ar/')

@login_required(login_url='ar/register/login')
def management_makeup(request):
    if request.user.username == 'rosy':
        return render(request, 'ar/management.html', {'items':Product.objects.filter(category='Makeup')})
    else:
        return redirect('/ar/')

@login_required(login_url='ar/register/login')
def management_careProducts(request):
    if request.user.username == 'rosy':
        return render(request, 'ar/management.html', {'items':Product.objects.filter(category='Care Products')})
    else:
        return redirect('/ar/')
        
@login_required(login_url='ar/register/login')
def management_perfumes(request):
    if request.user.username == 'rosy':
        return render(request, 'ar/management.html', {'items':Product.objects.filter(category='Perfumes')})
    else:
        return redirect('/ar/')
        
@login_required(login_url='ar/register/login')
def management_presents(request):
    if request.user.username == 'rosy':
        return render(request, 'ar/management.html', {'items':Product.objects.filter(category='Presents')})
    else:
        return redirect('/ar/')

@login_required(login_url='ar/register/login')
def management_men_clothes(request):
    if request.user.username == 'rosy':
        return render(request, 'ar/management.html', {'items':Product.objects.filter(category='Men Clothes')})
    else:
        return redirect('/ar/')
    
@login_required(login_url='ar/register/login')
def management_women_clothes(request):
    if request.user.username == 'rosy':
        return render(request, 'ar/management.html', {'items':Product.objects.filter(category='Women Clothes')})
    else:
        return redirect('/ar/')

@login_required(login_url='ar/register/login')
def management_girls_clothes(request):
    if request.user.username == 'rosy':
        return render(request, 'ar/management.html', {'items':Product.objects.filter(category='Girls\' Baby Clothes')})
    else:
        return redirect('/ar/')

@login_required(login_url='ar/register/login')
def management_boys_clothes(request):
    if request.user.username == 'rosy':
        return render(request, 'ar/management.html', {'items':Product.objects.filter(category='Boys\' Baby Clothes')})
    else:
        return redirect('/ar/')
    
@method_decorator(login_required, name='dispatch')
class CreateProduct(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'ar/create_product.html'
    success_url = '/ar/management/'

@login_required(login_url='ar/register/login')
def search_products_management(request):
    if request.user.username == 'rosy':
        return render(request, 'ar/search_products_management.html',{'users':User.objects.all(),'items':Product.objects.filter(title__icontains=request.GET.get('search_products_management'))})
    else:
        return redirect('/ar/')
    
@login_required(login_url='ar/register/login')
def search_users_management(request):
    if request.user.username == 'rosy':
        return render(request, 'ar/search_users_management.html',{'users':User.objects.filter(username__icontains=request.GET.get('search_users_management')),'items':Product.objects.all()})
    else:
        return redirect('/ar/')

@method_decorator(login_required, name='dispatch')
class UpdateProduct(UpdateView):
    model = Product
    fields = ['photo','sell']
    template_name = 'ar/update_product.html'
    success_url = '/ar/management/'

@login_required(login_url='ar/register/login')
def delete_product(request,id):
    if request.user.username == 'rosy':
        item = Product.objects.get(id=id)
        orders = Order.objects.filter(number=id)
        if request.method == 'POST':
            item.delete()
            for order in orders:
                order.delete()
            return redirect('/ar/management/')
        return render(request, 'ar/delete_product.html',{'item':item})
    else:
        return redirect('/ar/')

@login_required(login_url='ar/register/login')
def orders_product(request, id):
    if request.user.username == 'rosy':
        item = Product.objects.get(id=id)
        orders = Order.objects.filter(number=id)
        return render(request, 'ar/orders_product.html',{'items':orders,'product':item})
    else:
        return redirect('/ar/')

@login_required(login_url='ar/register/login')
def delete_user(request, id):
    if request.user.username == 'rosy':
        user = User.objects.get(id=id)
        if request.method == 'POST':
            user.delete()
            return redirect('/ar/management/')
        return render(request, 'ar/delete_user.html',{'user':user})
    else:
        return redirect('/ar/')

@login_required(login_url='ar/register/login')
def user(request, id):
    if request.user.username == 'rosy':
        user = User.objects.get(id=id)
        orders = Order.objects.filter(user=user)
        return render(request, 'ar/user.html',{'user':user,'items1':orders.filter(account='𝑹𝑶𝑺𝒀 𝑺𝑻𝑶𝑹𝑬'),'items2':orders.filter(account='𝑽𝑰𝑪𝑻𝑶𝑹𝑰𝑨 𝑺𝑻𝑶𝑹𝑬')})
    else:
        return redirect('/ar/')
    
@login_required(login_url='ar/register/login')
def orders(request):
    return render(request, 'ar/orders.html',{'ordersROSY':Order.objects.filter(user=request.user,account='𝑹𝑶𝑺𝒀 𝑺𝑻𝑶𝑹𝑬'),'ordersVICTORIA':Order.objects.filter(user=request.user,account='𝑽𝑰𝑪𝑻𝑶𝑹𝑰𝑨 𝑺𝑻𝑶𝑹𝑬')})

@login_required(login_url='ar/register/login')
def order_delete(request, id):
    order = Order.objects.get(id=id)
    if request.user == order.user :
        order.delete()
        return redirect('/ar/orders/')
    else:
        return redirect('/ar/orders/')

def discounts(request):
    return render(request, 'ar/disc/discounts.html',{'discounts':Sale.objects.all().order_by('-date')})

@method_decorator(login_required, name='dispatch')
class Discount_delete(DeleteView):
    model = Sale
    template_name = 'ar/disc/delete.html'
    success_url = '/ar/discounts/'

@method_decorator(login_required, name='dispatch')
class Discount_update(UpdateView):
    model = Sale
    fields = '__all__'
    template_name = 'ar/disc/update.html'
    success_url = '/ar/discounts/'
    
@method_decorator(login_required, name='dispatch')
class Discount_create(CreateView):
    model = Sale
    fields = '__all__'
    template_name = 'ar/disc/create.html'
    success_url = '/ar/discounts/'