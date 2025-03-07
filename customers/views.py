from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm, ChangePasswordForm
from payment.forms import ShippingInfo
from payment.models import ShippingAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from payment.models import Order_item, Order
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .tokens import email_verification_token
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

#this decorator prevents signed users form accessing the register page 
#it checks if the user is authenticated and if it is sends it to home page 
#else allows user to access register page
#i am using this function in project's main url 
def user_not_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Redirect to the home page if the user is logged in
        return view_func(request, *args, **kwargs)
    return wrapper


@user_not_authenticated
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until it is verified
            user.save()
            user.refresh_from_db()
            user.profile.full_name = form.cleaned_data.get('full_name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            
            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message_html = render_to_string('account_activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': email_verification_token.make_token(user),
                        'language_code': request.LANGUAGE_CODE,  
                    })
            message_text = strip_tags(message_html)  # text version of the email
            to_email = form.cleaned_data.get('email')
            email = EmailMultiAlternatives(
            subject=mail_subject,
            body=message_text,
            from_email='no-reply@jerseys.ge',
            to=[to_email],
            )
            email.attach_alternative(message_html, "text/html") 
            # email.content_subtype = 'html' 
            email.send()
            
            return render(request, 'account_activation_sent.html')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')



@login_required
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated')
                login(request, current_user)
                return redirect('profile')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm (current_user)   
            return render(request, 'update_password.html', context={'form':form})


class CustomLoginView(LoginView):

    def get_success_url(self):
        # rdirect to the URL stored in the next parameter
        next_url = self.request.GET.get('next', '/')
        return next_url



@login_required
def profile(request):
    user_shipping_info = ShippingAddress.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        shippingInfo_form = ShippingInfo(request.POST, instance=user_shipping_info)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"{request.user.username} Your profile has been updated.")
            return redirect('profile')
        if shippingInfo_form.is_valid():
           shippingInfo_form.save()
           messages.success(request, f"{request.user.username} Your shipping Info has been updated.")
           return redirect('profile')
        
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        shippingInfo_form = ShippingInfo(instance=user_shipping_info)
    context = {
        'u_form': user_form,
        'p_form': profile_form,
        'shipping_info' : shippingInfo_form,
    }
    return render(request, 'profile.html', context)


@login_required
def my_orders(request):
    my_orders = Order.objects.filter(user=request.user).order_by('-date')
    my_items = Order_item.objects.filter(user=request.user)
    my_order_data = [
    {
        'order_id': my_order.pk,
        'order_desc': [
            {
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': item.price,
                'size': item.size,
            }
            for item in my_items if item.order == my_order
        ],
        'date': my_order.date,
        'status': my_order.shipped,
    }
    for my_order in my_orders
]
    paginator = Paginator(my_order_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    context = {
        'page_obj' : page_obj 
    }

    return render(request, 'my_orders.html', context)
