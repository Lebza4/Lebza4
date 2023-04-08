from django.shortcuts import render
from leboapp.models import Product
from math import ceil
from leboapp import keys

# Create your views here.
def home(request):
    current_user = request.user
    print (current_user)
    allProds =[]
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)  
        n = len(prod)
        nSlides = n // 4 + ceil(n / 4)-((n /4)) - ((n // 4)) 
        allProds.append([prod, range(1, int(nSlides)), int(nSlides)])
        
    params = {'allProds':allProds}
    return render(request,'index.html',params)
