from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length=100)
    caption = models.TextField(max_length=200, null=True, blank=True)
    price = models.IntegerField()
    sell = models.CharField(max_length=30,null=True, blank=True)
    category = models.CharField(max_length=50, choices={
        ('Makeup','Makeup'),
        ('Care Products','Care Products'),
        ('Perfumes','Perfumes'),
        ('Presents','Presents'),
        ('Men Clothes','Men Clothes'),
        ('Women Clothes','Women Clothes'),
        ('Girls\' Baby Clothes','Girls\' Baby Clothes'),
        ('Boys\' Baby Clothes','Boys\' Baby Clothes'),
    })
    account = models.CharField(max_length=50,choices={('𝑹𝑶𝑺𝒀 𝑺𝑻𝑶𝑹𝑬','𝑹𝑶𝑺𝒀 𝑺𝑻𝑶𝑹𝑬'),('𝑽𝑰𝑪𝑻𝑶𝑹𝑰𝑨 𝑺𝑻𝑶𝑹𝑬','𝑽𝑰𝑪𝑻𝑶𝑹𝑰𝑨 𝑺𝑻𝑶𝑹𝑬')})
    photo = models.ImageField(upload_to='p/')
    date = models.DateField(auto_now_add=True)
    class Meta :
        ordering = ["-date"]
    def __str__(self):
        return self.category

class Order(models.Model):
    title = models.CharField(max_length=100)
    caption = models.TextField(max_length=200, null=True, blank=True)
    price = models.IntegerField()
    sell = models.CharField(max_length=30,null=True, blank=True)
    category = models.CharField(max_length=50, choices={
        ('Makeup','Makeup'),
        ('Care Products','Care Products'),
        ('Perfumes','Perfumes'),
        ('Presents','Presents'),
        ('Men Clothes','Men Clothes'),
        ('Women Clothes','Women Clothes'),
        ('Girls\' Baby Clothes','Girls\' Baby Clothes'),
        ('Boys\' Baby Clothes','Boys\' Baby Clothes'),
    })
    account = models.CharField(max_length=50,choices={('𝑹𝑶𝑺𝒀 𝑺𝑻𝑶𝑹𝑬','𝑹𝑶𝑺𝒀 𝑺𝑻𝑶𝑹𝑬'),('𝑽𝑰𝑪𝑻𝑶𝑹𝑰𝑨 𝑺𝑻𝑶𝑹𝑬','𝑽𝑰𝑪𝑻𝑶𝑹𝑰𝑨 𝑺𝑻𝑶𝑹𝑬')})
    photo = models.ImageField(upload_to='p/')
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()
    count = models.IntegerField()
    class Meta :
        ordering = ["-date"]
    
class Sale(models.Model):
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    end_date = models.CharField(max_length=200)
    active = models.CharField(max_length=50,choices={('تعمل','تعمل'),('لا تعمل','لا تعمل')})
    class Meta :
        ordering = ["-date"]