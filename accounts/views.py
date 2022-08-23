from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from .forms import LoginForm, UserCreationForm, UserChangeForm

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