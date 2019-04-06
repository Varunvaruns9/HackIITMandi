from django.shortcuts import render, redirect
from .algo import *
from .models import User
from .choices import Organs
from .forms import SignUpForm
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm as LoginForm
from django.contrib.auth import login, authenticate


def index(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('results/')
	else:
		error=""
		lol = []
		for row in User.objects.all():
			print(row.organs)
			if row.donor == True:
				for a in row.organs:
					lol.append({'name': row.first_name + ' ' + row.last_name, 'organ': Organs[int(a)-1][1], 'email': row.email, })
		if request.method == 'POST':
			form = LoginForm(request.POST)
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect('results/')
			else:
				error+="Invalid details."
		else:
			form = LoginForm()
		return render(request, 'index.html', {'form': form, 'error': error, 'lol': lol})

def signup(request):
	if request.user.is_authenticated:
		return redirect('results')
	else:
		error=""
		lol = []
		for row in User.objects.all():
			print(row.organs)
			if row.donor == True:
				for a in row.organs:
					lol.append({'name': row.first_name + ' ' + row.last_name, 'organ': Organs[int(a)-1][1], 'email': row.email, })
		if request.method == 'POST':
			form = SignUpForm(request.POST)
			if not form.is_valid():
				error += "Invalid information/ Email already in use."
			else:
				user = form.save(commit=False)
				user.save()
		else:
			form = SignUpForm()
		return render(request, 'register.html', {'form': form, 'error': error, 'lol': lol})

def results(request):
	if not request.user.is_authenticated:
		return redirect('index')
	lista, listb = stable_match()
	lol = []
	for b in lista:
		for c in b[3]:
			if c == "Ineligible":
				continue
			d = c.split(' ')
			e = Organs[int(d[1][1])-1][1]
			lol.append({'rec': b[1], 'don': d[0], 'organ': e})
	context = {'lol': lol}
	return render(request, 'results.html', context)
