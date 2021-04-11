from django.shortcuts import render
from .models import login_model , fixture_model , prediction_model
from .database_form import login_form , fixture_form , prediciton_form

final_ranks , final_points , final_usernames = [],[],[]

team_logos = {
	"MI":"https://i.pinimg.com/originals/28/09/a8/2809a841bb08827603ccac5c6aee8b33.png",
	"RCB":"https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/Royal_Challengers_Bangalore_2020.svg/1200px-Royal_Challengers_Bangalore_2020.svg.png",
	"CSK":"https://2.bp.blogspot.com/-UV7XoEc2L_c/WH9mT8coZHI/AAAAAAAAF4U/FZKgtVEnAjYejf1H_BXTniTy1N7XkBUswCLcB/s1600/chennai-super-kings.jpg",
	"DC":"https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/Delhi_Capitals_Logo.svg/1200px-Delhi_Capitals_Logo.svg.png",
	"RR":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRFeEmZ-pCo5KA96Ij4xZoeEHIJzjc8mvOH833i3sLa9PNPwB9nKBVTLYc1qoQWeQUSVv0&usqp=CAU",
	"SRH":"https://themayanagari.com/wp-content/uploads/2020/10/sunrisers-hyderabad-logo-png-free-download-2.jpg",
	"KXIP":"https://upload.wikimedia.org/wikipedia/en/1/1c/Punjab_Kings_logo_2021.png",
	"KKR":"https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Kolkata_Knight_Riders_Logo.svg/1200px-Kolkata_Knight_Riders_Logo.svg.png"
}

def login_process(request):
	if request.method == "POST":
		objects = login_model.objects.all()
		for i in objects:
			if request.POST['username'] == i.username and request.POST['password'] == i.password:
				request.session['username'] = i.username
				print(request.session['username'])
				obj = list(login_model.objects.filter(username=i.username))[0]
				return render(request,"index.html",{"username":i.username,"rank":obj.rank,"points":obj.points})
	else:
		if len(request.session['username']) > 0:
			obj = list(login_model.objects.filter(username=request.session['username']))[0]
			return render(request,"index.html",{"username":request.session['username'],"rank":obj.rank,"points":obj.points})

	return render(request,"homepage.html",{})



def add_match(request):
	if len(request.session['username']) > 0:
		if request.method == "GET" :
			return render(request,"add_match.html",{})
		else:
			try:
				fixture_form().save()
			except:
				obj = list(fixture_model.objects.all())
				obj[-1].match_no = len(obj)
				obj[-1].team1 = request.POST['team1']
				obj[-1].team2 = request.POST['team2']
				obj[-1].deadline = request.POST['deadline']
				obj[-1].save()
		return render(request,"add_match.html",{})
	return render(request,"homepage.html",{})


def predict(request):
	if len(request.session['username']) >0:
		if request.method == "POST":
			if request.session['username'] != "admin": 
				try:
					prediciton_form().save()
				except:
					obj = list(prediction_model.objects.all())
					obj[-1].username = request.session['username']
					obj[-1].winner = request.POST['winner']
					obj[-1].date_time = request.POST['date_time']
					obj[-1].match_no = request.POST['match_no']
					obj[-1].save()
			else:
				users,points,rank = [],[],[]
				obj = list(login_model.objects.all()) 
				for i in obj:
					if i.username == "admin":
						continue
					users.append(i.username)
					scores = list(prediction_model.objects.filter(match_no=request.POST['match_no'],username=i.username))
					fix = list(fixture_model.objects.filter(match_no=request.POST['match_no']))[0]
					try:
						if fix.winner_predict == "f" and request.POST['winner'] == scores[-1].winner:
							i.points = int(i.points) + 3
							i.save()
							fix.winner_predict = "t"
							fix.save()
					except:
						pass
					points.append(int(i.points))
				for i in range(len(users)-1):
					for j in range(0,len(users)-i-1):
						if points[j] < points[j+1]:
							points[j],points[j+1] = points[j+1],points[j]
							users[j],users[j+1] = users[j+1],users[j]
				ranks = 1

				for i in range(len(users)-1):
					obj = list(login_model.objects.filter(username=users[i]))[0]
					obj.rank = ranks
					obj.save()

					rank.append(ranks)
					if points[i] != points[i+1]:
						ranks+=1
				obj = list(login_model.objects.filter(username=users[-1]))[0]
				obj.rank = ranks
				obj.save()
				rank.append(ranks)

				try:
					prediciton_form().save()
				except:
					obj = list(prediction_model.objects.all())
					obj[-1].username = request.session['username']
					obj[-1].winner = request.POST['winner']
					obj[-1].date_time = request.POST['date_time']
					obj[-1].match_no = request.POST['match_no']
					obj[-1].save()



		match_no , team1 , team2 , deadline , logo1 , logo2 = [],[],[],[],[],[]
		obj = list(fixture_model.objects.all())
		for i in range(len(obj)):
			match_no.append(obj[i].match_no)
			team1.append(obj[i].team1)
			team2.append(obj[i].team2)
			deadline.append(obj[i].deadline)
			logo1.append(team_logos[obj[i].team1])
			logo2.append(team_logos[obj[i].team2])
		return render(request,"predict.html",{"match_no":match_no,"team1":team1,"team2":team2,"deadline":deadline,"logo1":logo1,"logo2":logo2,"username":request.session['username']})

	return render(request,"homepage.html",{})


def scoreboard(request):
	if len(request.session['username']) > 0:
		if request.method == "GET" :
			users,points,rank = [],[],[]
			obj = list(login_model.objects.all()) 
			for i in obj:
				if i.username == "admin":
					continue
				users.append(i.username)
				points.append(int(i.points))

			for i in range(len(users)-1):
				for j in range(0,len(users)-i-1):
					if points[j] < points[j+1]:
						points[j],points[j+1] = points[j+1],points[j]
						users[j],users[j+1] = users[j+1],users[j]
			ranks = 1

			for i in range(len(users)-1):
				rank.append(ranks)
				if points[i] != points[i+1]:
					ranks+=1

			rank.append(ranks)

			return render(request,"scoreboard.html",{"usernames":users,"points":points,"rank":rank,"username":request.session['username']})
		else:
			winner ,team1 , team2 , my_pred , points = [],[],[],[],[]
			matches = len(list(fixture_model.objects.all()))
			for i in range(1,matches+1):
				try:
					winner.append(list(prediction_model.objects.filter(match_no=str(i),username="admin"))[-1].winner)
				except:
					winner.append("N/D")
					pass
				team1.append(list(fixture_model.objects.filter(match_no=str(i)))[0].team1)
				team2.append(list(fixture_model.objects.filter(match_no=str(i)))[0].team2)
				my_pred.append(list(prediction_model.objects.filter(match_no=str(i),username=request.POST['username']))[-1].winner)
				if winner[-1] != "N/D" and winner[-1] == my_pred[-1]:
					points.append("3")
				else:
					points.append("0")

			print(winner,team1,team2,my_pred,points)

			return render(request,"detail_pred.html",{"winner":winner,"team1":team1,"team2":team2,"my_pred":my_pred,"points":points})
		
	return render(request,"homepage.html",{})