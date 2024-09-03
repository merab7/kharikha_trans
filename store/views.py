from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductSize
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import translation
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
import os
from django.conf import settings

def home(request):
    # products = Product.objects.all().order_by('id')  # Order products by id (or another field)
    # paginator = Paginator(products, 5)  # Show 5 products per page
    # categories = Category.objects.all()
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    

    # # for category in categories:
    # #     if category.image:
    # #         image_exists = os.path.exists(os.path.join(settings.MEDIA_ROOT, category.image.path))
    # #         print(f"Category image path: {os.path.join(settings.MEDIA_ROOT, category.image.path)}")
    # #     else:
    # #         print("Category image does not exist")

    # context = {
    #     'page_obj': page_obj,
    #     'categories': categories
    # }
    products = Product.objects.all()

    context = {
        'page_obj': products
    }
    return render(request, 'home.html', context)


    return render(request, 'home.html', context)


# def load_products(request):
#     products = Product.objects.all()

#     context = {
#         'page_obj': products
#     }
#     return render(request, 'home.html', context)


def details(request, pk):
    product = Product.objects.get(id=pk)
    size_count = ProductSize.objects.filter(product=product)
    max_quantity = int()
    
    


    context = {
        'product' : product,
        'size_count': size_count,
        'max_quantity': max_quantity

    }

    return render(request, 'details.html', context=context)




def category(request, cat_name):
    category = Category.objects.get(name=cat_name)
    products = Product.objects.filter(Category=category)

    page_number = request.GET.get('page')
    page_obj = products

    context = {
        'page_obj': page_obj,
        'cat_name': cat_name,
        'category': category
    }

    return render(request, 'categories.html', context)


def max_quantity(request):

    if request.POST.get('action') == 'post':
        product_size = request.POST.get('product_size')
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        sized_product = ProductSize.objects.filter(product=product)
        print('yes')

        for x in sized_product:
            if x.size == product_size:
                max_quantity = x.quantity
                
             

        response = JsonResponse({ 'max_quantity': max_quantity})
        return response




def quantity(request):
  if request.POST.get('action') == 'post':
        product_size = request.POST.get('product_size')
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        sized_product = ProductSize.objects.filter(product=product)

        for x in sized_product:
            if x.size == product_size:
                product_quantity = x.quantity

            

        response = JsonResponse({'size': product_size, 'product_quantity': product_quantity})
        return response


def set_language(request, lang_code):
    user_language = lang_code
    translation.activate(user_language)
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
    return response




def search(request):

     if request.method == "POST":
        #get input box with the name searhced
        searched = request.POST['searched']
   
        #searched productes after seearched
        searched_products = Product.objects.filter(Q(name__icontains = searched)| Q(name_en__icontains = searched) | Q(description__icontains = searched)| Q(description_en__icontains = searched)| Q(cn__icontains = searched) | Q(cn_en__icontains = searched) )
        if searched_products:

            return render(request, 'search.html',  {'searched_products':searched_products})
        
        else:
            if request.LANGUAGE_CODE == 'ka':
               messages.success(request, f"{searched}, მსგავსი პროდუქტი ან კატეგორია არ არსებობს სცადეთ თავიდან")
               return render(request, 'search.html',  {})    
            else:
               messages.success(request, f"Product or Category like {searched} does not exist, try again") 
               return render(request, 'search.html',  {})    

            
     else:
        return render(request, 'search.html',  {})    
    

