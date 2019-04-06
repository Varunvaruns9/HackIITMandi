from django.shortcuts import render
from .algo import *
from .models import User


def index(request):
	lol = []
	for row in User.objects.all():
		print(row.organs)
		if 5 in row.organs and row.donors == True:
			lol.append(row)
	return render(request, 'index.html', {'lol': lol})


def results(request):
	lista, listb = stable_match()
	context = {'lista': lista}
	return render(request, 'results.html', context)
