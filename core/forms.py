from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Producto



class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'    

     

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'    
        exclude = ['user_permissions', 'last_login','date_joined','is_superuser', 'is_active'  , 'is_staff', 'rango', 'password','groups']
