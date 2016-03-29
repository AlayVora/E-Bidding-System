from django import forms
from blog.models import CATEGORY



class CustomerForm(forms.Form):
	firstname = forms.CharField(label='First Name', max_length=100, required=True)
	lastname = forms.CharField(label='last Name', max_length=100, required=True)
	emailid = forms.EmailField(label='Email Id', max_length=100, required=True)
	username = forms.CharField(label='Username', max_length=20, required=True)
	password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=20, required=True)
	card_no = forms.CharField(label='Card No.', max_length=16, required=True)
	exp_date = forms.DateField(label='Expiry Date', required=True)
	cvv = forms.IntegerField(label='CVV', required=True)

class UpdateForm(forms.Form):
	firstname = forms.CharField(label='First Name', max_length=100, required=True)
	lastname = forms.CharField(label='last Name', max_length=100, required=True)
	emailid = forms.EmailField(label='Email Id', max_length=100, required=True)
	username = forms.CharField(label='Username', max_length=20, required=True)
	card_no = forms.CharField(label='Card No.', max_length=16, required=True)
	exp_date = forms.DateField(label='Expiry Date', required=True)
	cvv = forms.IntegerField(label='CVV', required=True)


class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=20, required=True)
	password = forms.CharField(widget=forms.PasswordInput(), required=True)

class passwordForm(forms.Form):
        oldpassword = forms.CharField(label='Old Password',widget=forms.PasswordInput(), required=True)
	password = forms.CharField(label='New Password',widget=forms.PasswordInput(), required=True)
	password1 = forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(), required=True)

class BidBuy(forms.Form):
	no_of_bids = forms.IntegerField(label='Number of Bids', required=True)

	


class ProductForm(forms.Form):
    fileName = forms.FileField(label='Image path',required=True)
    productname = forms.CharField(label='Product Name', max_length=100, required=True)
    product_desc = forms.CharField(label='Product Description', max_length=200, required=True)
    price = forms.IntegerField(label='Estimated Price', required=True)
    #product_path = forms.CharField(label='Image path', max_length=200, required=True)
    expdatetime = forms.CharField(label='Expiry Date Time', required=True,widget=forms.DateInput(attrs={'class':'some_class'}))
    expdatetimehidden=forms.CharField(widget=forms.HiddenInput())
    cat = CATEGORY.objects.all()
    CHOICES = []
    for c in cat:
        CHOICES.append((c.id, c.category_name))
    category = forms.ChoiceField(choices=tuple(CHOICES), required=True, label='Category')

					


	
