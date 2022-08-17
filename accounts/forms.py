from email.policy import default
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class LoginForm(forms.Form):
    email =  forms.EmailField(max_length=30)
    password =  forms.CharField(widget=forms.PasswordInput)


class UserCreationForm(forms.ModelForm):

    #is_staff =  forms.BooleanField(label='Business Advisor', required=False)
    #is_superuser = forms.BooleanField(label='Admin', required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "organization",
            "is_staff",
            "is_superuser"
        )

        labels = {
            'is_staff': _('Business Advisor'),
            'is_superuser': _('Admin'),
        }
        help_texts = {
            'phone': _('Example: 250787734876'),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "organization",
            "is_staff",
            "is_superuser"
        )
        labels = {
            'is_staff': _('Business Advisor'),
            'is_superuser': _('Admin'),
        }
        help_texts = {
            'phone': _('Example: 250787734876'),
        }


