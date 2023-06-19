from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser


class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = get_user_model()
        fields = ['email']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','phone','email')

    def __init__(self,*args,**kwargs):
        super(CustomUserForm,self).__init__(*args,**kwargs)   

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class editprofile(forms.ModelForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone', 'email')