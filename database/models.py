from django.db import models

# Create your models here.
class login_model(models.Model):
	username = models.TextField(default='n/a')
	password = models.TextField(default='123')
	points = models.TextField(default='0')
	rank = models.TextField(default='n/a')

class fixture_model(models.Model):
	match_no = models.TextField(default='n/a') 
	team1 = models.TextField(default='n/a')
	team2 = models.TextField(default='123')
	deadline = models.TextField(default='123')
	winner_predict = models.TextField(default='f')

class prediction_model(models.Model):
	username = models.TextField(default='n/a') 
	winner = models.TextField(default='n/a')
	match_no = models.TextField(default='n/a')
	date_time = models.TextField(default='123')
	