from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .choices import Organs, Groups, RH
from multiselectfield import MultiSelectField

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	email = forms.EmailField(max_length=254)
	donor = forms.BooleanField(initial=False, required=False)
	organs = MultiSelectField(choices=Organs)
	bloodgroup = forms.ChoiceField(choices=Groups, label="BloodGroup", required=False)
	rh = forms.ChoiceField(choices=RH, label="RH", required=False)
	ailment = forms.BooleanField(initial=False, required=False)
	report = forms.FileField(required=False)
	age = forms.IntegerField()

	class Meta:
		model = User
		fields = ['email', 'age', 'first_name', 'last_name', 'donor', 'organs', 'bloodgroup', 'rh', 'ailment', 'report', 'password1', 'password2']