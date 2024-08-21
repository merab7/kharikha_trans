from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap, index
from .siteMap import ProductSitemap, CategorySitemap, sizeSitemap,StaticPageSitemap

sitemaps = {
    ProductSitemap.name: ProductSitemap,
    CategorySitemap.name: CategorySitemap,
    sizeSitemap.name: sizeSitemap,
    StaticPageSitemap.name: StaticPageSitemap
}



urlpatterns = [
    path('', views.home, name='home'),
    path('load-products/', views.load_products, name='load_products'),
    path('product/<int:pk>', views.details, name='details'),
    path('product/<cat_name>', views.category, name='category'),
    path('quantity', views.quantity, name='quantity'),
    path('max_quantity', views.max_quantity, name='max_quantity'),
    path('set_language/<str:lang_code>/', views.set_language, name='set_language'),
    path('search', views.search, name='search'),
    path('sitemap.xml', index, {'sitemaps': sitemaps}, name='sitemap-index'),
    path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
   
]