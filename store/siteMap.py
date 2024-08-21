from django.contrib.sitemaps import Sitemap
from .models import Product, Category, ProductSize
from django.urls import reverse

class ProductSitemap(Sitemap):
    name = 'products'
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Product.objects.all()
    
    def location(self, item):
        return reverse('details', args=[item.pk])
    

class CategorySitemap(Sitemap):
    name = 'cat'
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Category.objects.all()
    
    def location(self, item):
        return reverse('category', args=[item.name])



class sizeSitemap(Sitemap):
    name = 'size'
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return ProductSize.objects.all()
    
    def location(self, item):
        return reverse('category', args=[item.name])

class StaticPageSitemap(Sitemap):
    name = 'static'
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['details', 'home', 'about', 'contact', 'category', 'login','signup']

    def location(self, item):
        return reverse(item)