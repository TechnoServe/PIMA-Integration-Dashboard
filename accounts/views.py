from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from .forms import LoginForm, UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from PIMA_Dashboard.settings import env

# Create your views here.

# def user_login(request):
#     form = LoginForm()

#     if request.method == 'POST':
#         form = LoginForm(request.POST)
        
#         if form.is_valid():
#             email = request.POST['email']
#             password =  request.POST['password']
#             user = authenticate(request, email=email, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.success(request, "Error: email or password")
#                 return redirect('login')

#         else:
#             messages.success(request, "Form is not valid")
#             return redirect('login')
    
#     else:
#         return render(request, 'registration/login.html', {'form':form})


def user_logout(request):
    logout(request)
    return redirect('login')

@user_passes_test(lambda user: user.is_superuser)
def create_user_account(request):
    context = {}

    if request.method == 'POST':
        form =  UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "User Created Successfully")
            return redirect('manage_users')

        else:
            context['form'] = form
    else:
        form =  UserCreationForm()
        context['form'] = form
    return render(request, 'registration/create_user.html', context=context )

@user_passes_test(lambda user: user.is_superuser)
def manage_users(request):
    user_object = get_user_model()
    users = user_object.objects.filter(is_active=True)
    context = {'users': users}
    return render(request, 'user_dash.html', context)


@user_passes_test(lambda user: user.is_superuser)
def edit_user(request, id):
    user_object = get_user_model()
    user_ = user_object.objects.get(id=id)

    if request.method == 'POST':
        form =  UserChangeForm(request.POST, instance=user_)

        if form.is_valid():
            form.save()
            messages.success(request, "User edited Successfully")
            return redirect('manage_users')
        
    else:
        form =  UserChangeForm(instance=user_)
        context = {'form': form }
        return render(request, 'registration/edit_user.html', context)





@user_passes_test(lambda user: user.is_superuser)
def delete_user(request, id):

    user_object = get_user_model()

    try:
        u = user_object.objects.get(id=id)
        u.is_active = False
        u.save()
        messages.success(request, "User is deleted successfully")
        return redirect('manage_users')

    except user_object.DoesNotExist:
        messages.error(request, "User doesnot exist")    
        return redirect('manage_users')

    except Exception as e: 
        messages.error(request, "There are some errors")    
        return redirect('manage_users')



def password_reset_request(request):
    
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        
        if password_reset_form.is_valid():
            user_object = get_user_model()
            data = password_reset_form.cleaned_data['email']
            associated_users = user_object.objects.filter(Q(email=data))
            
            if associated_users.exists():
                for user in associated_users:
                    
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
					
                    opts = {
                        'email': user.email,
                        'domain': env('SITE_DOMAIN'),
                        'site_name': 'PIMA Dashboard',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': env('SITE_WEB_PROTOCOL'),
                    }
                    email = render_to_string(email_template_name, opts)

                    try:
                        send_mail(subject, email, env('EMAIL_USER') , [user.email], fail_silently=False)    
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
					
            return redirect ("password_reset_done")

    password_reset_form = PasswordResetForm()

    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})