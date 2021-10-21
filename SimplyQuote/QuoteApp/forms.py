from django import forms
from django.forms import ModelForm
from django.forms.widgets import EmailInput
from QuoteApp.models import Quote
from QuoteApp.models import SalesPerson
from QuoteApp.models import Account
from QuoteApp.models import Product
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelChoiceField

class AccountModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.company_name

class SalesPersonModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name, obj.last_name

class ProductModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.description

class QuoteForm(forms.Form):
    sales_person = SalesPersonModelChoiceField(queryset=SalesPerson.objects.all(), required=True)
    quote_name = forms.CharField(label="Quote name in the format:: Q.ACNT.DATE ", widget=forms.Textarea, max_length=800, required=False)
    account = AccountModelChoiceField(queryset=Account.objects.all())
    product = ProductModelChoiceField(queryset=Product.objects.all())
    amount = forms.DecimalField(label="Number of Licenses", widget=forms.NumberInput)
    discount = forms.DecimalField(label="Discount in percentage ( i.e 50 = 50% ) ", widget=forms.NumberInput)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class form_Account(forms.Form):
   
    company_name = forms.CharField(label="Quote name in the format:: Q.ACNT.DATE ", widget=forms.Textarea, max_length=200, required=True) 
    main_contact =  forms.CharField(label="Quote name in the format:: Q.ACNT.DATE ", widget=forms.Textarea, max_length=200, required=True) 
    email = forms.EmailField(max_length=254, widget=EmailInput, required=True) 




    