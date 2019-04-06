from django.shortcuts import render
from .algo import *
from .models import User
from .choices import Organs


def index(request):
	lol = []
	for row in User.objects.all():
		print(row.organs)
		if row.donor == True:
			for a in row.organs:
				lol.append({'name': row.first_name + ' ' + row.last_name, 'organ': Organs[int(a)][1], 'email': row.email, })
	return render(request, 'index.html', {'lol': lol})


def results(request):
	lista, listb = stable_match()
	context = {'lista': lista}
	return render(request, 'results.html', context)
