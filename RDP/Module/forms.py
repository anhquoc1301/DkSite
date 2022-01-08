from django.contrib.auth.forms import forms
from .models import *
class addproduct(forms.Form):
    class Meta:
        model = Product
        fields=('type_item','country','price', 'state', 'city', 'infomation')
