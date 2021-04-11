from django.shortcuts import render
from database.models import login_model , fixture_model , prediction_model
from database.database_form import login_form , fixture_form , prediciton_form
# Create your views here.

def homepage_view(request):
	if request.method == 'POST':
		print(request.POST)
		try:
			del request.session['username']
		except KeyError:
			pass
	else:
		try:
			if len(request.session['username']) > 0  :
				print(request.session['username'])
				obj = login_model.objects.filter(username=request.session['username'])[0]
				return render(request,"index.html",{"username":request.session['username'],"rank":obj.rank,"points":obj.points})
		except:
			pass
	
	return render(request,"homepage.html",{})