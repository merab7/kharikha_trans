from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from customers.views import user_not_authenticated, CustomLoginView
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.views.generic.base import TemplateView 


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('', include('payment.urls')),
    path('', include('customers.urls')),
    path('', include('card.urls')),
     path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', login_required(auth_views.LogoutView.as_view(template_name='logout.html')), name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "reset_password.html"), name ='reset_password'),
        path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name ='password_reset_complete'),
     path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "google2d988332cc1b49f0.html",
        TemplateView.as_view(template_name="google2d988332cc1b49f0.html"),
    ),
        path(
        "new_sitemap.xml",
        TemplateView.as_view(template_name="new_sitemap.xml"),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)